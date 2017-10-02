import pymysql
import numpy as np

# 统计每一天的发帖量，本次标签生成每日总的发帖量在700(本次处理为了减少标签量)以上的(共有6天)，记做有大事发生，统计每一个学生在该天的参与能力

# 打开数据库连接
db = pymysql.connect("localhost", "root", "******", "datacastlecom")
cursor = db.cursor()

sel_sql = "select * from forum_message"
cursor.execute(sel_sql)
results = cursor.fetchall()
IDData = []
dayPostCount = []  # 每一天发帖量统计
bigEventList = []  # 记录有大事发生的下标值，即第几列
result_to_csv = []

for i in range(1, len(results[0])):
    num = 0
    for j in range(len(results)):
        num += results[j][i]
    dayPostCount.append(num)
# print(dayPostCount)

for i in range(len(dayPostCount)):
    if dayPostCount[i] > 700:
        bigEventList.append(i + 1)  # 在数据库中第零列是id，所以此处要加一
# print(bigEventList)
for i in range(len(results)):
    temp = []
    temp.append(int(results[i][0]))
    for j in range(len(bigEventList)):
        dataValue = results[i][bigEventList[j]]
        abilityValue = 0
        if j == 0:
            if dataValue > 200:
                abilityValue = 1
            else:
                abilityValue = round(dataValue/50 * 0.8, 2)
        elif j == 1:
            if dataValue > 100:
                abilityValue = 1
            else:
                abilityValue = round(dataValue/88 * 0.9, 2)
        elif j == 2:
            if dataValue > 40:
                abilityValue = round((dataValue - 51)/(140 - 51) * 0.3 + 0.7, 2)   # 映射到0.7-1
            else:
                abilityValue = round(dataValue/26 * 0.6, 2)             # 映射到0 - 0.6
        elif j == 3:
            if dataValue > 50:
                abilityValue = round((dataValue - 71)/(369 - 71) * 0.2 + 0.8, 2)
            else:
                abilityValue = round(dataValue/48 * 0.7, 2)
        elif j == 4:
            if dataValue > 300:
                abilityValue = 1
            elif 100 < dataValue < 300:
                abilityValue = 0.8
            else:
                abilityValue = round(dataValue/25 * 0.6, 2)
        else:
            if dataValue > 50:
                abilityValue = round((dataValue - 64)/(214 - 64) * 0.3 + 0.7, 2)
            else:
                abilityValue = round(dataValue/33 * 0.65, 2)
        temp.append(abilityValue)
    result_to_csv.append(temp)
# print(result_to_csv)

np.savetxt('forum_event_label.csv', result_to_csv,
           delimiter=',', header='stu_id, eventA, eventB, eventC, eventD, eventE, eventF',
           comments='', fmt='%d, %f, %f, %f, %f, %f, %f')

db.close()
