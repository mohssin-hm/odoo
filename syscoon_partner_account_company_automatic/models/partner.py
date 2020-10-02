#See LICENSE file for full copyright and licensing details.


from odoo import models, api



class ResPartner(models.Model):
    _inherit = 'res.partner'

    # ===========================================================================
    # Class : ResPartner
    # Method : create
    # Description: Default method inherited for creating new receivable and payable while
    #              creating a partner based on its customer_rank and supplier_rank
    # ===========================================================================
    def create (self, vals):
        company_id =self.env.user.company_id
        result = super(ResPartner, self).create(vals)
        if company_id.create_auto_account_on == 'partners':
            if not result.parent_id:
                ctx = dict(self._context)
                if result.customer_rank>0:
                    ctx['type'] = 'receivable'
                    result.create_accounts( ctx)
                if result.supplier_rank>0:
                    ctx['type'] = 'payable'
                    result.create_accounts(ctx)
        return result
