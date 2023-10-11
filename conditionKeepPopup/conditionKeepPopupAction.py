from myTkFrameWork.myDate import myDate
from myTkFrameWork.db.myDao import *
from myTkFrameWork.myConst import *
from myTkFrameWork.mySession import *

from searchA.searchConst import *

class conditionKeepPopupAction:
    mainTableName = "conditionMemory"

    def doSave(params):
        userName = mySession.getUserId() #ユーザーID取得
        sortNumber = conditionKeepPopupAction.getNewSort() #自動採番
        keyDic = conditionKeepPopupAction.getConditionDic(params) #検索条件辞書取得
    
        #検索条件保存
        conn = myDao()

        for key in keyDic.keys():
            if key == "calcKeyword1": 
                itemName = getRatioItemName("keyword1")
            else:
                itemName = getConditionValue(key)
            
            insertTuple = (
                userName,
                getMainTitle(),
                params["conditionName"].get(),
                itemName,
                keyDic[key],
                sortNumber
            )
            sql = "INSERT INTO " + conditionKeepPopupAction.getMainTable() + " VALUES (?,?,?,?,?,?)"
            conn.myExecUpdate(sql, insertTuple)
        
        del conn
    
    #更新処理
    def doUpdate(params):
        userName = mySession.getUserId() #ユーザーID取得
        keyDic = conditionKeepPopupAction.getConditionDic(params) #検索条件辞書取得

        conn = myDao()

        for key in keyDic.keys():
            if key == "calcKeyword1": 
                itemName = getRatioItemName("keyword1")
            else:
                itemName = getConditionValue(key)
            
            updateTuple = (keyDic[key],)
            sql = "UPDATE " + conditionKeepPopupAction.getMainTable() + " SET item = ? WHERE userName = " + myDao.valueSqlComp(userName, "text") + " AND display = " + myDao.valueSqlComp(getMainTitle(), "text") + " AND conditionName = " + myDao.valueSqlComp(params["conditionName"].get(), "text") + " AND itemName = " + myDao.valueSqlComp(itemName, "text")
            conn.myExecUpdate(sql, updateTuple)
        
        del conn
    
    #削除処理
    def doDelete(conditionName):
        sql = "DELETE FROM " + conditionKeepPopupAction.getMainTable() + " WHERE conditionName = :conditionName"
        whereDic = {"conditionName": conditionName}

        conn = myDao()
        conn.myExecUpdate(sql, whereDic)
        del conn
    
    def getNewSort():
        conn = myDao()
        #ソートナンバーの最大値を取得
        maxSortNumberRecord = conn.myExecFindRecord("SELECT MAX(sort) FROM " + conditionKeepPopupAction.getMainTable())
        #ソートナンバーの最大値を取得
        maxSortNumber = None
        maxSortNumberRecord = conn.myExecFindRecord("SELECT MAX(sort) FROM " + conditionKeepPopupAction.getMainTable())
        if maxSortNumberRecord != None: maxSortNumber = maxSortNumberRecord[0]

        #ソートナンバーの最大値を取得
        newSortNumber = 0
        if maxSortNumber != None: 
            newSortNumber = maxSortNumber + 1
        del conn
        return newSortNumber
    
    def getMainTable():
        return conditionKeepPopupAction.mainTableName
    
    def getConditionDic(params):
        #日付（開始）
        dateFromYear = params["dateFromYear"].get()
        dateFromMonth = params["dateFromMonth"].get()
        dateFromDay = params["dateFromDay"].get()

        #日付（終了）
        dateToYear = params["dateToYear"].get()
        dateToMonth = params["dateToMonth"].get()
        dateToDay = params["dateToDay"].get()

        moneyMin = params["moneyMin"].get().replace(',','') #金額（最低）
        moneyMax = params["moneyMax"].get().replace(',','') #金額（最高）
        
        #キーワード1
        keyword1 = params["keyWord1"].get()
        keyword1not = params["keyWord1not"].get()
        keyWord1orAnd = params["keyWord1orAnd"].get()

        #キーワード2
        keyword2 = params["keyWord2"].get()
        keyword2not = params["keyWord2not"].get()
        keyWord2orAnd = params["keyWord2orAnd"].get()

        #キーワード3
        keyword3 = params["keyWord3"].get()
        keyword3not = params["keyWord3not"].get()

        #並び替え1
        sort1 = params["sort1"].get()
        sort1AscDesc = params["sort1AscDesc"].get()

        #並び替え2
        sort2 = params["sort2"].get()
        sort2AscDesc = params["sort2AscDesc"].get()

        #並び替え3
        sort3 = params["sort3"].get()
        sort3AscDesc = params["sort3AscDesc"].get()

        #ドラフト
        draft = params["draft"].get()

        #キーワード
        calcKeyword1 = params["calcKeyword1"].get()

        return {
            "dateFromYear": dateFromYear,
            "dateFromMonth": dateFromMonth,
            "dateFromDay": dateFromDay,
            "dateToYear": dateToYear,
            "dateToMonth": dateToMonth,
            "dateToDay": dateToDay,
            "moneyMin": moneyMin,
            "moneyMax": moneyMax,
            "keyWord1": keyword1,
            "keyWord1not": keyword1not,
            "keyWord1orAnd": keyWord1orAnd,
            "keyWord2": keyword2,
            "keyWord2not": keyword2not,
            "keyWord2orAnd": keyWord2orAnd,
            "keyWord3": keyword3,
            "keyWord3not": keyword3not,
            "sort1": sort1,
            "sort1AscDesc": sort1AscDesc,
            "sort2": sort2,
            "sort2AscDesc": sort2AscDesc,
            "sort3": sort3,
            "sort3AscDesc": sort3AscDesc,
            "draft": "1" if draft else "0",
            "calcKeyword1": calcKeyword1
        }