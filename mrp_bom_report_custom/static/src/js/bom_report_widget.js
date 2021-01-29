odoo.define('mrp_bom_report_custom.mrp_bom_report_extend', function (require) {
'use strict';

var core = require('web.core');
var framework = require('web.framework');
var stock_report_generic = require('stock.stock_report_generic');
var MrpBomReport = require('mrp.mrp_bom_report');

var QWeb = core.qweb;
var _t = core._t;

MrpBomReport.include({
    _reload_report_type: function () {
        this._super.apply(this, arguments);
        this.$('.td_img').addClass('o_hidden');
        this.$('.o_mrp_prod_cost').addClass('o_hidden');
        this.$('.o_mrp_bom_cost').addClass('o_hidden');

        // To Hide/Show Image
        if (this.given_context.report_type === 'all_4' || this.given_context.report_type === 'all_3') {
            this.$('.td_img').removeClass('o_hidden');
        }
        else {
            this.$('.td_img').addClass('o_hidden');
        }

        // To Hide/Show Product Cost and BoM Cost
        if (this.given_context.report_type === 'all' || this.given_context.report_type === 'all_3') {
            this.$('.o_mrp_prod_cost').removeClass('o_hidden');
            this.$('.o_mrp_bom_cost').removeClass('o_hidden');
        }
        else {
            this.$('.o_mrp_prod_cost').addClass('o_hidden');
            this.$('.o_mrp_bom_cost').addClass('o_hidden');
        }
    }
});

});