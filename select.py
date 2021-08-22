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


def query(conn: MySQLdb.Connection, sqls: str):
    length = 0
    desc = []
    data = []

    for sql in sqls.split(";"):
        sql = sql.strip("\r\n ")
        if len(sql) == 0:
            continue

        # Prepare a cursor object using cursor() method
        cursor: MySQLdb.cursors.Cursor = conn.cursor()

        # Execute SQL query
        cursor.execute(sql)

        # Max length
        length = max(length, len(cursor.description))

        # Meta data
        desc.append(cursor.description)

        # Row data
        data.append(cursor.fetchall())
    return length, desc, data


def write(length, desc, data, table: str, file: TextIOWrapper):
    # Write table name
    file.write("## ")
    file.write(table)
    file.write(" \r ")

    for index in range(len(desc)):
        meta = desc[index]
        rows = data[index]

        # Write meta data
        file.write(' | ')
        for column_des in meta:
            file.write("<center><b>")
            file.write(column_des[0])
            file.write("</center></b>")
            file.write(" | ")
        for i in range(length - len(meta)):
            file.write("<center><b> - </b></center>")
            file.write(" | ")
        file.write(" \r ")

        # Smart head
        if index == 0:
            file.write(" | ")
            for i in range(length):
                file.write(" ----- |")
            file.write(" \r ")

        # Write rows data
        file.write(" | ")
        for row in rows:
            for column in row:
                if column is None:
                    file.write("<center> NA </center>")
                elif column == '':
                    file.write("<center> NA </center>")
                else:
                    file.write(escape(str(column)))
                file.write(" | ")
            for i in range(length - len(meta)):
                file.write("<center> NA </center>")
                file.write(" | ")
            # New line
            file.write(" \r ")

        # Empty data
        if len(rows) == 0:
            file.write(" | ")
            for i in range(length):
                file.write("<center> NA </center>|")
            file.write(" \r ")

    # New line
    file.write(" \r ")


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
