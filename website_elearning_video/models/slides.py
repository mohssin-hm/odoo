# -*- coding: utf-8 -*-
#################################################################################
#
#   Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE file for full copyright and licensing details.
#   If not, see <https://store.webkul.com/license.html/>
#
#################################################################################

from odoo import api, fields, models, _
import logging
_logger = logging.getLogger(__name__)

class Slide(models.Model):
    _inherit = 'slide.slide'

    slide_attachment = fields.Many2one('ir.attachment', help="Video/Document")
    document_type = fields.Selection([('url', 'URL'), ('binary', 'File')],
                            string='Document Type', required=True, default='url', change_default=True,
                            help="You can either upload a file from your computer or copy/paste an internet link to your file.")

    @api.model
    def create(self, values):
        channel_id = self._context.get('default_channel_id')
        if channel_id:
            values['channel_id'] = channel_id
        if values.get('document_type') == 'binary':
            values['slide_type'] = 'video'
        res = super(Slide, self).create(values)
        return res

    def write(self, values):
        if values.get('document_type') == 'binary':
            values['slide_type'] = 'video'
        res = super(Slide, self).write(values)
        return res
    
    @api.onchange('document_type')
    def remove_link(self):
        self.url = ''
    
    @api.onchange('url')
    def remove_attachment_link(self):
        self.slide_attachment = False

class WebsiteSlides(models.Model):
    _name = "website.slide.video"
    
    allowed_types = fields.Many2many("wk.video.types")
    is_active = fields.Boolean("Is Active")

    @api.onchange('is_active')
    def set_active(self):
        if self.is_active:
            for setting in self.search([]):
                if setting.id != self.id:
                    setting.is_active = False
            self.is_active = True

class VideoTypes(models.Model):
    _name = "wk.video.types"

    name = fields.Char("Types",help="Write extension of videos allowed")

    @api.onchange('name')
    def add_prefix(self):

        if self.name:
            self.name = "video/"+self.name

