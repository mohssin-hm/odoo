odoo.define('custom_print_report.basic_fields', function (require) {
"use strict";

    var core = require('web.core');
    var AbstractFieldBinary = require('web.basic_fields').AbstractFieldBinary;

    require("web.zoomodoo");

    var qweb = core.qweb;
    var _t = core._t;
    var _lt = core._lt;

    var FieldBinaryInherit = AbstractFieldBinary.include({
        init: function (parent, name, record) {
            this._super.apply(this, arguments);
            this.fields = record.fields;
            this.useFileAPI = !!window.FileReader;
            this.max_upload_size = 500 * 1024 * 1024; // 25Mo
            if (!this.useFileAPI) {
                var self = this;
                this.fileupload_id = _.uniqueId('o_fileupload');
                $(window).on(this.fileupload_id, function () {
                    var args = [].slice.call(arguments).slice(1);
                    self.on_file_uploaded.apply(self, args);
                });
            }
        },
    });

});