from io import TextIOWrapper

import MySQLdb

'''
我一次次地面对
那孟加拉虎的雄姿
直到傍晚披上金色
凝望着它，在铁笼里咆哮往返
全然不顾樊篱的禁阻
世上还会有别的黄色
那是宙斯的金属
每隔九夜变幻出相同的指环
绵绵不息，循环不止
逝者如斯
其他颜色弃我而去
惟有朦胧的光明、模糊的黑暗
和那原始的金黄
'''


def select(conn: MySQLdb.Connection, sql: str, table: str, file: TextIOWrapper):
    # Prepare a cursor object using cursor() method
    cursor: MySQLdb.cursors.Cursor = conn.cursor()

    # Execute SQL query
    cursor.execute(sql)

    file.write("## ")
    file.write(table)
    file.write("\r")

    # Fetch meta
    file.write('|')
    for column_des in cursor.description:
        file.write(column_des[0])
        file.write("|")

    # Make a new line
    file.write("\r")

    # Split
    file.write('|')
    for column_des in cursor.description:
        file.write(" ----- |")

    # Fetch data
    for row in cursor.fetchall():
        file.write("\r|")
        for column in row:
            if column is None:
                file.write("-")
            elif column == '':
                file.write("-")
            else:
                file.write(escape(str(column)))
            file.write("|")

    # A new line
    file.write("\r")


# 转义字符集
chars = [
    ["\\", "\\\\"],
    ["`", "\`"],
    ["*", "\*"],
    ["_", "\_"],
    ["{", "\{"],
    ["}", "\}"],
    ["[", "\["],
    ["]", "\]"],
    ["(", "\("],
    [")", "\)"],
    ["#", "\#"],
    ["+", "\+"],
    ["-", "\-"],
    [".", "\."],
    ["!", "\!"],
    ["|", "\|"],
]


# 转义
def escape(c):
    for spe in chars:
        c = c.replace(spe[0], spe[1])
    return c
