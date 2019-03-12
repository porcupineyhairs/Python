from Module import MsSql
from Module import DataBase_Dict


class UserPerm:
    def __init__(self):
        self.__mssql = MsSql()
        self.__json = None

        self.__back = []

        self.__U_ID = None
        self.__U_NAME = None
        self.__Permission_ID = None
        self.__Group_ID = None

        self.__User_Dpt = None

        self.__get_WGPerm = None
        self.__get_WGPermID = None
        self.__get_WGPermName = None
        self.__get_GroupID = None
        self.permission = []

        self.__WG_Conn = DataBase_Dict['WG_DB']

    def __start(self, _json):
        self.__init__()
        self.__json = _json

        self.__U_ID = self.__json['Login_Uid']
        self.__U_Name = self.__json['Login_Name']
        self.__User_Dpt = self.__json['Login_Dpt']

        self.__GetWGPerm()

        perm_list = []

        self.SetPermission(perm_list)
        return self.__back

    def SetPermission(self, perm_list):
        for i in range(len(perm_list)):
            perm_ID = self.__GetPermID(perm_list[i])
            if perm_ID in self.permission:
                self.__Set_WGPerm(perm_ID)
            else:
                self.__Set_WGPerm(perm_ID)
                self.__InsertWGPerm()

        for j in range(len(self.permission)):
            perm_Name = self.__GetPermName(self.permission[j])
            if perm_Name in perm_list:
                if self.permission[j] in self.__back:
                    continue
                else:
                    self.__Set_WGPerm(self.permission[j])
            else:
                self.__Delete_Perm(self.permission[j])
                self.permission.pop(j)

    def __GetWGPerm(self):
        __sqlstr = (r"SELECT U_ID, U_NAME,Permission_ID, Group_ID FROM WG_PERM_USER "
                    r"WHERE U_ID = '" + self.__U_ID + "'")
        self.__get_WGPerm = self.__mssql.Sqlwork(DataBase=self.__WG_Conn, SqlStr=__sqlstr)
        for i in range(len(self.__get_WGPerm)):
            self.permission.append(self.__get_WGPerm[i][2])

    def __GetPermID(self, perm_str):
        __sqlstr = (r"SELECT K_ID FROM WG_PERM_BASE "
                    r"WHERE Name = '" + perm_str + "'")
        self.__get_WGPermID = self.__mssql.Sqlwork(DataBase=self.__WG_Conn, SqlStr=__sqlstr)
        return self.__get_WGPermID[0]

    def __GetPermName(self, perm_id):
        __sqlstr = (r"SELECT Name FROM WG_PERM_BASE "
                    r"WHERE K_ID = '" + perm_id + "'")
        self.__get_WGPermName = self.__mssql.Sqlwork(DataBase=self.__WG_Conn, SqlStr=__sqlstr)
        return self.__get_WGPermName[0]

    def __GetGroupID(self, perm_id):
        __sqlstr = (r"SELECT Group_ID FROM WG_GROUP "
                    r"WHERE Permission_ID = '" + perm_id + "'")
        self.__get_GroupID = self.__mssql.Sqlwork(DataBase=self.__WG_Conn, SqlStr=__sqlstr)
        return self.__get_GroupID[0]

    def __InsertWGPerm(self):
        __sqlstr = (r"INSERT INTO WG_PERM_USER (U_ID, U_NAME, Permission_ID,Group_ID) "
                    r"VALUES("
                    r"'" + self.__U_ID + "', "
                    r"'" + self.__U_NAME + "', "
                    r"'" + self.__Permission_ID + "', "
                    r"'" + self.__Group_ID + "', "
                    r")")
        self.__mssql.Sqlwork(DataBase=self.__WG_Conn, SqlStr=__sqlstr)

    def __Update_WGPerm(self):
        __sqlstr = (r"UPDATE WG_PERM_USER SET "
                    r"U_NAME = '" + self.__U_NAME + "', "
                    r"Permission_ID = '" + self.__Permission_ID + "', "
                    r"Group_ID = '" + self.__Group_ID +
                    r"WHERE U_ID = '" + self.__U_ID + "''")
        self.__mssql.Sqlwork(DataBase=self.__WG_Conn, SqlStr=__sqlstr)

    def __Delete_Perm(self, perm_ID):
        __sqlstr = ("DELETE FROM WG_PERM_USER WHERE U_ID = '" + self.__U_ID + "' AND Permission_ID = '" + perm_ID + "'")
        self.__mssql.Sqlwork(DataBase=self.__WG_Conn, SqlStr=__sqlstr)

    def __Set_WGPerm(self, perm):
        self.__Permission_ID = perm
        self.__Group_ID = self.__GetGroupID(perm)
        self.__back.append(self.__Permission_ID)
