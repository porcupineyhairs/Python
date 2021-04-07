from modules.Sql import MsSqlHelper
import modules.Object as Object


class PrintWorkStatus:
    def __init__(self):
        self.__mssqlWg = MsSqlHelper(host='192.168.0.99', user='sa',passwd='comfortgroup2016{', database='WG_DB')
        self.__getList = None
        self.__getBackTmp = None
        self.__getBack = []
