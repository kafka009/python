import os
import MySQLdb

'''
我滑下你的暮色如厌倦滑下一道斜坡的虔诚。
年轻的夜晚像你屋顶平台上的一片翅膀。
你是我们曾经有的布宜诺斯艾利斯，那座随着岁月悄悄溜走的城市。
你是我们的，节日的，像水中倒映的星星。
时间中虚假的门，你的街道朝向更轻柔的往昔。
黎明之光，它送出的早晨向我们走来，越过甘甜的褐色海水。
在照亮我的百叶窗之前，你低低的日色已赐福于你的花园。
被听成了一首诗的城市。
'''

import select

# 数据库
mysql_config = {
    "host": 'localhost',
    "port": 3306,
    "user": "root",
    "password": "kingdee",
    "database": "account"
}
# 数据将要去到的文件目录
folder = 'D:/python/sql/target'
# 文件名前缀
file_prefix = "rpp_approve_"
# 查询的数据的id号
id = "2"
# 待查询的数据集
sql_map = {
    "测试1": "select * from tb_student where stu_id = :id",
    "测试2": "select * from tb_student",
    "测试3": "select * from tb_student where stu_id = :id",
    "测试4": "select 1 as name from dual",
    "测试5": '''
        select 2 as 姓名 from dual;
        select 5 as 姓名 from dual;
        select 2 as 测试, 3 as 哈哈 from dual;
    ''',
}

if __name__ == '__main__':
    # 数据库连接
    conn = MySQLdb.connect(host=mysql_config['host'],
                           port=mysql_config['port'],
                           user=mysql_config['user'],
                           password=mysql_config['password'],
                           database=mysql_config['database'],
                           charset='utf8')
    os.makedirs(folder, exist_ok=True)
    name = folder + "/" + file_prefix + id + ".md"
    file = open(name, 'w', encoding="utf-8")
    file.write("# *" + id + "* 的数据")
    file.write("\r")
    for key in sql_map:
        print("查询\t" + key + ": (id = " + id + ")")
        # select(conn, sql_map[key].replace(":id", "'" + id + "'"), key, file)
        (length, desc, data) = select.query(conn, sql_map[key].replace(":id", "'" + id + "'"))
        select.write(length, desc, data, key, file)
    file.flush()
    file.close()
    conn.close()
