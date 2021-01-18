# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright 2019 EquickERP
#
##############################################################################

from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError
from odoo.tools import mute_logger
import time

SKIP_MODEL = ['_unknown', 'base', 'base_import.mapping', 'base_import.tests.models.char',
              'base_import.tests.models.char.noreadonly', 'base_import.tests.models.char.readonly',
              'base_import.tests.models.char.required', 'base_import.tests.models.char.states',
              'base_import.tests.models.char.stillreadonly', 'base_import.tests.models.complex',
              'base_import.tests.models.float', 'base_import.tests.models.m2o', 'base_import.tests.models.m2o.related',
              'base_import.tests.models.m2o.required', 'base_import.tests.models.m2o.required.related',
              'base_import.tests.models.o2m', 'base_import.tests.models.o2m.child', 'base_import.tests.models.preview',
              'format.address.mixin', 'ir.actions.act_url', 'ir.actions.act_window', 'ir.actions.act_window.view',
              'ir.actions.act_window_close', 'ir.actions.actions', 'ir.actions.client', 'ir.actions.report',
              'ir.actions.server', 'ir.actions.todo', 'ir.attachment', 'ir.autovacuum', 'ir.config_parameter',
              'ir.cron', 'ir.default', 'ir.exports', 'ir.exports.line', 'ir.fields.converter', 'ir.filters',
              'ir.http', 'ir.logging', 'ir.mail_server', 'ir.model', 'ir.model.access', 'ir.model.constraint',
              'ir.model.data', 'ir.model.fields', 'ir.model.relation', 'ir.module.category', 'ir.module.module',
              'ir.module.module.dependency', 'ir.module.module.exclusion', 'ir.property', 'ir.qweb', 'ir.qweb.field',
              'ir.qweb.field.barcode', 'ir.qweb.field.contact', 'ir.qweb.field.date', 'ir.qweb.field.datetime',
              'ir.qweb.field.duration', 'ir.qweb.field.float', 'ir.qweb.field.float_time', 'ir.qweb.field.html',
              'ir.qweb.field.image', 'ir.qweb.field.integer', 'ir.qweb.field.many2many', 'ir.qweb.field.many2one',
              'ir.qweb.field.monetary', 'ir.qweb.field.qweb', 'ir.qweb.field.relative', 'ir.qweb.field.selection',
              'ir.qweb.field.text', 'ir.rule', 'ir.sequence.date_range', 'ir.server.object.lines', 'ir.translation',
              'ir.ui.menu', 'ir.ui.view', 'ir.ui.view.custom', 'report.base.report_irmodulereference', 'report.layout',
              'web_editor.converter.test', 'web_editor.converter.test.sub', 'web_tour.tour', 'mail.tracking.value', 'mail.mail',
              'mail.message', 'res.users.log', 'iap.account', 'wizard.merge.data.ext', 'wizard.duplicate.data.merge', 'wizard.duplicate.data.merge.line', 'res.lang']


