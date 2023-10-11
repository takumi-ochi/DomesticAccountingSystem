searchAButtonName = {
    "clear": 'カレンダークリア',
    "toYear": 'カレンダー今年',
    "toMonth": 'カレンダー今月',
    "toDay": 'カレンダー今日',
    "year": 'カレンダー年',
    "month": 'カレンダー月',
    "ratioCalc": '比率計算',
    "yesteday": 'カレンダー←',
    "tomorrow": 'カレンダー→',
    "thisWeek": 'カレンダー今週'
}

def getSearchAButtonName(key):
    return searchAButtonName[key]

itemName = {
    "year": 'n年',
    "month": 'n月',
}
def getItemName(key):
    return itemName[key]

ratioItemName = {
    "keyword1": '比率キーワード',
    "sum": 'キーワード合計',
    "ratio": '比率(比率合計/収入)'
}
def getRatioItemName(key):
    return ratioItemName[key]