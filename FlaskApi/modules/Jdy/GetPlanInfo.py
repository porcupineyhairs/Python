from modules.Sql import MsSqlHelper
from modules.Sql.DataConvert import list2dict
import modules.Object as Object


class PlanInfo:
    def __init__(self):
        self.__mssqlWg = MsSqlHelper(host='192.168.0.99', user='sa',passwd='comfortgroup2016{', database='WG_DB')
        self.__getList = None
        self.__getBackTmp = None
        self.__getBack = []

    def get(self, order=None, date=None, space=None, ):
        self.__getList = None
        self.__getBack = []

        sqlStr = r"Select SC001 订单号, SC003 上线日期 , SC013 上线数量, SC023 生产部门 FROM SC_PLAN " \
                 r"WHERE 1=1 "

        sqlStr += "AND SC001 Like '%{0}%' ".format(order) if order is not None else ''
        sqlStr += "AND SC003 = '{0}' ".format(date) if date is not None else ''
        sqlStr += "AND SC023 Like '%{0}%' ".format(space) if space is not None else ''
        sqlStr += "ORDER BY SC003, SC001, SC013 "

        try:
            self.__getList = self.__mssqlWg.sqlWork(sqlStr, getTitle=True, )

        except Exception as e:
            print(e)
            self.__getList = None

        # if self.__getList is not None:
        #     title = self.__getList.pop(0)
        #
        #     for row in self.__getList:
        #         self.__getBackTmp = {}
        #         for index in range(len(title)):
        #             self.__getBackTmp.update({title[index]: row[index]})
        #         self.__getBack.append(self.__getBackTmp)
        return list2dict(self.__getList)
