# -*- coding: utf-8 -*-
##############################################################################
#
#    Haresh Kansara
#    Copyright (C) 2020-TODAY Haresh Kansara(hareshkansara00@gmail.com).
#    Author: Haresh Kansara(hareshkansara00@gmail.com).
#    you can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    It is forbidden to publish, distribute, sublicense, or sell copies
#    of the Software or modified copies of the Software.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    GENERAL PUBLIC LICENSE (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from werkzeug.urls import url_encode
from odoo.tools.misc import get_lang
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class StockPicking(models.Model):

    _name = 'stock.picking'
    _inherit = ['stock.picking', 'portal.mixin',
                'mail.thread', 'mail.activity.mixin', 'utm.mixin']

    def send_template_email(self, template_id, model_desc):
        ctx = {
            'default_model': 'stock.picking',
            'default_res_id': self.id,
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'custom_layout': "mail.mail_notification_paynow",
            'force_email': True,
            'model_description': model_desc,
        }
        ctx.update(self._context)
        compose_record = self.env['mail.compose.message'].sudo(
        ).with_context(ctx).create({})
        if compose_record and compose_record.template_id:
            compose_record.onchange_template_id_wrapper()
        compose_record.action_send_mail()

    def action_done(self):
        res = super(StockPicking, self).action_done()
        for picking in self:
            if picking.picking_type_code == 'outgoing':
                template_id = self.env.ref(
                    'stock.mail_template_data_delivery_confirmation').id
                model_desc = 'Delivery Order'
                picking.with_user(self.env.ref('base.user_root').sudo(
                )).send_template_email(template_id, model_desc)
        return res

    def button_send_email(self):
        template = self.env.ref(
            'stock.mail_template_data_delivery_confirmation')
        ctx = {
            'default_model': 'stock.picking',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template.id),
            'default_template_id': template.id,
            'default_composition_mode': 'comment',
            'custom_layout': "mail.mail_notification_paynow",
            'force_email': True,
            'model_description': 'Delivery Order',
        }
        return {
            'name': _('Send Delivery Confirmation Email'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(False, 'form')],
            'view_id': False,
            'target': 'new',
            'context': ctx,
        }


class SaleOrderTemplate(models.Model):

    _inherit = 'sale.order.template'

    is_printing_inv = fields.Boolean(string='Is Printing Template?')


