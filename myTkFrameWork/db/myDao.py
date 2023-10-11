import sqlite3

class myDao:
    dbName = ""
    conn = None
    cur = None

    def __init__(self, myDbName = ""):
        #DB名取得
        if myDbName:
            myDao.dbName = "./db/" + myDbName + ".db"
        else:
            file = None
            try:
                file = open("./myTkFrameWork/db/dbname.txt")
                myDao.dbName = file.read()
            except Exception as e:
                print(e)
            finally:
                if file != None: file.close()
        #DB接続開始
        self.conn = sqlite3.connect(myDao.dbName)
        self.cur = self.conn.cursor()
    
    #DB切断
    def __del__(self):
        self.cur.close()
        self.conn.close()
    
    #SQLログ出力
    def log(self, sql, condition, mode):
        logSql = sql
        if mode == "select":
            for key in condition.keys():
                if type(condition[key]) is int:
                    repStr = str(condition[key])
                else:
                    repStr = '\'' + str(condition[key]) + '\''
                logSql = logSql.replace(':' + key, repStr)
        else:
            for value in condition:
                if value == None: 
                    repStr = 'null'
                else:
                    if type(value) is int:
                        repStr = str(value)
                    else:
                        #シーケンス文字をログに残したい
                        repStr = '\'' + str(value) + '\''
                logSql = logSql.replace('?', repStr, 1)
        print(logSql)
    
    #1行取得
    def myExecFindRecord(self, sql, condition = {}):
        self.log(sql, condition, "select")
        self.cur.execute(sql, condition)
        record = self.cur.fetchone()
        if record == None: return None
        return list(record)
    
    #複数行取得
    def myExecFindList(self, sql, condition = {}):
        self.log(sql, condition, "select")
        self.cur.execute(sql, condition)
        recordList = []
        for record in self.cur.fetchall(): recordList.append(list(record))

        return recordList
    
    #登録・更新・削除実行
    def myExecUpdate(self, sql, values = ()):
        self.log(sql, values, "update")
        self.cur.execute(sql, values)
        self.conn.commit()
    
    #前方一致
    def myPrefixMatch(word):
        return '%' + word

    #部分一致
    def myPartialMatch(word):
        return '%' + word + '%'

    #後方一致
    def myBackwardMatch(word):
        return word + '%'
    
    def valueSqlComp(value, type):
        returnValue = ""
        if type == "text":
            returnValue = "\'" + str(value) + "\'"
        elif type == "integer":
            returnValue = str(value)
        
        return returnValue

#メソッドテスト 起動コマンド：python3 .\db\myDao.py
if __name__ == "__main__":
    print("test myDao")
    myConn = myDao()
    #検索テンプレ
    # record = myConn.myExecFindRecord("SELECT name FROM memberInfo WHERE name = :name", {"name":'生田絵梨花'})
    # print(record)

    #登録テンプレ
    # myConn.myExecUpdate("INSERT INTO memberInfo VALUES(?,?,?,?,?,?,?,?,?)", (2, None, '乃木坂46', 1, None, '東京', 'A', 160.2, None)) #Noneはnullで登録される
    # print(myConn.myExecFindList("SELECT name FROM memberInfo"))