
insertStrTmp = r"INSERT INTO COPTR ({0}) VALUES ({1})"
insertStrList = []
headList = []
detailList = []

headStr = ''
detailStr = ''


# 文件处理部分
sourceList = []
file = open('1.txt', 'r')
strSourceList = file.readlines()
for sourceListTmp in strSourceList:
    sourceListTmp = sourceListTmp.replace('"', '').strip('\r\n')
    # sourceList.append(sourceListTmp.split('DETAIL: ')[1])
    sourceListTmp = sourceListTmp.split('DETAIL: ')[1]
    # print(sourceListTmp)

    strList = sourceListTmp.split(', ')

    headList = []
    detailList = []
    headStr = ''
    detailStr = ''

    for strTmp in strList:
        str1 = strTmp.split('=')[0]
        str2 = strTmp.split('=')[1]

        headList.append(str1)
        if str2 == '[]':
            detailList.append('')
        else:
            detailList.append(str2.strip('[').strip(']'))

    for headStrTmp in headList:
        headStr += headStrTmp + ', '

    for detailStrTmp in detailList:
        detailStr += r"'" + detailStrTmp + r"', "

    headStr = headStr.strip(', ')
    detailStr = detailStr.strip(', ')

    # print(headStr)
    # print(detailStr)

    # print(insertStrTmp.format(headStr, detailStr))
    insertStrList.append(insertStrTmp.format(headStr, detailStr))

for k in range(len(insertStrList)):
    print(insertStrList[k])
