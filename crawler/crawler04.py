# -*coding=utf-8*-

from bs4 import BeautifulSoup
import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

import random
import os

# GoogleChrome版本：129.0.6668.90
# download_url = 'https://storage.googleapis.com/chrome-for-testing-public/129.0.6668.89/win64/chrome-win64.zip'

# 【URL池】
url_01 = 'https://hotel.tuniu.com/'  # 途牛旅游网 (Tuniu) - [途牛旅游网](https://www.tuniu.com/)
url_02 = 'https://www.ly.com/hotel/'  # 同程旅行 (Tongcheng Travel) - [同程旅行](https://www.ly.com/)
url_03 = 'https://www.mafengwo.cn/hotel/'  # 马蜂窝 (Mafengwo) - [马蜂窝](https://www.mafengwo.cn/)
url_04 = 'https://www.elong.com/'  # 艺龙 (eLong) - [艺龙旅行网](https://www.elong.com/)
url_05 = 'https://www.chinapp.com/pinpai/jingpinjiudian.html'  # 品牌网

url_tuniu_login = "https://passport.tuniu.com/login?origin=https://www.tuniu.com/ssoConnect"
url_tuniu = "https://hotel.tuniu.com/list/2500p0s0b0?checkindate=2024-10-07&checkoutdate=2024-10-08&cityName=%E4%B8%8A%E6%B5%B7"

# 【城市列表】
# 用于遍历搜索酒店
place = ["北京", "上海", "天津", "重庆", "香港", "澳门", "黄山", "安庆", "蚌埠", "滁州", "阜阳", "淮北", "合肥", "淮南",
         "铜陵", "芜湖", "宿州", "巢湖", "宣城", "马鞍山", "六安", "厦门", "福州", "龙岩", "宁德", "泉州", "三明",
         "漳州", "南平", "莆田", "兰州", "嘉峪关", "平凉", "庆阳", "天水", "酒泉", "张掖", "威武", "定西", "金昌",
         "白银", "临夏", "陇南", "深圳", "珠海", "广州", "潮州", "东菀", "佛山", "惠州", "江门", "韶关", "汕头", "湛江",
         "肇庆", "中山", "阳江", "河源", "揭阳", "茂名", "清远", "汕尾", "梅州", "云浮", "桂林", "北海", "柳州", "南宁",
         "梧州", "玉林", "百色", "贵港", "防城港", "来宾", "崇左", "钦州", "河池", "贺州", "贵阳", "安顺", "遵义",
         "六盘水", "同仁", "毕节", "三亚", "儋州", "秦皇岛", "保定", "沧州", "邯郸", "衡水", "廊坊", "石家庄", "唐山",
         "张家口", "承德", "邢台", "哈尔滨", "齐齐哈尔", "牡丹江", "鸡西", "大庆", "黑河", "佳木斯", "伊春", "绥化",
         "七台河", "鹤岗", "双鸭山", "大兴安岭", "安阳", "开封", "洛阳", "南阳", "三门峡", "商丘", "新乡", "信阳",
         "驻马店", "郑州", "鹤壁", "漯河", "焦作", "许昌", "濮阳", "济源", "周口", "平顶山", "恩施", "黄石", "荆州",
         "十堰", "武汉", "襄阳", "宜昌", "咸宁", "鄂州", "随州", "荆门", "孝感", "仙桃", "黄冈", "天门", "潜江",
         "张家界", "常德", "长沙", "怀化", "衡阳", "岳阳", "湘潭", "郴州", "娄底", "永州", "邵阳", "益阳", "南京",
         "无锡", "苏州", "扬州", "镇江", "南通", "常州", "连云港", "徐州", "淮安", "泰州", "盐城", "宿迁", "九江",
         "赣州", "景德镇", "南昌", "上饶", "宜春", "鹰潭", "新余", "吉安", "萍乡", "抚州", "长春",
         "辽源", "长白山", "延吉", "吉林市", "延边", "辽源", "四平", "通化", "白城", "松原", "白山", "大连",
         "鞍山", "朝阳", "丹东", "抚顺", "阜新", "锦州", "辽阳", "盘锦", "沈阳", "铁岭", "葫芦岛", "本溪", "营口",
         "呼和浩特", "包头", "赤峰", "通辽", "乌海", "巴彦淖尔", "鄂尔多斯", "呼伦贝尔", "乌兰察布", "银川", "固原",
         "中卫", "石嘴山", "吴忠", "西宁", "海东", "海南", "黄南", "海北", "青岛", "济南", "东营", "济宁", "泰安",
         "潍坊", "威海", "烟台", "淄博", "临沂", "枣庄", "聊城", "菏泽", "日照", "德州", "莱芜", "滨州", "西安",
         "延安", "咸阳", "宝鸡", "铜川", "汉中", "安康", "榆林", "渭南", "商洛", "太原", "大同", "长治", "临汾",
         "运城", "忻州", "阳泉", "晋城", "朔州", "晋中", "吕梁", "成都", "德阳", "广元", "乐山", "泸州", "绵阳",
         "南充", "宜宾", "自贡", "攀枝花", "广安", "眉山", "达州", "遂宁", "资阳", "内江", "阿坝", "雅安", "巴中",
         "凉山", "高雄", "花莲", "基隆", "嘉义", "金门", "垦丁", "苗栗", "南投", "澎湖", "屏东", "台北", "台东",
         "台南", "台中", "桃园", "新北市", "新竹", "宜兰", "云林", "彰化", "乌鲁木齐", "吐鲁番", "喀什", "克拉玛依",
         "阿克苏", "阿勒泰", "哈密", "和田", "塔城", "昌吉", "拉萨", "日喀则", "阿里", "林芝", "山南", "昌都", "那曲",
         "昆明", "西双版纳", "大理", "丽江", "迪庆", "玉溪", "宝山", "昭通", "曲靖", "临沧", "楚雄", "普洱", "文山",
         "杭州", "舟山", "绍兴", "湖州", "金华", "丽水", "宁波", "衢州", "温州", "嘉兴"]

