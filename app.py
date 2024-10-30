# -*coding=utf-8*-
import sqlite3
from flask import Flask, request, jsonify, render_template
import json
import numpy as np

app = Flask(__name__)

# 加载权重
weights = np.load('models/weights_20241018_051848.npy')


# 获取数据库链接
def get_db_connection(db_name):
    conn = sqlite3.connect(db_name)
    conn.row_factory = sqlite3.Row
    return conn


# 数据库关键词检索函
def query_keywords(db_name, keywords):
    conn = get_db_connection(db_name)
    cur = conn.cursor()

    # 构建 SQL 查询，对每个关键词使用 LIKE 操作符
    query_parts = []
    params = []
    for keyword in keywords:
        like_keyword = '%' + keyword + '%'
        query_parts.append("(destination LIKE ? OR name LIKE ? OR position LIKE ?)")
        params.extend([like_keyword, like_keyword, like_keyword])

    # 将所有的查询部分用 OR 连接起来
    sql_query = f"""
        SELECT * FROM stocks 
        WHERE {' OR '.join(query_parts)}
        ORDER BY 
            CASE 
                WHEN destination LIKE ? THEN 1
                WHEN name LIKE ? THEN 2
                WHEN position LIKE ? THEN 3
                ELSE 4
            END
    """
    # 为排序添加参数
    params.extend(['%' + keywords[0] + '%', '%' + keywords[0] + '%', '%' + keywords[0] + '%'])

    cur.execute(sql_query, params)

    results = cur.fetchall()
    conn.close()
    return [dict(result) for result in results]


# 数据库酒店名称检索函
def query_hotel(db_name, hotel_name):
    conn = get_db_connection(db_name)
    cur = conn.cursor()
    # cur.execute("SELECT * FROM stocks WHERE name = ?", (hotel_name,))
    # 使用LIKE操作符进行模糊匹配，两边加上通配符%
    cur.execute("SELECT * FROM stocks WHERE name LIKE ?", ('%' + hotel_name + '%',))

    hotel_info = cur.fetchone()
    conn.close()
    return dict(hotel_info) if hotel_info else None


# 根URL请求路由，搜索页主界面
@app.route('/')
def index():
    return render_template('hotsrch_homepage.html')


# 酒店搜索主页路由
@app.route('/search_hotels', methods=['GET'])
def search_hotels():
    # print("开始搜索")
    query = request.args.get('query', '')  # 从查询参数获取搜索关键词
    keywords = query.split()  # 分割成多个关键词
    databases = ['data/ctrip.db', 'data/mafengwo.db', 'data/tuniu.db']
    all_results = []
    for db in databases:
        results = query_keywords(db, keywords)
        for result in results:
            # 收集每个数据库中的评分
            scores = []
            valid_scores = []

            for db_check in databases:
                hotel_info = query_hotel(db_check, result['name'])
                if hotel_info and hotel_info['score']:
                    try:
                        # 尝试将评分转换为浮点数
                        score = float(hotel_info['score'])
                        scores.append(score)
                        valid_scores.append(score)
                    except ValueError:
                        # 如果转换失败，使用None作为占位符
                        scores.append(None)
                else:
                    # 如果没有评分信息，使用None作为占位符
                    scores.append(None)

            # 处理缺失的评分
            for i in range(len(scores)):
                if scores[i] is None:
                    # 如果当前评分缺失，计算其他有效评分的均值
                    if len(valid_scores) > 0:
                        scores[i] = sum(valid_scores) / len(valid_scores)
                    else:
                        scores[i] = 0.0  # 如果没有任何有效评分，使用0.0

            # 计算真值评分
            true_score = np.dot(weights, scores)
            # 保留两位小数
            result['score'] = round(true_score, 2)

        all_results.extend(results)
    return jsonify(all_results)


# 酒店详情页路由
@app.route('/hotsrch_detail')
def hotsrch_detail():
    hotel_json = request.args.get('hotel', None)  # 获取传参传递的酒店信息
    hotel_data = json.loads(hotel_json)  # 将其重构为json数据
    hotel_name = hotel_data['name']  # 提取酒店名称
    ctrip_info = query_hotel('data/ctrip.db', hotel_name)
    mafengwo_info = query_hotel('data/mafengwo.db', hotel_name)
    tuniu_info = query_hotel('data/tuniu.db', hotel_name)
    return render_template('hotsrch_detail.html',
                           hotel_img=hotel_data['image'],
                           hotel_score=hotel_data['score'],
                           hotel_position=hotel_data['position'],
                           hotel_destination=hotel_data['destination'],
                           hotel_website=hotel_data['website'],
                           ctrip=ctrip_info,
                           mafengwo=mafengwo_info,
                           tuniu=tuniu_info,
                           hotel_name=hotel_name)


if __name__ == '__main__':
    app.run(debug=True)
