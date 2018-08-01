import logging
import pymssql

format_dict = {
   1: logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
   2: logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
   3: logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
   4: logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
   5: logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
}


class Logger():
    def __init__(self, logname, loglevel, logger):
        '''
           指定保存日志的文件路径，日志级别，以及调用文件
           将日志存入到指定的文件中
        '''

        # 创建一个logger
        self.logger = logging.getLogger(logger)
        self.logger.setLevel(logging.DEBUG)

        # 创建一个handler，用于写入日志文件
        fh = logging.FileHandler(logname)
        fh.setLevel(logging.DEBUG)

        # 再创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # 定义handler的输出格式
        # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        formatter = format_dict[int(loglevel)]
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # 给logger添加handler
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

    def getlog(self):
        return self.logger


class MySql(object):
    def __init__(self, host, user, password, datebase, charset='utf8'):

        self.host = host
        self.user = user
        self.password = password
        self.datebase = datebase
        self.charset = charset
    def __GetCursor(self):
        if self.datebase is None:
            raise (NameError, '数据库名称为空')
        try:
            self.conn = pymssql.connect(host=self.host, user=self.user, password=self.password, database=self.datebase, charset=self.charset)
            cursor=self.conn.cursor()
        except Exception as err:
            raise (NameError,'连接数据库失败')
        return cursor

    def insertdata(self, sqlstr, res):
        cur = self.__GetCursor()
        try:
            cur.executemany(sqlstr, res)
            self.conn.commit()
        except Exception as err:
            self.conn.rollback()
            raise (NameError, '插入数据失败：'+str(err))
        finally:
            self.conn.close()

    def insertdata(self, sqlstr):
        cur = self.__GetCursor()
        try:
            cur.execute(sqlstr)
            self.conn.commit()
        except Exception as err:
            self.conn.rollback()
            raise (NameError, '插入数据失败：'+str(err))
        finally:
            self.conn.close()
    def selectData(self,sqlstr):
        cur = self.__GetCursor()
        try:
            cur.execute(sqlstr)
            resList = cur.fetchall()
        except Exception as err:
            raise (NameError, '查询数据失败'+str(err))
        finally:

            # 查询完毕后必须关闭连接
            self.conn.close()
        return resList
    def ExecNon(self,sqlstr):
        cur = self.__GetCursor()
        try:
            cur.execute(sqlstr)
            self.conn.commit()
        except Exception as err:
            raise (NameError, '操作失败！'+str(err))
        self.conn.close()




# mysql = MySql('127.0.0.1', 'sa', '', 'movie')
# mysql.insertdata("insert into T_Url(Url) values('qwe')")
