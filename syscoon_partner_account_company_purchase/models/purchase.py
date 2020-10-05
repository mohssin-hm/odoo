#See LICENSE file for full copyright and licensing details.


from odoo import models, api


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def button_confirm(self):
        res = super(PurchaseOrder, self).button_confirm()
        company = self.env.user.company_id
        if company.create_auto_account_on == 'orders':
            partner = self.partner_id
            if partner.parent_id:
                partner = partner.parent_id
            if partner and not partner.supplier_number:
                partner_default_id = str(partner['property_account_payable_id'].id)
                default_property_id = self.env['ir.property'].search(['&', (
                    'name', '=', 'property_account_payable_id'), ('res_id', '=', None), 
                    ('company_id', '=', self.env.company.id)])
                if default_property_id:
                    property_id = str(default_property_id['value_reference'].split(',')[1])
                    if property_id == partner_default_id:
                        ctx = dict(self._context)
                        ctx['type'] = 'payable'
                        self.env['res.partner'].browse(partner.id).create_accounts( ctx)
        return res

