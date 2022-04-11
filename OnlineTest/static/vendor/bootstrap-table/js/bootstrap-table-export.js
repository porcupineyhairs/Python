/**
 * @author zhixin wen <wenzhixin2010@gmail.com>
 * extensions: https://github.com/kayalshri/tableExport.jquery.plugin
 */

(function ($) {
    'use strict';
    var sprintf = $.fn.bootstrapTable.utils.sprintf;

    var TYPE_NAME = {
        json: 'JSON',
        xml: 'XML',
        png: 'PNG',
        csv: 'CSV',
        txt: 'TXT',
        sql: 'SQL',
        doc: 'MS-Word',
        excel: 'MS-Excel',
        xlsx: 'MS-Excel (OpenXML)',
        powerpoint: 'MS-Powerpoint',
        pdf: 'PDF'
    };

    $.extend($.fn.bootstrapTable.defaults, {
        showExport: false,
        exportDataType: 'basic', // basic, all, selected
        // 'json', 'xml', 'png', 'csv', 'txt', 'sql', 'doc', 'excel', 'powerpoint', 'pdf'
        exportTypes: ['json', 'xml', 'csv', 'txt', 'sql', 'excel'],
        exportOptions: {}
    });

    $.extend($.fn.bootstrapTable.defaults.icons, {
        export: 'glyphicon-export icon-share',
    });

    $.extend($.fn.bootstrapTable.locales, {
        formatExport: function () {
            return 'Export data';
        }
    });
    $.extend($.fn.bootstrapTable.defaults, $.fn.bootstrapTable.locales);

    var BootstrapTable = $.fn.bootstrapTable.Constructor,
        _initToolbar = BootstrapTable.prototype.initToolbar;

    BootstrapTable.prototype.initToolbar = function () {
        this.showToolbar = this.options.showExport;

        _initToolbar.apply(this, Array.prototype.slice.apply(arguments));

        /*自定义导出按钮*/
        var that = this;
        $(".export-excel").click(function () {

            var type = $(this).data('type');
            var doExport = function () {
                that.$el.tableExport($.extend({}, that.options.exportOptions, {
                    type: type,
                    escape: false
                }));
            };
            if (that.options.exportDataType === 'all' && that.options.pagination) {
                that.$el.one(that.options.sidePagination === 'server' ? 'post-body.bs.table' : 'page-change.bs.table', function () {
                    //渲染页面 合并单元格
                    if(that.options.exportOptions.mergeCell){
                        mergeTable(that,that.options.exportOptions.mergeCells)
                    }
                    doExport();
                    that.togglePagination();
                });
                that.togglePagination();
            } else if (that.options.exportDataType === 'selected') {
                var data = that.getData(),
                    selectedData = that.getAllSelections();

                // Quick fix #2220
                if (that.options.sidePagination === 'server') {
                    data = {total: that.options.totalRows};
                    data[that.options.dataField] = that.getData();

                    selectedData = {total: that.options.totalRows};
                    selectedData[that.options.dataField] = that.getAllSelections();
                }

                that.load(selectedData);
                doExport();
                that.load(data);
            } else {
                doExport();
            }

        })
        

        //动态合并单元格，获取object
        function getFromTable(table,field){
            var $table = table.$el
            var obj=[];
            var maxV=$table.find("th").length;

            var columnIndex=0;
            var filedVar;
            for(columnIndex=0;columnIndex<maxV;columnIndex++){
                filedVar=$table.find("th").eq(columnIndex).attr("data-field");
                if(filedVar==field) break;
            }
            var $trs=$table.find("tbody > tr");
            var $tr;
            var index=0;
            var content="";
            var contentid="";
            var row=1;
            for (var i = 0; i <$trs.length;i++)
            {
                $tr=$trs.eq(i);
                var contentItem=$tr.find("td").eq(columnIndex).find("div").eq(0).attr("title");
                var contentItemId=$tr.find("td").eq(0).find("div").eq(0).attr("data-id");
                //exist
                if((contentItem != '' &&  contentItem != null)&& (contentItemId != '' && contentItemId != null) && content==contentItem &&  contentid==contentItemId){
                    row++;
                }else{
                    //save
                    if(row>1){
                        obj.push({"index":index,"row":row});
                    }
                    index=i;
                    content=contentItem;
                    contentid=contentItemId;
                    row=1;
                }
            }
            if(row>1){
                obj.push({"index":index,"row":row});
            }
            return obj;

        }
      
        //动态合并单元格，方法
        function mergeTable($table,mergeCells){

            for(var i = 0 ; i < mergeCells.length ; i++){
                var obj=getFromTable($table,mergeCells[i]);
                for(var item in obj){
                    var options = {index:obj[item].index,
                        field:mergeCells[i],
                        colspan:1,
                        rowspan:obj[item].row
                    }
                    $table.mergeCells(options)

                }
            }

        }


        /******************* 自定义end****************/
        if (this.options.showExport) {
            var that = this,
                $btnGroup = this.$toolbar.find('>.btn-group'),
                $export = $btnGroup.find('div.export');

            if (!$export.length) {
                $export = $([
                    '<div class="export btn-group">',
                        '<button class="btn' +
                            sprintf(' btn-%s', this.options.buttonsClass) +
                            sprintf(' btn-%s', this.options.iconSize) +
                            ' dropdown-toggle" aria-label="export type" ' +
                            'title="' + this.options.formatExport() + '" ' +
                            'data-toggle="dropdown" type="button">',
                            sprintf('<i class="%s %s"></i> ', this.options.iconsPrefix, this.options.icons.export),
                            '<span class="caret"></span>',
                        '</button>',
                        '<ul class="dropdown-menu" role="menu">',
                        '</ul>',
                    '</div>'].join('')).appendTo($btnGroup);

                var $menu = $export.find('.dropdown-menu'),
                    exportTypes = this.options.exportTypes;

                if (typeof this.options.exportTypes === 'string') {
                    var types = this.options.exportTypes.slice(1, -1).replace(/ /g, '').split(',');

                    exportTypes = [];
                    $.each(types, function (i, value) {
                        exportTypes.push(value.slice(1, -1));
                    });
                }
                $.each(exportTypes, function (i, type) {
                    if (TYPE_NAME.hasOwnProperty(type)) {
                        $menu.append(['<li role="menuitem" data-type="' + type + '">',
                                '<a href="javascript:void(0)">',
                                    TYPE_NAME[type],
                                '</a>',
                            '</li>'].join(''));
                    }
                });

                $menu.find('li').click(function () {
                    var type = $(this).data('type'),
                        doExport = function () {
                            that.$el.tableExport($.extend({}, that.options.exportOptions, {
                                type: type,
                                escape: false
                            }));
                        };

                    if (that.options.exportDataType === 'all' && that.options.pagination) {
                        that.$el.one(that.options.sidePagination === 'server' ? 'post-body.bs.table' : 'page-change.bs.table', function () {
                            doExport();
                            that.togglePagination();
                        });
                        that.togglePagination();
                    } else if (that.options.exportDataType === 'selected') {
                        var data = that.getData(),
                            selectedData = that.getAllSelections();

                        // Quick fix #2220
                        if (that.options.sidePagination === 'server') {
                            data = {total: that.options.totalRows};
                            data[that.options.dataField] = that.getData();

                            selectedData = {total: that.options.totalRows};
                            selectedData[that.options.dataField] = that.getAllSelections();
                        }

                        that.load(selectedData);
                        doExport();
                        that.load(data);
                    } else {
                        doExport();
                    }
                });
            }
        }
    };
})(jQuery);