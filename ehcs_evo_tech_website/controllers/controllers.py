# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo.addons.website.controllers import main


class ThemeMenu(http.Controller):
    @http.route('/', type='http', auth='public', website=True)
    def home_menu(self, **kw):
        return request.render('ehcs_evo_tech_website.theme_menu_home_page', {})

    @http.route('/filamente/', type='http', auth='public', website=True)
    def filamente_menu(self, **kw):
        return request.render('ehcs_evo_tech_website.theme_menu_filamente_page', {})
 
    @http.route('/branchen/', type='http', auth='public', website=True)
    def branchen_menu(self, **kw):
        return request.render('ehcs_evo_tech_website.theme_menu_branchen_page', {})
 
    @http.route('/ueber-uns/', type='http', auth='public', website=True)
    def ueberuns_menu(self, **kw):
        return request.render('ehcs_evo_tech_website.theme_menu_ueber_page', {})
    
    @http.route('/kunden-area/', type='http', auth='public', website=True)
    def kunden_area_menu(self, **kw):
        return request.render('ehcs_evo_tech_website.theme_menu_kundenarea_page', {})
    
    @http.route('/contactus/', type='http', auth='public', website=True)
    def contactus_menu(self, **kw):
        return request.render('ehcs_evo_tech_website.theme_menu_contactus_page', {})
    
    @http.route('/3d-druck-dienstleistung/', type='http', auth='public', website=True)
    def dienstleistung_menu(self, **kw):
        return request.render('ehcs_evo_tech_website.theme_menu_dienstleistung_page', {})
 
 
class ThemSubeMenuOne(http.Controller): 
    @http.route('/3d-drucker-el-102/', type='http', auth='public', website=True)
    def drucker_submenu_one(self, **kw):
        return request.render('ehcs_evo_tech_website.theme_menu_drucker_submenu', {})
    
    @http.route('/3d-drucker-el-11/', type='http', auth='public', website=True)
    def drucker_submenu_two(self, **kw):
        return request.render('ehcs_evo_tech_website.theme_menu_drucker_submenu_two', {})
    
    @http.route('/3d-drucker-all-inclusive-leasing/', type='http', auth='public', website=True)
    def drucker_submenu_three(self, **kw):
        return request.render('ehcs_evo_tech_website.theme_menu_drucker_submenu_three', {})
    
 
class ThemSubeMenutwo(http.Controller): 
    @http.route('/filamente/ultem-9085/', type='http', auth='public', website=True)
    def filamente_submenu_one(self, **kw):
        return request.render('ehcs_evo_tech_website.theme_menu_filamente_submenu_one', {})
    
    @http.route('/filamente/ultem-1010/', type='http', auth='public', website=True)
    def filamente_submenu_two(self, **kw):
        return request.render('ehcs_evo_tech_website.theme_menu_filamente_submenu_two', {})
 
    @http.route('/filamente/polyamid-cf/', type='http', auth='public', website=True)
    def filamente_submenu_three(self, **kw):
        return request.render('ehcs_evo_tech_website.theme_menu_filamente_submenu_three', {})
    
    @http.route('/filamente/abs/', type='http', auth='public', website=True)
    def filamente_submenu_four(self, **kw):
        return request.render('ehcs_evo_tech_website.theme_menu_filamente_submenu_four', {})
    
    @http.route('/filamente/abs-esd/', type='http', auth='public', website=True)
    def filamente_submenu_five(self, **kw):
        return request.render('ehcs_evo_tech_website.theme_menu_filamente_submenu_five', {})
    
    @http.route('/filamente/abs-fr/', type='http', auth='public', website=True)
    def filamente_submenu_six(self, **kw):
        return request.render('ehcs_evo_tech_website.theme_menu_filamente_submenu_six', {})
    
    @http.route('/filamente/pc-lexan/', type='http', auth='public', website=True)
    def filamente_submenu_seven(self, **kw):
        return request.render('ehcs_evo_tech_website.theme_menu_filamente_submenu_seven', {})
    
    @http.route('/filamente/iglidur/', type='http', auth='public', website=True)
    def filamente_submenu_eight(self, **kw):
        return request.render('ehcs_evo_tech_website.theme_menu_filamente_submenu_eight', {})
    
    @http.route('/filamente/asa/', type='http', auth='public', website=True)
    def filamente_submenu_nine(self, **kw):
        return request.render('ehcs_evo_tech_website.theme_menu_filamente_submenu_nine', {})
    
    @http.route('/filamente/abs-pc/', type='http', auth='public', website=True)
    def filamente_submenu_ten(self, **kw):
        return request.render('ehcs_evo_tech_website.theme_menu_filamente_submenu_ten', {})
    
    @http.route('/filamente/pps/', type='http', auth='public', website=True)
    def filamente_submenu_ele(self, **kw):
        return request.render('ehcs_evo_tech_website.theme_menu_filamente_submenu_ele', {})
    
    @http.route('/filamente/pla/', type='http', auth='public', website=True)
    def filamente_submenu_twe(self, **kw):
        return request.render('ehcs_evo_tech_website.theme_menu_filamente_submenu_twe', {})
    
    @http.route('/filamente/pet/', type='http', auth='public', website=True)
    def filamente_submenu_thirteen(self, **kw):
        return request.render('ehcs_evo_tech_website.theme_menu_filamente_submenu_thirteen', {})
    
    @http.route('/filamente/metall-druck/', type='http', auth='public', website=True)
    def filamente_submenu_fourteen(self, **kw):
        return request.render('ehcs_evo_tech_website.theme_menu_filamente_submenu_fourteen', {})
    
    @http.route('/filamente/tpu/', type='http', auth='public', website=True)
    def filamente_submenu_fifty(self, **kw):
        return request.render('ehcs_evo_tech_website.theme_menu_filamente_submenu_fifty', {})
    
    @http.route('/evo-supp/', type='http', auth='public', website=True)
    def filamente_submenu_sixteen(self, **kw):
        return request.render('ehcs_evo_tech_website.theme_menu_filamente_submenu_sixteen', {})
    
 
