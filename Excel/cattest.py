import csv
import pandas as pd

# with open('cattest.csv', newline='') as f:
#     #参数encoding = 'utf-8'防止出现乱码
#     reader = csv.reader(f)
#     for row in reader:
#         print(row)



def pd_excel():
    xl = pd.read_excel('111.xlsx')
    print(xl)









if __name__ == '__main__':
    pd_excel()
