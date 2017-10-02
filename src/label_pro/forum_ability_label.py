import pymysql
import numpy as np

# 487天的数据

# 打开数据库连接
db = pymysql.connect("localhost", "root", "******", "datacastlecom")
cursor = db.cursor()

sel_sql = "select * from forum_message"
cursor.execute(sel_sql)
results = cursor.fetchall()
IDData = []
postCount = []  # 日均发帖量
postAbility = []  # 最大最小规范化后的发帖能力
result_to_csv = []
for row in results:
    count = 0
    for i in range(1,len(row)):
        count += row[i]
    IDData.append(row[0])
    postCount.append(float(count/487))
# print(len(IDData))
'''
# 找离群点
temp = []
for item in postCount:
    temp.append(item)
temp.sort()
print(temp)
'''

for item in postCount:
    if item > 1:
        t = 1
    else:
        t = round((item - min(postCount))/(1-min(postCount))*0.9, 4)
    postAbility.append(t)
# print(postCount)


for i in range(len(postAbility)):
    result_to_csv.append([int(IDData[i]), postAbility[i]])


np.savetxt('forum_ability_label.csv', result_to_csv,
           delimiter=',', header='stu_id, value',
           comments='', fmt='%d, %f')

db.close()