class ThemSubeMenuthree(http.Controller):    
    @http.route('/automotive/', type='http', auth='public', website=True)
    def menu_branchen_subone(self, **kw):
        return request.render('ehcs_evo_tech_website.theme_menu_branchen_subone', {})
    
    @http.route('/maschinenbau/', type='http', auth='public', website=True)
    def menu_branchen_subtwo(self, **kw):
        return request.render('ehcs_evo_tech_website.theme_menu_branchen_subtwo', {})
    
    @http.route('/werkzeug-und-vorrichtungsbau/', type='http', auth='public', website=True)
    def menu_branchen_subthree(self, **kw):
        return request.render('ehcs_evo_tech_website.theme_menu_branchen_subthree', {})
    
    @http.route('/bildungseinrichtungen/', type='http', auth='public', website=True)
    def menu_branchen_subfour(self, **kw):
        return request.render('ehcs_evo_tech_website.theme_menu_branchen_subfour', {})
    
    @http.route('/prototypenbau/', type='http', auth='public', website=True)
    def menu_branchen_five(self, **kw):
        return request.render('ehcs_evo_tech_website.theme_menu_branchen_five', {})
    
    @http.route('/serienproduktion/', type='http', auth='public', website=True)
    def menu_branchen_six(self, **kw):
        return request.render('ehcs_evo_tech_website.theme_menu_branchen_six', {})
 

class ThemSubeMenufour(http.Controller): 
    
    @http.route('/academy/', type='http', auth='public', website=True)
    def menu_about_subtwo(self, **kw):
        return request.render('ehcs_evo_tech_website.theme_menu_about_subtwo', {})
    
    @http.route('/termine/', type='http', auth='public', website=True)
    def menu_about_subthree(self, **kw):
        return request.render('ehcs_evo_tech_website.theme_menu_about_subthree', {})
    
    @http.route('/jobs/', type='http', auth='public', website=True)
    def menu_about_subfour(self, **kw):
        return request.render('ehcs_evo_tech_website.theme_menu_about_subfour', {})
    
    @http.route('/presse/', type='http', auth='public', website=True)
    def menu_about_five(self, **kw):
        return request.render('ehcs_evo_tech_website.theme_menu_about_subfive', {})

    @http.route('/events/opening-moenchengladbach/', type='http', auth='public', website=True)
    def menu_about_subthree_moenchengladbach(self, **kw):
        return request.render('ehcs_evo_tech_website.menu_about_subthree_moenchengladbach', {})
    
    @http.route('/events/fakuma-2/', type='http', auth='public', website=True)
    def menu_about_subthree_event_fakuma(self, **kw):
        return request.render('ehcs_evo_tech_website.menu_about_subthree_event_fakuma', {})
    
    @http.route('/events/formnext-2/', type='http', auth='public', website=True)
    def menu_about_subthree_event_fakuma2(self, **kw):
        return request.render('ehcs_evo_tech_website.menu_about_subthree_event_formnext2', {})
    
    
class ThemSubeMenufive(http.Controller):
    @http.route('/kunden-area/kvp-kontinuierlicher-verbesserungsprozess/', type='http', auth='public', website=True)
    def menu_customer_subone(self, **kw):
        return request.render('ehcs_evo_tech_website.theme_menu_customer_subone', {})
    
    @http.route('/kunden-area/material-datenblaetter/', type='http', auth='public', website=True)
    def menu_customer_subtwo(self, **kw):
        return request.render('ehcs_evo_tech_website.theme_menu_customer_subtwo', {})
    
    @http.route('/kunden-area/support/', type='http', auth='public', website=True)
    def menu_customer_three(self, **kw):
        return request.render('ehcs_evo_tech_website.theme_menu_customer_subthree', {})
    
    @http.route('/kunden-area/firmware/', type='http', auth='public', website=True)
    def menu_customer_four(self, **kw):
        return request.render('ehcs_evo_tech_website.theme_menu_customer_subfour', {})
    
    @http.route('/kunden-area/simplify/', type='http', auth='public', website=True)
    def menu_customer_five(self, **kw):
        return request.render('ehcs_evo_tech_website.theme_menu_customer_subfive', {})
    
