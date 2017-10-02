import pymysql
import numpy as np

col_data = ["x912", "z052", "x616", "y663", "z512", "x492_y524", "y076", "z918", "z735", "y786", "x986"]

# 打开数据库连接
db = pymysql.connect("localhost", "root", "******", "datacastlecom")
cursor = db.cursor()

'''
# 插入列
for item in col_data:
    sql = "alter table scholarship_data add column " + item + " int not null"
    try:
        # 执行sql语句
        cursor.execute(sql)


        # 提交到数据库执行
        db.commit()

    except Exception as  e:
        # 如果发生错误则进行回滚
        print(e)
        db.rollback()
'''
'''
# 更新列标签
sel_sql = "select this_ID, scholarship_type from scholarship_data"
cursor.execute(sel_sql)
results = cursor.fetchall()
for row in results:
    # up_sql = "update scholarship_data set " + row[1] + "= 1 where this_ID = " + str(row[0])
    if row[1] == "x492" or row[1] == "y524":
        up_sql = "update scholarship_data set x492_y524 = 1 where this_ID = " + str(row[0])
        try:
            cursor.execute(up_sql)
            db.commit()
        except Exception as e:
            # 发生错误时回滚
            print(e)
            db.rollback()
'''
sel_sql = "select * from scholarship_data order by student_id"
cursor.execute(sel_sql)
results = cursor.fetchall()
result_to_csv = []
temp = ["stu_id",0,0,0,0,0,0,0,0,0,0,0]
i = 0
temp[0] = results[i][1]
temp[1] = results[i][3]
temp[2] = results[i][4]
temp[3] = results[i][5]
temp[4] = results[i][6]
temp[5] = results[i][7]
temp[6] = results[i][8]
temp[7] = results[i][9]
temp[8] = results[i][10]
temp[9] = results[i][11]
temp[10] = results[i][12]
temp[11] = results[i][13]
# temp装载的永远是i指向的学号学生数据
num = 0
for j in range(1, len(results)):
    if results[i][1] == results[j][1]:
        num += 1
        for k in range(0, 11):
            temp[1+k] += results[j][3+k]
    else:
        for k in range(0, 11):
            temp[1 + k] /= 4  # 4年每年平均拿奖的权值
        result_to_csv.append(temp)
        i = j
        temp = ["stu_id", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        temp[0] = results[i][1]
        temp[1] = results[i][3]
        temp[2] = results[i][4]
        temp[3] = results[i][5]
        temp[4] = results[i][6]
        temp[5] = results[i][7]
        temp[6] = results[i][8]
        temp[7] = results[i][9]
        temp[8] = results[i][10]
        temp[9] = results[i][11]
        temp[10] = results[i][12]
        temp[11] = results[i][13]

print(result_to_csv)
np.savetxt('scholarship_label.csv', result_to_csv,
           delimiter=',', header='stu_id, x912, z052, x616, y663, z512, x492_y524, y076, z918, z735, y786, x986 ',
           comments='', fmt='%d,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f')
# 关闭数据库连接
db.close()
