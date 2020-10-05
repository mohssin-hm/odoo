#See LICENSE file for full copyright and licensing details.


from odoo import models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        company = self.env.user.company_id
        if company.create_auto_account_on == 'orders':
            partner = self.partner_id
            if partner.parent_id:
                partner = partner.parent_id
            if partner and not partner.customer_number:
                partner_default_id = str(partner['property_account_receivable_id'].id)
                default_property_id = self.env['ir.property'].search(['&', (
                    'name', '=', 'property_account_receivable_id'), ('res_id', '=', None),
                    ('company_id', '=', self.env.company.id)])
                if default_property_id:
                    property_id = str(default_property_id['value_reference'].split(',')[1])
                    if property_id == partner_default_id:
                        ctx = dict(self._context)
                        ctx['type'] = 'receivable'
                        partner.create_accounts(ctx)
        return res


