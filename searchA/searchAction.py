from myTkFrameWork.db.myDao import *
from myTkFrameWork.myConst import *
from myTkFrameWork.mySession import *

from .searchConst import *

class searchAction:

    def doSearch(params):
        dateFrom = ''
        if params["dateFromYear"].get():
            dateFrom += params["dateFromYear"].get()
            if params["dateFromMonth"].get():
                dateFrom += '-' + params["dateFromMonth"].get()
                if params["dateFromDay"].get():
                    dateFrom += '-' + params["dateFromDay"].get()
                else:
                    dateFrom += '-01' #1日設定
            else:
                dateFrom += '-01-01' #1月1日設定
        
        dateTo = ''
        if params["dateToYear"].get():
            dateTo += params["dateToYear"].get()
            if params["dateToMonth"].get():
                dateTo += '-' + params["dateToMonth"].get()
                if params["dateToDay"].get():
                    dateTo += '-' + params["dateToDay"].get()
                else:
                    dateTo += '-01' #1日設定
            else:
                dateTo += '-01-01' #1月1日設定
        

        moneyMin = int(params["moneyMin"].get().replace(',','')) if params["moneyMin"].get() else 0
        moneyMax = int(params["moneyMax"].get().replace(',','')) if params["moneyMax"].get() else 0
        keyword1 = params["keyWord1"].get()
        keyword1not = params["keyWord1not"].get()
        keyWord1orAnd = params["keyWord1orAnd"].get()
        keyword2 = params["keyWord2"].get()
        keyword2not = params["keyWord2not"].get()
        keyWord2orAnd = params["keyWord2orAnd"].get()
        keyword3 = params["keyWord3"].get()
        keyword3not = params["keyWord3not"].get()
        sort1 = params["sort1"].get()
        sort1AscDesc = params["sort1AscDesc"].get()
        sort2 = params["sort2"].get()
        sort2AscDesc = params["sort2AscDesc"].get()
        sort3 = params["sort3"].get()
        sort3AscDesc = params["sort3AscDesc"].get()
        draft = params["draft"].get()

        #クエリ
        sqlCount = "SELECT COUNT(*) FROM HouseholdAccountBook "
        sqlSelect = "SELECT * FROM HouseholdAccountBook "
        sqlWhere = ""
        sqlOrderBy = "ORDER BY "

        #検索条件(where句)作成
        whereDic = {}

        #日付(開始)
        if dateFrom:
            sqlWhere += "purchaseDate >= :dateFrom AND "
            whereDic["dateFrom"] = dateFrom
        
        #日付(終了)
        if dateTo:
            sqlWhere += "purchaseDate <= :dateTo AND "
            whereDic["dateTo"] = dateTo
        
        #金額(最低)
        if moneyMin:
            sqlWhere += "money >= :moneyMin AND "
            whereDic["moneyMin"] = moneyMin

        #金額(最高)
        if moneyMax:
            sqlWhere += "money <= :moneyMax AND "
            whereDic["moneyMax"] = moneyMax

        #キーワードが存在する場合
        iskeyword = keyword1 or keyword2 or keyword3
        if iskeyword:
            sqlWhere += "( "
        
        #キーワード1
        if keyword1:
            if keyword1not == '以外':
                sqlWhere += "NOT "
            sqlWhere += "(store LIKE :keyword1 OR remarks LIKE :keyword1) "
            whereDic["keyword1"] = myDao.myPartialMatch(keyword1)
        
        if keyword1 and (keyword2 or keyword3):
            if keyWord1orAnd == 'もしくは':
                sqlWhere += "OR "
            elif keyWord1orAnd == 'かつ':
                sqlWhere += "AND "
        
        #キーワード2
        if keyword2:
            if keyword2not == '以外':
                sqlWhere += "NOT "
            sqlWhere += "(store LIKE :keyword2 OR remarks LIKE :keyword2) "
            whereDic["keyword2"] = myDao.myPartialMatch(keyword2)
        
        if  keyword2 and keyword3:
            if keyWord2orAnd == 'もしくは':
                sqlWhere += "OR "
            elif keyWord2orAnd == 'かつ':
                sqlWhere += "AND "

        #キーワード3
        if keyword3:        
            if keyword3not == '以外':
                sqlWhere += "NOT "
            sqlWhere += "(store LIKE :keyword3 OR remarks LIKE :keyword3) "
            whereDic["keyword3"] = myDao.myPartialMatch(keyword3)

        if iskeyword:
            sqlWhere += ") AND "
        
        #ドラフト
        if draft:
            sqlWhere += "draft = 1 AND "
        else:
            sqlWhere += "draft = 0 AND "
        
        if sqlWhere:
            sqlWhere = "WHERE " + sqlWhere[:-4]
                
        #ORDER BY句
        if sort1:
            sqlOrderBy += getSortDicKey(sort1) + " " + getAscDescKey(sort1AscDesc) + ", "
        
        if sort2:
            sqlOrderBy += getSortDicKey(sort2) + " " + getAscDescKey(sort2AscDesc) + ", "

        if sort3:
            sqlOrderBy += getSortDicKey(sort3) + " " + getAscDescKey(sort3AscDesc) + ", "

        sqlOrderBy += "receiptId desc, "

        #検索処理
        conn = myDao()
        recordCount = conn.myExecFindRecord(sqlCount + sqlWhere + sqlOrderBy[:-2], whereDic)[0]
        recordList = None
        if recordCount: 
            recordList = conn.myExecFindList(sqlSelect + sqlWhere + sqlOrderBy[:-2], whereDic)
        del conn

        resultSet = {}
        resultSet["count"] = recordCount
        resultSet["list"] = recordList
        imcomeSum = 0
        expenditureSum = 0
        if resultSet["list"] != None:
            
            for record in resultSet["list"]:
                if record[6] == 0: #収入明細の場合
                    imcomeSum += record[4]
                else: #支出明細の場合
                    expenditureSum += record[4]
        resultSet["imcomeSum"] = imcomeSum
        resultSet["expenditureSum"] = expenditureSum
        return resultSet
    
    #検索条件保存
    def doConditionSave(params):
        userId = mySession.getUserId() #ユーザーID取得
        dateFromYear = params["dateFromYear"].get()
        dateFromMonth = params["dateFromMonth"].get()
        dateFromDay = params["dateFromDay"].get()
        dateToYear = params["dateToYear"].get()
        dateToMonth = params["dateToMonth"].get()
        dateToDay = params["dateToDay"].get()        
        moneyMin = params["moneyMin"].get().replace(',','')
        moneyMax = params["moneyMax"].get().replace(',','')
        keyword1 = params["keyWord1"].get()
        keyword1not = params["keyWord1not"].get()
        keyWord1orAnd = params["keyWord1orAnd"].get()
        keyword2 = params["keyWord2"].get()
        keyword2not = params["keyWord2not"].get()
        keyWord2orAnd = params["keyWord2orAnd"].get()
        keyword3 = params["keyWord3"].get()
        keyword3not = params["keyWord3not"].get()
        sort1 = params["sort1"].get()
        sort1AscDesc = params["sort1AscDesc"].get()
        sort2 = params["sort2"].get()
        sort2AscDesc = params["sort2AscDesc"].get()
        sort3 = params["sort3"].get()
        sort3AscDesc = params["sort3AscDesc"].get()
        draft = params["draft"].get()
        calcKeyword1 = params["calcKeyword1"].get()

        keyDic = {
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

        #前回検索条件削除
        sql = "DELETE FROM Log WHERE userId = :userId AND display =:display"
        whereDic = {"userId": userId, "display": getMainTitle()}
        conn = myDao()
        conn.myExecUpdate(sql, whereDic)

        #検索条件登録
        for key in keyDic.keys():
            
            if key == "calcKeyword1": 
                itemName = getRatioItemName("keyword1")
            else:
                itemName = getConditionValue(key)
            
            insertTuple = (
                userId,
                getMainTitle(),
                itemName,
                keyDic[key]
            )
            sql = "INSERT INTO Log VALUES (?,?,?,?)"
            conn.myExecUpdate(sql, insertTuple)
        
        del conn
    
    #前回検索条件呼び出し
    def getBeforeCondition(itemName):
        sql = "SELECT item FROM Log WHERE userId = :userId AND display =:display AND itemName = :itemName"
        whereDic = {
            "userId": mySession.getUserId(),
            "display": getMainTitle(),
            "itemName": itemName
        }

        conn = myDao()
        item = conn.myExecFindRecord(sql, whereDic)
        del conn
        if item != None:
            if itemName == "ドラフト":
                if item[0] == "0":
                    return False
                else:
                    return True
            else:
                return item[0]
        else: #前回検索が存在しない場合
            if itemName == "キーワード1orAnd" or itemName == "キーワード2orAnd":
                return getOrAndTuple()[0]
            elif itemName == "並び替え1AscDesc" or itemName == "並び替え2AscDesc" or itemName == "並び替え3AscDesc":
                return getAscDescTuple()[0]
            elif itemName == "ドラフト":
                return False
            return ""

    #指定検索条件呼び出し
    def getKeepCondition(conditionName, itemName):
        sql = "SELECT item FROM conditionMemory WHERE userName = :userName AND display = :display AND conditionName =:conditionName AND itemName = :itemName"
        whereDic = {
            "userName": mySession.getUserId(),
            "display": getMainTitle(),
            "conditionName": conditionName,
            "itemName": itemName
        }

        conn = myDao()
        item = conn.myExecFindRecord(sql, whereDic)
        del conn
        if item != None:
            if itemName == "ドラフト":
                if item[0] == "0":
                    return False
                else:
                    return True
            else:
                return item[0]
        else: #指定検索条件が存在しない場合
            if itemName == "キーワード1orAnd" or itemName == "キーワード2orAnd":
                return getOrAndTuple()[0]
            elif itemName == "並び替え1AscDesc" or itemName == "並び替え2AscDesc" or itemName == "並び替え3AscDesc":
                return getAscDescTuple()[0]
            elif itemName == "ドラフト":
                return False
            return ""