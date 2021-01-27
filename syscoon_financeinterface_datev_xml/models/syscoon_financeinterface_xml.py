# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _

import re
from lxml import etree

EU_VAT = ['BE', 'BG', 'DK', 'DE', 'EE', 'FI', 'FR', 'GR', 'GB', 'IE',
          'IT', 'HR', 'LV', 'LT', 'LU', 'MT', 'NL', 'AT', 'PL', 'PT',
          'RO', 'SE', 'SK', 'SI', 'ES', 'CZ', 'HU', 'CY']

class syscoonFinanceinterfaceXML(models.TransientModel):
    _name = 'syscoon.financeinterface.xml'
    _description = 'definitions for the syscoon financeinterface DATEV XML-export'

    def create_invoice_xml(self, move_id, invoice_mode):
        xml = self.make_invoice_xml(move_id, invoice_mode)
        invoice = etree.tostring(xml, pretty_print = True, xml_declaration = True, encoding = 'UTF-8')
        return invoice

    def get_subelement(self, tag, d):
        elem = etree.Element(tag)
        for key, val in d.items():
            elem.attrib[key] = self.make_string(val)
        return elem

    def make_string(self, val):
        if type(val) == float:
            return format(val, '.2f')
        else:
            return str(val)

    def get_invoice_info(self, move_id, invoice_mode):
        vals = {}
        vals['invoice_date'] = move_id.invoice_date
        if move_id.type in ['out_invoice', 'in_invoice']:
            vals['invoice_type'] = 'Rechnung'
        if move_id.type in ['out_refund', 'in_refund']:
            vals['invoice_type'] = 'Gutschrift/Rechnungskorrektur'
        if move_id.type in ['in_invoice', 'in_refund'] and move_id.ref:
            vals['invoice_id'] = re.sub(r'[^\w]', '', move_id.ref[:35])
        else:
            vals['invoice_id'] = re.sub(r'[^\w]', '', move_id.name[:35])
        vals['delivery_date'] = str(move_id.date)
        return vals

    def get_accounting_info(self, move_id, invoice_mode):
        vals = {}
        if move_id.type == 'out_invoice':
            vals['booking_text'] = 'Erlöse'
        if move_id.type == 'out_refund':
            vals['booking_text'] = 'Gutschrift Erlöse'
        if move_id.type == 'in_invoice':
            vals['booking_text'] = 'Aufwand'
        if move_id.type == 'in_refund':
            vals['booking_text'] = 'Gutschrift Aufwand'
        return vals

    def get_invoice_party(self, move_id, invoice_mode):
        if move_id.type in ['out_invoice', 'out_refund']:
            ip = move_id.commercial_partner_id
            booking_info = True
        if move_id.type in ['in_invoice', 'in_refund']:
            ip = move_id.company_id
            booking_info = False
        vals = {}
        if ip.vat and ip.vat[:2] in EU_VAT:
            vals['vat_id'] = ip.vat
        vals['address'] = {}
        if ip.name:
            vals['address']['name'] = ip.name[:50]
        elif ip.parent_id.name:
            vals['address']['name'] = ip.parent_id.name[:50]
        if ip.street:
            vals['address']['street'] = ip.street
        if ip.zip:
            vals['address']['zip'] = ip.zip
        if ip.city:
            vals['address']['city'] = ip.city
        if ip.country_id:
            vals['address']['country'] = ip.country_id.code
        if invoice_mode == 'extended':
            if ip.phone:
                vals['address']['phone'] = ip.phone[:20]
            if 'ref' in ip._fields and ip.ref:
                if ip.ref != ip.customer_number:
                    vals['address']['party_id'] = ip.ref
            if ip.bank_ids:
                bank = ip.bank_ids[0]
                if bank.acc_type == 'iban' and bank.bank_id.name:
                    vals['account'] = {}
                    if bank.sanitized_acc_number:
                        vals['account']['iban'] = bank.sanitized_acc_number
                    if bank.bank_id.bic:
                        vals['account']['swiftcode'] = bank.bank_id.bic
                    if bank.bank_id.name:
                        vals['account']['bank_name'] = bank.bank_id.name[:27]
            if booking_info:
                vals['booking_info_bp'] = {}
                vals['booking_info_bp']['bp_account_no'] = ip.customer_number or ip.property_account_receivable_id.code
        return vals

    def get_supplier_party(self, move_id, invoice_mode):
        if move_id.type in ['out_invoice', 'out_refund']:
            sp =  move_id.company_id
            booking_info = False
        if move_id.type in ['in_invoice', 'in_refund']:
            sp = move_id.commercial_partner_id
            booking_info = True
        vals = {}
        if sp.vat and sp.vat[:2] in EU_VAT:
            vals['vat_id'] = sp.vat
        vals['address'] = {}
        if sp.name:
            vals['address']['name'] = sp.name[:50]
        if sp.street:
            vals['address']['street'] = sp.street
        if sp.zip:
            vals['address']['zip'] = sp.zip
        if sp.city:
            vals['address']['city'] = sp.city
        if sp.country_id:
            vals['address']['country'] = sp.country_id.code
        if invoice_mode == 'extended':
            if sp.phone:
                vals['address']['phone'] = sp.phone[:20]
            if 'ref' in sp._fields and sp.ref:
                vals['address']['party_id'] = sp.ref
            if sp.bank_ids:
                bank = sp.bank_ids[0]
                if bank.acc_type == 'iban' and bank.bank_id.name:
                    vals['account'] = {}
                    if bank.sanitized_acc_number:
                        vals['account']['iban'] = bank.sanitized_acc_number
                    if bank.bank_id.bic:
                        vals['account']['swiftcode'] = bank.bank_id.bic
                    if bank.bank_id.name:
                        vals['account']['bank_name'] = bank.bank_id.name[:27]
            if booking_info:
                vals['booking_info_bp'] = {}
                vals['booking_info_bp']['bp_account_no'] = sp.supplier_number or sp.property_account_payable_id.code
                vals['party_id'] = vals['booking_info_bp']['bp_account_no']
        return vals

    def get_payment_conditions(self, move_id):
        vals = {}
        vals['currency'] = move_id.currency_id.name
        vals['due_date'] = move_id.invoice_date_due
        vals['payment_conditions_text'] = move_id.invoice_payment_term_id.name
        if move_id.invoice_payment_term_id.datev_payment_conditons_id:
            vals['payment_conditions_id'] = move_id.invoice_payment_term_id.datev_payment_conditons_id
        return vals

    def get_invoice_item_list(self, move_id, invoice_mode):
        vals = []
        total_invoice_amount = 0.0
        for line in move_id.invoice_line_ids:
            total_invoice_amount += line.price_total
            if not line.display_type and not line.price_subtotal == 0.0:
                item = {}
                item['description_short'] = line.name and line.name[:40] or _('Description')
                item['quantity'] = line.quantity or 1.0
                item['price_line_amount'] = {}
                item['price_line_amount']['tax'] = line.tax_ids and line.tax_ids[0].amount or 0.0
                if invoice_mode == 'extended':
                    if move_id.type in ['out_refund', 'in_refund']:
                        if move_id.currency_id.round(line.price_total - line.price_subtotal) != 0.0:
                            item['price_line_amount']['tax_amount'] = - (line.price_total - line.price_subtotal)
                        item['price_line_amount']['gross_price_line_amount'] = - line.price_total
                        item['price_line_amount']['net_price_line_amount'] = - line.price_subtotal
                    else:
                        if move_id.currency_id.round(line.price_total - line.price_subtotal) != 0.0:
                            item['price_line_amount']['tax_amount'] = line.price_total - line.price_subtotal
                        item['price_line_amount']['gross_price_line_amount'] = line.price_total
                        item['price_line_amount']['net_price_line_amount'] = line.price_subtotal
                    item['price_line_amount']['currency'] = line.currency_id.name or 'EUR'
                    item['accounting_info'] = {}
                    item['accounting_info']['account_no'] = line.account_id.code.lstrip('0')
                    item['accounting_info']['booking_text'] = line.name and line.name[:60] or _('Description')
                    if line.analytic_account_id:
                        item['accounting_info']['cost_category_id'] = line.analytic_account_id.code
                    if line.analytic_tag_ids and line.analytic_tag_ids[0]:
                        item['accounting_info']['cost_category_id2'] = line.analytic_tag_ids[0].name
                vals.append(item)
        if move_id.currency_id.round(total_invoice_amount) != move_id.amount_total:
            difference = move_id.currency_id.round(total_invoice_amount - move_id.amount_total)
            last_val = vals[-1]
            del vals[-1]
            if last_val['price_line_amount'].get('tax_amount'):
                last_val['price_line_amount']['tax_amount'] = move_id.currency_id.round(last_val['price_line_amount']['tax_amount'] - difference)
            last_val['price_line_amount']['gross_price_line_amount'] = move_id.currency_id.round(item['price_line_amount']['gross_price_line_amount'] - difference)
            vals.append(last_val)
        return vals

    def get_total_amount(self, move_id, invoice_mode):
        vals = {}
        if move_id.type in ['out_refund', 'in_refund']:
            vals['total_gross_amount_excluding_third-party_collection'] = - move_id.amount_total
        else:
            vals['total_gross_amount_excluding_third-party_collection'] = move_id.amount_total
        if invoice_mode == 'extended':
            if move_id.type in ['out_refund', 'in_refund']:
                vals['net_total_amount'] = - move_id.amount_untaxed
            else:
                vals['net_total_amount'] = move_id.amount_untaxed
        vals['currency'] = move_id.currency_id.name or 'EUR'
        tax_lines = move_id.line_ids.filtered(lambda line: line.tax_line_id)
        tax_key_lines = move_id.line_ids.filtered(lambda line: line.tax_ids)
        vals['tax_line'] = []
        res = {}
        done_taxes = set()
        done_tax_key_lines = set()
        for line in tax_lines:
            res.setdefault(line.tax_line_id.tax_group_id, {'rate': 0.0, 'base': 0.0, 'amount': 0.0})
            res[line.tax_line_id.tax_group_id]['rate'] = line.tax_line_id.amount
            res[line.tax_line_id.tax_group_id]['amount'] += line.price_subtotal
            tax_key_add_base = tuple(move_id._get_tax_key_for_group_add_base(line))
            if tax_key_add_base not in done_taxes:
                # The base should be added ONCE
                res[line.tax_line_id.tax_group_id]['base'] += line.tax_base_amount
                done_taxes.add(tax_key_add_base)
        for line in tax_key_lines:
            if line.tax_ids[0].amount == 0.0:
                res.setdefault(line.tax_ids[0].tax_group_id, {'rate': 0.0, 'base': 0.0, 'amount': 0.0})
                res[line.tax_ids[0].tax_group_id]['base'] += line.debit + line.credit
        res = sorted(res.items(), key=lambda l: l[0].sequence)
        for group, amounts in res:
            line_vals = {}
            line_vals['tax'] = amounts['rate']
            line_vals['currency'] = move_id.currency_id.name
            if invoice_mode == 'extended':
                if move_id.type in ['out_refund', 'in_refund']:
                    line_vals['net_price_line_amount'] = - amounts['base']
                    line_vals['gross_price_line_amount'] = - (amounts['base'] + amounts['amount'])
                else:
                    line_vals['net_price_line_amount'] = amounts['base']
                    line_vals['gross_price_line_amount'] = amounts['base'] + amounts['amount']
                if amounts['amount'] > 0.0:
                    if move_id.type in ['out_refund', 'in_refund']:
                        line_vals['tax_amount'] = - amounts['amount']
                    else:
                        line_vals['tax_amount'] = amounts['amount']
            vals['tax_line'].append(line_vals)
        if not vals['tax_line']:
            line_vals = {}
            line_vals['tax'] = 0.0
            line_vals['currency'] = move_id.currency_id.name
            vals['tax_line'].append(line_vals)
        return vals

    def get_additional_footer(self, move_id):
        vals = {}
        vals['type'] = 'text'
        vals['content'] = move_id.narration and move_id.narration[:60] or ''
        return vals

    def make_invoice_xml(self, move_id, invoice_mode):
        attr_qname = etree.QName('http://www.w3.org/2001/XMLSchema-instance', 'schemaLocation')
        nsmap = {'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
                 None: 'http://xml.datev.de/bedi/tps/invoice/v050'}

        invoice = etree.Element('invoice',
            {attr_qname: 'http://xml.datev.de/bedi/tps/invoice/v050 Belegverwaltung_online_invoice_v050.xsd'},
            nsmap=nsmap)
        invoice.attrib['generator_info'] = 'Odoo 13'
        invoice.attrib['generating_system'] = 'Odoo-ERP Software'
        invoice.attrib['description'] = 'DATEV Import invoices'
        invoice.attrib['version'] = '5.0'
        invoice.attrib['xml_data'] = 'Kopie nur zur Verbuchung berechtigt nicht zum Vorsteuerabzug'

        invoice_info = etree.SubElement(invoice, 'invoice_info')
        for key, val in self.get_invoice_info(move_id, invoice_mode).items():
            invoice_info.attrib[key] = self.make_string(val)

        if invoice_mode == 'extended':
            account_info = etree.SubElement(invoice, 'accounting_info')
            for key, val in self.get_accounting_info(move_id, invoice_mode).items():
                account_info.attrib[key] = self.make_string(val)

        invoice_party = etree.SubElement(invoice, 'invoice_party')
        for key, val in self.get_invoice_party(move_id, invoice_mode).items():
            if key == 'vat_id':
                invoice_party.attrib[key] = self.make_string(val)
            if key == 'address':
                invoice_party.append(self.get_subelement(key, val))
            if key == 'account':
                invoice_party.append(self.get_subelement(key, val))
            if key == 'booking_info_bp':
                invoice_party.append(self.get_subelement(key, val))

        supplier_party = etree.SubElement(invoice, 'supplier_party')
        for key, val in self.get_supplier_party(move_id, invoice_mode).items():
            if key == 'vat_id':
                supplier_party.attrib[key] = self.make_string(val)
            if key == 'address':
                supplier_party.append(self.get_subelement(key, val))
            if key == 'account':
                supplier_party.append(self.get_subelement(key, val))
            if key == 'booking_info_bp':
                supplier_party.append(self.get_subelement(key, val))

        if invoice_mode == 'extended' and move_id.invoice_payment_term_id:
            payment_conditions = etree.SubElement(invoice, 'payment_conditions')
            for key, val in self.get_payment_conditions(move_id).items():
                payment_conditions.attrib[key] = self.make_string(val)

        for item in self.get_invoice_item_list(move_id, invoice_mode):
            invoice_item_list = etree.SubElement(invoice, 'invoice_item_list')
            for key, val in item.items():
                if key == 'description_short':
                    invoice_item_list.attrib[key] = self.make_string(val)
                if key == 'quantity':
                    invoice_item_list.attrib[key] = self.make_string(val)
                if key == 'price_line_amount':
                    invoice_item_list.append(self.get_subelement(key, val))
                if key == 'accounting_info':
                    invoice_item_list.append(self.get_subelement(key, val))

        total_amount = etree.SubElement(invoice, 'total_amount')
        for key, val in self.get_total_amount(move_id, invoice_mode).items():
            if key != 'tax_line':
                total_amount.attrib[key] = self.make_string(val)
            if key == 'tax_line':
                for line in val:
                    total_amount.append(self.get_subelement(key, line))

        if move_id.narration:
            additional_info_footer = etree.SubElement(invoice, 'additional_info_footer')
            additional_info_footer.attrib['type'] = 'text'
            additional_info_footer.attrib['content'] = move_id and move_id.narration[:60] or ''

        return invoice

    def create_documents_xml(self, docs, timestamp):
        xml = self.make_documents_xml(docs, timestamp)
        documents = etree.tostring(xml, pretty_print = True, xml_declaration = True, encoding = 'UTF-8')
        return documents

    def make_documents_xml(self, docs, timestamp):
        attr_qname = etree.QName('http://www.w3.org/2001/XMLSchema-instance', 'schemaLocation')
        qname = etree.QName('http://www.w3.org/2001/XMLSchema-instance', 'type')
        nsmap = {'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
                 None: 'http://xml.datev.de/bedi/tps/document/v05.0'}

        archive = etree.Element('archive',
            {attr_qname: 'http://xml.datev.de/bedi/tps/document/v05.0 document_v050.xsd'},
            nsmap=nsmap)
        archive.attrib['version'] = '5.0'
        archive.attrib['generatingSystem'] = 'Odoo-ERP Software'
        header = etree.SubElement(archive, 'header')
        date = etree.SubElement(header, 'date')
        date.text = str(timestamp)
        description = etree.SubElement(header, 'description')
        description.text = 'Rechnungsexport'
        content = etree.SubElement(archive, 'content')
        for doc in docs:
            document = etree.SubElement(content, 'document')
            extension = etree.Element('extension', {qname: 'Invoice'})
            extension.attrib['datafile'] = doc.xml_path
            property = etree.SubElement(extension, 'property')
            property.attrib['key'] = 'InvoiceType'
            property.attrib['value'] = self.get_document_value(doc.inv)
            document.append(extension)
            extension = etree.Element('extension', {qname: 'File'})
            extension.attrib['name'] = doc.pdf_path
            document.append(extension)
        return archive

    def get_document_value(self, move_id):
        if move_id.type in ['out_invoice', 'out_refund']:
            return 'Outgoing'
        else:
            return 'Incoming'

