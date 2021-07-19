import requests
import json
import time


class APIUtils:

    WEBSITE = "https://api.jiandaoyun.com"
    RETRY_IF_LIMITED = True

    # 构造函数
    def __init__(self, appId, entryId, api_key):
        # 获取表单字段
        self.url_get_widgets = APIUtils.WEBSITE + '/api/v1/app/' + appId + '/entry/' + entryId + '/widgets'
        # 查询多条数据接口
        self.url_get_data = APIUtils.WEBSITE + '/api/v2/app/' + appId + '/entry/' + entryId + '/data'
        # 查询单条数据接口
        self.url_retrieve_data = APIUtils.WEBSITE + '/api/v2/app/' + appId + '/entry/' + entryId + '/data_retrieve'
        # 修改单条数据接口
        self.url_update_data = APIUtils.WEBSITE + '/api/v3/app/' + appId + '/entry/' + entryId + '/data_update'
        # 新建单条数据接口
        self.url_create_data = APIUtils.WEBSITE + '/api/v3/app/' + appId + '/entry/' + entryId + '/data_create'
        # 删除单条数据接口
        self.url_delete_data = APIUtils.WEBSITE + '/api/v1/app/' + appId + '/entry/' + entryId + '/data_delete'

        self.api_key = api_key

    # 带有认证信息的请求头
    def get_req_header(self):
        return {
            'Authorization': 'Bearer ' + self.api_key,
            'Content-Type': 'application/json;charset=utf-8'
        }

    # 发送http请求
    def send_request(self, method, request_url, data):
        headers = self.get_req_header()
        if method == 'GET':
            res = requests.get(request_url, params=data, headers=headers, verify=False)
        if method == 'POST':
            res = requests.post(request_url, data=json.dumps(data), headers=headers, verify=False)
        result = res.json()
        if res.status_code >= 400:
            if result['code'] == 8303 and APIUtils.RETRY_IF_LIMITED:
                # 5s后重试
                time.sleep(5)
                return self.send_request(method, request_url, data)
            else:
                raise Exception('请求错误！', result)
        else:
            return result

    # 获取表单字段
    def get_form_widgets(self):
        result = self.send_request('POST', self.url_get_widgets, {})
        return result['widgets']

    # 根据条件获取表单中的数据
    def get_form_data(self, dataId, limit, fields, data_filter):
        result = self.send_request('POST', self.url_get_data, {
            'data_id': dataId,
            'limit': limit,
            'fields': fields,
            'filter': data_filter
        })
        return result['data']

    # 获取表单中满足条件的所有数据
    def get_all_data(self, fields, data_filter):
        form_data = []

        # 递归取下一页数据
        def get_next_page(dataId):
            data = self.get_form_data(dataId, 100, fields, data_filter)
            if data:
                for v in data:
                    form_data.append(v)
                dataId = data[len(data) - 1]['_id']
                get_next_page(dataId)
        get_next_page('')
        return form_data

    # 检索一条数据
    def retrieve_data(self, dataId):
        result = self.send_request('POST', self.url_retrieve_data, {
            'data_id': dataId
        })
        return result['data']

    # 创建一条数据
    def create_data(self, data):
        result = self.send_request('POST', self.url_create_data, {
            'data': data
        })
        return result['data']

    # 更新数据
    def update_data(self, dataId, data):
        result = self.send_request('POST', self.url_update_data, {
            'data_id': dataId,
            'data': data
        })
        return result['data']

    # 删除数据
    def delete_data(self, dataId):
        result = self.send_request('POST', self.url_delete_data, {
            'data_id': dataId
        })
        return result

    def set_dict_value(self, dicts, key, value):
        dicts.update({key: {'value': value}})

    def set_dict_values(self, dicts, data_dict):
        for key in data_dict.keys():
            self.set_dict_value(dicts, key, data_dict[key])

    def set_dict_filter(self, field, method, value1=None, value2=None):
        dicts = {}
        if method in ['eq', 'ne', 'like', 'in', 'nin']:
            dicts = {'field': field, 'method': method, 'value': value1}
        elif method in ['empty', 'not_empty']:
            dicts = {'field': field, 'method': method}
        elif method in ['range']:
            dicts = {'field': field, 'method': method, 'value': [value1, value2]}
        return dicts

    # def set_dict_fliters(self, dicts):
    #     dict2 = {}