class AccountMove(models.Model):

    _inherit = 'account.move'

    is_printing_inv = fields.Boolean(string='Is Printing Invoice?')

    def action_invoice_sent(self):
        """ Open a window to compose an email, with the edi invoice template
            message loaded by default
        """
        self.ensure_one()
        template = self.env.ref(
            'account.email_template_edi_invoice', raise_if_not_found=False)
        if self.is_printing_inv:
            template_rec = self.env['mail.template'].sudo().search(
                [('name', 'ilike', '3D-Printing-Service-Invoice: Send by email')], limit=1)
            if template_rec:
                template = template_rec
        lang = get_lang(self.env)
        if template and template.lang:
            lang = template._render_template(
                template.lang, 'account.move', self.id)
        else:
            lang = lang.code
        compose_form = self.env.ref(
            'account.account_invoice_send_wizard_form', raise_if_not_found=False)
        ctx = dict(
            default_model='account.move',
            default_res_id=self.id,
            # For the sake of consistency we need a default_res_model if
            # default_res_id is set. Not renaming default_model as it can
            # create many side-effects.
            default_res_model='account.move',
            default_use_template=bool(template),
            default_template_id=template and template.id or False,
            default_composition_mode='comment',
            mark_invoice_as_sent=True,
            custom_layout="mail.mail_notification_paynow",
            model_description=self.with_context(lang=lang).type_name,
            force_email=True
        )
        return {
            'name': _('Send Invoice'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'account.invoice.send',
            'views': [(compose_form.id, 'form')],
            'view_id': compose_form.id,
            'target': 'new',
            'context': ctx,
        }


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    is_printing_inv = fields.Boolean(
        string='Is Printing Template?', store=True, related='sale_order_template_id.is_printing_inv')

    def _find_mail_template(self, force_confirmation_template=False):
        template_id = False

        if force_confirmation_template or (self.state == 'sale' and not self.env.context.get('proforma', False)):
            template_id = int(self.env['ir.config_parameter'].sudo(
            ).get_param('sale.default_confirmation_template'))
            template_id = self.env['mail.template'].search(
                [('id', '=', template_id)]).id
            if not template_id:
                template_id = self.env['ir.model.data'].xmlid_to_res_id(
                    'custom_print_report.mail_template_sale_confirmation_inh', raise_if_not_found=False)
        if not template_id:
            template_id = self.env['ir.model.data'].xmlid_to_res_id(
                'sale.email_template_edi_sale', raise_if_not_found=False)
            if self.is_printing_inv:
                template = self.env['mail.template'].search(
                    [('name', '=', 'Sales Order 3D Printing Service')], limit=1)
                if template:
                    template_id = template.id

        return template_id

    def _prepare_invoice(self):
        """
        Prepare the dict of values to create the new invoice for a sales order. This method may be
        overridden to implement custom invoice generation (making sure to call super() to establish
        a clean extension chain).
        """
        self.ensure_one()
        # ensure a correct context for the _get_default_journal method and company-dependent fields
        self = self.with_context(
            default_company_id=self.company_id.id, force_company=self.company_id.id)
        journal = self.env['account.move'].with_context(
            default_type='out_invoice')._get_default_journal()
        if not journal:
            raise UserError(_('Please define an accounting sales journal for the company %s (%s).') % (
                self.company_id.name, self.company_id.id))

        invoice_vals = {
            'is_printing_inv': self.is_printing_inv,
            'ref': self.client_order_ref or '',
            'type': 'out_invoice',
            'narration': self.note,
            'currency_id': self.pricelist_id.currency_id.id,
            'campaign_id': self.campaign_id.id,
            'medium_id': self.medium_id.id,
            'source_id': self.source_id.id,
            'invoice_user_id': self.user_id and self.user_id.id,
            'team_id': self.team_id.id,
            'partner_id': self.partner_invoice_id.id,
            'partner_shipping_id': self.partner_shipping_id.id,
            'invoice_partner_bank_id': self.company_id.partner_id.bank_ids[:1].id,
            'fiscal_position_id': self.fiscal_position_id.id or self.partner_invoice_id.property_account_position_id.id,
            'journal_id': journal.id,  # company comes from the journal
            'invoice_origin': self.name,
            'invoice_payment_term_id': self.payment_term_id.id,
            'invoice_payment_ref': self.reference,
            'transaction_ids': [(6, 0, self.transaction_ids.ids)],
            'invoice_line_ids': [],
            'company_id': self.company_id.id,
        }
        return invoice_vals

    def send_template_email(self, template_id, model_desc, cc=''):
        ctx = {
            'default_model': 'sale.order',
            'default_res_id': self.id,
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True,
            'custom_layout': "mail.mail_notification_paynow",
            'force_email': True,
            'model_description': model_desc,
            'default_partner_ids': [(6, 0, [self.partner_id.id])]
        }
        compose_record = self.env['mail.compose.message'].sudo(
        ).with_context(ctx).create({})
        if compose_record and compose_record.template_id:
            compose_record.onchange_template_id_wrapper()
        compose_record.action_send_mail()


class SaleAdvancePaymentInv(models.TransientModel):

    _inherit = "sale.advance.payment.inv"

    def _prepare_invoice_values(self, order, name, amount, so_line):
        invoice_vals = {
            'is_printing_inv': order.is_printing_inv,
            'ref': order.client_order_ref,
            'type': 'out_invoice',
            'invoice_origin': order.name,
            'invoice_user_id': order.user_id.id,
            'narration': order.note,
            'partner_id': order.partner_invoice_id.id,
            'fiscal_position_id': order.fiscal_position_id.id or order.partner_id.property_account_position_id.id,
            'partner_shipping_id': order.partner_shipping_id.id,
            'currency_id': order.pricelist_id.currency_id.id,
            'invoice_payment_ref': order.reference,
            'invoice_payment_term_id': order.payment_term_id.id,
            'invoice_partner_bank_id': order.company_id.partner_id.bank_ids[:1].id,
            'team_id': order.team_id.id,
            'campaign_id': order.campaign_id.id,
            'medium_id': order.medium_id.id,
            'source_id': order.source_id.id,
            'invoice_line_ids': [(0, 0, {
                'name': name,
                'price_unit': amount,
                'quantity': 1.0,
                'product_id': self.product_id.id,
                'product_uom_id': so_line.product_uom.id,
                'tax_ids': [(6, 0, so_line.tax_id.ids)],
                'sale_line_ids': [(6, 0, [so_line.id])],
                'analytic_tag_ids': [(6, 0, so_line.analytic_tag_ids.ids)],
                'analytic_account_id': order.analytic_account_id.id or False,
            })],
        }

        return invoice_vals


class ProductTemplate(models.Model):

    _inherit = 'product.template'

    def _get_combination_info(self, combination=False, product_id=False, add_qty=1, pricelist=False, parent_combination=False, only_template=False):
        combination_info = super(ProductTemplate, self)._get_combination_info(
            combination=combination, product_id=product_id, add_qty=add_qty, pricelist=pricelist,
            parent_combination=parent_combination, only_template=only_template)

        current_website = False

        if self.env.context.get('website_id'):
            current_website = self.env['website'].get_current_website()
            if not pricelist:
                pricelist = current_website.get_current_pricelist()

        current_pricelist = pricelist
        # product_variant = self.env['product.product'].browse(combination_info['product_id']) or self
        product_variant = self.env['product.product'].browse(combination_info['product_id'])
        if not product_variant:
            product_variant = self.env['product.product'].search([('product_tmpl_id', '=', self.ids[0])], limit=1)
        var_qty = current_pricelist.item_ids.filtered(lambda r: (r.applied_on == '0_product_variant' and r.product_id == product_variant)).sorted(key=lambda m: m.min_quantity,reverse=False).mapped('min_quantity')
        pro_qty = current_pricelist.item_ids.filtered(lambda r: (r.applied_on == '1_product' and r.product_tmpl_id == product_variant.product_tmpl_id)).sorted(key=lambda m: m.min_quantity,reverse=False).mapped('min_quantity')
        item = []
        glob_qty = current_pricelist.item_ids.filtered(lambda r: (r.applied_on == '3_global')).sorted(key=lambda m: m.min_quantity,reverse=False).mapped('min_quantity')
        if var_qty:
            item = var_qty + [x for x in pro_qty if x < var_qty[0]] + [x for x in glob_qty if x < var_qty[0]]
        elif not var_qty and pro_qty:
            item = pro_qty + [x for x in glob_qty if x < pro_qty[0]]
        elif glob_qty and not var_qty and not pro_qty:
            item = glob_qty
        item.sort()
        items = item

        if self.env.ref('custom_print_report.product_price_discount_details', raise_if_not_found=False):
            combination_info.update(product_details=self.env['ir.ui.view'].render_template('custom_print_report.product_price_discount_details', values={
                'product_variant': product_variant,
                'items': items,
            }))
        return combination_info
