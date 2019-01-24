import pymongo


def connect_mongodb():
    """
    连接 mongodb，获取 百度百科 表 中记录
    :return:  百度百科表 集合
    """
    myclient = pymongo.MongoClient('mongodb://47.97.189.163:27017/')
    db = myclient['ml_entity']
    table = db['entities']
    return table


col = connect_mongodb()
for x in col.find():
    print(x['_id'])
    break
