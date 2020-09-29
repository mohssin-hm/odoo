# -*- coding: utf-8 -*-
################################################################################
#
#   Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#
################################################################################

# Part of Odoo. See LICENSE file for full copyright and licensing details.

import base64
import os,shutil   #shutil for removing all files
import re
import odoo
from odoo.tools import config,pycompat  # config to get file storing folder
from odoo.tools.translate import _
from odoo.tools.mimetypes import guess_mimetype
from odoo import http
from odoo.http import request
from odoo.exceptions import UserError
from odoo.addons.web.controllers.main import ExcelExport,serialize_exception,ExportFormat

try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    xlsxwriter = None

class ExcelExport_New(ExcelExport):
    # Excel needs raw data to correctly handle numbers and date values
    raw_data = True

    @http.route('/web/export/xlsx', type='http', auth="user")
    @serialize_exception
    def index(self, data, token):
        return self.base(data, token)

    @property
    def content_type(self):
        return 'application/vnd.ms-excel'

    def filename(self, base):
        return base + '.xlsx'

    # ===================================================================================================
    #                        few functions use to store images and generate file name
    # ===================================================================================================
    def _filestore(self):
        return config.filestore(request._cr.dbname)

    def _full_folder_path(self, path):
        # sanitize path
        return os.path.join(self._filestore(), path)

    def _generate_semi_path(self, path, row_index, cell_index):
        return path+"/"+str(row_index)+str(cell_index)

    def _create_image(self,path,data,format):
        f = open(path+"."+format,"wb")
        f.write(base64.b64decode(data))
        f.close()
    # ======================================================================================================

    def from_data(self, fields, rows):
        if len(rows) > 65535:
            raise UserError(_('There are too many rows (%s rows, limit: 65535) to export as Excel 97-2003 (.xls) format. Consider splitting the export.') % len(rows))

        path=self._full_folder_path("WK_export_update") # ================ Use to Create Folder to store File

        workbook = xlsxwriter.Workbook(path+"/file_data.xlsx") # ============= Use xlsxwriter instead of xlwt
        worksheet = workbook.add_worksheet('Sheet 1')
        # ===================================================================================================
        #                    check that the folder exsists or not if not then create it
        # ===================================================================================================
        if not os.path.isdir(path):
            os.mkdir(path)
        bold = workbook.add_format({'bold': True})
        # ===================================================================================================

        for i, fieldname in enumerate(fields):
            worksheet.write(0, i, fieldname,bold)  # ====================== Create the heading in BOLD
            worksheet.set_column(0,i, 15)          # ====================== Set column size
        worksheet.set_row(0,20)


        for row_index, row in enumerate(rows):
            for cell_index, cell_value in enumerate(row):
                worksheet.set_row(row_index+1,80)  #

                if isinstance(cell_value, bytes):
                    # because xls uses raw export, we can get a bytes object
                    # here. xlwt does not support bytes values in Python 3 ->
                    # assume this is base64 and decode to a string, if this
                    # fails note that you can't export
                    try:
                        # ======================================================================================
                        #                               lde to store image not as b64
                        # ======================================================================================
                        mimetype = guess_mimetype(base64.b64decode(cell_value))
                        path1=self._generate_semi_path(path, row_index, cell_index)
                        if (mimetype.startswith('image')):
                            cell_value = odoo.tools.image_process(cell_value, size=odoo.tools.image_guess_size_from_field_name(fieldname), crop=False, quality=0)
                            img_format = mimetype.split('/')[1]
                            self._create_image(path1,cell_value,img_format)
                            worksheet.insert_image(row_index + 1, cell_index, path1+"."+img_format, options={})
                        else:
                            cell_value = pycompat.to_text(cell_value)
                    except UnicodeDecodeError:
                        raise UserError(_("Binary fields can not be exported to Excel unless their content is base64-encoded. That does not seem to be the case for %s.") % fields[cell_index])

                # if isinstance(cell_value, pycompat.string_types):
                if isinstance(cell_value, bytes):
                    cell_value = re.sub("\r", " ", pycompat.to_text(cell_value))
                    # Excel supports a maximum of 32767 characters in each cell:
                    cell_value = cell_value[:32767]
                # elif isinstance(cell_value, datetime.datetime):
                #     cell_style = datetime_style
                # elif isinstance(cell_value, datetime.date):
                #     cell_style = date_style
                worksheet.write(row_index + 1, cell_index, cell_value)

        # =======================================================================================================
        #                    Store the data in xls and then open and send that file to the user
        # =======================================================================================================
        workbook.close()
        fp = open(path+"/file_data.xlsx","rb")
        # =======================================================================================================
        data = fp.read()
        fp.close()
        if os.path.isdir(path): shutil.rmtree(path)
        return data