#     @http.route('/kunden-area/material-datenblaetter/', type='http', auth='public', website=True)
#     def menu_customer_six(self, **kw):
#         return request.render('ehcs_evo_tech_website.theme_menu_customer_subtwo', {})
    
    @http.route('/additive-fertigung/', type='http', auth='public', website=True)
    def menu_customer_seven(self, **kw):
        return request.render('ehcs_evo_tech_website.theme_menu_customer_subseven', {})
    
    @http.route('/rapid-prototyping/', type='http', auth='public', website=True)
    def menu_customer_eight(self, **kw):
        return request.render('ehcs_evo_tech_website.theme_menu_customer_subseven_one', {})
    
    @http.route('/simplify3d/', type='http', auth='public', website=True)
    def menu_customer_nine(self, **kw):
        return request.render('ehcs_evo_tech_website.theme_menu_customer_subseven_two', {})
    

class ThemSubeMenuSimplifyTab(http.Controller):
    @http.route('/additions-tab/', type='http', auth='public', website=True)
    def theme_submenu_tab_additions(self, **kw):
        return request.render('ehcs_evo_tech_website.theme_submenu_tab_additions', {})
    
    @http.route('/advanced-tab/', type='http', auth='public', website=True)
    def theme_submenu_tab_advanced(self, **kw):
        return request.render('ehcs_evo_tech_website.theme_submenu_tab_advanced', {})
    
    @http.route('/extruder-tab/', type='http', auth='public', website=True)
    def theme_submenu_tab_extruder(self, **kw):
        return request.render('ehcs_evo_tech_website.theme_submenu_tab_extruder', {})
    
    @http.route('/infill-tab/', type='http', auth='public', website=True)
    def theme_submenu_tab_infill(self, **kw):
        return request.render('ehcs_evo_tech_website.theme_submenu_tab_infill', {})
    
    @http.route('/layer-tab/', type='http', auth='public', website=True)
    def theme_submenu_tab_layer(self, **kw):
        return request.render('ehcs_evo_tech_website.theme_submenu_tab_layer', {})
    
    @http.route('/other-tab/', type='http', auth='public', website=True)
    def theme_submenu_tab_other(self, **kw):
        return request.render('ehcs_evo_tech_website.theme_submenu_tab_other', {})
    
    @http.route('/speeds-tab/', type='http', auth='public', website=True)
    def theme_submenu_tab_speeds(self, **kw):
        return request.render('ehcs_evo_tech_website.theme_submenu_tab_speeds', {})
    
    @http.route('/support-tab/', type='http', auth='public', website=True)
    def theme_submenu_tab_support(self, **kw):
        return request.render('ehcs_evo_tech_website.theme_submenu_tab_support', {})
    
    @http.route('/temperature-tab/', type='http', auth='public', website=True)
    def theme_submenu_tab_temperature(self, **kw):
        return request.render('ehcs_evo_tech_website.theme_submenu_tab_temperature', {})
    
    @http.route('/anwenderbericht-pmt/', type='http', auth='public', website=True)
    def theme_submenu_tab_anwenderbericht(self, **kw):
        return request.render('ehcs_evo_tech_website.theme_submenu_tab_anwenderbericht', {})
    
    @http.route('/angebotsanfrage/', type='http', auth='public', website=True)
    def theme_submenu_tab_angebotsanfrage(self, **kw):
        return request.render('ehcs_evo_tech_website.theme_submenu_tab_angebotsanfrage', {})
    
    @http.route('/metusan/', type='http', auth='public', website=True)
    def theme_submenu_tab_metusan(self, **kw):
        return request.render('ehcs_evo_tech_website.theme_submenu_tab_metusan', {})
    
    @http.route('/smart-labs-carinthia/', type='http', auth='public', website=True)
    def theme_submenu_tab_smart_labs(self, **kw):
        return request.render('ehcs_evo_tech_website.theme_submenu_tab_smart_labs', {})
    
    @http.route('/cnc-academy/', type='http', auth='public', website=True)
    def theme_submenu_tab_cnc_academy(self, **kw):
        return request.render('ehcs_evo_tech_website.theme_submenu_tab_cnc_academy', {})
    
    @http.route('/kolm-motoren/', type='http', auth='public', website=True)
    def theme_submenu_tab_kolm_motoren(self, **kw):
        return request.render('ehcs_evo_tech_website.theme_submenu_tab_kolm_motoren', {})
    
    @http.route('/inocon/', type='http', auth='public', website=True)
    def theme_submenu_tab_inocon(self, **kw):
        return request.render('ehcs_evo_tech_website.theme_submenu_tab_inocon', {})
    
    
    
    