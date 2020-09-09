# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
from odoo.exceptions import UserError

import base64
import csv
import logging
import dateutil.relativedelta
import re
from io import StringIO
from pytz import timezone

_logger = logging.getLogger(__name__)


class syscoonFinanceinterface(models.Model):
    """Inherits the basic class to provide the export for DATEV ASCII"""
    _inherit = 'syscoon.financeinterface'

    journals = fields.Char('Journals', readonly=True)
    mode = fields.Selection(selection_add=[('datev_ascii', 'DATEV ASCII')])

    def header_template(self):
        """ DATEV ASCII Header V700 """
        return {
        'DATEVFormatKZ': 'EXTF',
        'Versionsnummer': '',
        'Datenkategorie': '',
        'Formatname': '',
        'Formatversion': '',
        'Erzeugtam': '',
        'Importiert': '',
        'Herkunft': 'OE',
        'Exportiertvon': '',
        'Importiertvon': '',
        'Berater': '',
        'Mandant': '',
        'WJBeginn': '',
        'Sachkontenlaenge': '',
        'Datumvon': '',
        'Datumbis': '',
        'Bezeichnung': '',
        'Diktatkuerzel': '',
        'Buchungstyp': '',
        'Rechnungslegungszweck': '',
        'Festschreibung': '',
        'WKZ': '',
        'res1': '',
        'Derivatskennzeichen': '',
        'res2': '',
        'res3': '',
        'SKR': '',
        'Branchenlösungs-Id': '',
        'res4': '',
        'res5': '',
        'Anwendungsinformationen': '',
    }

    def export_template(self):
        """ DATEV ASCII Structure V700 """
        return {
            'Umsatz (ohne Soll/Haben-Kz)': '',
            'Soll/Haben-Kennzeichen': '',
            'WKZ Umsatz': '',
            'Kurs': '',
            'Basis-Umsatz': '',
            'WKZ Basis-Umsatz': '',
            'Konto': '',
            'Gegenkonto (ohne BU-Schlüssel)': '',
            'BU-Schlüssel': '',
            'Belegdatum': '',
            'Belegfeld 1': '',
            'Belegfeld 2': '',
            'Skonto': '',
            'Buchungstext': '',
            'Postensperre': '',
            'Diverse Adressnummer': '',
            'Geschäftspartnerbank': '',
            'Sachverhalt': '',
            'Zinssperre': '',
            'Beleglink': '',
            'Beleginfo - Art 1': '',
            'Beleginfo - Inhalt 1': '',
            'Beleginfo - Art 2': '',
            'Beleginfo - Inhalt 2': '',
            'Beleginfo - Art 3': '',
            'Beleginfo - Inhalt 3': '',
            'Beleginfo - Art 4': '',
            'Beleginfo - Inhalt 4': '',
            'Beleginfo - Art 5': '',
            'Beleginfo - Inhalt 5': '',
            'Beleginfo - Art 6': '',
            'Beleginfo - Inhalt 6': '',
            'Beleginfo - Art 7': '',
            'Beleginfo - Inhalt 7': '',
            'Beleginfo - Art 8': '',
            'Beleginfo - Inhalt 8': '',
            'KOST1 - Kostenstelle': '',
            'KOST2 - Kostenstelle': '',
            'Kost-Menge': '',
            'EU-Mitgliedstaat u. UStIdNr': '',
            'EU-Steuersatz': '',
            'Abw. Versteuerungsart': '',
            'Sachverhalt L+L': '',
            'Funktionsergänzung L+L': '',
            'BU 49 Hauptfunktionstyp': '',
            'BU 49 Hauptfunktionsnummer': '',
            'BU 49 Funktionsergänzung': '',
            'Zusatzinformation - Art 1': '',
            'Zusatzinformation- Inhalt 1': '',
            'Zusatzinformation - Art 2': '',
            'Zusatzinformation- Inhalt 2': '',
            'Zusatzinformation - Art 3': '',
            'Zusatzinformation- Inhalt 3': '',
            'Zusatzinformation - Art 4': '',
            'Zusatzinformation- Inhalt 4': '',
            'Zusatzinformation - Art 5': '',
            'Zusatzinformation- Inhalt 5': '',
            'Zusatzinformation - Art 6': '',
            'Zusatzinformation- Inhalt 6': '',
            'Zusatzinformation - Art 7': '',
            'Zusatzinformation- Inhalt 7': '',
            'Zusatzinformation - Art 8': '',
            'Zusatzinformation- Inhalt 8': '',
            'Zusatzinformation - Art 9': '',
            'Zusatzinformation- Inhalt 9': '',
            'Zusatzinformation - Art 10': '',
            'Zusatzinformation- Inhalt 10': '',
            'Zusatzinformation - Art 11': '',
            'Zusatzinformation- Inhalt 11': '',
            'Zusatzinformation - Art 12': '',
            'Zusatzinformation- Inhalt 12': '',
            'Zusatzinformation - Art 13': '',
            'Zusatzinformation- Inhalt 13': '',
            'Zusatzinformation - Art 14': '',
            'Zusatzinformation- Inhalt 14': '',
            'Zusatzinformation - Art 15': '',
            'Zusatzinformation- Inhalt 15': '',
            'Zusatzinformation - Art 16': '',
            'Zusatzinformation- Inhalt 16': '',
            'Zusatzinformation - Art 17': '',
            'Zusatzinformation- Inhalt 17': '',
            'Zusatzinformation - Art 18': '',
            'Zusatzinformation- Inhalt 18': '',
            'Zusatzinformation - Art 19': '',
            'Zusatzinformation- Inhalt 19': '',
            'Zusatzinformation - Art 20': '',
            'Zusatzinformation- Inhalt 20': '',
            'Stück': '',
            'Gewicht': '',
            'Zahlweise': '',
            'Forderungsart': '',
            'Veranlagungsjahr': '',
            'Zugeordnete Fälligkeit': '',
            'Skontotyp': '',
            'Auftragsnummer': '',
            'Buchungstyp': '',
            'USt-Schlüssel (Anzahlungen)': '',
            'EU-Land (Anzahlungen)': '',
            'Sachverhalt L+L (Anzahlungen)': '',
            'EU-Steuersatz (Anzahlungen)': '',
            'Erlöskonto (Anzahlungen)': '',
            'Herkunft-Kz': '',
            'Buchungs GUID': '',
            'KOST-Datum': '',
            'SEPA-Mandatsreferenz': '',
            'Skontosperre': '',
            'Gesellschaftername': '',
            'Beteiligtennummer': '',
            'Identifikationsnummer': '',
            'Zeichnernummer': '',
            'Postensperre bis': '',
            'Bezeichnung SoBil-Sachverhalt': '',
            'Kennzeichen SoBil-Buchung': '',
            'Festschreibung': '',
            'Leistungsdatum': '',
            'Datum Zuord. Steuerperiode': '',
            'Fälligkeit': '',
            'Generalumkehr (GU)': '',
            'Steuersatz': '',
            'Land': '',
        }

    def export(self, mode=False, date_from=False, date_to=False, args=False):
        """ Method that generates the csv export by the given parameters """
        csv = False
        export_id = super(syscoonFinanceinterface, self).export(mode, date_from, date_to, args)
        if mode == 'datev_ascii':
            journal_ids = args[0]
            moves = self.env['account.move'].search([
                ('date', '>=', date_from), ('date', '<=', date_to), ('journal_id', 'in', journal_ids),
                ('export_id', '=', False), ('state', '=', 'posted')])
            if not moves:
                raise UserError(_('There are no moves to export in the selected date range and journals!'))
            else:
                export_moves = self.generate_export_moves(moves)
                export_header = self.generate_export_header(self.header_template(), date_from, date_to)
                csv = self.generate_csv_file(self.export_template(), export_header, export_moves)
            if csv:
                self.env['ir.attachment'].create({
                    'name': '%s.csv' % (export_id.name),
                    'res_model': 'syscoon.financeinterface',
                    'res_id': export_id.id,
                    'type': 'binary',
                    'datas': csv,
                })
                moves.write({'export_id': export_id.id})
                return export_id.id
            else:
                raise UserError(_('Something went wrong, because a export file could not generated!'))
        else:
            return export_id

    def generate_export_moves(self, moves):
        """ Generates a list of dicts which have all the exportlines to datev """
        export_lines = []
        date_range = []
        for move in moves:
            date_range.append(move.date)
            converted_move_lines = self.generate_export_lines(move)
            export_lines.extend(converted_move_lines)
        return export_lines

    def generate_export_lines(self, move):
        """ Checks if lines are exportable and inits the generation of the export line """
        export_lines = []
        group = False
        for line in move.line_ids:
            if self.env.company.datev_export_method == 'gross':
                if self.env['account.tax.repartition.line'].search([('account_id', '=', line.account_id.id)]).ids:
                    continue
            if line.account_id.id == move.export_account_counterpart.id:
                continue
            converted_line, group = self.generate_export_line(self.export_template(), line)
            export_lines.append(converted_line)
        export_lines = self.group_converted_move_lines(export_lines, group)
        return export_lines

    def generate_export_line(self, export_line, line):
        """ Generates the amount, the sign, the tax key and the tax case of the move line """
        """ Computes currencies and exchange rates """
        group = True
        if line.debit:
            total = line.debit
            export_line['Soll/Haben-Kennzeichen'] = 'S'
        if line.credit:
            total = line.credit
            export_line['Soll/Haben-Kennzeichen'] = 'H'
        if not line.debit and not line.credit:
            total = 0.0
            export_line['Soll/Haben-Kennzeichen'] = 'S'
        if line.currency_id and line.currency_id != self.env.company.currency_id and line.amount_currency != 0.0:
            if line.amount_currency < 0:
                total = -line.amount_currency
            else:
                total = line.amount_currency
        if self.env.company.datev_export_method == 'gross':
            if line.tax_ids:
                tax_id = line.tax_ids[0]
                taxes_computed = tax_id.compute_all(total, line.currency_id)
                total = self.compute_total_if_taxes(taxes_computed)
                if not line.account_id.datev_automatic_account:
                    if tax_id.datev_tax_key:
                        export_line['BU-Schlüssel'] = tax_id.datev_tax_key
                    if tax_id.datev_tax_case:
                        export_line['Sachverhalt'] = tax_id.datev_tax_case
        if line.currency_id and line.currency_id != self.env.company.currency_id and line.amount_currency != 0.0:
            if line.balance < 0:
                base_total = -line.balance
            else:
                base_total = line.balance 
            if self.env.company.datev_export_method == 'gross':
                if line.tax_ids:
                    base_tax_id = line.tax_ids[0]
                    base_taxes_computed = base_tax_id.compute_all(base_total, self.env.company.currency_id)
                    base_total = self.compute_total_if_taxes(base_taxes_computed)
            export_line['WKZ Umsatz'] = line.currency_id.name
            export_line['Basis-Umsatz'] = self.currency_round(base_total, self.env.company.currency_id)
            export_line['WKZ Basis-Umsatz'] = self.env.company.currency_id.name
            export_line['Kurs'] = line.currency_id.with_context(date=line.date).rate
        export_line['Umsatz (ohne Soll/Haben-Kz)'] = self.currency_round(total, line.currency_id)
        if line.partner_id:
            if line.account_id.user_type_id.type == 'payable' and line.partner_id.supplier_number:
                export_line['Konto'] = self.remove_leading_zero(line.partner_id.supplier_number)
            if line.account_id.user_type_id.type == 'receivable' and line.partner_id.customer_number:
                export_line['Konto'] = self.remove_leading_zero(line.partner_id.customer_number)
        if not export_line['Konto']:
            export_line['Konto'] = self.remove_leading_zero(line.account_id.code)
        if line.move_id.partner_id:
            if line.move_id.export_account_counterpart.user_type_id.type == 'payable' and line.move_id.partner_id.supplier_number:
                export_line['Gegenkonto (ohne BU-Schlüssel)'] = self.remove_leading_zero(line.move_id.partner_id.supplier_number)
            if line.move_id.export_account_counterpart.user_type_id.type == 'receivable' and line.move_id.partner_id.customer_number:
                export_line['Gegenkonto (ohne BU-Schlüssel)'] = self.remove_leading_zero(line.move_id.partner_id.customer_number)
        if not export_line['Gegenkonto (ohne BU-Schlüssel)']:
            export_line['Gegenkonto (ohne BU-Schlüssel)'] = self.remove_leading_zero(line.move_id.export_account_counterpart.code)
        export_line['Belegdatum'] = self.convert_date(line.date, self.env.company.datev_voucher_date_format)
        export_line['Belegfeld 1'], group  = self.create_doc_field(line[:36], group)
        maturity_dates = []
        for l in line.move_id.line_ids:
            if l.date_maturity:
                maturity_dates.append(l.date)
        if maturity_dates:
            export_line['Belegfeld 2'] = self.convert_date(max(maturity_dates), '%d%m%y')
        export_line['Buchungstext'] = self.create_label(line)[:60]
        if line.analytic_account_id.code:
            export_line['KOST1 - Kostenstelle'] = line.analytic_account_id.code
        if line.analytic_tag_ids:
            export_line['KOST2 - Kostenstelle'] = line.analytic_tag_ids[0].name
        if line.account_id.datev_vatid_required:
            export_line['EU-Mitgliedstaat u. UStIdNr'] = line.partner_id.vat
        export_line['Festschreibung'] = int(self.env.company.datev_enable_fixing)
        return export_line, group

    def create_doc_field(self, line, group):
        doc_field = line.move_name
        if line.journal_id.type == 'purchase' and line.ref:
            doc_field = line.ref
        if line.journal_id.type != 'sale' or line.journal_id.type != 'purchase':
            inv_num = False
            if line.full_reconcile_id.reconciled_line_ids:
                for lf in line.full_reconcile_id.reconciled_line_ids:
                    if lf.move_id.name and lf.move_id.type in ['out_invoice', 'out_refund']:
                        inv_num = lf.move_id.name
                    if lf.move_id.ref and lf.move_id.type in ['in_invoice', 'in_refund']:
                        inv_num = lf.move_id.ref
            if inv_num:
                doc_field = inv_num
                group = False
        doc_field = re.sub(r'[\W_]+', '', doc_field)
        return doc_field, group

    def create_label(self, line):
        labels = self.env['syscoon.financeinterface.bookingtext.config'].search([], order='sequence asc')
        bookingtext = []
        for label in labels:
            value = self.get_field(line, label.field)
            if value:
                bookingtext.append(value)
        bookingtext = ', '.join(bookingtext)
        return bookingtext

    def get_field(self, model, field_name):
        value = model
        for part in field_name.split('.'):
            value = getattr(value, part)
        return value

    def group_converted_move_lines(self, move_lines, group):
        grouped_lines = []
        for ml in move_lines:
            if self.env.company.datev_group_lines and group:
                if not any( gl['Konto'] == ml['Konto'] and gl['Gegenkonto (ohne BU-Schlüssel)'] == ml['Gegenkonto (ohne BU-Schlüssel)']
                    and gl['BU-Schlüssel'] == ml['BU-Schlüssel'] and gl['Soll/Haben-Kennzeichen'] == ml['Soll/Haben-Kennzeichen'] 
                    and gl['WKZ Umsatz'] == ml['WKZ Umsatz'] for gl in grouped_lines):
                    grouped_lines.append(ml)
                else:
                    for gl in grouped_lines:
                        if gl['Konto'] == ml['Konto'] and gl['Gegenkonto (ohne BU-Schlüssel)'] == ml['Gegenkonto (ohne BU-Schlüssel)'] \
                            and gl['BU-Schlüssel'] == ml['BU-Schlüssel'] and gl['Soll/Haben-Kennzeichen'] == ml['Soll/Haben-Kennzeichen']:
                            if gl['Basis-Umsatz'] and ml['Basis-Umsatz']:
                                gl['Basis-Umsatz'] += ml['Basis-Umsatz']
                            if gl['Umsatz (ohne Soll/Haben-Kz)'] and ml['Umsatz (ohne Soll/Haben-Kz)']:
                                gl['Umsatz (ohne Soll/Haben-Kz)'] += ml['Umsatz (ohne Soll/Haben-Kz)']
                            break
            else:
                grouped_lines.append(ml)
        new_lines = []
        for line in grouped_lines:
            new_lines.append(self.convert_line_float_to_char(line))
        return new_lines

    def remove_leading_zero(self, account):
        if self.env.company.datev_remove_leading_zeros:
            if account:
                account = account.lstrip('0')
        return account

    def generate_export_header(self, header, date_from, date_to):
        if int(self.env.company.fiscalyear_last_month) == 12:
            fy_start = date_from.strftime('%Y') + '{:02d}'.format(1) + '01'
        else:
            year_from = date_from - dateutil.relativedelta.relativedelta(months=11)
            fy_start = year_from.strftime('%Y') + '{:02d}'.format(int(self.env.company.fiscalyear_last_month) + 1) + '01'
        header['Versionsnummer'] = 700
        header['Datenkategorie'] = 21
        header['Formatname'] = 'Buchungsstapel'
        header['Formatversion'] = 9
        header['Erzeugtam'] = fields.datetime.now(timezone(self.env.context.get('tz') or self.env.user.tz or 'UTC')).strftime('%Y%m%d%H%M%S%f')[:-3]
        header['Exportiertvon'] = self.env.user.partner_id.name
        header['Berater'] = self.env.company.datev_accountant_number or '10000'
        header['Mandant'] = self.env.company.datev_client_number or '10000'
        header['WJBeginn'] = fy_start
        header['Sachkontenlaenge'] = self.env.company.datev_account_code_digits
        header['Datumvon'] = date_from.strftime('%Y%m%d')
        header['Datumbis'] = date_to.strftime('%Y%m%d')
        header['Bezeichnung'] = 'Odoo-Export Buchungen'
        header['Buchungstyp'] = 1
        header['Festschreibung'] = int(self.env.company.datev_enable_fixing)
        return header

    def generate_csv_file(self, template, header, lines):
        """ Generates the CSV file as in memory with StringIO """
        buf = StringIO()
        export_csv = csv.writer(buf, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
        if header:
            export_csv.writerow(header.values())
        export_csv.writerow(template.keys())
        for line in lines:
            export_csv.writerow(line.values())
        output = base64.b64encode(buf.getvalue().encode('iso-8859-1', 'ignore'))
        return output

