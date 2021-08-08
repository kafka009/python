from redis.client import Redis, StrictRedis

'''
有一首博尔赫斯的诗，我再也不能记起
有一颗头顶的星，我再也不能梦见
有一面镜子，我照了最后一次
有一扇门，我将它关闭
'''


def update(conn: Redis, redis_key: str, redis_value: str, expire: int):
    ori_value = conn.get(redis_key)

    if redis_value is None:
        if ori_value is None:
            print("忽略\t" + redis_key + "\t=\tNone")
        else:
            conn.delete(redis_key)
            print("删除\t" + redis_key + "\t=\t" + str(ori_value, encoding='utf-8'))
        return

    # 被设置的值和redis一样，刷新过期时间
    if ori_value is not None and str(redis_value) == str(ori_value, encoding='utf-8'):
        conn.expire(redis_key, expire)
        print("重置\t" + redis_key + "\t=\t" + str(redis_value))
        return

    conn.set(redis_key, str(redis_value).strip(' \n\t'), ex=expire)
    if ori_value is None:
        print("插入\t" + redis_key + "\t=\t" + str(redis_value))
    else:
        print("更新\t" + redis_key + "\t=\t" + str(redis_value) + ", \t原始值\t=\t" + str(ori_value, encoding='utf-8'))


redis_config = {
    "host": 'localhost',
    "port": 6379,
    "password": None,
    "database": 0
}

# redis的过期时间(秒)
expire_seconds = 3600

# 需要更新的数据
redis_update_data = {
    "rpp.a": '{a:1,b:false}',
    "rpp.b": None,
    "rpp.c": None,
    "rpp.d": None,
    "rpp.e": True,
}

if __name__ == '__main__':
    r = StrictRedis(host=redis_config['host'],
                    port=redis_config['port'],
                    db=redis_config['database'],
                    password=redis_config['password'])

    for key in redis_update_data:
        value = redis_update_data[key]
        if value is str:
            value = value.strip(" \r\n\t")
        update(r, key, value, expire_seconds)

    r.close()
