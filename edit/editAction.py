from functools import update_wrapper
from myTkFrameWork.myDate import myDate
from myTkFrameWork.db.myDao import *
from myTkFrameWork.myConst import *
from myTkFrameWork.mySession import *

class editAction:
    def doInsert(params):
        userId = mySession.getUserId() #ユーザーID取得
        id = editAction.getNewId() #自動採番
        date = params["date"].get().replace('/','-')
        store = params["store"].get()
        money = params["money"].get().replace(',','')
        remarks = params["remarks"].get("1.0", "end -1c")
        imcExpDic = getImcomeExpenditureReverseDic()
        imcomeExpenditure = int(imcExpDic[params["imcomeExpenditure"].get()])
        if params["draft"].get():
            draft = 1 
        else:
            draft = 0
        sql = "INSERT INTO HouseholdAccountBook VALUES (?,?,?,?,?,?,?,?)"
        insertTuple = (userId, id, date, store, money, remarks, imcomeExpenditure, draft)
        conn = myDao()
        conn.myExecUpdate(sql, insertTuple)
        del conn
    
    def doUpdate(params):
        userId = mySession.getUserId() #ユーザーID取得
        id = params["id"]
        date = params["date"].get().replace('/','-')
        store = params["store"].get()
        money = params["money"].get().replace(',','')
        remarks = params["remarks"].get("1.0", "end -1c")
        imcExpDic = getImcomeExpenditureReverseDic()
        imcomeExpenditure = int(imcExpDic[params["imcomeExpenditure"].get()])
        if params["draft"].get():
            draft = 1
        else:
            draft = 0
        
        sql = "UPDATE HouseholdAccountBook SET purchaseDate = ?, store = ?, money = ?, remarks = ?, imcomeExpenditure = ?, draft = ? WHERE userId = " + myDao.valueSqlComp(userId, "text") + " and receiptId = " + myDao.valueSqlComp(id, "integer")
        updateList = []
        
        #日付
        if date:
            updateList.append(date)
        else:
            updateList.append(None)
        
        #店舗・用途
        if store:
            updateList.append(store)
        else:
            updateList.append(None)
        
        #金額
        if money:
            updateList.append(money)
        else:
            updateList.append(None)
        
        #備考
        if remarks:
            updateList.append(remarks)
        else:
            updateList.append(None)

        #収入・支出
        updateList.append(imcomeExpenditure)
        
        #ドラフト
        updateList.append(draft)
        
        conn = myDao()
        conn.myExecUpdate(sql, tuple(updateList))
        del conn
    
    def doDelete(params):
        sql = "DELETE FROM HouseholdAccountBook WHERE receiptId = :id"
        whereDic = {"id": int(params["id"])}
        conn = myDao()
        conn.myExecUpdate(sql, whereDic)
        del conn
    
    def getNewId():
        conn = myDao()
        newId = conn.myExecFindRecord("SELECT MAX(receiptId) FROM HouseholdAccountBook")[0] + 1
        del conn
        return newId