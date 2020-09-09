# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    customer_number = fields.Char(string='Customer Number / DATEV-Debitor', company_dependent=True)
    supplier_number = fields.Char(string='Supplier Number / DATEV-Creditor', company_dependent=True)

    def create_receivable_account(self):
        return self.create_accounts({'type': 'receivable'})

    def create_payable_account(self):
        return self.create_accounts({'type':'payable'})

    def create_accounts(self, context={}):
        ctx = context
        auto_account = self.env['ecoservice.partner.auto.account.company']
        receivable_property = self.env['ir.property'].search([
                                ('company_id', '=', self.env.user.company_id.id),
                                ('res_id', '=', False),
                                ('name', '=', 'property_account_receivable_id')])
        payable_property = self.env['ir.property'].search([
                                ('company_id', '=', self.env.user.company_id.id),
                                ('res_id', '=', False),
                                ('name', '=', 'property_account_payable_id')])
        receivable = False#
        payable = False
        for partner in self:
            if 'type' in ctx and ctx['type'] == 'receivable' and not partner.customer_number:
                if partner.property_account_receivable_id.id != int(receivable_property.value_reference.split(',')[1]):
                    partner.write({
                        'customer_number': partner.property_account_receivable_id.code,
                    })
                    return False, False, False, False
            if 'type' in ctx and ctx['type'] == 'payable' and not partner.supplier_number:
                if partner.property_account_payable_id.id != int(payable_property.value_reference.split(',')[1]):
                    partner.write({
                        'supplier_number': partner.property_account_payable_id.code,
                    })
                    return False, False, False, False
            if partner.customer_number:
                receivable = partner.customer_number
            if partner.supplier_number:
                payable = partner.supplier_number
            receivable, payable, receivable_id, payalbe_id = auto_account.get_accounts(partner, receivable, payable, ctx)
            if receivable:
                receivable_values = {
                    'customer_number': receivable
                }
                if self.env.user.company_id.add_number_to_partner_ref:
                    receivable_values['ref'] = receivable
                if self.env.user.company_id.use_separate_accounts:
                    receivable_values['property_account_receivable_id'] = receivable_id.id
                partner.write(receivable_values)
            if payable:
                payable_values = {
                    'supplier_number': payable,
                }
                if self.env.user.company_id.add_number_to_partner_ref:
                    payable_values['ref'] = payable
                if self.env.user.company_id.use_separate_accounts:
                    payable_values['property_account_payable_id'] = payalbe_id.id
                partner.write(payable_values)
        return receivable, payable, receivable_id, payalbe_id
