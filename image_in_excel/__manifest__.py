# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>
#################################################################################
{
    'name'                       : "Show Images in Excel",

    'summary'                    : """This module allows you to export the images instead of Base64 while exporting Excel file.""",

    'description'                : """Allows you to export the images instead of Base64 while exporting Excel file.""",

    'category'                   : 'eCommerce',
    'author'                     : 'Webkul Software Pvt. Ltd.',
    'version'                    : '1.0.0',
    'license'                    : 'Other proprietary',
    'maintainer'                 : 'Mandeep Duggal',
    "css"                        :  [],
    "js"                         :  [],
    'images'                     :  ['static/description/Banner.png'],
    'depends'                    : ['base','web'],
    'demo'                       : [],
    'website'                    : '',
    'live_test_url'              : 'http://odoodemo.webkul.com/?module=image_in_excel&lifetime=90&lout=1&custom_url=/',
    'data'                       : [
                                    # 'security/ir.model.access.csv',
                                ],
    'application'               :  True,
    'installable'               :  True,
    'auto_install'              :  False,
    'price'                     :  35,
    'currency'                  :  'EUR',
    'sequence'                  :  1,
    'external_dependencies'     :  {'python3': ['XlsxWriter']},
}
