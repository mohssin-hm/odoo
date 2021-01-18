# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright 2019 EquickERP
#
##############################################################################

from odoo import models, fields, api,_


class ir_model_fields(models.Model):
    _inherit = 'ir.model.fields'

    def name_get(self):
        res = []
        for field in self:
            if self.env.context.get('ctx_from_merge_data'):
                res.append((field.id, '%s' % (field.field_description)))
            else:
                res.append((field.id, '%s (%s)' % (field.field_description, field.model)))
        return res

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: