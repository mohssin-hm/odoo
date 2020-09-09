# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, _
from odoo.exceptions import UserError

import re


class AccountMove(models.Model):
    """ Adds the posibility to check the move line if they are compatible for 
    the DATEV export"""
    _inherit = 'account.move'

    datev_checks_enabled = fields.Boolean('Perform Datev Checks', default=lambda self: self.env.user.company_id.datev_checks_enabled)
    datev_ref = fields.Char(string='DATEV Ref', index=True)

    def post(self):
        """Inherits the post method to provide the DATEV checks"""
        for move in self:
            if move.datev_checks_enabled:
                self.make_datev_checks(move)
        return super(AccountMove, self).post()

    def write(self, vals):
        if vals.get('state') == 'posted':
            if self.journal_id.type == 'purchase' and self.ref:
                vals['datev_ref'] = re.sub(r'[\W_]+', '', self.ref)
            else:
                vals['datev_ref'] = re.sub(r'[\W_]+', '', self.name)
        return super(AccountMove, self).write(vals)

    def make_datev_checks(self, move):
        """Checks the move and the move lines if the counteraccount is set and
        if the account_id is an automatic account in DATEV. Checks also if the
        taxes are set correctly and if a VAT-ID is required if it is set in the partner."""
        errors = []
        #if not move.export_account_counterpart:
        #    errors.append(_('The move has no account counterpart. Please set it manually.'))
        line_count = 1
        for line in move.line_ids:
            if len(line.tax_ids) > 1:
                errors.append(_('Move Line %s has more than one tax account, but allowed is only one.' % line_count))
            if line.account_id.datev_automatic_account:
                if not line.tax_ids:
                    errors.append(_('Move line %s has an automatic account, but there is no tax set.' % line_count))
                else:
                    for tax in line.tax_ids:
                        if tax.id not in line.account_id.datev_automatic_tax.ids:
                            errors.append(_('Move line %s has an automatic account, but the tax %s is not in the list of the allowed taxes!' % (line_count, tax.name)))
            if not line.account_id.datev_automatic_account:
                if line.tax_ids and not line.tax_ids[0].datev_tax_key:
                    errors.append(_('Move line %s has taxes applied, but the tax has no DATEV Tax Key' % line_count))
            if line.account_id.datev_vatid_required and not line.partner_id.vat:
                errors.append(_('The account on move line %s needs the VAT-ID, but in the Partner %s it is not set' % (line_count, line.partner_id.name)))
        if errors:
            raise UserError('\n'.join(errors))
        return errors


