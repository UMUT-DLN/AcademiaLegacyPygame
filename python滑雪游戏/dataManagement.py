import pymysql

"""
数据管理，如判断用户名和密码的准确性
"""


class dbMgr:
    def __init__(self):
        self.db = pymysql.connect(host='localhost', user='root', password='123456', database='skinggame')

    # 查询用户名和密码进行判断
    def selectFromUsers(self, userName, userPassword):
        # 注册的账户的同时，也会注册数据
        sql1 = "select * from users where username='%s' and password='%s';" % (userName, userPassword)
        sql2 = "update fightdata set loginTimes=loginTimes+1 where username='%s';" % userName
        cursor = self.db.cursor()
        cursor.execute(sql1)
        data = cursor.fetchall()
        if data:
            cursor.execute(sql2)
            self.db.commit()  # 刷新数据库
            return True
        return False

    # 判断账户存不存在
    def regester(self, userName, passWord):
        cursor = self.db.cursor()
        sql = "select * from users where username = '%s';" % userName
        cursor.execute(sql)
        data = cursor.fetchall()
        if data:
            # 该账户存在
            return False
        else:
            if self.insertIntoUsers(userName, passWord):
                return True
            else:
                return False
            pass

    # 注册函数
    def insertIntoUsers(self, userName, passWord):
        cursor = self.db.cursor()
        sql1 = "insert into users values('%s','%s');" % (userName, passWord)
        sql2 = "insert into fightdata values('%s',0,0);" % userName
        try:
            cursor.execute(sql1)
            cursor.execute(sql2)
            self.db.commit()  # 刷新数据库
            return True
        except:
            self.db.rollback()
            return False

    # 查询最高分
    def selectHighScore(self, userName):
        cursor = self.db.cursor()
        sql1 = "SELECT highScore FROM fightdata WHERE username='%s';" % userName
        cursor.execute(sql1)
        data = cursor.fetchall()
        hightScore = 0
        for i in data:
            hightScore = i[0]
        print(hightScore)
        return hightScore

    # 更新最高分
    def commitHighScore(self, userName, score):
        cursor = self.db.cursor()
        sql1 = "update fightdata set highScore=%d where username='%s';" % (score, userName)
        cursor.execute(sql1)
        self.db.commit()  # 刷新数据库


# 创建表
def createTable():
    db = pymysql.connect(host='localhost', user='root', password='123456', database='skinggame')
    cursor = db.cursor()
    sql1 = ("create table if not exists users("
            "username varchar(50) primary key comment '姓名',"
            "password varchar(50) comment '密码'"
            ")comment '用户信息';")
    cursor.execute(sql1)
    sql2 = ("create table if not exists fightData("
            "username varchar(50) comment '姓名',"
            "highScore int comment '最高分数',"
            "loginTimes int comment '玩的次数');")
    cursor.execute(sql2)
    db.commit()  # 操作存入数据库


if __name__ == '__main__':
    createTable()