class WizardMergeData(models.Model):
    _name = 'wizard.merge.data.ext'
    _description = "Merge Data"

    @api.model
    def fetch_model_list(self):
        model_lst = []
        for model in self.env['ir.model'].search([('transient', '=', False)], order="name"):
            if model.model in SKIP_MODEL:
                continue
            model_lst += [(model.model, model.name + " (%s)" % (model.model))]
        return model_lst

    duplicate_rec_id = fields.Reference(selection='fetch_model_list', string="Duplicate Record")
    original_rec_id = fields.Reference(selection='fetch_model_list', string="Original Record")
    take_action = fields.Selection([('none', 'None'),
                                    ('delete', 'Delete'),
                                    ('archived', 'Archived')],
                                   default="delete",
                                   string="Action on Duplicate Record",
                                   help="""If this option is not selected, then the duplicate record will remains into database as it is. Only update the reference of the duplicate record.
                                        * Delete : it means the duplicate record will be delete.
                                        * Archived : it means it will exist into database as archived record. For this action into the table must be have 'active' field.""")

    def get_used_ref_table_list(self, table_name):
        self._cr.execute('''SELECT tc.constraint_name "constraint_name",
                                   tc.table_name "FK_tbl_name",
                                   kcu.column_name "FK_col_name",
                                   ccu.table_name "PK_tbl_name",
                                   ccu.column_name "PK_col_name"
                            FROM information_schema.table_constraints tc
                                JOIN information_schema.key_column_usage kcu ON tc.constraint_name = kcu.constraint_name
                                JOIN information_schema.constraint_column_usage ccu ON ccu.constraint_name = tc.constraint_name
                            WHERE constraint_type = 'FOREIGN KEY'
                                AND ccu.table_name='%s' ''' % table_name)
        return self._cr.dictfetchall()

    def get_list_of_fields(self, model_name):
        self._cr.execute("""SELECT name FROM ir_model_fields
                            WHERE model='%s'
                            AND relation='%s'
                            AND ttype='many2one'""" % (model_name, model_name))
        list_of_fields = [each['name'] for each in self._cr.dictfetchall()]
        return list_of_fields

    def action_merge_duplicate_data(self):
        duplicate_id = self.duplicate_rec_id
        original_id = self.original_rec_id
        if duplicate_id._name != original_id._name:
            raise ValidationError(_('Please select same Models.'))
        if duplicate_id.id == original_id.id:
            raise ValidationError(_('Please select different Record ID.'))

        # search for the reference used
        context = self.env.context
        if 'ctx_used_ref_table_list' in context:
            used_ref_table_list = context.get('ctx_used_ref_table_list')
        else:
            used_ref_table_list = self.get_used_ref_table_list(duplicate_id._table)

        # search for the parent child relationship
        if 'ctx_list_of_fields' in context:
            list_of_fields = context.get('ctx_list_of_fields')
        else:
            list_of_fields = self.get_list_of_fields(original_id._name)

        # for checking the parent-child relation ship
        if original_id._parent_name in list_of_fields:
            qry_dict = {'table': original_id._table,
                        'parent_col': original_id._parent_name,
                        'original_id': original_id.id}
            qry = """WITH RECURSIVE result_table AS (
                        SELECT id, %(parent_col)s FROM %(table)s WHERE id = %(original_id)s
                        UNION ALL
                        SELECT sub.id, sub.%(parent_col)s FROM %(table)s sub
                            INNER JOIN result_table r ON sub.id=r.%(parent_col)s
                    )
                    SELECT %(parent_col)s FROM result_table""" % qry_dict
            self._cr.execute(qry)
            check_parent_rec_qry_result = list(filter(None, map(lambda x: x[0], self._cr.fetchall())))
            if duplicate_id.id in check_parent_rec_qry_result:
                raise ValidationError(_("You cannot merge a record with parent record."))
        # Update reference into table.
        for each in used_ref_table_list:
            fk_table = each.get('FK_tbl_name')
            fk_col = each.get('FK_col_name')
            # Get column of all Table
            result = self._cr.execute("SELECT column_name FROM information_schema.columns WHERE table_name = '%s'" % (fk_table))
            other_column = []
            for data in self._cr.fetchall():
                if data[0] != fk_col:
                    other_column.append(data[0])
            params = {
                'table': fk_table,
                'column': fk_col,
                'value': other_column[0],
                'duplicate_id': duplicate_id.id,
                'original_id': original_id.id
            }
            if len(other_column) <= 1:
                self._cr.execute("""
                    UPDATE "%(table)s" as main1
                    SET "%(column)s" = %(original_id)s
                    WHERE
                        "%(column)s" = %(duplicate_id)s AND
                        NOT EXISTS (
                            SELECT 1
                            FROM "%(table)s" as sub1
                            WHERE
                                "%(column)s" = %(original_id)s AND
                                main1.%(value)s = sub1.%(value)s
                        )""" % params)
            else:
                try:
                    with mute_logger('odoo.sql_db'), self._cr.savepoint():
                        qry = '''UPDATE %(table)s SET %(column)s = %(original_id)s
                                    WHERE %(column)s = %(duplicate_id)s''' % params
                        self._cr.execute(qry)
                except Exception as e:
                    raise ValidationError(_('Error %s') % e)
        for fieldname in original_id._field_computed.keys():
            fieldname.compute_value(original_id)
            fieldname.compute_value(duplicate_id)

        # UPDATE The display_name value
        if 'name' in original_id._fields:
            old_name = original_id.sudo().name
            original_id.sudo().write({'name': old_name})
        # Update the parent_path into parent-child relation table like product category, location
        original_id._parent_store_compute()

        # Action on the the duplicate records
        if self.take_action == 'delete' and not self.env.context.get('ctx_from_multiple'):
            self._cr.execute("""DELETE FROM %s WHERE id = %s """ % (duplicate_id._table, duplicate_id.id))
        if self.take_action == 'archived':
            if 'active' in duplicate_id.fields_get():
                self._cr.execute("""UPDATE %s SET active='f' WHERE id=%s""" % (duplicate_id._table, duplicate_id.id))


class wizard_search_duplicate_data(models.TransientModel):
    _name = 'wizard.search.duplicate.data'
    _description = "wizard.search.duplicate.data"

    flds_lines = fields.One2many('wizard.search.duplicate.data.line', 'wizard_id', string="Fields List")

    def action_find_duplicate_data(self):
        context = self.env.context
        fields_lst = []
        for line in self.flds_lines:
            fields_lst.append(line.field_id.name)
        if not fields_lst:
            raise ValidationError(_("Please Select at least one field."))
        if len(fields_lst) != len(set(fields_lst)):
            raise ValidationError(_("You cannot select one field multiple times."))
        action_obj = self.env[context.get('active_model')]
        # start the process for searching the data
        str_fld = ','.join(map(str, fields_lst))
        self._cr.execute("""SELECT %s, count(*)
                            FROM %s
                            GROUP BY %s
                            HAVING count(*) > 1""" % (str_fld, action_obj._table, str_fld))
        result = self._cr.dictfetchall()
        record_ids = []
        for each in result:
            del each['count']
            domain = [(k, '=', v) for k, v in each.items()] 
            record_ids += action_obj.search(domain).ids
        return {'name': _(action_obj._description),
                'type': 'ir.actions.act_window',
                'view_mode': 'tree,form',
                'view_type': 'form',
                'res_model': context.get('active_model'),
                'domain': [('id', 'in', record_ids)],
                'context': {'group_by': fields_lst},
                'target': 'main',
        }


