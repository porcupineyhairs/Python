# # 获取表单字段
    # widgets = api.get_form_widgets()
    # print('获取表单字段：')
    # print(widgets)

    # # 按条件获取表单数据
    # title = ['work_uuid',
    #          'insert_time', 'insert_date',
    #          'update_time', 'update_date',
    #          'final_time', 'final_date',
    #          'work_time_type',
    #          'process_flag_1', 'process_flag_2',
    #          ]
	#
    # data_filter = {
    #                 'rel': 'and',
    #                 'cond': [
    #                     api.set_dict_filter('process_flag_1', 'eq', '0')
    #                 ]
    #             }
	#
    # # print(data_filter)
	#
    # data = api.get_form_data('', 100, title, data_filter)
	#
    # delta = datetime.timedelta(hours=-12)
	#
    # # print('按条件获取表单数据：')
    # if not data:
    #     print('API返回无数据')
    # else:
    #     for tmp in data:
    #         print(tmp)
    #         _id = tmp['_id']
    #         work_uuid = tmp['work_uuid']
	#
    #         insert_time = tmp['insert_time']
    #         update_time = tmp['update_time']
	#
    #         insert_date = insert_time.split('T')[0] + 'T00:00:00.000Z'
    #         update_date = update_time.split('T')[0] + 'T00:00:00.000Z'
    #         final_time = ''
    #         final_date = ''
	#
    #         if tmp['work_time_type'] == '夜班':
    #             final_time = (datetime.datetime.strptime(insert_time, "%Y-%m-%dT%H:%M:%S.000Z") + delta).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    #             final_date = final_time.split('T')[0] + 'T00:00:00.000Z'
    #         else:
    #             final_time = insert_time
    #             final_date = insert_date
	#
    #         # print(_id)
    #         # print(insert_time)
    #         # print(insert_date)
	#
    #         update = {}
    #         # data_dict = {'insert_date': insert_date, }
    #         # api.set_dict_values(update, data_dict)
	#
    #         api.set_dict_value(update, 'insert_date', insert_date)
    #         api.set_dict_value(update, 'update_date', update_date)
    #         api.set_dict_value(update, 'final_time', final_time)
    #         api.set_dict_value(update, 'final_date', final_date)
    #         api.set_dict_value(update, 'process_flag_1', '1')
	#
    #         result = api.update_data(dataId=_id, data=update)

    # # 获取所有表单数据
    # form_data = api.get_all_data([], {})
    # print('所有表单数据：')
    # for v in form_data:
    #     print(v)
    #
    # # 创建单条数据
    # data = {
    #     # 单行文本
    #     '_widget_1528252846720': {
    #         'value': '123'
    #     },
    #     # 子表单
    #     '_widget_1528252846801': {
    #         'value': [{
    #             '_widget_1528252846952': {
    #                 'value': '123'
    #             }
    #         }]
    #     },
    #     # 数字
    #     '_widget_1528252847027': {
    #         'value': 123
    #     },
    #     # 地址
    #     '_widget_1528252846785': {
    #         'value': {
    #             'province': '江苏省',
    #             'city': '无锡市',
    #             'district': '南长区',
    #             'detail': '清名桥街道'
    #         }
    #     },
    #     # 多行文本
    #     '_widget_1528252846748': {
    #         'value': '123123'
    #     }
    # }
    #
    # create_data = api.create_data(data)
    # print('创建单条数据：')
    # print(create_data)
    #
    # # 更新单条数据
    # update = {
    #     # 单行文本
    #     '_widget_1528252846720': {
    #         'value': '12345'
    #     },
    #     # 子表单
    #     '_widget_1528252846801': {
    #         'value': [{
    #             '_widget_1528252846952': {
    #                 'value': '12345'
    #             }
    #         }]
    #     },
    #     # 数字
    #     '_widget_1528252847027': {
    #         'value': 12345
    #     },
    #     # 地址
    #     '_widget_1528252846785': {
    #         'value': {
    #             'province': '江苏省',
    #             'city': '无锡市',
    #             'district': '南长区',
    #             'detail': '清名桥街道'
    #         }
    #     },
    #     # 多行文本
    #     '_widget_1528252846748': {
    #         'value': '123123'
    #     }
    # }
    # result = api.update_data(create_data['_id'], update)
    # print('更新单条数据：')
    # print(result)
    #
    # # 查询单条数据
    # retrieve_data = api.retrieve_data(create_data['_id'])
    # print('查询单条数据：')
    # print(retrieve_data)
    #
    # # 删除单条数据
    # result = api.delete_data(create_data['_id'])
    # print('删除单条数据：')
    # print(result)