# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError

import re
import time


class syscoonFinanceinterface(models.Model):
    """ The class syscoon.financeinterface is the central object to generate 
    exports for the selected moves that can be used to be imported in the 
    different financial programms on different ways """
    _name = 'syscoon.financeinterface'
    _description = 'syscoon Financial Interface'
    _order = 'name desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Name', required=True, readonly=True)
    period = fields.Char('Date', required=True, readonly=True)
    account_moves_ids = fields.One2many('account.move', 'export_id', 'Account Moves', readonly=True)
    mode = fields.Selection(selection=[], string='Export Mode', required=True)
    log = fields.Text('Log')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)

    def replace_characters(self, text, replacement=''):
        """replaces non ascii characters"""
        return re.sub(r'[^\x00-\x7F]+', replacement, text)

    def convert_line_float_to_char(self, line):
        """ Converts all floats of a line to char for using in DATEV ASCII Export """
        for key in line.keys():
            if isinstance(line[key], float):
                line[key] = str(line[key]).replace('.', ',')
        return line

    def currency_round(self, value, currency=False):
        if not currency:
            currency = self.env.company.currency_id
        return currency.round(value)

    def compute_total_if_taxes(self, taxes_computed):
        """ Compute the total include taxes """
        total = taxes_computed['total_excluded']
        for tax in taxes_computed['taxes']:
            total += tax['amount']
        return total

    def convert_date(self, date, date_format='%d%m%y'):
        """ Converts the date to the needed format for the export:
        The format can be given free by using the known python formats """
        return date.strftime(date_format)

    def copy(self, selfdefault=None):
        """ Prevent the copy of the object"""
        raise UserError(_('Warning! Exports cannot be duplicated.'))

    def pre_export(self):
        """ Method to call before the Import starts and the moves to export
        are going to be browsed"""
        return True

    def export(self, mode=False, date_from=False, date_to=False, args=False):
        """ Method that generates the csv export by the given parameters """
        if date_from and date_to:
            period = str(date_from) + ' - ' + str(date_to)
        elif date_from and not date_to:
            period = str(date_from)
        else:
            period = ''
        export_id = self.create({
            'name': self.env['ir.sequence'].next_by_code('syscoon.financeinterface.name'),
            'mode': mode,
            'period': period,
        })
        return export_id


class syscoonFinanceinterfaceBookingtextConfig(models.Model):
    """ This class provides parameters for the configuration of the creation of the bookingtext """
    _name = 'syscoon.financeinterface.bookingtext.config'
    _description = 'syscoon Financial Interface Config for the Bookingtext'
    _order = 'sequence asc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    sequence = fields.Integer(string='Sequence', default=10)
    name = fields.Char('Name', compute='_name_get', store=True)
    field = fields.Selection([
        ('partner_id.name', 'Partner Name'),
        ('move_name', 'Move Name'),
        ('ref', 'Move Reference'),
        ('name', 'Move Line Name')], string='Fields')

    @api.depends('field')
    def _name_get(self):
        self.name = dict(self._fields['field'].selection).get(self.field)

