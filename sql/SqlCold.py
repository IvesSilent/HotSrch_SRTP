# -*coding=utf-8*-
import sqlite3

# 连接到 SQLite 数据库
conn = sqlite3.connect('../data/new_mafengwo.db')
c = conn.cursor()

# # 执行查询
# c.execute("SELECT * FROM stocks WHERE destination='上海'")
c.execute("SELECT score FROM stocks")

results = c.fetchall()
for result in results:
    print(str(result).encode('gbk', 'ignore').decode('gbk'))
#
# c.execute("DELETE FROM stocks WHERE name = ?", ('上海国际贵都大饭店',))
# c.execute("DELETE FROM stocks WHERE name = ?", ('上海裕景大饭店',))
# c.execute("DELETE FROM stocks WHERE name = ?", ('天津五大道小白楼地铁站亚朵酒店',))
# c.execute("DELETE FROM stocks WHERE name = ?", ('重庆万州富力希尔顿逸林酒店',))
# c.execute("DELETE FROM stocks WHERE name = ?", ('厦门五缘水乡酒店（湿地公园店）',))
# c.execute("DELETE FROM stocks WHERE name = ?", ('福州聚春园大酒店',))
# c.execute("DELETE FROM stocks WHERE name = ?", ('龙岩冠豸秘谷佰翔度假酒店',))
# c.execute("DELETE FROM stocks WHERE name = ?", ('宁德万达广场锦江都城酒店',))
# c.execute("DELETE FROM stocks WHERE name = ?", ('泉州厦航酒店（古城店）',))
# c.execute("DELETE FROM stocks WHERE name = ?", ('香港富豪九龙酒店',))



# # 获取查询结果
# print(c.fetchall())  # fetchall() 获取所有结果行
# conn.commit()

conn.close()
