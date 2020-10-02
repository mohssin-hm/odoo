# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import api, fields, models, _

class AccountMove(models.Model):
    _inherit = 'account.move'


    @api.onchange('partner_id', 'journal_id')
    def _check_account_created(self):
        accounts = False
        if self.partner_id and self.journal_id:
            if self.journal_id.type in ['sale', 'purchase']:
                journal_id = self.journal_id
                partner = self.partner_id
                if partner.parent_id:
                    partner = partner.parent_id
                if journal_id.type == 'sale':
                    partner_default_id = str(partner['property_account_receivable_id'].id)
                    default_property_id = self.env['ir.property'].search(['&', 
                        ('name', '=', 'property_account_receivable_id'), ('res_id', '=', None),
                        ('company_id', '=', self.env.company.id)
                    ])
                    if default_property_id:
                        property_id = str(default_property_id['value_reference'].split(',')[1])
                        if property_id == partner_default_id:
                            ctx = dict(self._context)
                            ctx['type'] = 'receivable'
                            accounts = partner.create_accounts(ctx)

                if journal_id.type == 'purchase':
                    partner_default_id = str(partner['property_account_payable_id'].id)
                    default_property_id = self.env['ir.property'].search(['&', (
                        'name', '=', 'property_account_payable_id'), ('res_id', '=', None),
                        ('company_id', '=', self.env.company.id)])
                    if default_property_id:
                        property_id = str(default_property_id[0]['value_reference'].split(',')[1])
                        if property_id == partner_default_id:
                            ctx = dict(self._context)
                            ctx['type'] = 'payable'
                            accounts = partner.create_accounts(ctx)
            if self.line_ids and accounts:
                for line in self.line_ids:
                    if self.partner_id and line.account_id.id == int(partner_default_id):
                        if accounts and accounts[3]:
                            line.account_id = accounts[3].id

    @api.model_create_multi
    def create(self, vals_list):
        for val in vals_list:
            accounts = False
            partner_default_id = False
            if val.get('journal_id') and val.get('partner_id'):
                journal_id = self.env['account.journal'].browse(val['journal_id'])
                if journal_id.type in ['sale', 'purchase']:
                    partner = self.env['res.partner'].browse(val['partner_id'])
                    if partner.parent_id:
                        partner = partner.parent_id
                    if journal_id.type == 'sale':
                        partner_default_id = str(partner['property_account_receivable_id'].id)
                        default_property_id = self.env['ir.property'].search(['&', 
                            ('name', '=', 'property_account_receivable_id'), ('res_id', '=', None),
                            ('company_id', '=', self.env.company.id)
                        ])
                        if default_property_id:
                            property_id = str(default_property_id['value_reference'].split(',')[1])
                            if property_id == partner_default_id:
                                ctx = dict(self._context)
                                ctx['type'] = 'receivable'
                                accounts = partner.create_accounts(ctx)

                    if journal_id.type == 'purchase':
                        partner_default_id = str(partner['property_account_payable_id'].id)
                        default_property_id = self.env['ir.property'].search(['&', (
                            'name', '=', 'property_account_payable_id'), ('res_id', '=', None), 
                            ('company_id', '=', self.env.company.id)])
                        if default_property_id:
                            property_id = str(default_property_id[0]['value_reference'].split(',')[1])
                            if property_id == partner_default_id:
                                ctx = dict(self._context)
                                ctx['type'] = 'payable'
                                accounts = partner.create_accounts(ctx)
                if 'line_ids' in val and val['line_ids']:
                    for id in val['line_ids']:
                        if self.partner_id and id[2]['account_id'] == int(partner_default_id):
                            if accounts and accounts[3]:
                                id[2]['account_id'] = accounts[3].id
        return super(AccountMove, self).create(vals_list)

