# Operation_SRTP - HotelSearch������ֵ���ֵľƵ��ѯ�Ƽ�Ӧ��

---

## ��Ŀ���

����ĿΪ������ֵ�Ƽ��㷨�ľƵ��ѯϵͳ�����ǻ�����ֵ���ּ��������ɶ��ֹ��ߺ��㷨��ʵ���˾Ƶ���Ϣ����ֵ�Ƽ���

�ڱ���Ŀ�У���ֵ���ּ����Ǻ��ģ����������ǴӶ������Դ����ȡ��ȷ����Ϣ����ʵ�ԡ�ͨ���㷨�ȽϺͺϳɣ������ܹ�ȷ����Щ��Ϣ�ǿɿ��ģ���Щ���������ԵĻ����ġ���һ�����ر������ڴ������Բ�ͬ������վ���ظ�����ͻ�������ľƵ����ݡ�

---

## ��Ŀ�ṹ

����Ŀ�Ľṹ������������ڿ�����ά���������Ǹ���Ŀ��Ŀ¼�ṹ��

```plaintext
Operation_SRTP - HotSrch_SRTP/
��
������ app.py                    # ��Ӧ�ó�����ڣ�FlaskӦ�õ������ļ�
������ run_web.py                # Web���������ű�
������ train.py                  # ��ֵ�㷨ѵ������
������ run_train.py              # ��ֵ�㷨ѵ�������ű�
��
������ crawler/                  # ����ģ��Ŀ¼
��   ������ crawler04.py          # ��̬��ȡ��;ţ������ȡ
��
������ templates/                # ���HTML�ļ���Ŀ¼
��   ������ hotsrch_homepage.html # �Ƶ�������ҳ
��   ������ hotsrch_detail.html   # �Ƶ�����ҳ��
��
������ static/                   # ��̬�ļ�Ŀ¼�����JS��CSS�ļ�
��   ������ script_homepage.js    # ��ҳ�õ���JavaScript�ļ�
��   ������ script_detail.js      # ����ҳ�õ���JavaScript�ļ�
��   ������ style_homepage.css    # ��ҳ��CSS��ʽ�ļ�
��   ������ style_detail.css      # ����ҳ��CSS��ʽ�ļ�
��
������ data/                     # SQLite���ݿ��ļ����Ŀ¼
��   ������ ctrip.db              # Я�����Ƶ����ݿ�
��   ������ mafengwo.db           # ����ѾƵ����ݿ�
��   ������ tuniu.db              # ;ţ���Ƶ����ݿ�
��
������ hotel_json/               # ���������ȡ��json��ʽ�����ļ�
��   ������ ctrip_hotel.json      # ��Я������ȡ�ľƵ�����
��   ������ mafengwo_hotel.json   # ���������ȡ�ľƵ�����
��   ������ tuniu_hotel.json      # ��;ţ����ȡ�ľƵ�����
��
������ models/                   # ��ֵ���ֺ���Ȩ��Ŀ¼
��
������ sql/                      # ���ݿ�ű�Ŀ¼
��   ������ SqlHot.py             # ��json��ȡ���ݲ�����SQLite���ݿ�
��   ������ SqlCold.py            # ���ݿ����ݼ��ű�
��
������ README.md                 # ��Ŀ��README�ļ�


```

---

## ����������

����ͨ���������װ����������

```bash
pip install -r requirements.txt
```

���������ÿ�����顣

### python

����Ŀ��Ҫ`python3.9`�����python�汾��

```bash
python --version
```

### Flask

����Ŀ����Flask��ܿ����������Ҫ��װFlask����ؿ⡣ ��`flask_sqlalchemy`�������ݿ������`flask_cors`���ڴ���������⡣

```bash
pip install flask flask_sqlalchemy flask_cors
```

Ϊ���⵼�����⣬������ذ�

```bash
pip install --upgrade flask
pip install --upgrade watchdog
```

---

## ����

˫������`run_web.py`����������Ŀ������������������`app.py`��

```bash
python app.py
```

### `app.py`

����FlaskӦ�õ�������ļ����������ú�����Web����������������·�ɺ���ͼ������������Ӧ�õĺ��ġ�

### `run_web.bat`

����ű���������Web����ͨ������`app.py`����������FlaskӦ�ã����Զ������������Ӧ��

---

## ѵ��

˫������`run_train.bat`����������Ŀ������������������`train.py`��

```bash
python train.py
```

### `train.py`

������ֵ�Ƽ��㷨����Ȩ�ص�ѵ��������`new_ctrip.db`��`new_mafengwo.db`��`new_tuniu.db`�Ͻ���ѵ����Ȩ�ؽ������`\models`Ŀ¼��

### `run_train.bat`

����ű���������Web����ͨ������`train.py`����������ѵ������

---

## ��ֵ�㷨

### ѵ��

Ȩ��ѵ����Ҫ��`train.py`��ʵ�֣�

```python
import numpy as np


def train_weights(databases, epsilon=2000):
    # ��ʼ��Ȩ��
    weights = np.ones(len(databases))

    # ��ʼ���Ƶ������ֵ�
    hotel_scores = {db: fetch_scores(get_db_connection(db)) for db in databases}
    hotels = set(hotel for scores in hotel_scores.values() for hotel in scores)

    # ��������Ȩ��
    for _ in range(epsilon):
        # ����ÿ���Ƶ�Ĺ�����ֵ
        O = {hotel: np.average([scores.get(hotel, 0) for scores in hotel_scores.values()], weights=weights) for hotel in
             hotels}

        # ����Ȩ��
        for i, db in enumerate(databases):
            losses = np.array([abs(O[hotel] - hotel_scores[db].get(hotel, O[hotel])) for hotel in hotels])
            weights[i] = 1 / np.mean(losses) if np.mean(losses) > 0 else 1.0

    return weights / np.sum(weights)

```

