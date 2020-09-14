# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
from odoo.exceptions import UserError

from collections import namedtuple
from functools import partial, reduce
from itertools import chain
from lxml import etree
import base64
import io
import logging
import os
import PyPDF2
import re
import shutil
import zipfile

_logger = logging.getLogger(__name__)


class syscoonFinanceinterface(models.Model):
    """Inherits the basic class to provide the export for DATEV ASCII"""
    _inherit = 'syscoon.financeinterface'

    mode = fields.Selection(selection_add=[('datev_xml', 'DATEV XML')])

    def export(self, mode=False, date_from=False, date_to=False, args=False):
        """ Method that generates the export by the given parameters """
        export_id = super(syscoonFinanceinterface, self).export(mode, date_from, date_to, args)
        zipfile = False
        if mode == 'datev_xml':
            invoice_mode = args[0]
            invoice_selection = args[1]
            invoice_type = []
            if invoice_selection in ['customers', 'both']:
                invoice_type.extend(['out_invoice', 'out_refund'])
            if invoice_selection in ['vendors', 'both']:
                invoice_type.extend(['in_invoice', 'in_refund'])
            moves = self.env['account.move'].search([
                ('date', '>=', date_from), ('date', '<=', date_to), ('type', 'in', invoice_type),
                ('export_id', '=', False), ('state', '=', 'posted')])
            if not moves:
                raise UserError(_('There are no invoices to export in the selected date range!'))
            else:
                export_invoices, export_path, export_time, move_errors, moves_ok = self.generate_export_invoices(invoice_mode, moves, export_id)
                if export_invoices:
                    zipfile = self.make_zip_file(export_path, export_invoices, export_time)
            if zipfile:
                self.env['ir.attachment'].create({
                    'name': '%s.zip' % (export_id.name),
                    'store_fname': '%s.zip' % (export_id.name),
                    'res_model': 'syscoon.financeinterface',
                    'res_id': export_id.id,
                    'type': 'binary',
                    'datas': base64.b64encode(zipfile),
                })
                moves_ok.write({'export_id': export_id.id})
                if move_errors:
                    move_errors = self.env['account.move'].browse(move_errors)
                    move_errors.write({'export_id': False})
                if os.path.exists(export_path):
                    shutil.rmtree(export_path)
            return export_id.id
        else:
            return export_id

    def generate_export_invoices(self, invoice_mode, moves, export_id):
        """ Generates a list of dicts which have all the exportlines to datev """

        def clean_move_number(move):
            """
            Return a cleaned invoice
            number consisting only of
            alphanumeric characters
            """
            return ''.join(re.findall(r'\w+', move.name or ''))

        export_time = fields.Datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        move_xmls = []
        move_errors = []
        moves_with_xml = []
        for move in moves:
            xml = self.get_invoice_xml(move, invoice_mode, export_id)
            if xml:
                move_xmls.append(xml)
                moves_with_xml.append(move.id)
            else:
                move_errors.append(move.id)
        moves_ok = self.env['account.move'].browse(moves_with_xml)       
        invoice_pdfs = map(self.get_invoice_pdf, moves_ok)
        move_numbers = moves_ok.mapped(clean_move_number)
        move_ids = moves_ok.ids
        invoice_docs = filter(all, zip(move_ids, move_numbers, move_xmls, invoice_pdfs))
        export_path = self.get_export_dir_path()
        docs = map(partial(self.write_export_invoice, export_path), invoice_docs)
        doc_paths = self.write_docs(docs, export_time, export_path)
        return doc_paths, export_path, export_time, move_errors, moves_ok

    def get_export_dir_path(self):
        """ Check if temporary directory exists for buffering documents before zipping it """
        path = '/tmp/odoo/datev_xml_export'
        if not os.path.exists(path) or not os.path.isdir(path):
            os.makedirs(path, exist_ok=True)
        return path

    def get_invoice_pdf(self, move):
        """ Return the PDF report for a given invoice """
        datas = False
        content = False
        report = namedtuple('Report', ['content', 'filetype'])
        datas = self.env['ir.attachment'].search([
            ('res_model', '=', 'account.move'),
            ('res_id', '=', move.id),
            ('mimetype', '=', 'application/pdf'),
        ])
        if datas:
            content, filetype = self.merge_pdf(datas, move)
        else:
            content, filetype = self.env.ref('account.account_invoices').render_qweb_pdf([move.id])
        report_maked = report._make((content, filetype))
        return report_maked

    def get_invoice_xml(self, move_id, invoice_mode, export_id):
        """ Return the XML Export for a given invoice """
        errors = []
        vnote = ''
        if type(move_id) is list:
            move = move_id[0][0].id
        else:
            move = move_id.id
        schema = etree.parse(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'schemas/Belegverwaltung_online_invoice_v050.xsd'))
        schema = etree.XMLSchema(schema)
        parser = etree.XMLParser(schema=schema, encoding='utf-8')
        xml = self.env['syscoon.financeinterface.xml'].create_invoice_xml(move_id, invoice_mode)
        try:
            etree.fromstring(xml, parser)
            return xml
        except Exception as e:
            errors.append(self.get_error_msg(move_id))
            for arg in e.args:
                errors.append(arg)
            if export_id.log:
                vnote = export_id.log
                vnote += '\n'.join(errors)
                vnote += '\n'
            else:
                vnote = '\n'.join(errors)
                vnote += '\n'
            export_id.write({
                'log': vnote,
            })
            return False

    def write_export_invoice(self, dir_path, inv_doc):
        """
        Either both files are written or niether.
        """
        id, name, xml, report = inv_doc
        print(name, xml[150:300])

        xml_path = os.path.join(dir_path, name + '.xml')
        pdf_path = os.path.join(dir_path, '.'.join([name, report.filetype]))
        try:
            with open(xml_path, 'w') as f:
                xml = xml.decode(encoding='utf-8', errors='strict')
                f.write(xml)
            with open(pdf_path, 'wb') as f:
                f.write(report.content)
            return (id, name, xml_path, pdf_path)
        except Exception:
            _logger.error(
                _("An error occured while saving %s export in %s"
                  % (name, dir_path)))
            if os.path.exists(xml_path):
                os.remove(xml_path)
            if os.path.exists(pdf_path):
                os.remove(pdf_path)
            raise

    def write_export(self, dir_path, inv_doc):
        """
        Either both files are written or niether.
        """
        id, name, xml, report = inv_doc

        xml_path = os.path.join(dir_path, name + '.xml')
        pdf_path = os.path.join(dir_path, '.'.join([name, report.filetype]))
        try:
            with open(xml_path, 'w') as f:
                xml = xml.decode(encoding='utf-8', errors='strict')
                f.write(xml)
            with open(pdf_path, 'wb') as f:
                f.write(report.content)
            return (id, name, xml_path, pdf_path)
        except Exception:
            _logger.error(
                _("An error occured while saving %s export in %s"
                  % (name, dir_path)))
            if os.path.exists(xml_path):
                os.remove(xml_path)
            if os.path.exists(pdf_path):
                os.remove(pdf_path)
            raise

    @api.model
    def write_docs(self, docs, timestamp, dir_path):
        """
        Consumes the docs generator and additionally
        writes an xml file with info of the made exports
        """
        WrittenDoc = namedtuple(
            'WrittenDoc', ['inv', 'name', 'xml_path', 'pdf_path'])

        def join_recs(list_of_recs):
            return reduce(add, list_of_recs)

        def get_inv(tupl):
            return tupl[0]

        def clean_tstamp(tstamp):
            return tstamp.replace('T', ' ')

        def get_doc_paths(doc):
            return dir_path + '/' + doc.pdf_path, dir_path + '/' + doc.xml_path

        written_docs = []
        inv_info_xml_path = None
        try:
            for id, name, xml_path, pdf_path in docs:
                inv = self.env['account.move'].browse(id)
                xp = xml_path.replace(dir_path + '/', '')
                pp = pdf_path.replace(dir_path + '/', '')
                written_docs.append(
                    WrittenDoc._make((inv, name, xp, pp)))
                _logger.info(_('%s has been exported' % name))
                _logger.info(xml_path)
                _logger.info(pdf_path)
                export_info_xml = self.get_documents_xml(written_docs, timestamp)
                inv_documents_xml_path = self.write_export_invoice_info(dir_path, export_info_xml, timestamp)
            return filter(None, chain((inv_documents_xml_path,), *map(get_doc_paths, written_docs)))
        except:
            return False

    def get_error_msg(self, move_id):
        return _('%s (id=%s) could not be exported: ' % (move_id.name, move_id.id))

    def make_zip_file(self, export_path, doc_path, timestamp):
        zip_path = os.path.join(export_path, timestamp + '.zip')
        with zipfile.ZipFile(zip_path, 'w', compression=zipfile.ZIP_DEFLATED) as f:
            for path in doc_path:
                f.write(path, os.path.basename(path))

        datas_file = open(zip_path, 'rb')
        datas_content = datas_file.read()

        if os.path.exists(zip_path):
            os.remove(zip_path)

        return datas_content

    def get_documents_xml(self, docs, timestamp):
        """ Return the XML Export for a given invoice """
        errors = []
        vnote = ''
        schema = etree.parse(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'schemas/Document_v050.xsd'))
        schema = etree.XMLSchema(schema)
        parser = etree.XMLParser(schema=schema, encoding='utf-8')
        xml = self.env['syscoon.financeinterface.xml'].create_documents_xml(docs, timestamp)
        try:
            etree.fromstring(xml, parser)
            return xml
        except Exception as e:
            errors.append('documents.xml')
            for arg in e.args:
                errors.append(arg)
            if export_id.log:
                vnote = export_id.log
                vnote += '\n'.join(errors)
                vnote += '\n'
            else:
                vnote = '\n'.join(errors)
                vnote += '\n'
            export_id.write({
                'log': vnote,
            })
            return

    def write_export_invoice_info(self, dir_path, xml, timestamp):
        xml_path = os.path.join(dir_path, 'document.xml')
        if not xml:
            xml = False
        if xml:
            try:
                with open(xml_path, 'w') as f:
                    f.write(xml.decode("utf-8"))
                return xml_path
            except Exception:
                _logger.error(
                    _("An error occured while saving %s export in %s"
                      % (timestamp, dir_path)))
                if os.path.exists(xml_path):
                    os.remove(xml_path)
                raise

    def merge_pdf(self, datas, inv):
        """
        concentrate pdfs if the number of the attachemnts is > 1
        otherwise use odoo standard for reading the pdf
        """
        if len(datas) > 1:
            merger = PyPDF2.PdfFileMerger(strict=False)
            myio = io.BytesIO()
            for pdf in datas:
                attach = pdf._file_read(pdf.store_fname)
                content = base64.b64decode(attach)
                content = io.BytesIO(content)
                try:
                    merger.append(content, import_bookmarks=False)
                except:
                    raise UserError(_('Export stopped! \n Invoice %s can not exported, because the PDF has no EOF-Marker. \n Please repair it and start the export again.' % inv.number))
            merger.write(myio)
            merger.close()
            content, filetype = myio.getvalue(), 'pdf'
        else:
            attach = datas._file_read(datas.store_fname)
            content, filetype = base64.b64decode(attach), 'pdf'
        return content, filetype

