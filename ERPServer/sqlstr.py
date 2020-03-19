getDate = "REPLACE(REPLACE(REPLACE(REPLACE(CONVERT(varchar(100), GETDATE(), 25), '-', ''), ' ', ''), ':', ''), '.', '')"

sqlStrLa = "INSERT INTO COMFORT.dbo.LRPLA (LA001, LA002, LA003, LA004, LA005, LA012, LA013, LA014, " \
           "COMPANY, CREATE_DATE, CREATOR, USR_GROUP, FLAG) " \
           "VALUES('{LA001}', '{LA002}', '{LA003}', '{LA004}', '{LA005}', '{LA012}', '{LA013}', '{LA014}', " \
           "'COMFORT', {getDate}, 'Robot', '', 1) "

sqlStrLb = "INSERT INTO COMFORT.dbo.LRPLB (LB001, LB002, LB003, LB004, LB005, LB006, LB007, LB008, LB009, LB010, " \
           "LB017, COMPANY, CREATE_DATE, CREATOR, USR_GROUP, FLAG) " \
           "VALUES('{LB001}', '', '', '', 'CONVERT(VARCHAR(8), GETDATE(), 112)', '{LB006}', 'Robot', '', '2', " \
           "'3', '0001', 'COMFORT', {getDate}, 'Robot', '', 1)"
