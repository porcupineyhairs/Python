# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import time
import datetime

from dingtalk.client.api.base import DingTalkBaseAPI


class Vacation(DingTalkBaseAPI):

    DATE_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

    def type_list(self, op_userid, vacation_source='all'):
        """
        查询假期类型

        :param op_userid: 拥有“OA审批”应用权限的管理员的userid
        :param vacation_source: 假期来源。取值：all：所有假期类型；null：开放接口定义假期类型
        :return:
        """

        return self._post(
            '/topapi/attendance/vacation/type/list',
            {
                "op_userid": op_userid,
                "vacation_source": vacation_source
            },
            # result_processor=lambda x: x['recordresult']
        )

    def type_create(self, op_userid, vacation_source='all'):
        """
        创建假期类型

        :param op_userid: 拥有“OA审批”应用权限的管理员的userid
        :param vacation_source: 假期来源。取值：all：所有假期类型；null：开放接口定义假期类型
        :return:
        """

        return self._post(
            '/topapi/attendance/vacation/type/create',
            {
                "op_userid": op_userid,
                "vacation_source": vacation_source
            }
        )

    def type_update(self, op_userid, vacation_source='all'):
        """
        更新假期类型

        :param op_userid: 拥有“OA审批”应用权限的管理员的userid
        :param vacation_source: 假期来源。取值：all：所有假期类型；null：开放接口定义假期类型
        :return:
        """

        return self._post(
            '/topapi/attendance/vacation/type/update',
            {
                "op_userid": op_userid,
                "vacation_source": vacation_source
            }
        )

    def type_delete(self, op_userid, leave_code):
        """
        删除假期类型

        :param op_userid: 拥有“OA审批”应用权限的管理员的userid
        :param leave_code: 期类型唯一标识，可通过查询假期类型接口获取
        :return:
        """

        return self._post(
            '/topapi/attendance/vacation/type/delete',
            {
                "op_userid": op_userid,
                "vacation_source": vacation_source
            }
        )

    def quota_list(self, leave_code, op_userid, userid_list, offset=0, limit=50):
        """
        考勤打卡数据开放

        :param leave_code: 假期类型唯一标识。可以通过调用假期类型查询接口获取
        :param op_userid: 拥有“OA审批”应用权限的管理员的userid
        :param userid_list: 待查询的员工ID列表
        :param offset: 表示获取考勤数据的起始点，第一次传0，如果还有多余数据，下次获取传的offset值为之前的offset+limit
        :param limit: 表示获取考勤数据的条数，最大不能超过50条
        :return:
        """
        
        if isinstance(userid_list, (list, tuple, set)):
            userid_list = ','.join(map(to_text, userid_list))

        return self._post(
            '/topapi/attendance/vacation/quota/list',
            {
                "leave_code": leave_code,
                "op_userid": op_userid,
                "userids": userid_list,
                "offset": offset,
                "limit": limit
            }
        )

    def record_list(self, leave_code, op_userid, userid_list, offset=0, limit=50):
        """
        查询假期消费记录

        :param leave_code: 假期类型唯一标识。可以通过调用假期类型查询接口获取
        :param op_userid: 拥有“OA审批”应用权限的管理员的userid
        :param userid_list: 待查询的员工ID列表
        :param offset: 表示获取考勤数据的起始点，第一次传0，如果还有多余数据，下次获取传的offset值为之前的offset+limit
        :param limit: 表示获取考勤数据的条数，最大不能超过50条
        :return:
        """
        
        if isinstance(userid_list, (list, tuple, set)):
            userid_list = ','.join(map(to_text, userid_list))

        return self._post(
            '/topapi/attendance/vacation/record/list',
            {
                "leave_code": leave_code,
                "op_userid": op_userid,
                "userids": userid_list,
                "offset": offset,
                "limit": limit
            }
        )
