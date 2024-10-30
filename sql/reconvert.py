# -*coding=utf-8*-

def convert_encoding(from_file, to_file, from_encoding='gbk', to_encoding='utf-8'):
    # 打开原始编码的文件
    with open(from_file, 'r', encoding=from_encoding) as file:
        content = file.read()

    # 将内容写入新文件，使用新的编码
    with open(to_file, 'w', encoding=to_encoding) as file:
        file.write(content)


# 使用函数进行转换
convert_encoding('../hotel_json/tuniu_hotel_1.json', '../hotel_json/tuniu_hotel_2.json')
