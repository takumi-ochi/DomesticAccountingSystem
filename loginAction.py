from myTkFrameWork.db.myDao import *
from myTkFrameWork.mySession import *

class loginAction:

    def getSession(params):
        sql = "SELECT * FROM userManager WHERE userId = :userId and userPassword = :userPassword"
        whereDic = {
            "userId": params["id"].get(),
            "userPassword": params["pass"].get()
        }

        conn = myDao()
        record = conn.myExecFindRecord(sql, whereDic)
        del conn

        if record == None:
            return False
        else:
            mySession.setUserId(record[0])
            mySession.setUserName(record[2])
            mySession.setAutho(record[3])
            return True