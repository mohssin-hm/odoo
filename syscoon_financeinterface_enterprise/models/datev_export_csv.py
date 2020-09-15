
from odoo import models

class DatevExportCSV(models.AbstractModel):
    _inherit = 'account.general.ledger'

    def _get_reports_buttons(self):
        buttons = super(DatevExportCSV, self)._get_reports_buttons()
        button_count = 0
        for button in buttons:
            if button['name'] == 'Export Datev (zip)':
                del buttons[button_count]
            button_count += 1
        return buttons