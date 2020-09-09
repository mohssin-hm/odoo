# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'

class AccountMoveL10NDe(models.Model):
    _inherit = 'account.move'

    export_id = fields.Many2one('syscoon.financeinterface', 'Export', ondelete='set null', copy=False)
    export_manual = fields.Boolean('Set Account Counterpart')
    export_account_counterpart = fields.Many2one('account.account', compute='_get_export_datev_account',
        help='Technical field needed for move exports', store=True)

    @api.depends('journal_id', 'line_ids', 'journal_id.default_debit_account_id', 'journal_id.default_credit_account_id')
    def _get_export_datev_account(self):
        """
        Set the account counterpart for the move autmaticaly
        """
        for move in self:
            value = False
            # If move has an invoice, return invoice's account_id
            if move.is_invoice(include_receipts=True):
                payment_term_lines = move.line_ids.filtered(
                    lambda line: line.account_id.user_type_id.type in ('receivable', 'payable'))
                if payment_term_lines and payment_term_lines[0].account_id:
                    move.export_account_counterpart = payment_term_lines[0].account_id
                continue
            # If move belongs to a bank journal, return the journal's account (debit/credit should normally be the same)
            if move.journal_id.type == 'bank' and move.journal_id.default_debit_account_id:
                move.export_account_counterpart = move.journal_id.default_debit_account_id
                continue
            # If the move is an automatic exchange rate entry, take the gain/loss account set on the exchange journal
            elif move.journal_id.type == 'general' and move.journal_id == self.env.company.currency_exchange_journal_id:
                accounts = [
                    move.journal_id.default_debit_account_id,
                    move.journal_id.default_credit_account_id,
                ]
                lines = move.line_ids.filtered(lambda r: r.account_id in accounts)
                if len(lines) == 1:
                    move.export_account_counterpart = lines.account_id
                    continue

            # Look for an account used a single time in the move, that has no originator tax
            aml_debit = self.env['account.move.line']
            aml_credit = self.env['account.move.line']
            for aml in move.line_ids:
                if aml.debit > 0:
                    aml_debit += aml
                if aml.credit > 0:
                    aml_credit += aml
            if len(aml_debit) == 1:
                value = aml_debit[0].account_id
            elif len(aml_credit) == 1:
                value = aml_credit[0].account_id
            else:
                aml_debit_wo_tax = [a for a in aml_debit if not a.tax_line_id]
                aml_credit_wo_tax = [a for a in aml_credit if not a.tax_line_id]
                if len(aml_debit_wo_tax) == 1:
                    value = aml_debit_wo_tax[0].account_id
                elif len(aml_credit_wo_tax) == 1:
                    value = aml_credit_wo_tax[0].account_id
            if not value:
                lines = []
                for line in move.line_ids:
                    lines.append(line.account_id)
                if lines:
                    counterpart_account = max(x for x in lines if lines.count(x) > 0)
                    value = counterpart_account
            if not move.export_manual:
                move.export_account_counterpart = value

