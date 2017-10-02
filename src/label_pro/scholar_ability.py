import pandas as pd
import numpy as np
data = pd.read_csv("scholarship_label.csv")     # data为DataFram类型
scholarData = data.iloc[:, 1:]
IDData = data.iloc[:, 0]
# 将DataFrame类型转换为列表
scholarData = np.array(scholarData)
scholarData = scholarData.tolist()
IDData = np.array(IDData)
IDData = IDData.tolist()
scholarAbility = []
result_to_csv = []
for item in scholarData:
    # 加权处理
    temp = item[0]*11 + item[1]*10 + item[2]*9 + item[3]*8 + item[4]*6.5 + item[5]*6 + item[6]*5 + item[7]*3 + item[8]*1.5 + item[9]*1 + item[10] *0.5
    scholarAbility.append(temp)

tList = list(set(scholarAbility))
temp = []
for item in tList:
    item = round((item - min(tList))/(max(tList)-min(tList))*(0.8)+0.1,2)   # 最大最小规范化，映射到[0.1, 0.9],保留两位小数
    temp.append(item)
print(tList)
print(temp)
for i in range(len(scholarAbility)):
    scholarAbility[i] = round((scholarAbility[i] - min(tList))/(max(tList)-min(tList))*0.8+0.1, 2)  # 最大最小规范化，映射到[0.1, 0.9],保留两位小数
    result_to_csv.append([int(IDData[i]), scholarAbility[i]])
print(result_to_csv[1])
np.savetxt('scholar_ability_label.csv', result_to_csv,
           delimiter=',', header='stu_id, ability',
           comments='', fmt='%d, %f')
