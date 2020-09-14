#See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api


class AccountMove(models.Model):
    _inherit = 'account.move'
    
    syscoon_datev_import_id = fields.Many2one('syscoon.datev.import', 'DATEV Import', readonly=True)