place = place[::-1]


# print(place)
# breakpoint()
# 【随机等待时间】
def random_delay():
    time.sleep(random.uniform(3.5, 4))


def setOption():
    # 设置Chrome选项，避免被网站识别为自动化操作
    option = webdriver.ChromeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    option.add_experimental_option('useAutomationExtension', False)
    option.add_argument('--disable-blink-features=AutomationControlled')
    return option


def login_tuniu(driver, login_url):
    # 登录途牛
    driver.get(login_url)
    random_delay()

    driver.find_element(By.ID, 'normal_tel').send_keys("【你的手机号】")
    driver.find_element(By.ID, 'phone_login').send_keys("【你的途牛手机账户密码】")
    driver.find_element(By.ID, 'rememberme2').click()
    driver.find_element(By.ID, 'isAgreenUs1').click()

    time.sleep(10)

    driver.find_element(By.NAME, 'submit_login').click()

    # driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/div[2]/'
    #                               'a/div/form[1]/div/table/tbody/tr[6]/td/div/input').click()


# def intoTXT(driver):
#     html_source = driver.page_source
#     if html_source:
#         print("网页内容获取成功")
#     filename = 'webTXT/tuniu/tuniu7.txt'
#     with open(filename, 'w', encoding='utf-8') as file:
#         file.write(html_source)


def write_file(driver, destination, file):
    # 对于每一家酒店的信息录入函

    # 解析页面源代码
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    hotels = soup.find_all('div', class_='hotel-item-inner')
    c = 0
    for h in hotels:
        # 提取酒店的图片、名称、评分和价格信息
        image = h.find('img', class_='hotel-pic')["data-src"]
        name = h.find('span', class_='hotel-name f-m').string
        tuniu_score = h.find('div', class_='hotel-score f-b f-DINA').string
        price = h.find('span', class_='amount f-b f-DINA').string

        random_delay()

        # 点击每个酒店项，进入酒店详情页面
        # driver.find_elements(By.CLASS_NAME, 'detail-bottom')[c].click()
        detail_bottom_list = driver.find_elements(By.CSS_SELECTOR, '.detail-btn.f-s')

        detail_bottom_list[c].click()
        c += 1
        random_delay()

        handles = driver.window_handles  # 获取当前所有窗口的句柄

        # 检查是否有足够的窗口句柄
        if len(handles) > 1:
            driver.switch_to.window(handles[1])  # 切换到第二个窗口
        else:
            print("没有足够的窗口可切换。当前窗口数量：", len(handles))

        # 在新打开的窗口中解析详细信息
        tuniu_website = driver.current_url

        random_delay()

        hotel_soup = BeautifulSoup(driver.page_source, 'html.parser')

        # 获取地址
        position_element = hotel_soup.find('div', class_='address f-r')
        if position_element:
            # 提取元素中的文本内容
            position = position_element.get_text(strip=True)
        else:
            # 如果没有找到元素，输出错误信息
            position = "无法找到位置信息"

        comment_container = hotel_soup.find('div', class_='textBox textCommon')
        if comment_container:
            # 提取元素中的文本内容
            tuniu_comment = comment_container.find('p').string
        else:
            # 如果没有找到元素，输出错误信息
            tuniu_comment = "无法找到评论"

        # 构建信息字典
        info = {
            "destination": destination,
            "name": name,
            "image": image,
            "position": position,
            "price": price,
            "tuniu_website": tuniu_website,
            "tuniu_score": tuniu_score,
            "tuniu_comment": tuniu_comment
        }

        # 转换为JSON并写入文件
        js_str = json.dumps(info, indent=4, ensure_ascii=False)  # 将信息转换为JSON格式
        file.write(js_str)  # 写入JSON文件
        file.write(",")

        # 关闭当前详情页，返回列表页
        driver.close()
        driver.switch_to.window(handles[0])
        random_delay()

    # breakpoint()


if __name__ == '__main__':
    # 初始化浏览器驱动driver
    driver = webdriver.Chrome(options=setOption())
    driver.maximize_window()

    # 登录途牛
    login_tuniu(driver, url_tuniu_login)

    # 开始爬取数据
    driver.get(url_tuniu)
    # intoTXT(driver)

    # 确保目录存在
    project_root = os.path.dirname(os.path.dirname(__file__))  # 获取到项目根目录
    directory = os.path.join(project_root, "hotel_json")  # 构建正确的路径
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(os.path.join(directory, "tuniu_hotel.json"), "a", encoding="utf-8") as file:
        # file.write("[")
        for i in place:
            destination = i
            driver.find_element(By.XPATH, '//*[@id="hotel_list_page"]/div[2]/div/div[1]/div[1]/input').clear()
            driver.find_element(By.XPATH, '//*[@id="hotel_list_page"]/div[2]/div/div[1]/div[1]/input').send_keys(i)
            random_delay()

            # 选择搜索结果中的第一个城市
            driver.find_element(By.XPATH, '//*[@id="hotel_list_page"]/div[2]/div/div[3]/div/ul/li[1]').click()
            random_delay()

            # 调用write_file函数来抓取并写入酒店数据
            write_file(driver, i, file)
            random_delay()

            # 尝试点击下一页，继续抓取
            driver.find_element(By.XPATH, '//li[@class="arrowR"]').click()
            random_delay()
            write_file(driver, i, file)
        file.write("]")
