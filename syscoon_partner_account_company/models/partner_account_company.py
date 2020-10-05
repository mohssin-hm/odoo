#See LICENSE file for full copyright and licensing details.


from odoo import models, fields, api, _


class ecoservice_partner_auto_account_company(models.Model):
    _name = 'ecoservice.partner.auto.account.company'
    _description = 'Configuration rules for automatic account generation'

    def get_accounts(self, partner_id, receivable_code, payable_code, ctx={}):
        partner_name = partner_id.name
        config_ids = self.env.company
        account_obj = self.env['account.account']
        receivable_account_id, receivable_code = False, False
        payable_account_id, payable_code = False, False
        for config in config_ids:
            if receivable_account_id:
                receivable_account_id, receivable_code = False, False
            if payable_account_id:
                payable_account_id, payable_code = False, False
            if 'type' in ctx and ctx['type'] == 'receivable' or 'type' not in ctx:
                receivable_field_ids = self.env['ir.model.fields'].search([('model', '=', 'res.partner'), ('name', '=', 'property_account_receivable_id')])
                if len(receivable_field_ids) == 1:
                    if not receivable_code:
                        receivable_code = config.receivable_sequence_id.next_by_id()
                    if config.use_separate_accounts:
                        receiveable_tax_ids = []
                        for ids in config.payable_template_id.tax_ids:
                            receiveable_tax_ids.append(ids.id)
                        receivable_account_values = {
                            'name': partner_name,
                            'currency_id': config.receivable_template_id.currency_id and config.receivable_template_id.currency_id.id or False,
                            'code': receivable_code,
                            'user_type_id': config.receivable_template_id.user_type_id.id,
                            'reconcile': config.receivable_template_id.reconcile,
                            'tax_ids': [(6, 0, receiveable_tax_ids)],
                            'company_id': config.id,
                            'tag_ids': [(6, 0, config.receivable_template_id.tag_ids.ids)],
                        }
                        receivable_account_id = account_obj.create(receivable_account_values)
            if 'type' in ctx and ctx['type'] == 'payable' or 'type' not in ctx:
                payable_field_ids = self.env['ir.model.fields'].search([('model', '=', 'res.partner'),('name', '=', 'property_account_payable_id')])
                if len(payable_field_ids) == 1:
                    if not payable_code:
                        payable_code = config.payable_sequence_id.next_by_id()
                    if config.use_separate_accounts:
                        payable_tax_ids = []
                        for ids in config.payable_template_id.tax_ids:
                            payable_tax_ids.append(ids.id)
                        payable_account_values = {
                            'name': partner_name,
                            'currency_id': config.payable_template_id.currency_id and config.payable_template_id.currency_id.id or False,
                            'code': payable_code,
                            'user_type_id': config.payable_template_id.user_type_id.id,
                            'reconcile': config.payable_template_id.reconcile,
                            'tax_ids': [(6, 0, payable_tax_ids)],
                            'company_id': config.id,
                            'tag_ids': [(6, 0, config.payable_template_id.tag_ids.ids)],
                        }
                        payable_account_id = account_obj.create(payable_account_values)
        return receivable_code, payable_code, receivable_account_id, payable_account_id

