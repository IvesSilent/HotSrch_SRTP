# Operation_SRTP - HotelSearch基于真值发现的酒店查询推荐应用

---

## 项目简介

本项目为基于真值推荐算法的酒店查询系统，我们基于真值发现技术，集成多种工具和算法，实现了酒店信息的真值推荐。

在本项目中，真值发现技术是核心，它帮助我们从多个数据源中提取和确认信息的真实性。通过算法比较和合成，我们能够确定哪些信息是可靠的，哪些可能是误导性的或错误的。这一技术特别适用于处理来自不同旅游网站的重复、冲突或不完整的酒店数据。

---

## 项目结构

本项目的结构设计清晰，便于开发和维护。以下是该项目的目录结构：

```plaintext
Operation_SRTP - HotSrch_SRTP/
│
├── app.py                    # 主应用程序入口，Flask应用的启动文件
├── run_web.py                # Web服务启动脚本
├── train.py                  # 真值算法训练程序
├── run_train.py              # 真值算法训练启动脚本
│
├── crawler/                  # 爬虫模块目录
│   └── crawler04.py          # 动态爬取，途牛数据爬取
│
├── templates/                # 存放HTML文件的目录
│   ├── hotsrch_homepage.html # 酒店搜索首页
│   └── hotsrch_detail.html   # 酒店详情页面
│
├── static/                   # 静态文件目录，存放JS和CSS文件
│   ├── script_homepage.js    # 首页用到的JavaScript文件
│   ├── script_detail.js      # 详情页用到的JavaScript文件
│   ├── style_homepage.css    # 首页的CSS样式文件
│   └── style_detail.css      # 详情页的CSS样式文件
│
├── data/                     # SQLite数据库文件存放目录
│   ├── ctrip.db              # 携程网酒店数据库
│   ├── mafengwo.db           # 马蜂窝酒店数据库
│   └── tuniu.db              # 途牛网酒店数据库
│
├── hotel_json/               # 存放爬虫爬取的json格式数据文件
│   ├── ctrip_hotel.json      # 从携程网爬取的酒店数据
│   ├── mafengwo_hotel.json   # 从马蜂窝爬取的酒店数据
│   └── tuniu_hotel.json      # 从途牛网爬取的酒店数据
│
├── models/                   # 真值发现函数权重目录
│
├── sql/                      # 数据库脚本目录
│   ├── SqlHot.py             # 从json提取数据并存入SQLite数据库
│   └── SqlCold.py            # 数据库数据检查脚本
│
└── README.md                 # 项目的README文件


```

---

## 环境与依赖

可以通过以下命令安装所有依赖：

```bash
pip install -r requirements.txt
```

以下是所用库的详情。

### python

本项目需要`python3.9`，检查python版本：

```bash
python --version
```

### Flask

本项目基于Flask框架开发，因此需要安装Flask等相关库。 如`flask_sqlalchemy`用于数据库操作，`flask_cors`用于处理跨域问题。

```bash
pip install flask flask_sqlalchemy flask_cors
```

为避免导入问题，更新相关包

```bash
pip install --upgrade flask
pip install --upgrade watchdog
```

---

## 启动

双击运行`run_web.py`以启动本项目，或在命令行中运行`app.py`：

```bash
python app.py
```

### `app.py`

这是Flask应用的主入口文件，负责配置和启动Web服务器。它定义了路由和视图函数，是整个应用的核心。

### `run_web.bat`

这个脚本用于启动Web服务，通过调用`app.py`来快速启动Flask应用，并自动打开浏览器访问应用

---

## 训练

双击运行`run_train.bat`以启动本项目，或在命令行中运行`train.py`：

```bash
python train.py
```

### `train.py`

这是真值推荐算法所用权重的训练程序，在`new_ctrip.db`，`new_mafengwo.db`和`new_tuniu.db`上进行训练，权重结果存入`\models`目录。

### `run_train.bat`

这个脚本用于启动Web服务，通过调用`train.py`来快速启动训练程序。

---

## 真值算法

### 训练

权重训练主要在`train.py`中实现：

```python
import numpy as np


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

```

通过迭代优化的方式，不断更新每个预测提供商的权重，以便更准确地估计对象的真值评分。

### 预测

在运行app.py后，加载已训练的权重。

在酒店搜索过程中，对`all_results`中每个酒店：

* 用`query_hotel()`分别搜索三个数据库中该酒店的评分，调用真值算法，通过评分计算得分真值
* 如果其中一个数据库中没有该酒店的信息，用另外两个数据库的酒店评分真值填充该数据库的评分
* 如果其中两个数据库中没有该酒店的信息，直接取该平台评分为该酒店评分

最后，用所得评分真值替换`all_results`中该酒店的评分

```python
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

```

---

## 文档和学习资源

在完成该项目过程中，我自学了爬虫、SQLite数据库、简单的前端搭建和API应用搭建。我编写的笔记文档位于目录`/note`
内，能帮助团队成员理解和使用不同的技术。

* **`Introduction_API应用.md`：** 从零开始的**API应用**搭建教程;
* **`Introduction_Crawler.md`：** 从零开始的**爬虫**搭建教程;
* **`Introduction_SQLite.md`：** 从零开始的**数据库**搭建教程;
* **`Introduction_前端.md`：** 从零开始的**前端**搭建教程.

---

## 爬虫模块

- **`crawler01.py`** 和 **`crawler03.py`**：这两个脚本分别负责静态和动态的数据爬取，输出数据至文本文件，用于初步的数据抓取和分析。
- **`crawler02.py`**：记录了静态爬取过程中的失败尝试，有助于记录和分析哪些方法不适用于特定的数据源。
- **`crawler04.py`**：专门用于动态爬取途牛网的数据，并将数据以JSON格式保存，为数据处理和存储提供原始材料。

---

## 前端模块

前端的HTML模版页面位于目录`\templates`内，用于渲染用户界面

* **`hotsrch_homepage.html`：** 酒店搜索页，提供用户输入和显示搜索结果
* **`hotsrch_detail.html`：** 显示酒店的详细信息，如图片、评分、位置等

相应的静态资源，如JavaScript文件和CSS样式表，件位于目录`\static`内，用于增强前端页面的交互性和视觉效果

- **`script_homepage.js`** 和 **`script_detail.js`**：分别为首页和详情页提供动态功能，如API调用和页面跳转。
- **`style_homepage.css`** 和 **`style_detail.css`**：定义了首页和详情页的样式，确保页面美观且易于使用。

---

## 数据库

数据存放于`/hotel_json`目录和`/data`目录中

### `data/`

这个目录包含所有数据库文件，用于持久存储爬取的数据。

- **`ctrip.db`**、**`mafengwo.db`**、**`tuniu.db`**：分别存储从携程、马蜂窝和途牛网爬取的数据。

### `hotel_json/`

存放由爬虫模块生成的JSON格式的酒店数据文件。这些文件为数据库提供了数据源。

#### `sql/`

包含用于数据管理的脚本。

- **`SqlHot.py`**：用于从JSON文件中提取数据并导入到SQLite数据库中。
- **`SqlCold.py`**：用于执行数据库查询和数据检查，确保数据的完整性和准确性。

