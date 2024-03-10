import csv
import random
rows=[]
with open('很多城市餐厅列表.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        rows.append(row)

with open('抽样后餐厅列表.csv', 'w', encoding='utf-8', newline='') as w:
    writer = csv.writer(w)
    for i in range(0, 760):
        row = rows[i*10+random.randint(0, 9)]
        writer.writerow(row)




