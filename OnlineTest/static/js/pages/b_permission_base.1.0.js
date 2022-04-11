		window.operateEvents = {
            'click .Btn-Edit': function (e, value, row, index) {
                dataEdit(row);
            },
            'click .Btn-Add': function (e, value, row, index) {
                dataAdd(row);
            },
        };
        function statusFormatter(value, row, index) {
            if (value == true) {
                return '<span class="label label-success">启用</span>';
            } else {
                return '<span class="label label-default">失效</span>';
            }
        };
        function operateFormatter(value, row, index) {
            var rtnStr = '';
            rtnStr += '<div class="bk-margin-5 btn-group">'
            if(row.parent == '0'){
                rtnStr += '<button type="button" class="Btn-Add btn btn-xs btn-info"><i class="fa fa-plus" ></i>新增</button>'
            }
            rtnStr += '<button type="button" class="Btn-Edit btn btn-xs btn-info"><i class="fa fa-pencil-square-o" ></i>修改</button>'
            rtnStr += '</div>'
            return rtnStr;
        };
        $('#table').bootstrapTable({
            toolbar: '#toolbar',
            striped: true,                      //是否显示行间隔色
            cache: false,                       //是否使用缓存，默认为true，所以一般情况下需要设置一下这个属性（*）
            //pagination: true,                   //是否显示分页（*）
            sortable: true,                     //是否启用排序
            sortOrder: "asc",                   //排序方式
            sidePagination: "client",           //分页方式：client客户端分页，server服务端分页（*）
            //pageNumber: 1,                       //初始化加载第一页，默认第一页
            //pageSize: 1000,                       //每页的记录行数（*）
            //pageList: [25, 50],        //可供选择的每页的行数（*）
            search: true,                       //是否显示表格搜索，此搜索是客户端搜索，不会进服务端，所以，个人感觉意义不大
            strictSearch: true,
            showColumns: true,                  //是否显示所有的列
            minimumCountColumns: 2,             //最少允许的列数
            clickToSelect: false,                //是否启用点击选中行
            //height: 500,                        //行高，如果没有设置height属性，表格自动根据记录条数觉得表格高度
            idField: "id",                     //每一行的唯一标识，一般为主键列
            showToggle: true,                    //是否显示详细视图和列表视图的切换按钮
            cardView: false,                    //是否显示详细视图
            detailView: false,                   //是否显示父子表

            columns: [
                { field: 'name', title: '权限名称', width:'300px',  },
                { field: 'valid',  title: '状态', align: 'center', width:'50px', formatter: statusFormatter },
                { field: 'url', title: '访问地址' },
                { field: 'show_index', title: '序号', align: 'center', width:'80px'},
                { field: 'operate', title: '操作', width: '180px', align: 'center', events : operateEvents, formatter: operateFormatter},
            ],
            treeShowField: 'name',
            parentIdField: 'parent',
            onResetView: function(data) {
                //console.log('load');
                $('#table').treegrid({
                    initialState: 'collapsed',// 所有节点都折叠
                    //initialState: 'expanded',// 所有节点都展开，默认展开
                    treeColumn: 0,
                    // expanderExpandedClass: 'glyphicon glyphicon-minus',  //图标样式
                    // expanderCollapsedClass: 'glyphicon glyphicon-plus',
                    onChange: function() {
                        //$('#table').bootstrapTable('resetWidth');
                    }
                });
            },
        });

        var url = location.href;
        var opt = '';
        $('#btn-perm-add').click(function (t) {
            opt = 'post';
            $('#perm-opt-add-son').hide();
            $('#perm-opt-edit').hide();
            $('#perm-opt-add-parent').show();
            $('#form-group-perm-parent-id').hide();
            $('#form-group-perm-parent-name').hide();
            $('#form-group-perm-id').hide();
            $('#form-group-perm-valid').show();
            $('#perm-name').val('')
            $('#perm-parent-id').val('0')
            $('#perm-parent-name').val('')
            $('#perm-id').val('-1')
            $('#perm-show-index').val('')
            $('#perm-iamge').val('')
            $('#perm-remark').val('')
            $('#form-group-perm-name').removeClass('has-error');
            $('#perm-name-exists').hide();
            $('#form-group-perm-url').removeClass('has-error');
            $('#perm-url-exists').hide();
            $('#permModal').modal('show')
        });
        $('#btn-perm-save').click(function(t) {
            $.ajax({
                url: url,
                dataType: 'json',
                type: 'POST',
                async: true,
                data: {
                    'opt': opt,
                    'id': $('#perm-id').val(),
                    'name': $('#perm-name').val(),
                    'parent': $('#perm-parent-id').val(),
                    'parent_name': $('#perm-parent-name').val(),
                    'valid': $('#valid-select').val(),
                    'url': $('#perm-url').val(),
                    'show_index': $('#perm-show-index').val(),
                    'image': $('#perm-image').val(),
                    'remark': $('#perm-remark').val()},
                success: function(req){
                    $('#permModal').modal('hide');
                    init();
                },
                error: function(){

                },
            });
        });
        init();
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
        function dataEdit(row){
            opt = 'put';
            $('#perm-opt-add-son').hide();
            $('#perm-opt-edit').show();
            $('#perm-opt-add-parent').hide();
            $('#form-group-perm-parent-name').show();
            $('#form-group-perm-id').show();
            $('#form-group-perm-valid').show();
            $('#form-group-perm-name').removeClass('has-error');
            $('#perm-name-exists').hide();
            $('#perm-url-exists').hide();
            $('#perm-id').attr('readonly', true);
            $('#perm-id').val(row.id);
            $('#perm-parent-id').attr('readonly', true);
            $('#perm-parent-id').val(row.parent);
            $('#perm-parent-name').attr('readonly', true);
            $('#perm-parent-name').val(row.parent_name);
            $('#perm-name').val(row.name);
            $('#perm-url').val(row.url);
            $('#valid-select').val(row.valid ? 1 : 0);
            $('#perm-show-index').val(row.show_index);
            $('#perm-image').val(row.image);
            $('#perm-remark').val(row.remark);
            $('#btn-perm-save').attr('disabled', false);

            $('#permModal').modal('show');
        }
        function dataAdd(row){
            opt = 'post';
            $('#perm-opt-edit').hide();
            $('#perm-opt-add').show();
            $('#perm-opt-add-parent').hide();
            $('#form-group-perm-parent-name').show();
            $('#form-group-perm-id').show();
            $('#form-group-perm-valid').show();
            $('#form-group-perm-name').removeClass('has-error');
            $('#perm-name-exists').hide();
            $('#perm-url-exists').hide();
            $('#perm-id').attr('readonly', true);
            $('#perm-id').val('-1');
            $('#form-group-perm-id').hide();
            $('#perm-parent-id').attr('readonly', true);
            $('#perm-parent-id').val(row.id);
            $('#perm-parent-name').attr('readonly', true);
            $('#perm-parent-name').val(row.name);
            $('#perm-name').val('');
            $('#perm-url').val('');
            $('#perm-show-index').val('1');
            $('#perm-image').val('');
            $('#perm-remark').val('');
            $('#btn-perm-save').attr('disabled', false);
            $('#permModal').modal('show');
        }