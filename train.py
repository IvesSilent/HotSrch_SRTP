# -*coding=utf-8*-
import sqlite3
import numpy as np
import datetime


def get_db_connection(db_name):
    conn = sqlite3.connect(db_name)
    conn.row_factory = sqlite3.Row
    return conn


def fetch_scores(conn):
    cur = conn.cursor()
    cur.execute("SELECT name, score FROM stocks")
    results = cur.fetchall()
    # 处理空字符串，如果score为空则视为0.0
    return {row['name']: float(row['score']) if row['score'] else 0.0 for row in results}


def train_weights(databases, epsilon=2000):
    # 初始化权重
    weights = np.ones(len(databases))

    # 初始化酒店评分字典
    hotel_scores = {db: fetch_scores(get_db_connection(db)) for db in databases}
    hotels = set(hotel for scores in hotel_scores.values() for hotel in scores)

    # 迭代更新权重
    for _ in range(epsilon):
        # 计算每个酒店的估计真值
        O = {hotel: np.average([scores.get(hotel, 0) for scores in hotel_scores.values()], weights=weights) for hotel in
             hotels}

        # 更新权重
        for i, db in enumerate(databases):
            losses = np.array([abs(O[hotel] - hotel_scores[db].get(hotel, O[hotel])) for hotel in hotels])
            weights[i] = 1 / np.mean(losses) if np.mean(losses) > 0 else 1.0

    return weights / np.sum(weights)


# 训练并保存权重
if __name__ == "__main__":
    databases = ['data/new_ctrip.db', 'data/new_mafengwo.db', 'data/new_tuniu.db']
    weights = train_weights(databases)

    # 获取当前日期和时间
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime('%Y%m%d_%H%M%S')

    # 保存权重，文件名包含日期和时间
    np.save(f'models/weights_{formatted_time}.npy', weights)
