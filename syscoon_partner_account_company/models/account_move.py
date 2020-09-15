
# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import api, fields, models, _
from odoo.exceptions import RedirectWarning, UserError, ValidationError

class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        warning = {}
        if self.partner_id:
            rec_account = self.partner_id.property_account_receivable_id
            pay_account = self.partner_id.property_account_payable_id
            if not rec_account and not pay_account:
                action = self.env.ref('account.action_account_config')
                msg = _(
                    'Cannot find a chart of accounts for this company, You should configure it. \nPlease go to Account Configuration.')
                raise RedirectWarning(msg, action.id, _('Go to the configuration panel'))
            p = self.partner_id
            if p.invoice_warn == 'no-message' and p.parent_id:
                p = p.parent_id
            if p.invoice_warn and p.invoice_warn != 'no-message':
                # Block if partner only has warning but parent company is blocked
                if p.invoice_warn != 'block' and p.parent_id and p.parent_id.invoice_warn == 'block':
                    p = p.parent_id
                warning = {
                    'title': _("Warning for %s") % p.name,
                    'message': p.invoice_warn_msg
                }
                if p.invoice_warn == 'block':
                    self.partner_id = False
                    return {'warning': warning}
        for line in self.line_ids:
            line.partner_id = self.partner_id.commercial_partner_id
        if self.is_sale_document(include_receipts=True):
            self.invoice_payment_term_id = self.partner_id.property_payment_term_id
        elif self.is_purchase_document(include_receipts=True):
            self.invoice_payment_term_id = self.partner_id.property_supplier_payment_term_id

        self._compute_bank_partner_id()
        self.invoice_partner_bank_id = self.bank_partner_id.bank_ids and self.bank_partner_id.bank_ids[0]

        # Find the new fiscal position.
        delivery_partner_id = self._get_invoice_delivery_partner_id()
        new_fiscal_position_id = self.env['account.fiscal.position'].get_fiscal_position(
            self.partner_id.id, delivery_id=delivery_partner_id)
        self.fiscal_position_id = self.env['account.fiscal.position'].browse(new_fiscal_position_id)
        existing_terms_lines = self.line_ids.filtered(
            lambda line: line.account_id.user_type_id.type in ('receivable', 'payable'))
        self.line_ids -= existing_terms_lines
        self._recompute_dynamic_lines()
        if warning:
            return {'warning': warning}
