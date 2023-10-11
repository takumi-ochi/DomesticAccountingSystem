import datetime
from tkinter import messagebox
from myTkFrameWork.db.myDao import *
from myTkFrameWork.mySession import *

class Error:
    #エラーメッセージ
    errors = []

    #エラーをリセット
    def errorReset():
        Error.errors = []

    #エラーが存在するかチェック
    def isError():
        if Error.errors:
            return True
        return False
    
    #エラーを取得
    def getErrors():
        return Error.errors
    
    #エラーメッセージを表示
    def showError():
        errorMsg = ""
        for error in Error.getErrors():
            errorMsg += error + '\n'
        messagebox.showerror('エラーメッセージ', errorMsg)
    
    def createMessage(msg, widgetName = ''):
        if widgetName:
            msg += '：' + widgetName
        Error.errors.append(msg)
    
    def createMessage2(msg, widgetNames = []):
        for name in widgetNames:
            msg = msg.replace('?', str(name), 1)
        Error.errors.append(msg)

    #必須チェック
    def validateRequired(inputWidget, widgetName = ''):
        inputData = inputWidget.get()
        if inputData == '':
                Error.validateRequiredMessage(widgetName)
    
    def validateRequiredMessage(widgetName):
        Error.createMessage2('?は必ず入力してください', [widgetName])
    
    #日付入力チェック
    def validateDateRequied(inputWidgetYear, inputWidgetMonth, inputWidgetDay, widgetName = ''):
        year = inputWidgetYear.get()
        month = inputWidgetMonth.get()
        day = inputWidgetDay.get()

        #月と日のみ入力された場合
        if month != '' and year == '':
            Error.validateDateMonthMessage(widgetName)
        if day != '' and (year == '' or month == ''):
            Error.validateDateDayMessage(widgetName)
        
    def validateDateMonthMessage(widgetName = ''):
        Error.createMessage('月を入力するときは年も入力して下さい', widgetName)
    
    def validateDateDayMessage(widgetName = ''):
        Error.createMessage('日を入力するときは年と月も入力して下さい', widgetName)
    
    #日付妥当性チェック
    def validateDateValidity(inputWidgetYear, inputWidgetMonth, inputWidgetDay, widgetName = ''):
        year = inputWidgetYear.get()
        month = inputWidgetMonth.get()
        day = inputWidgetDay.get()

        if year == '' or month == '' or day == '':
            return
        
        year = int(year)
        month = int(month)
        day = int(day)
        
        if month in [4, 6, 9, 11]:
            if day == 31:
                    Error.validateDateValidityMessage(widgetName)
        elif month == 2:
            if day >= 30:
                Error.validateDateValidityMessage(widgetName)
            elif day == 29: #閏年チェック
                if year % 400 == 0 or (year % 100 != 0 and year % 4 == 0):
                    return
                else:
                    Error.validateDateValidityMessage(widgetName)
    
    #日付チェック テキストボックス用
    def validateDateCheck(inputWidget, widgetName = ''):
        value = str(inputWidget.get())
        if value == '': return

        if value.count('/') != 2:
            Error.validateDateValidityMessage(widgetName)
            return

        dateList = value.split('/')
        year = int(dateList[0])
        month = int(dateList[1])
        day = int(dateList[2])

        try:
            newDataStr="%04d/%02d/%02d" % (year,month,day)
            datetime.datetime.strptime(newDataStr,"%Y/%m/%d")
            return
        except ValueError:
            Error.validateDateValidityMessage(widgetName)
    
    def validateDateValidityMessage(widgetName = ''):
        Error.createMessage('日付がおかしいです', widgetName)
    
    #数値チェック
    def validateNumberCheck(inputWidgetNum, widgetName = ''):
        if inputWidgetNum.get() == '':
            return
        
        #整数チェック
        try:
            int(inputWidgetNum.get())
        except:
            Error.validateNumberCheckMessage(widgetName)
    
    def validateNumberCheckMessage(widgetName = ''):
        Error.createMessage('数値を入力して下さい', widgetName)
    
    #マイナス値チェック
    def validateMinus(inputWidgetNum, widgetName = ''):
        if inputWidgetNum.get() == '':
            return 
        
        num = int(inputWidgetNum.get())
        if num < 0:
            Error.validateMinusMessage(widgetName)
    
    def validateMinusMessage(widgetName = ''):
        Error.createMessage('マイナス値を入力しないで下さい', widgetName)
    
    #日付比較チェック
    def validateDateComparison(beforeInputWidgetYear, beforeInputWidgetMonth, beforeInputWidgetDay, afterInputWidgetYear, afterInputWidgetMonth, afterInputWidgetDay, beforeWidgetName = '', afterWidgetName = ''):
        beforeYear = beforeInputWidgetYear.get()
        beforeMonth = beforeInputWidgetMonth.get()
        beforeDay = beforeInputWidgetDay.get()
        afterYear = afterInputWidgetYear.get()
        afterMonth = afterInputWidgetMonth.get()
        afterDay = afterInputWidgetDay.get()

        if beforeYear == '':
            return
        else:
            beforeYear = int(beforeYear)
        
        if afterYear == '':
            return 
        else:
            afterYear = int(afterYear)
        
        if beforeMonth == '':
            beforeMonth = 1
        else:
            beforeMonth = int(beforeMonth)
        
        if afterMonth == '':
            afterMonth = 1
        else:
            afterMonth = int(afterMonth)
        
        if beforeDay == '':
            beforeDay = 1
        else:
            beforeDay = int(beforeDay)
        
        if afterDay == '':
            afterDay = 1
        else:
            afterDay = int(afterDay)
        
        beforeDate = datetime.date(beforeYear, beforeMonth, beforeDay)
        afterDate = datetime.date(afterYear, afterMonth, afterDay)

        if beforeDate > afterDate:
            Error.validateDateComparisonMessage(beforeWidgetName, afterWidgetName)
    
    def validateDateComparisonMessage(beforeWidgetName = '', afterWidgetName = ''):
        Error.createMessage2('?より?を過去日にしないで下さい', [beforeWidgetName, afterWidgetName])
    
    #数値比較チェック
    def validateNumberComparison(inputWidgetNumberMin, inputWidgetNumberMax, widgetName1 = '', widgetName2 = ''):
        if inputWidgetNumberMin.get() == '' or inputWidgetNumberMax.get() == '':
            return 
        
        numberMin = int(inputWidgetNumberMin.get())
        numberMax = int(inputWidgetNumberMax.get())

        if numberMin > numberMax:
            Error.validateNumberComparisonMessage(widgetName1, widgetName2)

    
    def validateNumberComparisonMessage(widgetName1 = '', widgetName2 = ''):
        Error.createMessage2('?より?を低くしないで下さい', [widgetName1, widgetName2])
    
    #桁数チェック(n桁のみ)
    def validateNumberOfDigisIdentification(inputWidget, numberOfDigis, widgetName):
        if len(inputWidget.get()) != numberOfDigis:
            Error.validateNumberOfDigisIdentificationMessage(numberOfDigis, widgetName)
    
    def validateNumberOfDigisIdentificationMessage(numberOfDigis, widgetName):
        Error.createMessage2('?桁を入力して下さい：?', [numberOfDigis, widgetName])
    
    #桁数チェック(n桁以下)
    def validateNumberOfDigis(inputWidget, numberOfDigis, widgetName):
        if len(inputWidget.get()) > numberOfDigis:
            Error.validateNumberOfDigisMessage(numberOfDigis, widgetName)
    
    def validateNumberOfDigisMessage(numberOfDigis, widgetName):
        Error.createMessage2('?桁を以下を下さい：?', [numberOfDigis, widgetName])
    
    #入力制限(?と,)
    def limitInput(inputWidgetText, widgetName):
        if inputWidgetText in ['?', ',']:
            Error.limitInputMessage(widgetName)
    
    def limitInputMessage(widgetName):
        Error.createMessage('?と,は使用不可能です', widgetName)
    
    #重複チェック
    def doubleCheck(tableName, whereSetList):
        #クエリ
        sqlCount = "SELECT COUNT(*) FROM " + tableName + " "
        sqlWhere = "WHERE "

        #検索条件(where句)作成
        whereDic = {}

        for whereSet in whereSetList:
            if whereSet:
                sqlWhere += whereSet["where"]
                whereDic[whereSet["columun"]] = whereSet["value"]

        conn = myDao()
        count = conn.myExecFindRecord(sqlCount + sqlWhere, whereDic)[0]
        del conn

        if count > 0:
            Error.doubleCheckMessage()
    
    def doubleCheckMessage():
        Error.createMessage('データが重複しています')
    
    #存在チェック
    def isExist(tableName, whereSetList):
        #クエリ
        sqlCount = "SELECT COUNT(*) FROM " + tableName + " "
        sqlWhere = "WHERE "

        #検索条件(where句)作成
        whereDic = {}

        for whereSet in whereSetList:
            if whereSet:
                sqlWhere += whereSet["where"]
                whereDic[whereSet["columun"]] = whereSet["value"]

        conn = myDao()
        count = conn.myExecFindRecord(sqlCount + sqlWhere, whereDic)[0]
        del conn

        if count == 0:
            Error.isExistMessage()
    
    def isExistMessage():
        Error.createMessage('該当データが存在しません')