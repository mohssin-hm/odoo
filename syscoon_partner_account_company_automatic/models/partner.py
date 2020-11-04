#See LICENSE file for full copyright and licensing details.


from odoo import models, api



class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def create (self, vals):
        company_id =self.env.user.company_id
        result = super(ResPartner, self).create(vals)
        if company_id.create_auto_account_on == 'partners':
            if not result.parent_id:
                ctx = dict(self._context)
                if ctx.get('default_customer_rank'):
                    ctx['type'] = 'receivable'
                    result.create_accounts( ctx)
                if ctx.get('default_suppier_rank'):
                    ctx['type'] = 'payable'
                    result.create_accounts(ctx)
        return result
