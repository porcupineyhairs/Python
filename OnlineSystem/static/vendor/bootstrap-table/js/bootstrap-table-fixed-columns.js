(function ($) {
    'use strict';

    $.extend($.fn.bootstrapTable.defaults, {
        fixedColumns: false,
        fixedNumber: 1
    });

    var BootstrapTable = $.fn.bootstrapTable.Constructor,
        _initHeader = BootstrapTable.prototype.initHeader,
        _initBody = BootstrapTable.prototype.initBody,
        _resetView = BootstrapTable.prototype.resetView;

    BootstrapTable.prototype.initFixedColumns = function () {
        this.$fixedHeader = $([
            '<div class="fixed-table-header-columns">',
            '<table>',
            '<thead></thead>',
            '</table>',
            '</div>'].join(''));

        this.timeoutHeaderColumns_ = 0;
        this.$fixedHeader.find('table').attr('class', this.$el.attr('class'));
        this.$fixedHeaderColumns = this.$fixedHeader.find('thead');
        this.$tableHeader.before(this.$fixedHeader);

        this.$fixedBody = $([
            '<div class="fixed-table-body-columns">',
            '<table>',
            '<tbody></tbody>',
            '</table>',
            '</div>'].join(''));

        this.timeoutBodyColumns_ = 0;
        this.$fixedBody.find('table').attr('class', this.$el.attr('class'));
        this.$fixedBodyColumns = this.$fixedBody.find('tbody');
        this.$tableBody.before(this.$fixedBody);
    };

    BootstrapTable.prototype.initHeader = function () {
        _initHeader.apply(this, Array.prototype.slice.apply(arguments));

        if (!this.options.fixedColumns) {
            return;
        }

        this.initFixedColumns();
        
        var that = this, $trs = this.$header.find('tr').clone();
        $trs.each(function () {
            $(this).find('th:gt(' + (that.options.fixedNumber - 1) + ')').remove();
        });
        this.$fixedHeaderColumns.html('').append($trs);
    };

    BootstrapTable.prototype.initBody = function () {
        _initBody.apply(this, Array.prototype.slice.apply(arguments));

        if (!this.options.fixedColumns) {
            return;
        }
        var that = this,
            rowspan = 0;
        this.$fixedBodyColumns.html('');
        this.$body.find('> tr[data-index]').each(function () {
            var $tr = $(this).clone(),
                $tds = $tr.find('td');

            //$tr.html('');这样存在一个兼容性问题，在IE浏览器里面，清空tr,$tds的值也会被清空。
            //$tr.html('');
            var $newtr = $('<tr></tr>');
            $newtr.attr('data-index', $tr.attr('data-index'));
            $newtr.attr('data-uniqueid', $tr.attr('data-uniqueid'));
            var end = that.options.fixedNumber;
            if (rowspan > 0) {
                --end;
                --rowspan;
            }
            for (var i = 0; i < end; i++) {
            	if($tds.eq(i).has("input")){
            		$tds.eq(i).find("input").each(function(){
            			this.name="";
            		})
            	}
            	if($tds.eq(i).has("select")){
            		$tds.eq(i).find("select").each(function(){
            			this.name="";
            		})
            	}
                $newtr.append($tds.eq(i).clone());
            }
            that.$fixedBodyColumns.append($newtr);

            if ($tds.eq(0).attr('rowspan')) {
                rowspan = $tds.eq(0).attr('rowspan') - 1;
            }
        });
        
    };

    BootstrapTable.prototype.resetView = function () {
        _resetView.apply(this, Array.prototype.slice.apply(arguments));

        if (!this.options.fixedColumns) {
            return;
        }

        clearTimeout(this.timeoutHeaderColumns_);
        this.timeoutHeaderColumns_ = setTimeout($.proxy(this.fitHeaderColumns, this), this.$el.is(':hidden') ? 100 : 0);

        clearTimeout(this.timeoutBodyColumns_);
        this.timeoutBodyColumns_ = setTimeout($.proxy(this.fitBodyColumns, this), this.$el.is(':hidden') ? 100 : 0);
    };

    BootstrapTable.prototype.fitHeaderColumns = function () {
        var that = this,
            visibleFields = this.getVisibleFields(),
            headerWidth = 0;

        this.$body.find('tr:first-child:not(.no-records-found) > *').each(function (i) {
            var $this = $(this),
                index = i;
            if (i >= that.options.fixedNumber) {
                return false;
            }

            if (that.options.detailView && !that.options.cardView) {
                index = i - 1;
            }
            
            that.$fixedHeader.find('th[data-field="' + visibleFields[index] + '"]')
                .find('.fht-cell').width($this.innerWidth());
            headerWidth += $this.outerWidth();
        });
        this.$fixedHeader.width(headerWidth).show();
    };

    BootstrapTable.prototype.fitBodyColumns = function () {
        var that = this,
            top = -(parseInt(this.$el.css('margin-top'))),
            // the fixed height should reduce the scorll-x height
            height = this.$tableBody.height() - 18;
        if (!this.$body.find('> tr[data-index]').length) {
            this.$fixedBody.hide();
            return;
        }
        if (!this.options.height) {
            top = this.$fixedHeader.height()- 1;
            height = height - top;
        }
				
        this.$fixedBody.css({
            width: this.$fixedHeader.width(),
            height: height,
            top: top + 1
        }).show();
				
        this.$body.find('> tr').each(function (i) {
            that.$fixedBody.find('tr:eq(' + i + ')').height($(this).height() - 0.5);
            var thattds = this;
            that.$fixedBody.find('tr:eq(' + i + ')').find('td').each(function (j) {
                $(this).width($($(thattds).find('td')[j]).width() + 1);
            });
        });
        /*
         *页脚footer
         * */
        if (this.options.showFooter) {
        	var fotterElm=this.$body.parents(".fixed-table-body").next();
        	var a=this.$body.parents(".fixed-table-body").width();
        	var b=this.$body.parents(".fixed-table-body").scrollWidth;
        	fotterElm.width(this.$body.parents(".fixed-table-body").width());
        	var fixedNumberFooter=this.options.fixedNumber;
        	if($(".fixed-table-footer tr").length>1){
        		$(".fixed-table-footer tr:last").html("");
        		var $newFooterTr=$(".fixed-table-footer tr:last");
        	}else{
        		var $newFooterTr= $('<tr class="hideFooter"></tr>');
        	}
        	fotterElm.find("td").each(function(idx,val){
        		if(idx<fixedNumberFooter){
        			$newFooterTr.append($(val).clone());
        		}
        		fotterElm.find("tbody").append($newFooterTr);
        	})
        }
        /*
		 *显示footer统计
		 * */
        var isShowFooter=this.options.showFooter;
        var isFixed=this.options.fixedColumns;
        var FixedNum=this.options.fixedNumber;
        var fixedBottom=0;
        var obj=$(".fixed-table-body")[0];  
        var scrollBar=18;
	    /*if(obj.offsetHeight-obj.clientHeight<=0){  
	    	fixedBottom=54-scrollBar;
	    	var newHeight=parseFloat($(".fixed-table-body-columns").height())+scrollBar;
	    	$(".fixed-table-body-columns").css("height",newHeight+"px");
	    }else{
	    	fixedBottom=54;
	    } 
		if (isShowFooter&&isFixed&&(parseInt(FixedNum)>0)) {
			var boxWidth=parseFloat($(".fixed-table-body").width());
			var shijiWidth=parseFloat($(".fixed-table-footer .table").width());
			console.log(boxWidth+shijiWidth);
			//判断有无滚动条
			if(shijiWidth>=boxWidth){
				$(".fixed-table-footer").css("bottom",fixedBottom+"px");
				this.$body.parents(".fixed-table-body").css("paddingBottom","37px");
				var padB=parseFloat($(".fixed-table-header-columns").height());
				var obj=$(".fixed-table-body")[0];  
			    
	        	this.$body.parents(".fixed-table-container").css("paddingBottom",padB);
			}else{
				$(".fixed-table-footer").css("bottom","0");
				this.$body.parents(".fixed-table-body").css("paddingBottom","0px");
				this.$body.parents(".fixed-table-container").css("paddingBottom","37px");
			}
        }else{
        	$(".fixed-table-footer").css("bottom",fixedBottom+"px");
			this.$body.parents(".fixed-table-body").css("paddingBottom","37px");
        	this.$body.parents(".fixed-table-container").css("paddingBottom","37px");
        }*/
        // events
        this.$tableBody.on('scroll', function () {
            that.$fixedBody.find('table').css('top', -$(this).scrollTop());
            if((isShowFooter)&&(this.scrollLeft>0)){//水平滚动;
					$(".hideFooter").removeClass("hideFooter").addClass("footerFixed");
					var boxWidth=parseFloat($(".fixed-table-footer").width());
					var shijiWidth=parseFloat($(".fixed-table-footer .table").width());
					if(this.scrollLeft>(shijiWidth-boxWidth)){
						$(".footerFixed").css({left:this.scrollLeft-(this.scrollLeft-(shijiWidth-boxWidth))});
					}else{
						$(".footerFixed").css({left:this.scrollLeft});
					}
			}else{
				$(".footerFixed").removeClass("footerFixed").addClass("hideFooter");
			}
        });
        this.$body.find('> tr[data-index]').off('hover').hover(function () {
            var index = $(this).data('index');
            that.$fixedBody.find('tr[data-index="' + index + '"]').addClass('hover');
        }, function () {
            var index = $(this).data('index');
            that.$fixedBody.find('tr[data-index="' + index + '"]').removeClass('hover');
        });
        this.$fixedBody.find('tr[data-index]').off('hover').hover(function () {
            var index = $(this).data('index');
            that.$body.find('tr[data-index="' + index + '"]').addClass('hover');
        }, function () {
            var index = $(this).data('index');
            that.$body.find('> tr[data-index="' + index + '"]').removeClass('hover');
        });
    };

})(jQuery);

