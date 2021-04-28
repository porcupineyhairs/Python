import csv

with open('cattest.csv', newline='') as f:
    #参数encoding = 'utf-8'防止出现乱码
    reader = csv.reader(f)
    for row in reader:
        print(row)
