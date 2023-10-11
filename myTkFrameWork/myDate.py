from datetime import *

class myDate():
    def getDateWithSlash(date):
        date = str(date)
        return date[0:4] + '/' + date[5:7] + '/' + date[8:10]
    
    #うるう年判断
    def isleapYear(year):
        return int(year) % 400 == 0 or (int(year) % 100 != 0 and int(year) % 4 == 0)
    
    #日付が正しいか判断 yyyy/mm/dd用
    def isCorrectDate(value):
        if value == '': return

        if value.count('/') != 2:
            return False

        dateList = value.split('/')
        year = int(dateList[0])
        month = int(dateList[1])
        day = int(dateList[2])

        try:
            newDataStr="%04d/%02d/%02d" % (year,month,day)
            datetime.strptime(newDataStr,"%Y/%m/%d")
            return
        except ValueError:
            return False
        
        return True, year, month, day
    
    #今日の日付を取得
    def getToday(getType):
        createDate = str(date.today().strftime("%Y/%m/%d"))
        year = createDate[0:4]
        month = createDate[5:7]

        if getType == "date":
            return createDate
        elif getType == "year":
            return year
        elif getType == "month":
            return month
        elif getType == "day":
            return createDate[8:10]
        elif getType == "fistDay":
            return '01'
        elif getType == "lastDay":
            return myDate.getSelectLastDay(year, month)
    
    #指定月の最終日を取得
    def getSelectLastDay(year, month):
        if month in ['04', '06', '09', '11']:
                return '30'
        elif month == '02':
            if myDate.isleapYear(year):
                return '29'
            else:
                return '28'
        else:
            return '31'
    
    #日付から曜日を取得
    def getDay(tDate):
        dayJp = datetime.strptime(tDate, '%Y-%m-%d').strftime('%a')
        if dayJp == "Mon":
            dayJp = '月'
        elif dayJp == "Tue":
            dayJp = '火'
        elif dayJp == "Wed":
            dayJp = '水'
        elif dayJp == "Thu":
            dayJp = '木'
        elif dayJp == "Fri":
            dayJp = '金'
        elif dayJp == "Sat":
            dayJp = '土'
        else:
            dayJp = '日'
        
        return '(' + dayJp + ')'

    #画面の日付を前日にする
    def dateYesterdayPulldown(date):
        if date["year"] == '' or date["month"] == '' or date["day"] == '':
            return
        
        tstr = date["year"] + '-' + date["month"] + '-' + date["day"]
        tdatetime = datetime.strptime(tstr, '%Y-%m-%d')
        yesterday = tdatetime - timedelta(days=1)
        yesterdayStr = yesterday.strftime('%Y-%m-%d')

        date["year"] = yesterdayStr[0:4]
        date["month"] = yesterdayStr[5:7]
        date["day"] = yesterdayStr[8:10]

        return date
    
    #画面の日付を翌日にする
    def dateTomorrowPulldown(date):
        if date["year"] == '' or date["month"] == '' or date["day"] == '':
            return
        
        tstr = date["year"] + '-' + date["month"] + '-' + date["day"]
        tdatetime = datetime.strptime(tstr, '%Y-%m-%d')
        tomorrow = tdatetime + timedelta(days=1)
        tomorrowStr = tomorrow.strftime('%Y-%m-%d')

        date["year"] = tomorrowStr[0:4]
        date["month"] = tomorrowStr[5:7]
        date["day"] = tomorrowStr[8:10]

        return date
    
     #画面の日付を前日にする(テキスト)
    def dateYesterdayText(date):
        if date == '':
            return
        
        tstr = date.replace('/', '-')
        tdatetime = datetime.strptime(tstr, '%Y-%m-%d')
        yesterday = tdatetime - timedelta(days=1)
        yesterdayStr = yesterday.strftime('%Y/%m/%d')

        return yesterdayStr
    
    #画面の日付を翌日にする(テキスト)
    def dateTomorrowText(date):
        if date == '':
            return
        
        tstr = date.replace('/', '-')
        tdatetime = datetime.strptime(tstr, '%Y-%m-%d')
        tomorrow = tdatetime + timedelta(days=1)
        tomorrowStr = tomorrow.strftime('%Y/%m/%d')

        return tomorrowStr

if __name__ == "__main__":
    print(myDate.getToday("lastDay"))