# -*- coding : utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class SaleOrderUpdate(models.Model):
	_inherit = 'sale.order'

	invoiced_amount = fields.Float(String = 'Invoiced Amount' ,compute ='_computetotal')
	amount_due = fields.Float(String ='Amount Due',compute ='_computedue')
	paid_amount = fields.Float(String ='Paid Amount',compute ='_computepaid')
	amount_paid_percent = fields.Float(compute = 'action_amount_paid')
	currency_id = fields.Many2one('res.currency', string='Currency',
                              default=lambda self: self.env.user.company_id.currency_id)
	

	def _computetotal(self):
		invoice_id = self.env['account.move'].search(['&',('invoice_origin','=', self.name),'|',('state','=','posted'),('invoice_payment_state','=','paid')])
		total = 0
		for comp in invoice_id:
			total += comp.amount_total
		self.invoiced_amount = total

	def _computedue(self):
		item_id = self.env['account.move'].search(['&',('invoice_origin','=', self.name),'|',('state','=','posted'),('invoice_payment_state','=','paid')])
		aggregate = 0
		for comp in item_id:
			aggregate +=comp.amount_residual

		self.amount_due = aggregate

	@api.depends('invoiced_amount','amount_due')
	def _computepaid(self):
		for res in self:
			res.paid_amount = float(res.invoiced_amount) - float(res.amount_due)

	@api.depends('paid_amount','invoiced_amount')
	def action_amount_paid(self):
		for res in self:
			if res.invoiced_amount > 0:
				for res in self:
					res.amount_paid_percent = round(100 * res.paid_amount / res.invoiced_amount, 3)
			else:
				for res in self:
					res.amount_paid_percent = False





	
		



