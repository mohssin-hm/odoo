# -*- coding: utf-8 -*-
from odoo import api, fields , models


class Lang(models.Model):
    _inherit = 'res.lang'

    image = fields.Binary('Language Image',attachment=True)
    