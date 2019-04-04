import pymysql
from DBUtils.PooledDB import PooledDB

from shengshi.utils.dbconfig import mysqlInfo


class OPMysql(object):
    __pool = None

    def __init__(self):
        # 构造函数，创建数据库连接、游标
        self.pool = OPMysql.getmysqlconn()
        # self.cur = self.coon.cursor(cursor=pymysql.cursors.DictCursor)

    # 数据库连接池连接
    @staticmethod
    def getmysqlconn():
        if OPMysql.__pool is None:
            __pool = PooledDB(creator=pymysql,
                              mincached=20,
                              maxconnections=40,
                              blocking=True,
                              host=mysqlInfo['host'],
                              user=mysqlInfo['user'],
                              passwd=mysqlInfo['passwd'],
                              db=mysqlInfo['db'],
                              port=mysqlInfo['port'],
                              charset=mysqlInfo['charset'])
            # print(__pool)
        # return __pool.connection()
        return __pool

    def connection(self):
        coon = self.pool.connection()
        cur = coon.cursor()
        return coon, cur

    # 插入\更新\删除sql
    def op_insert(self, sql, *args):
        # print('op_insert', sql)
        coon, cur = self.connection()
        cur.execute(sql, *args)
        coon.commit()
        insert_id = cur.lastrowid
        self.closeall(cur, coon)
        return insert_id

    # 查询
    def op_select(self, sql, *args):
        # print('op_select', sql)
        coon, cur = self.connection()
        cur.execute(sql, *args)  # 执行sql
        select_res = cur.fetchall()  # 返回结果为字典
        # print('op_select', select_res)
        self.closeall(cur, coon)
        return select_res

    # 释放资源
    def closeall(self, cur, coon):
        # pass
        cur.close()
        coon.close()


mysql_con = OPMysql()
