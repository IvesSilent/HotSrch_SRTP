# -*coding=utf-8*-
import sqlite3
import json


# 读取 JSON 数据
def load_data(filename):
    # with open(filename, 'r', encoding='gbk') as file:
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)


# 连接到 SQLite 数据库
conn = sqlite3.connect('../data/tuniu.db')
c = conn.cursor()

# 创建数据表
c.execute('''
CREATE TABLE IF NOT EXISTS stocks
(destination text, name text, image text, position text, website text, score real, comment text)
''')
print("已创建数据表。")

# 调用函数，加载数据
data = load_data('../hotel_json/tuniu_hotel_2.json')

# breakpoint()

if data:
    print("成功加载数据。")

print("开始录入数据")

# 【携程】
# for hotel in data:
#     description = hotel['ctrip_describe'] if hotel['ctrip_describe'] is not None else ""
#     comment = hotel['ctrip_comment'] if hotel['ctrip_comment'] is not None else ""
#     combined_text = description + comment
#     c.execute(
#         "INSERT INTO stocks (destination, name, image, position, website, score, comment) VALUES (?, ?, ?, ?, ?, ?, ?)",
#         (hotel['destination'], hotel['name'], hotel['image'], hotel['position'], hotel['ctrip_website'],
#          hotel['ctrip_score'], combined_text))

# 【马蜂窝】
# for hotel in data:
#     c.execute(
#         "INSERT INTO stocks (destination, name, image, position, website, score, comment) VALUES (?, ?, ?, ?, ?, ?, ?)",
#         (hotel['destination'], hotel['name'], hotel['image'], hotel['position'], hotel['mafengwo_website'],
#          hotel['mafengwo_score'], hotel['mafengwo_comment']))

# # # 【途牛】
for hotel in data:
    description = hotel['tuniu_describe'] if hotel['tuniu_describe'] is not None else ""
    comment = hotel['tuniu_comment'] if hotel['tuniu_comment'] is not None else ""
    combined_text = description + comment
    c.execute(
        "INSERT INTO stocks (destination, name, image, position, website, score, comment) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (hotel['destination'], hotel['name'], hotel['image'], hotel['position'], hotel['tuniu_website'],
         hotel['tuniu_score'], combined_text))

# for hotel in data:
#     c.execute(
#         "INSERT INTO stocks (destination, name, image, position, website, score, comment) VALUES (?, ?, ?, ?, ?, ?, ?)",
#         (hotel['destination'], hotel['name'], hotel['image'], hotel['position'], hotel['tuniu_website'],
#          hotel['tuniu_score'], hotel['tuniu_comment']))


print("录入数据已完成")

# 提交事务
conn.commit()

# 关闭连接
conn.close()