ͨ�������Ż��ķ�ʽ�����ϸ���ÿ��Ԥ���ṩ�̵�Ȩ�أ��Ա��׼ȷ�ع��ƶ������ֵ���֡�

### Ԥ��

������app.py�󣬼�����ѵ����Ȩ�ء�

�ھƵ����������У���`all_results`��ÿ���Ƶ꣺

* ��`query_hotel()`�ֱ������������ݿ��иþƵ�����֣�������ֵ�㷨��ͨ�����ּ���÷���ֵ
* �������һ�����ݿ���û�иþƵ����Ϣ���������������ݿ�ľƵ�������ֵ�������ݿ������
* ��������������ݿ���û�иþƵ����Ϣ��ֱ��ȡ��ƽ̨����Ϊ�þƵ�����

���������������ֵ�滻`all_results`�иþƵ������

```python
for result in results:
    # �ռ�ÿ�����ݿ��е�����
    scores = []
    valid_scores = []

    for db_check in databases:
        hotel_info = query_hotel(db_check, result['name'])
        if hotel_info and hotel_info['score']:
            try:
                # ���Խ�����ת��Ϊ������
                score = float(hotel_info['score'])
                scores.append(score)
                valid_scores.append(score)
            except ValueError:
                # ���ת��ʧ�ܣ�ʹ��None��Ϊռλ��
                scores.append(None)
        else:
            # ���û��������Ϣ��ʹ��None��Ϊռλ��
            scores.append(None)

    # ����ȱʧ������
    for i in range(len(scores)):
        if scores[i] is None:
            # �����ǰ����ȱʧ������������Ч���ֵľ�ֵ
            if len(valid_scores) > 0:
                scores[i] = sum(valid_scores) / len(valid_scores)
            else:
                scores[i] = 0.0  # ���û���κ���Ч���֣�ʹ��0.0

    # ������ֵ����
    true_score = np.dot(weights, scores)
    # ������λС��
    result['score'] = round(true_score, 2)

all_results.extend(results)

```

---

## �ĵ���ѧϰ��Դ

����ɸ���Ŀ�����У�����ѧ�����桢SQLite���ݿ⡢�򵥵�ǰ�˴��APIӦ�ô���ұ�д�ıʼ��ĵ�λ��Ŀ¼`/note`
�ڣ��ܰ����Ŷӳ�Ա����ʹ�ò�ͬ�ļ�����

* **`Introduction_APIӦ��.md`��** ���㿪ʼ��**APIӦ��**��̳�;
* **`Introduction_Crawler.md`��** ���㿪ʼ��**����**��̳�;
* **`Introduction_SQLite.md`��** ���㿪ʼ��**���ݿ�**��̳�;
* **`Introduction_ǰ��.md`��** ���㿪ʼ��**ǰ��**��̳�.

---

## ����ģ��

- **`crawler01.py`** �� **`crawler03.py`**���������ű��ֱ���̬�Ͷ�̬��������ȡ������������ı��ļ������ڳ���������ץȡ�ͷ�����
- **`crawler02.py`**����¼�˾�̬��ȡ�����е�ʧ�ܳ��ԣ������ڼ�¼�ͷ�����Щ�������������ض�������Դ��
- **`crawler04.py`**��ר�����ڶ�̬��ȡ;ţ�������ݣ�����������JSON��ʽ���棬Ϊ���ݴ���ʹ洢�ṩԭʼ���ϡ�

---

## ǰ��ģ��

ǰ�˵�HTMLģ��ҳ��λ��Ŀ¼`\templates`�ڣ�������Ⱦ�û�����

* **`hotsrch_homepage.html`��** �Ƶ�����ҳ���ṩ�û��������ʾ�������
* **`hotsrch_detail.html`��** ��ʾ�Ƶ����ϸ��Ϣ����ͼƬ�����֡�λ�õ�

��Ӧ�ľ�̬��Դ����JavaScript�ļ���CSS��ʽ����λ��Ŀ¼`\static`�ڣ�������ǿǰ��ҳ��Ľ����Ժ��Ӿ�Ч��

- **`script_homepage.js`** �� **`script_detail.js`**���ֱ�Ϊ��ҳ������ҳ�ṩ��̬���ܣ���API���ú�ҳ����ת��
- **`style_homepage.css`** �� **`style_detail.css`**����������ҳ������ҳ����ʽ��ȷ��ҳ������������ʹ�á�

---

## ���ݿ�

���ݴ����`/hotel_json`Ŀ¼��`/data`Ŀ¼��

### `data/`

���Ŀ¼�����������ݿ��ļ������ڳ־ô洢��ȡ�����ݡ�

- **`ctrip.db`**��**`mafengwo.db`**��**`tuniu.db`**���ֱ�洢��Я�̡�����Ѻ�;ţ����ȡ�����ݡ�

### `hotel_json/`

���������ģ�����ɵ�JSON��ʽ�ľƵ������ļ�����Щ�ļ�Ϊ���ݿ��ṩ������Դ��

#### `sql/`

�����������ݹ���Ľű���

- **`SqlHot.py`**�����ڴ�JSON�ļ�����ȡ���ݲ����뵽SQLite���ݿ��С�
- **`SqlCold.py`**������ִ�����ݿ��ѯ�����ݼ�飬ȷ�����ݵ������Ժ�׼ȷ�ԡ�

