from .db.myDao import *
from .myDate import *
from .mySession import *

def createReverseDic(dic):
    reverseDic = {}
    for key in dic.keys(): reverseDic[dic[key]] = key
    return reverseDic

#全体ヘッダーリンク集
headDic = {
    "return": '戻る',
    "logout": 'ログアウト'
}
def getHeadDic(key):
    return headDic[key]

#***********************************************************
#メインウィンドウ
#***********************************************************
#メインウィンドウ設定
def getDefaultWindowSetting():
    return getMainWindowSize()  + "+" + getMainWindowPosition()

#メインウィンドウサイズ
def getMainWindowSize():
    return "1050x600"

#メインウィンドウ位置
def getMainWindowPosition():
    return getMainWindowPositionX() + "+" + getMainWindowPositionY()

#メインウィンドウ横座標
def getMainWindowPositionX():
    return "450"

#メインウィンドウ縦座標
def getMainWindowPositionY():
    return "200"

#***********************************************************
#編集画面ウィンドウ
#***********************************************************
#編集ウィンドウ設定
def getEditWindowSetting():
    return getEditWindowSize()  + "+" + getEditWindowPosition()

#編集ウィンドウサイズ
def getEditWindowSize():
    return "440x430"

#編集ウィンドウ位置
def getEditWindowPosition():
    x = int(getMainWindowPositionX()) + 610
    y = int(getMainWindowPositionY()) + 170
    return str(x) + "+" + str(y)

#***********************************************************
#検索条件保存ウィンドウ
#***********************************************************
#検索条件保存ウィンドウ設定
def getConditionKeepWindowSetting():
    return getConditionKeepWindowSize()  + "+" + getConditionKeepWindowPosition()

#検索条件保存ウィンドウサイズ
def getConditionKeepWindowSize():
    return "440x150"

#検索条件保存ウィンドウ位置
def getConditionKeepWindowPosition():
    x = int(getMainWindowPositionX()) + 580
    y = int(getMainWindowPositionY()) + 390
    return str(x) + "+" + str(y)

#メインタイトル一覧
def getTitle():
    return '家計簿システム'

#メイン画面タイトル
def getMainTitle():
    return '検索画面'
def getEditTitle():
    return '編集画面'

#検索画面　検索項目
conditionDic = {
    "dateFrom": '日付(開始)',
    "dateFromYear": '日付(開始)年',
    "dateFromMonth": '日付(開始)月',
    "dateFromDay": '日付(開始)日',
    "dateTo": '日付(終了)',
    "dateToYear": '日付(終了)年',
    "dateToMonth": '日付(終了)月',
    "dateToDay": '日付(終了)日',
    "moneyMin": "金額(最低)",
    "moneyMax": "金額(最高)",
    "keyWord1": "キーワード1",
    "keyWord1not": "キーワード1not",
    "keyWord1orAnd": "キーワード1orAnd",
    "keyWord2": "キーワード2",
    "keyWord2not": "キーワード2not",
    "keyWord2orAnd": "キーワード2orAnd",
    "keyWord3": "キーワード3",
    "keyWord3not": "キーワード3not",
    "keyWord3orAnd": "キーワード3orAnd",
    "sort1": "並び替え1",
    "sort1AscDesc": "並び替え1AscDesc",
    "sort2": "並び替え2",
    "sort2AscDesc": "並び替え2AscDesc",
    "sort3": "並び替え3",
    "sort3AscDesc": "並び替え3AscDesc",
    "draft": "ドラフト"
}
conditionDicReverse = createReverseDic(conditionDic)
def getConditionValue(key):
    return conditionDic[key]
def getConditionKey(key):
    return conditionDicReverse[key]

#明細部
detailItemDic = {
    "hitCount": "該当件数",
    "imcomeSum": "収入合計",
    "expenditureSum": "支出合計",
    "diff": "差額(入-出)"
}
def getDetailItemValue(key):
    return detailItemDic[key]

#明細
detailDic = {
    "id": 'ID',
    "date": '日付',
    "store": '店舗・用途',
    "money": '金額',
    "remarks": '備考',
    "imcomeExpenditure": '収支',
    "draft": 'ドラフト'
}
detailDicReverse = createReverseDic(detailDic)
def getDetailValue(key):
    return detailDic[key]
def getDetailKey(key):
    return detailDicReverse[key]
def getDetailAll():
    return detailDic

#並び替えリスト
sortDic = {
        "purchaseDate": '日付',
        "store": '店舗・用途',
        "money": '金額',
        "imcomeExpenditure": '収支'
    }
sortDicReverse = createReverseDic(sortDic)
def getSortDic():
    return sortDic
def getSortValueTuple(emptyFlg = False):
    if emptyFlg:
        List = list(sortDic.values())
        List.insert(0, '')
        return tuple(List)
    else:
        return tuple(sortDic.values())
def getSortDicValue(key):
    return sortDic[key]
def getSortDicKey(key):
    return sortDicReverse[key]

#ボタン名
buttonNameDic = {
    "clear": 'クリア',
    "search": '検索',
    "newInset": '新規登録',
    "insert": '登録',
    "update": '更新',
    "draft": 'ドラフト',
    "delete": '削除',
    "yesterDay": '←',
    "tomorrow": '→',
    "toDay": '今日',
    "conditionKeep": '検索条件保存',
    "keep": '保存',
    "reflect": '反映',
    "changeMode": '切り替え',
}
def getButtonName(key):
    return buttonNameDic[key]

#更新ボタンの背景色
def getUpdateButtonBGColor():
    return "deep sky blue"

#削除ボタンの背景色
def getDeleteButtonBGColor():
    return "indian red"

#検索条件保存ポップアップ画面の項目名辞書
itemNamedic = {"conditionName":"検索名"}
def getConditionKeepPopupViewItemName(key):
    return itemNamedic[key]

#年リスト
def getYearTuple(userId):
    conn = myDao()
    autho = conn.myExecFindRecord("SELECT Autho FROM userManager WHERE userId = :userId", {"userId": userId})[0]
    del conn
    sqlWhere = {}
    sql = "SELECT DISTINCT substr(purchaseDate, 0, 5) FROM HouseholdAccountBook "
    if autho != "A": 
        sql += "WHERE userId = :userId "
        sqlWhere = {"userId": userId}
    sql += "ORDER BY purchaseDate asc"
    regiterYearList = []
    conn = myDao()
    recordList = conn.myExecFindList(sql, sqlWhere)
    regiterYearList.append('')
    for value in recordList: regiterYearList.append(value[0])
    del conn
    return tuple(regiterYearList)

#月リスト
def getMonthTuple():
    return ('', '01','02','03','04','05','06','07','08','09','10','11','12')

#日リスト
def getDayTuple(year = '', month = ''):
    returnDayList = []
    lastDay = 31
    
    if month != '' and month in ['04','06','09','11']:
        lastDay = 30
    elif month == '02':
        if year != '' and myDate.isleapYear(year):
            lastDay = 29
        else:
            lastDay = 28

    returnDayList.append('')
    for day in range(1, lastDay + 1): 
        dayStr = ''
        if len(str(day)) == 1:
            dayStr = '0' + str(day)
        else:
            dayStr = str(day)
        returnDayList.append(dayStr)
    
    return tuple(returnDayList)

#以外リスト
def getNotTuple():
    return ('', '以外')

#もしくは、かつリスト
def getOrAndTuple():
    return ('もしくは', 'かつ')

#昇順、降順リスト
ascDescDic = {
    "asc": '昇順',
    "desc": '降順'
}
ascDescDicReverse = createReverseDic(ascDescDic)
def getAscDescTuple():
        return tuple(ascDescDic.values())
def getAscDescValue(key):
    return ascDescDic[key]
def getAscDescKey(key):
    return ascDescDicReverse[key]

#エラーメッセージ
errorMessageDic = {
    "er-001": '検索結果は0件です。',
    "er-002": '次の文字は入力できません',
    "er-003": '明細に検索結果がある状態でキーワードを入力してから計算してください',
    "er-004": '明細の収入合計が1以上でないと比率計算ができません',
    }
def getErrorMessage(key):
    return errorMessageDic[key]

#アラートメッセージ
messageDic = {
    "msg-001": "登録しました",
    "msg-002": "更新しました",
    "msg-003": "削除しました",
    "msg-004": "削除しますか？",
    "msg-005": "続けて登録しますか？",
    "msg-006": "保存しました",
    "msg-007": "更新しますか？",
    "msg-008": "反映しました",
    }
def getMessage(key):
    return messageDic[key]

#検索条件名リスト取得
def getConditionNameList():
    tableName = "conditionMemory"

    conn = myDao()
    recordList = conn.myExecFindList("SELECT DISTINCT conditionName FROM " + tableName + " WHERE userName = :userName", {"userName": mySession.getUserId()})
    del conn

    recordList.insert(0, '') #先頭に空欄追加
    return recordList

#検索条件反映プルダウン
def getConditionReflectValueTuple():
    return tuple(getConditionNameList())

#収入・支出コード変換表
def getImcomeExpenditureDic():
    conn = myDao()
    recordList = conn.myExecFindList("SELECT * FROM codeName WHERE columnName = :columnName", {"columnName": '収入・支出'})
    del conn
    return {
        recordList[0][1]: recordList[0][2],
        recordList[1][1]: recordList[1][2]
    }
def getImcomeExpenditureReverseDic():
    dic = getImcomeExpenditureDic()
    return createReverseDic(dic)

if __name__ == "__main__":
    print("test")
    # print(getYearTuple("takumi"))
    print(getDayTuple('2016', '12'))