class wizard_search_duplicate_data_line(models.TransientModel):
    _name = 'wizard.search.duplicate.data.line'
    _description = "wizard.search.duplicate.data.line"
    _order = 'sequence, id'

    sequence = fields.Integer(string="Sequence", default=10)
    field_id = fields.Many2one('ir.model.fields', string="Field(s)")
    wizard_id = fields.Many2one('wizard.search.duplicate.data', string="Wizard Ref.")


class wizard_duplicate_data_merge(models.TransientModel):
    _name = 'wizard.duplicate.data.merge'
    _description = "wizard.duplicate.data.merge"

    take_action = fields.Selection([('none', 'None'),
                                    ('delete', 'Delete'),
                                    ('archived', 'Archived')],
                                   default="delete",
                                   string="Action on Duplicate Record",
                                   help="""If this option is not selected, then the duplicate record will remains into database as it is. Only update the reference of the duplicate record.
                                        * Delete : it means the duplicate record will be delete.
                                        * Archived : it means it will exist into database as archived record. For this action into the table must be have 'active' field.""")
    selected_record_ids = fields.One2many('wizard.duplicate.data.merge.line', 'wizard_id', string="Selected Record")

    @api.model
    def default_get(self, fld_lst):
        res = super(wizard_duplicate_data_merge, self).default_get(fld_lst)
        active_model = self.env.context.get('active_model')
        ids = []
        for each_id in self.env.context.get('active_ids'):
            ids.append((0, 0, {'record_id': each_id,
                               'record_ref': '%s,%s' % (active_model, each_id)}))
        res.update({'selected_record_ids': ids})
        return res

    def btn_merge_multiple_data(self):
        active_model = self.env.context.get('active_model')
        merge_obj = self.env['wizard.merge.data.ext']
        all_records = self.selected_record_ids.mapped('record_ref')
        keep_original_line_id = self.selected_record_ids.filtered(lambda l: l.keep_original == True)
        if len(keep_original_line_id) != 1:
            raise ValidationError(_("Please select one record as Original Record."))
        orig_rec_id = keep_original_line_id.record_ref
        duplicate_ids = (all_records - orig_rec_id).ids
        if not duplicate_ids:
            return
        if len(duplicate_ids) > 3:
            raise ValidationError(_("For safety reasons, please select less than 5 records together. You can re-open the wizard for several times if needed."))
        ctx = {'ctx_from_multiple': 1,
               'ctx_used_ref_table_list': merge_obj.get_used_ref_table_list(orig_rec_id._table),
               'ctx_list_of_fields': merge_obj.get_list_of_fields(orig_rec_id._name)}
        for each_record in duplicate_ids:
            merge_id = merge_obj.create({'take_action': self.take_action,
                                         'original_rec_id': "%s,%s" % (active_model, orig_rec_id.id),
                                         'duplicate_rec_id': "%s,%s" % (active_model, each_record)
                                         })
            merge_id.with_context(ctx).action_merge_duplicate_data()
        time.sleep(10)
        if self.take_action == 'delete':
            query = 'DELETE FROM %s WHERE id IN %%s' % orig_rec_id._table
            self._cr.execute(query, (tuple(duplicate_ids),))
        return {'type': 'ir.actions.act_window_close'}


class wizard_duplicate_data_merge_line(models.TransientModel):
    _name = 'wizard.duplicate.data.merge.line'
    _description = 'wizard.duplicate.data.merge.line'

    @api.model
    def fetch_model_list(self):
        model_lst = []
        for model in self.env['ir.model'].search([('transient', '=', False)], order="name"):
            if model.model in SKIP_MODEL:
                continue
            model_lst += [(model.model, model.name + " (%s)" % (model.model))]
        return model_lst

    wizard_id = fields.Many2one('wizard.duplicate.data.merge', string="Wizard ID")
    keep_original = fields.Boolean(string="Original Record")
    record_id = fields.Integer(string="Record ID")
    record_ref = fields.Reference(selection='fetch_model_list', string="Display Name")


class IrActions(models.Model):
    _inherit = 'ir.actions.actions'

    @api.model
    @tools.ormcache('frozenset(self.env.user.groups_id.ids)', 'model_name')
    def get_bindings(self, model_name):
        result = super(IrActions, self).get_bindings(model_name)
        result.setdefault('action', [])
        if result and model_name not in SKIP_MODEL:
            # find duplicate data action
            find_duplicate_data_action = self.env.ref('eq_merge_duplicate_data_extended.action_wizard_search_duplicate_data').read()
            result['action'] += find_duplicate_data_action
            # merge duplicate data action
            if self.env.user.has_group('eq_merge_duplicate_data_extended.group_merge_duplicate_data'):
                merge_data_action = self.env.ref('eq_merge_duplicate_data_extended.action_wizard_duplicate_data_merge').read()
                result['action'] += merge_data_action
        return result

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: