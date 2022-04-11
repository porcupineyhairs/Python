        $('#table').bootstrapTable({
            toolbar: '#toolbar',
            striped: true,                      //是否显示行间隔色
            cache: false,                       //是否使用缓存，默认为true，所以一般情况下需要设置一下这个属性（*）
            pagination: true,                   //是否显示分页（*）
            sortable: true,                     //是否启用排序
            sortOrder: "asc",                   //排序方式
            sidePagination: "client",           //分页方式：client客户端分页，server服务端分页（*）
            pageNumber: 1,                       //初始化加载第一页，默认第一页
            pageSize: 25,                       //每页的记录行数（*）
            pageList: [25, 50],        //可供选择的每页的行数（*）
            search: true,                       //是否显示表格搜索，此搜索是客户端搜索，不会进服务端，所以，个人感觉意义不大
            strictSearch: true,
            showColumns: true,                  //是否显示所有的列
            minimumCountColumns: 2,             //最少允许的列数
            clickToSelect: false,                //是否启用点击选中行
            //height: 500,                        //行高，如果没有设置height属性，表格自动根据记录条数觉得表格高度
            uniqueId: "type_id",                     //每一行的唯一标识，一般为主键列
            showToggle: true,                    //是否显示详细视图和列表视图的切换按钮
            cardView: false,                    //是否显示详细视图
            detailView: false,                   //是否显示父子表

            columns: [
                { field: 'type_id', title: '编号', align: 'center', width: '30px' },
                { field: 'type_name', title: '类型名称' },
                { field: 'remark', title: '备注' },
                { field: 'createuser', title: '创建人' },
                { field: 'createdate', title: '创建时间' },
                { field: 'modiuser', title: '修改人' },
                { field: 'modidate', title: '修改时间' },
            ],
            onClickRow:function(row, $element, field)
            {
                 rowClick(row, $element, field);
            }
        });
        $('#table-detail').bootstrapTable({
            striped: false,                      //是否显示行间隔色
            cache: false,                       //是否使用缓存，默认为true，所以一般情况下需要设置一下这个属性（*）
            pagination: false,                   //是否显示分页（*）
            sortable: false,                     //是否启用排序
            sortOrder: "asc",                   //排序方式
            sidePagination: "client",           //分页方式：client客户端分页，server服务端分页（*）
            pageNumber: 1,                       //初始化加载第一页，默认第一页
            pageSize: 25,                       //每页的记录行数（*）
            pageList: [25, 50],        //可供选择的每页的行数（*）
            search: false,                       //是否显示表格搜索，此搜索是客户端搜索，不会进服务端，所以，个人感觉意义不大
            strictSearch: false,
            showColumns: false,                  //是否显示所有的列
            minimumCountColumns: 2,             //最少允许的列数
            clickToSelect: false,                //是否启用点击选中行
            //height: 500,                        //行高，如果没有设置height属性，表格自动根据记录条数觉得表格高度
            idField: "perm_id",                     //每一行的唯一标识，一般为主键列
            showToggle: false,                    //是否显示详细视图和列表视图的切换按钮
            cardView: false,                    //是否显示详细视图
            detailView: false,                   //是否显示父子表

            columns: [
                { field: 'perm_id', title: '权限编号', align: 'center', width: '30px', },
                { field: 'perm__name', title: '权限名称' },
                { field: 'run', title: '运行', align: 'center', width: '30px', formatter: function (value, row, index) { return checkBoxFormatter(row.run, row.perm__parent, index, 'run')}},
                { field: 'new', title: '新增', align: 'center', width: '30px', formatter: function (value, row, index) { return checkBoxFormatter(row.new, row.perm__parent, index, 'new')}},
                { field: 'edit', title: '修改', align: 'center', width: '30px', formatter: function (value, row, index) { return checkBoxFormatter(row.edit, row.perm__parent, index, 'edit')}},
                { field: 'delete', title: '删除', align: 'center', width: '30px', formatter: function (value, row, index) { return checkBoxFormatter(row.delete, row.perm__parent, index, 'delete')}},
                { field: 'print', title: '打印', align: 'center', width: '30px', formatter: function (value, row, index) { return checkBoxFormatter(row.print, row.perm__parent, index, 'print')}},
                { field: 'export', title: '导出', align: 'center', width: '30px', formatter: function (value, row, index) { return checkBoxFormatter(row.export, row.perm__parent, index, 'export')}},
                { field: 'lock', title: '锁定', align: 'center', width: '30px', formatter: function (value, row, index) { return checkBoxFormatter(row.lock, row.perm__parent, index, 'lock')}},
            ],
            treeShowField: 'perm__name',
            parentIdField: 'perm__parent',
            onResetView: function(data) {
                $('#table-detail').treegrid({
                    //initialState: 'collapsed',// 所有节点都折叠
                    //initialState: 'expanded',// 所有节点都展开，默认展开
                    treeColumn: 1,
                    // expanderExpandedClass: 'glyphicon glyphicon-minus',  //图标样式
                    // expanderCollapsedClass: 'glyphicon glyphicon-plus',
                    onChange: function() {
                        //$('#table-detail').bootstrapTable('resetWidth');
                    }
                });
            },
            onClickCell: function(field, value, row, $element){
                if(field in {'run':'', 'new':'', 'edit':'', 'delete':'', 'print':'', 'export':'', 'lock':''}){
                    var index = $element.parent().data('index');
                    var checked = $('#'+field+index).is(':checked')
                    row[field] = checked;
                    $("#table-detail").bootstrapTable('updateRow',{index: index, row: row});
                }
            }
        });
        var url = location.href;
        var opt = '';
        init();
        $('#btn-type-add').click(function (t) {
            opt = 'post';
            $('#type-opt-add').show();
            $('#type-opt-edit').hide();
            $('#form-group-type-id').hide();
            $('#table-detail').hide();
            $('#type-name').val('')
            $('#type-id').val('-1')
            $('#type-remark').val('')
            $('#form-group-type-name').removeClass('has-error');
            $('#type-name-exists').hide();
            $('#typeModal').modal('show')
        });
        $('#type-name').on('input propertychange',function(){
            if($('#type-name').val() == ''){
                $('#btn-type-save').attr('disabled', true);
            }
            else{
                $.ajax({
                    url: url,
                    dataType: 'json',
                    type: 'POST',
                    async: true,
                    data: {'opt': 'check', 'type_name': $('#type-name').val(), 'type_id': $('#type-id').val()},
                    success: function(req){
                        if(req.status != 'ok'){
                            $('#form-group-type-name').addClass('has-error')
                            $('#type-name-exists').show();
                            $('#btn-type-save').attr('disabled', true);
                        }
                        else{
                            $('#form-group-type-name').removeClass('has-error')
                            $('#type-name-exists').hide();
                            $('#btn-type-save').attr('disabled', false);
                        }
                    },
                    error: function(){

                    },
                });
            }
        });
        $('#btn-type-save').click(function(t) {
            var permission = []
            if(opt == 'put'){
                var permission_data = $('#table-detail').bootstrapTable('getData');
                permission_data.forEach(function(item){
                    var dict = {
                        'perm_id': item.perm_id,
                        'run': item.run,
                        'new': item.new,
                        'edit': item.edit,
                        'delete': item.delete,
                        'print': item.print,
                        'export': item.export,
                        'lock': item.lock,
                    }
                    permission.push(dict);
                });
            };
            $.ajax({
                url: url,
                dataType: 'json',
                type: 'POST',
                async: true,
                data: {'opt': opt, 'type_name': $('#type-name').val(), 'type_id': $('#type-id').val(), 'remark': $('#type-remark').val(), 'permission': JSON.stringify(permission)},
                success: function(req){
                    $('#typeModal').modal('hide');
                    init();
                },
                error: function(){

                },
            });
        });
        function getTableAll(){
            $.ajax({
                url: url,
                dataType: 'json',
                type: 'POST',
                async: true, //请求是否异步，默认为异步，这也是ajax重要特性
                data: {'opt': 'get'},
                success: function (data){
                    $('#table').bootstrapTable('load', data);
                },
                error: function (){

                },
            })
        }
        function init(){
            getTableAll();
            $('#type-name-exists').hide();
            $('#btn-type-save').attr('disabled', true);
        }
        function checkBoxFormatter(value, parent, index, field){
            if(parent == 0) { return '' }
            else{ var checked = ''; if (value == true) {checked = 'checked="chenked"'} return '<input id="'+field+index+'" class="checkbox-default" type="checkbox" ' + checked + '>'}
        };
        function rowClick(row, $element, field){
            opt = 'put';
            $('#type-opt-add').hide();
            $('#type-opt-edit').show();
            $('#form-group-type-id').show();
            $('#form-group-type-name').removeClass('has-error');
            $('#type-name-exists').hide();
            $('#table-detail').show();
            $('#type-id').attr('readonly', true);
            $('#type-id').val(row.type_id);
            $('#type-name').val(row.type_name);
            $('#type-remark').val(row.remark);
            $('#btn-type-save').attr('disabled', false);
            $('#table-detail').bootstrapTable('load', row.permission);

            $('#typeModal').modal('show');
        }