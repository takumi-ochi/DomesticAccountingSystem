from tkinter import Widget, messagebox

from myTkFrameWork.myTk import *
from myTkFrameWork.myConst import *
from myTkFrameWork.mySession import *
from myTkFrameWork.db.myDao import *
from myTkFrameWork.myDate import *

from .searchConst import *
from .searchAction import *
from edit.editView import *
from conditionKeepPopup.conditionKeepPopupView import *

class searchViewA:
    view = None
    editview = None
    mainFrame = "search"
    pulldownUpdateFlg = False #プルダウン更新フラグ

    def __init__(self):
        self.view = myTk("", "", "frame", searchViewA.mainFrame)
        self.reSearchFlg = False
        self.view.root.bind('<FocusIn>', self.forcusInFunc)

        #ヘッダー部
        headFrame = "head"
        self.view.createFrame(headFrame, searchViewA.mainFrame, 0, 0)
        self.view.titleLabel(headFrame, 'ユーザー名:' + mySession.getUserName(), 15)

        #ヘッダーリンク
        headLinkFrame = "headLink"
        self.view.createFrame(headLinkFrame, searchViewA.mainFrame, 990, 0)
        self.view.linkLabel(headLinkFrame, getHeadDic("return"))
        self.view.getWidgetDic(headLinkFrame, getHeadDic("return")).bind('<ButtonPress>', self.returnBind)

        #タイトル部
        self.view.createFrame("title", searchViewA.mainFrame, 400, 10)
        self.view.titleLabel("title", getMainTitle())

        #検索項目部
        conditionFrame = "condition"
        self.conditionFrame = conditionFrame
        self.view.createFrame(conditionFrame, searchViewA.mainFrame, 10, 80)
        
        #検索部
        #日付(開始)
        self.view.nameLabel(conditionFrame, getConditionValue("dateFrom"), False, "15", "normal", "lightskyblue", tk.RIDGE, 2, "MSゴシック", '日付')
        self.view.createCombobox(conditionFrame, getConditionValue("dateFromYear"), 4, getYearTuple(mySession.getUserId()))
        self.view.getWidgetDic(conditionFrame, getConditionValue("dateFromYear")).set(searchAction.getBeforeCondition(getConditionValue("dateFromYear")))
        self.view.createCombobox(conditionFrame, getConditionValue("dateFromMonth"), 2, getMonthTuple())
        self.view.getWidgetDic(conditionFrame, getConditionValue("dateFromMonth")).set(searchAction.getBeforeCondition(getConditionValue("dateFromMonth")))
        year, month = self.getYearMonth(conditionFrame, True)
        self.view.createCombobox(conditionFrame, getConditionValue("dateFromDay"), 2, getDayTuple(year, month))
        self.view.getWidgetDic(conditionFrame, getConditionValue("dateFromDay")).set(searchAction.getBeforeCondition(getConditionValue("dateFromDay")))
        self.view.getWidgetDic(conditionFrame, getConditionValue("dateFromYear")).bind('<<ComboboxSelected>>', lambda event: self.dateSet(event, conditionFrame, True))
        self.view.getWidgetDic(conditionFrame, getConditionValue("dateFromMonth")).bind('<<ComboboxSelected>>', lambda event: self.dateSet(event, conditionFrame, True))

        #日付(終了)
        self.view.nameLabel(conditionFrame, getConditionValue("dateTo"), False, "15", "normal", "lightskyblue", tk.RIDGE, 2, "MSゴシック", '～')
        self.view.createCombobox(conditionFrame, getConditionValue("dateToYear"), 4, getYearTuple(mySession.getUserId()))
        self.view.getWidgetDic(conditionFrame, getConditionValue("dateToYear")).set(searchAction.getBeforeCondition(getConditionValue("dateToYear")))
        self.view.createCombobox(conditionFrame, getConditionValue("dateToMonth"), 2, getMonthTuple())
        self.view.getWidgetDic(conditionFrame, getConditionValue("dateToMonth")).set(searchAction.getBeforeCondition(getConditionValue("dateToMonth")))
        year, month = self.getYearMonth(conditionFrame, True)
        self.view.createCombobox(conditionFrame, getConditionValue("dateToDay"), 2, getDayTuple(year, month))
        self.view.getWidgetDic(conditionFrame, getConditionValue("dateToDay")).set(searchAction.getBeforeCondition(getConditionValue("dateToDay")))
        self.view.getWidgetDic(conditionFrame, getConditionValue("dateToYear")).bind('<<ComboboxSelected>>', lambda event: self.dateSet(event, conditionFrame, False))
        self.view.getWidgetDic(conditionFrame, getConditionValue("dateToMonth")).bind('<<ComboboxSelected>>', lambda event: self.dateSet(event, conditionFrame, False))

        #日付ボタン
        buttonFontSize = 11
        self.view.createButton(conditionFrame, getSearchAButtonName("yesteday"), lambda: self.dateYesterday(conditionFrame), buttonFontSize, '', getSearchAButtonName("yesteday").replace('カレンダー', ''))#前日
        self.view.createButton(conditionFrame, getSearchAButtonName("tomorrow"), lambda: self.dateTomorrow(conditionFrame), buttonFontSize, '', getSearchAButtonName("tomorrow").replace('カレンダー', ''))#翌日
        self.view.createButton(conditionFrame, getSearchAButtonName("clear"), lambda: self.dateClear(conditionFrame), buttonFontSize, '', getSearchAButtonName("clear").replace('カレンダー', ''))#クリア
        self.view.createButton(conditionFrame, getSearchAButtonName("toYear"), lambda: self.dateSetToYear(conditionFrame), buttonFontSize, '', getSearchAButtonName("toYear").replace('カレンダー', ''))#今年
        self.view.createButton(conditionFrame, getSearchAButtonName("toMonth"), lambda: self.dateSetToMonth(conditionFrame), buttonFontSize, '', getSearchAButtonName("toMonth").replace('カレンダー', ''))#今月
        self.view.createButton(conditionFrame, getSearchAButtonName("thisWeek"), lambda: self.dateSetThisWeek(conditionFrame), buttonFontSize, '', getSearchAButtonName("thisWeek").replace('カレンダー', ''))#今週
        self.view.createButton(conditionFrame, getSearchAButtonName("toDay"), lambda: self.dateSetToDay(conditionFrame), buttonFontSize, '', getSearchAButtonName("toDay").replace('カレンダー', ''))#今日
        self.view.createCombobox(conditionFrame, getItemName("year"), 4, getYearTuple(mySession.getUserId()))
        self.view.getWidgetDic(conditionFrame, getItemName("year")).set(self.dateDefaultSet("year"))
        self.view.createButton(conditionFrame, getSearchAButtonName("year"), lambda: self.dateSetYear(conditionFrame), buttonFontSize, '', getSearchAButtonName("year").replace('カレンダー', ''))#年
        self.view.createCombobox(conditionFrame, getItemName("month"), 2, getMonthTuple())
        self.view.getWidgetDic(conditionFrame, getItemName("month")).set(self.dateDefaultSet("month"))
        self.view.createButton(conditionFrame, getSearchAButtonName("month"), lambda: self.dateSetMonth(conditionFrame), buttonFontSize, '', getSearchAButtonName("month").replace('カレンダー', ''))#月

        #金額(最低)
        self.view.nameLabel(conditionFrame, getConditionValue("moneyMin"), True, "15", "normal", "lightskyblue", tk.RIDGE, 2, "MSゴシック", '金額')
        self.view.moneyEntory(conditionFrame, getConditionValue("moneyMin"))
        defaultMoneyMin = searchAction.getBeforeCondition(getConditionValue("moneyMin"))
        if defaultMoneyMin: defaultMoneyMin = str("{:,}".format(int(defaultMoneyMin)))
        self.view.getWidgetDic(conditionFrame, getConditionValue("moneyMin")).insert(0, defaultMoneyMin)
        self.view.setWidgetParam(conditionFrame, "column", self.view.getWidgetParam(conditionFrame, "column") - 1)
        self.view.myGrid(conditionFrame, getConditionValue("moneyMin"), False, 1, 3)

        #金額(最高)
        self.view.nameLabel(conditionFrame, getConditionValue("moneyMax"), False, "15", "normal", "lightskyblue", tk.RIDGE, 2, "MSゴシック", '～')
        self.view.moneyEntory(conditionFrame, getConditionValue("moneyMax"))
        defaultMoneyMax = searchAction.getBeforeCondition(getConditionValue("moneyMax"))
        if defaultMoneyMax: defaultMoneyMax = str("{:,}".format(int(defaultMoneyMax)))
        self.view.getWidgetDic(conditionFrame, getConditionValue("moneyMax")).insert(0, defaultMoneyMax)
        self.view.setWidgetParam(conditionFrame, "column", self.view.getWidgetParam(conditionFrame, "column") - 1)
        self.view.myGrid(conditionFrame, getConditionValue("moneyMax"), False, 1, 3)

        #キーワード1
        self.view.nameLabel(conditionFrame, getConditionValue("keyWord1"), True)
        self.view.createEntry(conditionFrame, getConditionValue("keyWord1")) 
        self.view.getWidgetDic(conditionFrame, getConditionValue("keyWord1")).insert(0, searchAction.getBeforeCondition(getConditionValue("keyWord1")))
        self.view.setWidgetParam(conditionFrame, "column", self.view.getWidgetParam(conditionFrame, "column") - 1)
        self.view.myGrid(conditionFrame, getConditionValue("keyWord1"), False, 1, 4)
        self.view.createCombobox(conditionFrame, getConditionValue("keyWord1not"), 3, getNotTuple()) #以外コンボボックス
        self.view.getWidgetDic(conditionFrame, getConditionValue("keyWord1not")).set(searchAction.getBeforeCondition(getConditionValue("keyWord1not")))
        self.view.createCombobox(conditionFrame, getConditionValue("keyWord1orAnd"), 4, getOrAndTuple()) #もしくは、かつコンボボックス
        self.view.getWidgetDic(conditionFrame, getConditionValue("keyWord1orAnd")).set(searchAction.getBeforeCondition(getConditionValue("keyWord1orAnd")))
        self.view.setWidgetParam(conditionFrame, "column", self.view.getWidgetParam(conditionFrame, "column") - 1)
        self.view.myGrid(conditionFrame, getConditionValue("keyWord1orAnd"), False, 1, 2)

        #キーワード2
        self.view.nameLabel(conditionFrame, getConditionValue("keyWord2"), True)
        self.view.createEntry(conditionFrame, getConditionValue("keyWord2"))
        self.view.getWidgetDic(conditionFrame, getConditionValue("keyWord2")).insert(0, searchAction.getBeforeCondition(getConditionValue("keyWord2")))
        self.view.setWidgetParam(conditionFrame, "column", self.view.getWidgetParam(conditionFrame, "column") - 1)
        self.view.myGrid(conditionFrame, getConditionValue("keyWord2"), False, 1, 4)
        self.view.createCombobox(conditionFrame, getConditionValue("keyWord2not"), 3, getNotTuple()) #以外コンボボックス
        self.view.getWidgetDic(conditionFrame, getConditionValue("keyWord2not")).set(searchAction.getBeforeCondition(getConditionValue("keyWord2not")))
        self.view.createCombobox(conditionFrame, getConditionValue("keyWord2orAnd"), 4, getOrAndTuple()) #もしくは、かつコンボボックス
        self.view.getWidgetDic(conditionFrame, getConditionValue("keyWord2orAnd")).set(searchAction.getBeforeCondition(getConditionValue("keyWord2orAnd")))
        self.view.setWidgetParam(conditionFrame, "column", self.view.getWidgetParam(conditionFrame, "column") - 1)
        self.view.myGrid(conditionFrame, getConditionValue("keyWord2orAnd"), False, 1, 2)

        #キーワード3
        self.view.nameLabel(conditionFrame, getConditionValue("keyWord3"), True)
        self.view.createEntry(conditionFrame, getConditionValue("keyWord3"))
        self.view.getWidgetDic(conditionFrame, getConditionValue("keyWord3")).insert(0, searchAction.getBeforeCondition(getConditionValue("keyWord3")))
        self.view.setWidgetParam(conditionFrame, "column", self.view.getWidgetParam(conditionFrame, "column") - 1)
        self.view.myGrid(conditionFrame, getConditionValue("keyWord3"), False, 1, 4)
        self.view.createCombobox(conditionFrame, getConditionValue("keyWord3not"), 3, getNotTuple()) #以外コンボボックス
        self.view.getWidgetDic(conditionFrame, getConditionValue("keyWord3not")).set(searchAction.getBeforeCondition(getConditionValue("keyWord3not")))

        #並び替え1
        self.view.nameLabel(conditionFrame, getConditionValue("sort1"), True)
        self.view.createCombobox(conditionFrame, getConditionValue("sort1"), 4, getSortValueTuple(True))
        self.view.getWidgetDic(conditionFrame, getConditionValue("sort1")).set(searchAction.getBeforeCondition(getConditionValue("sort1")))
        self.view.createCombobox(conditionFrame, getConditionValue("sort1AscDesc"), 4, getAscDescTuple()) #昇順、降順コンボボックス
        self.view.getWidgetDic(conditionFrame, getConditionValue("sort1AscDesc")).set(searchAction.getBeforeCondition(getConditionValue("sort1AscDesc")))
        self.view.setWidgetParam(conditionFrame, "column", self.view.getWidgetParam(conditionFrame, "column") - 1)
        self.view.myGrid(conditionFrame, getConditionValue("sort1AscDesc"), False, 1, 2)

        #並び替え2
        self.view.nameLabel(conditionFrame, getConditionValue("sort2"), True)
        self.view.createCombobox(conditionFrame, getConditionValue("sort2"), 4, getSortValueTuple(True))
        self.view.getWidgetDic(conditionFrame, getConditionValue("sort1")).set(searchAction.getBeforeCondition(getConditionValue("sort1")))
        self.view.createCombobox(conditionFrame, getConditionValue("sort2AscDesc"), 2, getAscDescTuple()) #昇順、降順コンボボックス
        self.view.getWidgetDic(conditionFrame, getConditionValue("sort2AscDesc")).set(searchAction.getBeforeCondition(getConditionValue("sort2AscDesc")))
        self.view.setWidgetParam(conditionFrame, "column", self.view.getWidgetParam(conditionFrame, "column") - 1)
        self.view.myGrid(conditionFrame, getConditionValue("sort2AscDesc"), False, 1, 2)

        #並び替え3
        self.view.nameLabel(conditionFrame, getConditionValue("sort3"), True)
        self.view.createCombobox(conditionFrame, getConditionValue("sort3"), 4, getSortValueTuple(True))
        self.view.getWidgetDic(conditionFrame, getConditionValue("sort3")).set(searchAction.getBeforeCondition(getConditionValue("sort3")))
        self.view.createCombobox(conditionFrame, getConditionValue("sort3AscDesc"), 2, getAscDescTuple()) #昇順、降順コンボボックス
        self.view.getWidgetDic(conditionFrame, getConditionValue("sort3AscDesc")).set(searchAction.getBeforeCondition(getConditionValue("sort3AscDesc")))
        self.view.setWidgetParam(conditionFrame, "column", self.view.getWidgetParam(conditionFrame, "column") - 1)
        self.view.myGrid(conditionFrame, getConditionValue("sort3AscDesc"), False, 1, 2)

        #ドラフト
        self.view.createCheckButton(conditionFrame, getConditionValue("draft"), False, False, 13)
        self.view.setCheck(conditionFrame, getConditionValue("draft"), searchAction.getBeforeCondition(getConditionValue("draft")))

        #ボタン部
        buttonFontSize = 15
        buttonFrame = "button"
        self.buttonFrame = buttonFrame
        self.view.createFrame(buttonFrame, searchViewA.mainFrame, 10, 291)
        #検索
        bindKey = 'g'
        self.view.createButton(buttonFrame, getButtonName("search"), self.preDoSearch, buttonFontSize, bindKey)
        self.view.root.bind("<Alt-" + bindKey + ">", self.preDoSearchBind)
        #クリア
        bindKey = 'c'
        self.view.createButton(buttonFrame, getButtonName("clear"), self.doClear, buttonFontSize, bindKey)
        self.view.root.bind("<Alt-" + bindKey + ">", self.doClearBind)
        #新規登録
        bindKey = 'i'
        self.view.createButton(buttonFrame, getButtonName("newInset"), self.loadEditView, buttonFontSize, bindKey)
        self.view.root.bind("<Alt-" + bindKey + ">", self.loadEditViewBind)
        #検索条件保存
        bindKey = 'k'
        self.view.createButton(buttonFrame, getButtonName("conditionKeep"), self.loadConditionKeepPopupView, buttonFontSize, bindKey)
        self.view.root.bind("<Alt-" + bindKey + ">", self.loadConditionKeepPopupViewBind)
        #検索条件プルダウン
        self.view.createCombobox(buttonFrame, getConditionKeepPopupViewItemName("conditionName"), 20, getConditionReflectValueTuple(), "readonly", 20)
        #検索条件反映
        bindKey = 'r'
        self.view.createButton(buttonFrame, getButtonName("reflect"), self.conditionReflect, buttonFontSize, bindKey)
        self.view.root.bind("<Alt-" + bindKey + ">", self.conditionReflectBind)

        #明細ヘッダー
        detaiHeaderFrame = "detailHearder"
        self.detaiHeaderFrame = detaiHeaderFrame
        self.view.createFrame(detaiHeaderFrame, searchViewA.mainFrame, 50, 330)
        fontSize = 15
        
        #該当件数
        self.view.nameLabel(detaiHeaderFrame, getDetailItemValue("hitCount"), False, fontSize)
        self.view.readOnlyEntry(detaiHeaderFrame, getDetailItemValue("hitCount"), 5, fontSize)

        #収入合計
        self.view.nameLabel(detaiHeaderFrame, getDetailItemValue("imcomeSum"), False, fontSize)
        self.view.readOnlyEntry(detaiHeaderFrame, getDetailItemValue("imcomeSum"), 10, fontSize, "right")

        #支出合計
        self.view.nameLabel(detaiHeaderFrame, getDetailItemValue("expenditureSum"), False, fontSize)
        self.view.readOnlyEntry(detaiHeaderFrame, getDetailItemValue("expenditureSum"), 10, fontSize, "right")

        #差額(入-出)
        self.view.nameLabel(detaiHeaderFrame, getDetailItemValue("diff"), False, fontSize)
        self.view.readOnlyEntry(detaiHeaderFrame, getDetailItemValue("diff"), 10, fontSize, "right")

        #明細部
        detailFrame = "detail"
        self.detailFrame = detailFrame
        self.view.createFrame(detailFrame, searchViewA.mainFrame, 50, 360)
        self.view.createTree(detailFrame, "tree", True)
        self.createDetail(self.view.getWidgetDic(detailFrame, "tree"))

        #比率計算部
        ratioCalcFrame = "ratioCalc"
        self.ratioCalcFrame = ratioCalcFrame
        self.view.createFrame(ratioCalcFrame, searchViewA.mainFrame, 580, 360)
        ratioItemFontSize = 15
        
        self.view.createButton(ratioCalcFrame, getSearchAButtonName("ratioCalc"), self.doRatioCalc, 15, '', '', True)
        self.view.nameLabel(ratioCalcFrame, getRatioItemName("keyword1"), True)
        self.view.createEntry(ratioCalcFrame, getRatioItemName("keyword1"))
        self.view.getWidgetDic(ratioCalcFrame, getRatioItemName("keyword1")).insert(0, searchAction.getBeforeCondition(getRatioItemName("keyword1")))
        self.view.nameLabel(ratioCalcFrame, getRatioItemName("sum"), True)
        self.view.readOnlyEntry(ratioCalcFrame, getRatioItemName("sum"), 20, ratioItemFontSize, "right")
        self.view.nameLabel(ratioCalcFrame, getRatioItemName("ratio"), True)
        self.view.readOnlyEntry(ratioCalcFrame, getRatioItemName("ratio"), 20, ratioItemFontSize, "right")

    #明細部作成
    def createDetail(self, tree):
        detailTuple = tuple(getDetailAll().keys())
        tree["columns"] = detailTuple
        tree["show"] = "headings"
        tree["displaycolumns"] = (
            detailTuple[1], #日付
            detailTuple[2], #店舗・用途
            detailTuple[3], #金額
            detailTuple[5]) #収支
        #各列の幅を指定
        tree.column(getDetailKey('日付'), width=140, anchor=tk.CENTER)
        tree.column(getDetailKey('店舗・用途'), width=200, anchor=tk.W)
        tree.column(getDetailKey('金額'), width=110, anchor=tk.E)
        tree.column(getDetailKey('収支'), width=50, anchor=tk.CENTER)
        #項目名を指定
        tree.heading(getDetailKey('日付'), text=getDetailValue("date"))
        tree.heading(getDetailKey('店舗・用途'), text=getDetailValue("store"))
        tree.heading(getDetailKey('金額'), text=getDetailValue("money"))
        tree.heading(getDetailKey('収支'), text=getDetailValue("imcomeExpenditure"))
        tree.bind("<<TreeviewSelect>>", self.preViewEditBind)

    def editDetail(self, resultSet):
        #明細ヘッダー編集
        #編集可能にする
        self.view.getWidgetDic(self.detaiHeaderFrame, getDetailItemValue("hitCount")).configure(state = "normal")
        self.view.getWidgetDic(self.detaiHeaderFrame, getDetailItemValue("imcomeSum")).configure(state = "normal")
        self.view.getWidgetDic(self.detaiHeaderFrame, getDetailItemValue("expenditureSum")).configure(state = "normal")
        self.view.getWidgetDic(self.detaiHeaderFrame, getDetailItemValue("diff")).configure(state = "normal")

        self.view.getWidgetDic(self.detaiHeaderFrame, getDetailItemValue("hitCount")).delete(0, tk.END)
        self.view.getWidgetDic(self.detaiHeaderFrame, getDetailItemValue("imcomeSum")).delete(0, tk.END)
        self.view.getWidgetDic(self.detaiHeaderFrame, getDetailItemValue("expenditureSum")).delete(0, tk.END)
        self.view.getWidgetDic(self.detaiHeaderFrame, getDetailItemValue("diff")).delete(0, tk.END)
        
        self.view.getWidgetDic(self.detaiHeaderFrame, getDetailItemValue("hitCount")).insert(0, resultSet["count"])
        self.view.getWidgetDic(self.detaiHeaderFrame, getDetailItemValue("imcomeSum")).insert(0, "\\" +str("{:,}".format(resultSet["imcomeSum"])))
        self.view.getWidgetDic(self.detaiHeaderFrame, getDetailItemValue("expenditureSum")).insert(0, "\\" + str("{:,}".format(resultSet["expenditureSum"])))
        self.view.getWidgetDic(self.detaiHeaderFrame, getDetailItemValue("diff")).insert(0, "\\" + str("{:,}".format(resultSet["imcomeSum"] - resultSet["expenditureSum"])))

        #編集不可にする
        self.view.getWidgetDic(self.detaiHeaderFrame, getDetailItemValue("hitCount")).configure(state = "readonly")
        self.view.getWidgetDic(self.detaiHeaderFrame, getDetailItemValue("imcomeSum")).configure(state = "readonly")
        self.view.getWidgetDic(self.detaiHeaderFrame, getDetailItemValue("expenditureSum")).configure(state = "readonly")
        self.view.getWidgetDic(self.detaiHeaderFrame, getDetailItemValue("diff")).configure(state = "readonly")

        #明細編集
        tree = self.view.getWidgetDic(self.detailFrame, "tree")
        for i in tree.get_children():
            tree.delete(i)
        
        for record in resultSet["list"]:
            tree.insert("", "end", values=(
                record[1] if record[1] != None else "", #ID 非表示
                myDate.getDateWithSlash(record[2]) + myDate.getDay(record[2]) if record[2] != None else "", #日付
                record[3] if record[3] != None else "", #店舗・用途
                "\\" + str("{:,}".format(record[4])) if record[4] != None else "", #金額
                record[5] if record[5] != None else "", #備考 非表示
                self.imcomeExpenditureDic[str(record[6])] if record[6] != None else "", #入・出
                record[7] if record[7] != None else "", #ドラフト 非表示
                ),
                tags=record[6]
            )
            tree.tag_configure(0, background='deepskyblue')

    def detailEdit(self):
        return
    
    #検索条件反映　バインド用
    def conditionReflectBind(self, event):
        self.conditionReflect()

    #検索条件反映
    def conditionReflect(self):
        #チェック処理
        Error.errorReset()

         #検索名プルダウン
        Error.validateRequired(self.view.getWidgetDic(self.buttonFrame, getConditionKeepPopupViewItemName("conditionName")), getConditionKeepPopupViewItemName("conditionName") + "プルダウン")

        if Error.isError():
            Error.showError()
            return

        #存在チェック
        whereSetList = [
            {
                "columun": 'conditionName',
                "value": self.view.getWidgetDic(self.buttonFrame, getConditionKeepPopupViewItemName("conditionName")).get(),
                "where": 'conditionName = :conditionName',
            }
        ]
        Error.isExist(conditionKeepPopupAction.getMainTable(), whereSetList)

        if Error.isError():
            Error.showError()
            return

        conditionName = self.view.getWidgetDic(self.buttonFrame, getConditionKeepPopupViewItemName("conditionName")).get()
        self.doClear()
        #日付（開始）
        self.view.getWidgetDic(self.conditionFrame, getConditionValue("dateFromYear")).set(searchAction.getKeepCondition(conditionName, getConditionValue("dateFromYear")))
        self.view.getWidgetDic(self.conditionFrame, getConditionValue("dateFromMonth")).set(searchAction.getKeepCondition(conditionName, getConditionValue("dateFromMonth")))
        self.view.getWidgetDic(self.conditionFrame, getConditionValue("dateFromDay")).set(searchAction.getKeepCondition(conditionName, getConditionValue("dateFromDay")))
        #日付（終了）
        self.view.getWidgetDic(self.conditionFrame, getConditionValue("dateToYear")).set(searchAction.getKeepCondition(conditionName, getConditionValue("dateToYear")))
        self.view.getWidgetDic(self.conditionFrame, getConditionValue("dateToMonth")).set(searchAction.getKeepCondition(conditionName, getConditionValue("dateToMonth")))
        self.view.getWidgetDic(self.conditionFrame, getConditionValue("dateToDay")).set(searchAction.getKeepCondition(conditionName, getConditionValue("dateToDay")))
        #金額(最低)
        defaultMoneyMin = searchAction.getBeforeCondition(getConditionValue("moneyMin"))
        if defaultMoneyMin: defaultMoneyMin = str("{:,}".format(int(defaultMoneyMin)))
        self.view.getWidgetDic(self.conditionFrame, getConditionValue("moneyMin")).insert(0, defaultMoneyMin)
        #金額(最高)
        defaultMoneyMax = searchAction.getBeforeCondition(getConditionValue("moneyMax"))
        if defaultMoneyMax: defaultMoneyMax = str("{:,}".format(int(defaultMoneyMax)))
        self.view.getWidgetDic(self.conditionFrame, getConditionValue("moneyMax")).insert(0, defaultMoneyMax)
        #キーワード1
        self.view.getWidgetDic(self.conditionFrame, getConditionValue("keyWord1")).insert(0, searchAction.getKeepCondition(conditionName, getConditionValue("keyWord1")))
        self.view.getWidgetDic(self.conditionFrame, getConditionValue("keyWord1not")).set(searchAction.getKeepCondition(conditionName, getConditionValue("keyWord1not")))
        self.view.getWidgetDic(self.conditionFrame, getConditionValue("keyWord1orAnd")).set(searchAction.getKeepCondition(conditionName, getConditionValue("keyWord1orAnd")))        
        #キーワード2
        self.view.getWidgetDic(self.conditionFrame, getConditionValue("keyWord2")).insert(0, searchAction.getKeepCondition(conditionName, getConditionValue("keyWord2")))
        self.view.getWidgetDic(self.conditionFrame, getConditionValue("keyWord2not")).set(searchAction.getKeepCondition(conditionName, getConditionValue("keyWord2not")))
        self.view.getWidgetDic(self.conditionFrame, getConditionValue("keyWord2orAnd")).set(searchAction.getKeepCondition(conditionName, getConditionValue("keyWord2orAnd")))
        #キーワード3
        self.view.getWidgetDic(self.conditionFrame, getConditionValue("keyWord3")).insert(0, searchAction.getKeepCondition(conditionName, getConditionValue("keyWord3")))
        self.view.getWidgetDic(self.conditionFrame, getConditionValue("keyWord3not")).set(searchAction.getKeepCondition(conditionName, getConditionValue("keyWord3not")))
        #並び替え1
        self.view.getWidgetDic(self.conditionFrame, getConditionValue("sort1")).set(searchAction.getKeepCondition(conditionName, getConditionValue("sort1")))
        self.view.getWidgetDic(self.conditionFrame, getConditionValue("sort1AscDesc")).set(searchAction.getKeepCondition(conditionName, getConditionValue("sort1AscDesc")))
        #並び替え2
        self.view.getWidgetDic(self.conditionFrame, getConditionValue("sort2")).set(searchAction.getKeepCondition(conditionName, getConditionValue("sort2")))
        self.view.getWidgetDic(self.conditionFrame, getConditionValue("sort2AscDesc")).set(searchAction.getKeepCondition(conditionName, getConditionValue("sort2AscDesc")))
        #並び替え3
        self.view.getWidgetDic(self.conditionFrame, getConditionValue("sort3")).set(searchAction.getKeepCondition(conditionName, getConditionValue("sort3")))
        self.view.getWidgetDic(self.conditionFrame, getConditionValue("sort3AscDesc")).set(searchAction.getKeepCondition(conditionName, getConditionValue("sort3AscDesc")))
        #ドラフト
        self.view.setCheck(self.conditionFrame, getConditionValue("draft"), searchAction.getKeepCondition(conditionName, getConditionValue("draft")))

        messagebox.showinfo('メッセージ', getMessage("msg-008"))
    
    #プルダウン一括更新
    def pulldownUpdate(self):
        if searchViewA.pulldownUpdateFlg:
            searchViewA.pulldownUpdateFlg = False
            yearTuple = getYearTuple(mySession.getUserId())
            #年(開始)プルダウン
            self.view.getWidgetDic(self.conditionFrame, getConditionValue("dateFromYear")).config(values = yearTuple)
            #年(終了))プルダウン
            self.view.getWidgetDic(self.conditionFrame, getConditionValue("dateToYear")).config(values = yearTuple)

            #設定年プルダウン
            self.view.getWidgetDic(self.conditionFrame, getItemName("year")).config(values = yearTuple)

            #検索条件名プルダウン
            self.view.getWidgetDic(self.buttonFrame, getConditionKeepPopupViewItemName("conditionName")).config(values = getConditionReflectValueTuple())
    
    #選択中の年、月を取得
    def getYearMonth(self, conditionFrame, FromToFlg):
        year = ''
        month = ''
        if FromToFlg:
            year = self.view.getWidgetDic(conditionFrame, getConditionValue("dateFromYear")).get()
            month = self.view.getWidgetDic(conditionFrame, getConditionValue("dateFromMonth")).get()
        else:
            year = self.view.getWidgetDic(conditionFrame, getConditionValue("dateToYear")).get()
            month = self.view.getWidgetDic(conditionFrame, getConditionValue("dateToMonth")).get()
        
        return year, month

    #日プルダウン更新
    def dateSet(self, event, conditionFrame, FromToFlg):
        year, month = self.getYearMonth(conditionFrame, FromToFlg)
        if FromToFlg:
            self.view.getWidgetDic(conditionFrame, getConditionValue("dateFromDay")).config(values = getDayTuple(year, month))
        else:
            self.view.getWidgetDic(conditionFrame, getConditionValue("dateToDay")).config(values = getDayTuple(year, month))

    #日付　前日(画面の値から前日)
    def dateYesterday(self, conditionFrame):
        fromDate = {}
        fromDate["year"] = self.view.getWidgetDic(conditionFrame, getConditionValue("dateFromYear")).get()
        fromDate["month"] = self.view.getWidgetDic(conditionFrame, getConditionValue("dateFromMonth")).get()
        fromDate["day"] = self.view.getWidgetDic(conditionFrame, getConditionValue("dateFromDay")).get()

        toDate = {}
        toDate["year"] = self.view.getWidgetDic(conditionFrame, getConditionValue("dateToYear")).get()
        toDate["month"] = self.view.getWidgetDic(conditionFrame, getConditionValue("dateToMonth")).get()
        toDate["day"] = self.view.getWidgetDic(conditionFrame, getConditionValue("dateToDay")).get()
        myDate.dateYesterdayPulldown(fromDate)
        myDate.dateYesterdayPulldown(toDate)

        self.view.getWidgetDic(conditionFrame, getConditionValue("dateFromYear")).set(fromDate["year"])
        self.view.getWidgetDic(conditionFrame, getConditionValue("dateFromMonth")).set(fromDate["month"])
        self.view.getWidgetDic(conditionFrame, getConditionValue("dateFromDay")).set(fromDate["day"])
        self.view.getWidgetDic(conditionFrame, getConditionValue("dateToYear")).set(toDate["year"])
        self.view.getWidgetDic(conditionFrame, getConditionValue("dateToMonth")).set(toDate["month"])
        self.view.getWidgetDic(conditionFrame, getConditionValue("dateToDay")).set(toDate["day"])
    
    #日付　翌日(画面の値から翌日)
    def dateTomorrow(self, conditionFrame):
        fromDate = {}
        fromDate["year"] = self.view.getWidgetDic(conditionFrame, getConditionValue("dateFromYear")).get()
        fromDate["month"] = self.view.getWidgetDic(conditionFrame, getConditionValue("dateFromMonth")).get()
        fromDate["day"] = self.view.getWidgetDic(conditionFrame, getConditionValue("dateFromDay")).get()

        toDate = {}
        toDate["year"] = self.view.getWidgetDic(conditionFrame, getConditionValue("dateToYear")).get()
        toDate["month"] = self.view.getWidgetDic(conditionFrame, getConditionValue("dateToMonth")).get()
        toDate["day"] = self.view.getWidgetDic(conditionFrame, getConditionValue("dateToDay")).get()
        myDate.dateTomorrowPulldown(fromDate)
        myDate.dateTomorrowPulldown(toDate)

        self.view.getWidgetDic(conditionFrame, getConditionValue("dateFromYear")).set(fromDate["year"])
        self.view.getWidgetDic(conditionFrame, getConditionValue("dateFromMonth")).set(fromDate["month"])
        self.view.getWidgetDic(conditionFrame, getConditionValue("dateFromDay")).set(fromDate["day"])
        self.view.getWidgetDic(conditionFrame, getConditionValue("dateToYear")).set(toDate["year"])
        self.view.getWidgetDic(conditionFrame, getConditionValue("dateToMonth")).set(toDate["month"])
        self.view.getWidgetDic(conditionFrame, getConditionValue("dateToDay")).set(toDate["day"])
    
    #日付クリア
    def dateClear(self, conditionFrame):
        self.view.getWidgetDic(conditionFrame, getConditionValue("dateFromYear")).set('')
        self.view.getWidgetDic(conditionFrame, getConditionValue("dateFromMonth")).set('')
        self.view.getWidgetDic(conditionFrame, getConditionValue("dateFromDay")).set('')
        self.view.getWidgetDic(conditionFrame, getConditionValue("dateToYear")).set('')
        self.view.getWidgetDic(conditionFrame, getConditionValue("dateToMonth")).set('')
        self.view.getWidgetDic(conditionFrame, getConditionValue("dateToDay")).set('')
    
    #日付　今年自動入力
    def dateSetToYear(self, conditionFrame):
        self.view.getWidgetDic(conditionFrame, getConditionValue("dateFromYear")).set(myDate.getToday("year"))
        self.view.getWidgetDic(conditionFrame, getConditionValue("dateFromMonth")).set('01')
        self.view.getWidgetDic(conditionFrame, getConditionValue("dateFromDay")).set('01')
        self.view.getWidgetDic(conditionFrame, getConditionValue("dateToYear")).set(myDate.getToday("year"))
        self.view.getWidgetDic(conditionFrame, getConditionValue("dateToMonth")).set('12')
        self.view.getWidgetDic(conditionFrame, getConditionValue("dateToDay")).set('31')
    
    #日付　今月自動入力
    def dateSetToMonth(self, conditionFrame):
        self.view.getWidgetDic(conditionFrame, getConditionValue("dateFromYear")).set(myDate.getToday("year"))
        self.view.getWidgetDic(conditionFrame, getConditionValue("dateFromMonth")).set(myDate.getToday("month"))
        self.view.getWidgetDic(conditionFrame, getConditionValue("dateFromDay")).set(myDate.getToday("fistDay"))
        self.view.getWidgetDic(conditionFrame, getConditionValue("dateToYear")).set(myDate.getToday("year"))
        self.view.getWidgetDic(conditionFrame, getConditionValue("dateToMonth")).set(myDate.getToday("month"))
        self.view.getWidgetDic(conditionFrame, getConditionValue("dateToDay")).set(myDate.getToday("lastDay"))
    
    #日付　今週自動入力
    def dateSetThisWeek(self, conditionFrame): 
        today = myDate.getToday("year") + "-" + myDate.getToday("month") + "-" + myDate.getToday("day") #今日の日付を取得
        dayOfWeek = myDate.getDay(today) #今日の曜日を取得
        #今週の月曜日の日付を計算
        while dayOfWeek != '(月)':
            today = myDate.dateYesterdayText(today).replace("/","-") #日付を翌日にする
            dayOfWeek = myDate.getDay(today) #曜日を取得する
        
        #今週の月曜日の日付を描画
        year = today[0:4]
        month = today[5:7]
        day = today[8:10]
        self.view.getWidgetDic(conditionFrame, getConditionValue("dateFromYear")).set(year)
        self.view.getWidgetDic(conditionFrame, getConditionValue("dateFromMonth")).set(month)
        self.view.getWidgetDic(conditionFrame, getConditionValue("dateFromDay")).set(day)

        today = myDate.getToday("year") + "-" + myDate.getToday("month") + "-" + myDate.getToday("day") #今日の日付を取得
        dayOfWeek = myDate.getDay(today) #今日の曜日を取得
        #今週の月曜日の日付を計算
        while dayOfWeek != '(日)':
            today = myDate.dateTomorrowText(today).replace("/","-") #日付を翌日にする
            dayOfWeek = myDate.getDay(today) #曜日を取得する

        #今週の日曜日の日付を描画
        year = today[0:4]
        month = today[5:7]
        day = today[8:10]
        self.view.getWidgetDic(conditionFrame, getConditionValue("dateToYear")).set(year)
        self.view.getWidgetDic(conditionFrame, getConditionValue("dateToMonth")).set(month)
        self.view.getWidgetDic(conditionFrame, getConditionValue("dateToDay")).set(day)
    
    #日付　今日自動入力
    def dateSetToDay(self, conditionFrame):
        self.view.getWidgetDic(conditionFrame, getConditionValue("dateFromYear")).set(myDate.getToday("year"))
        self.view.getWidgetDic(conditionFrame, getConditionValue("dateFromMonth")).set(myDate.getToday("month"))
        self.view.getWidgetDic(conditionFrame, getConditionValue("dateFromDay")).set(myDate.getToday("day"))
        self.view.getWidgetDic(conditionFrame, getConditionValue("dateToYear")).set(myDate.getToday("year"))
        self.view.getWidgetDic(conditionFrame, getConditionValue("dateToMonth")).set(myDate.getToday("month"))
        self.view.getWidgetDic(conditionFrame, getConditionValue("dateToDay")).set(myDate.getToday("day"))

    #日付　指定年自動入力
    def dateSetYear(self, conditionFrame):
        year = self.view.getWidgetDic(conditionFrame, getItemName("year")).get()
        if year == '': return
        self.view.getWidgetDic(conditionFrame, getConditionValue("dateFromYear")).set(year)
        self.view.getWidgetDic(conditionFrame, getConditionValue("dateFromMonth")).set('01')
        self.view.getWidgetDic(conditionFrame, getConditionValue("dateFromDay")).set('01')
        self.view.getWidgetDic(conditionFrame, getConditionValue("dateToYear")).set(year)
        self.view.getWidgetDic(conditionFrame, getConditionValue("dateToMonth")).set('12')
        self.view.getWidgetDic(conditionFrame, getConditionValue("dateToDay")).set('31')
    
    #日付　指定月自動入力
    def dateSetMonth(self, conditionFrame):
        year = self.view.getWidgetDic(conditionFrame, getConditionValue("dateToYear")).get()
        month = self.view.getWidgetDic(conditionFrame, getItemName("month")).get()
        if month == '': return
        self.view.getWidgetDic(conditionFrame, getConditionValue("dateFromMonth")).set(month)
        self.view.getWidgetDic(conditionFrame, getConditionValue("dateFromDay")).set('01')
        self.view.getWidgetDic(conditionFrame, getConditionValue("dateToMonth")).set(month)
        self.view.getWidgetDic(conditionFrame, getConditionValue("dateToDay")).set(myDate.getSelectLastDay(year, month))

    #日付　先月の年か月を返す
    def dateDefaultSet(self, setDate):
        setDay = {}
        
        if myDate.getToday("month") == "01":
            setDay["year"] = str(int(myDate.getToday("year")) - 1)
            setDay["month"] = "12"
        else:
            setDay["year"] = myDate.getToday("year")
            setDay["month"] = str(int(myDate.getToday("month")) - 1)
        
        #一桁月の場合は先頭0埋め処理
        if (len(setDay["month"]) == 1):
            setDay["month"] = '0' + setDay["month"]
        
        return setDay[setDate]
    
    #比率計算
    def doRatioCalc(self):
        keyword = self.view.getWidgetDic(self.ratioCalcFrame, getRatioItemName("keyword1")).get()
        immcome = self.nowDitailSet["imcomeSum"]
        if keyword == "":
            messagebox.showerror('エラーメッセージ', getErrorMessage("er-003"))
            return
        
        if immcome == 0:
            messagebox.showerror('エラーメッセージ', getErrorMessage("er-004"))
            return
        
        params = params = self.getParams()
        searchAction.doConditionSave(params)
        ratioSum = 0
        for detailRecord in self.nowDitailSet["list"]:
            store = detailRecord[3]
            money = detailRecord[4]
            remarks = detailRecord[5]
            immcomeExpenditureFlg = detailRecord[6]
            #明細内キーワード検索
            if immcomeExpenditureFlg and ((keyword in str(store)) or (keyword in str(remarks))):
                ratioSum += money
        
        ratio = (ratioSum / immcome) * 100

        self.view.getWidgetDic(self.ratioCalcFrame, getRatioItemName("sum")).configure(state = "normal")
        self.view.getWidgetDic(self.ratioCalcFrame, getRatioItemName("ratio")).configure(state = "normal")

        self.view.getWidgetDic(self.ratioCalcFrame, getRatioItemName("sum")).delete(0, tk.END)
        self.view.getWidgetDic(self.ratioCalcFrame, getRatioItemName("ratio")).delete(0, tk.END)
        self.view.getWidgetDic(self.ratioCalcFrame, getRatioItemName("sum")).insert(0, "\\" +str("{:,}".format(ratioSum)))
        self.view.getWidgetDic(self.ratioCalcFrame, getRatioItemName("ratio")).insert(0, str(ratio) + "%")

        self.view.getWidgetDic(self.ratioCalcFrame, getRatioItemName("sum")).configure(state = "readonly")
        self.view.getWidgetDic(self.ratioCalcFrame, getRatioItemName("ratio")).configure(state = "readonly")
        return
    
    #検索画面エントリー取得
    def getSearchEntry(self):
        return {
            "moneyMin": self.view.getWidgetDic(self.conditionFrame, getConditionValue("moneyMin")),
            "moneyMax": self.view.getWidgetDic(self.conditionFrame, getConditionValue("moneyMax")),
            "keyWord1": self.view.getWidgetDic(self.conditionFrame, getConditionValue("keyWord1")),
            "keyWord2": self.view.getWidgetDic(self.conditionFrame, getConditionValue("keyWord2")),
            "keyWord3": self.view.getWidgetDic(self.conditionFrame, getConditionValue("keyWord3"))
        }
    
    #検索画面コンボボックス取得
    def getSearchCombobox(self):
        return {
            "dateFromYear": self.view.getWidgetDic(self.conditionFrame, getConditionValue("dateFromYear")),
            "dateFromMonth": self.view.getWidgetDic(self.conditionFrame, getConditionValue("dateFromMonth")),
            "dateFromDay": self.view.getWidgetDic(self.conditionFrame, getConditionValue("dateFromDay")),
            "dateToYear": self.view.getWidgetDic(self.conditionFrame, getConditionValue("dateToYear")),
            "dateToMonth": self.view.getWidgetDic(self.conditionFrame, getConditionValue("dateToMonth")),
            "dateToDay": self.view.getWidgetDic(self.conditionFrame, getConditionValue("dateToDay")),
            "keyWord1not": self.view.getWidgetDic(self.conditionFrame, getConditionValue("keyWord1not")),
            "keyWord1orAnd": self.view.getWidgetDic(self.conditionFrame, getConditionValue("keyWord1orAnd")),
            "keyWord2not": self.view.getWidgetDic(self.conditionFrame, getConditionValue("keyWord2not")),
            "keyWord2orAnd": self.view.getWidgetDic(self.conditionFrame, getConditionValue("keyWord2orAnd")),
            "keyWord3not": self.view.getWidgetDic(self.conditionFrame, getConditionValue("keyWord3not")),
            "sort1": self.view.getWidgetDic(self.conditionFrame, getConditionValue("sort1")),
            "sort1AscDesc": self.view.getWidgetDic(self.conditionFrame, getConditionValue("sort1AscDesc")),
            "sort2": self.view.getWidgetDic(self.conditionFrame, getConditionValue("sort2")),
            "sort2AscDesc": self.view.getWidgetDic(self.conditionFrame, getConditionValue("sort2AscDesc")),
            "sort3": self.view.getWidgetDic(self.conditionFrame, getConditionValue("sort3")),
            "sort3AscDesc": self.view.getWidgetDic(self.conditionFrame, getConditionValue("sort3AscDesc"))
        }
    
    #明細部ヘッダー
    def getDetailEntry(self):
        return {
            "hitCount": self.view.getWidgetDic(self.detaiHeaderFrame, getDetailItemValue("hitCount")),
            "imcomeSum": self.view.getWidgetDic(self.detaiHeaderFrame, getDetailItemValue("imcomeSum")),
            "expenditureSum": self.view.getWidgetDic(self.detaiHeaderFrame, getDetailItemValue("expenditureSum")),
            "diff": self.view.getWidgetDic(self.detaiHeaderFrame, getDetailItemValue("diff"))
        }
    
    #比率計算部
    def getRatioCalcEntry(self):
        return {
            "calcKeyword1": self.view.getWidgetDic(self.ratioCalcFrame, getRatioItemName("keyword1"))
        }
    
    #パラメーター取得
    def getParams(self):
        params = {}

        searchCombobox = self.getSearchCombobox()
        for key in searchCombobox.keys():
            params[key] = searchCombobox[key]
        
        searchEntry = self.getSearchEntry()
        for key in searchEntry.keys():
            params[key] = searchEntry[key]
        
        ratioCalcEntry = self.getRatioCalcEntry()
        for key in ratioCalcEntry.keys():
            params[key] = ratioCalcEntry[key]

        params["draft"] = self.view.getCheckButton(self.conditionFrame, getConditionValue("draft"))

        return params

    #クリアボタン
    def doClearBind(self, event):
        self.doClear()
    
    #クリアボタン
    def doClear(self):
        #ボタン非活性
        self.view.getWidgetDic(self.ratioCalcFrame, getSearchAButtonName("ratioCalc"))['state'] = tk.DISABLED

        #検索部エントリー初期化
        searchEntry = self.getSearchEntry()
        for key in searchEntry.keys():
            searchEntry[key].delete(0, tk.END)
        
        #コンボボックス初期化
        searchCombobox = self.getSearchCombobox()
        for key in searchCombobox.keys():
            searchCombobox[key].set('')
        searchCombobox["keyWord1orAnd"].set(getOrAndTuple()[0])
        searchCombobox["keyWord2orAnd"].set(getOrAndTuple()[0])
        searchCombobox["sort1AscDesc"].set(getAscDescTuple()[0])
        searchCombobox["sort2AscDesc"].set(getAscDescTuple()[0])
        searchCombobox["sort3AscDesc"].set(getAscDescTuple()[0])

        #チェックボックス初期化
        self.view.setCheck(self.conditionFrame, getConditionValue("draft"), False)

        self.detailDoClear()
    
    #明細部クリア処理
    def detailDoClear(self):
        #エントリー初期化
        searchEntry = self.getDetailEntry()
        for key in searchEntry.keys():
            searchEntry[key].configure(state = "normal")
            searchEntry[key].delete(0, tk.END)
            searchEntry[key].configure(state = "readonly")
        
        #明細
        tree = self.view.getWidgetDic(self.detailFrame, "tree")
        for i in tree.get_children():
            tree.delete(i)

    #検索前処理 バインド用
    def preDoSearchBind(self, event):
        self.preDoSearch()
    
    #検索前処理
    def preDoSearch(self):
        params = self.getParams()
        searchAction.doConditionSave(params)
        resultSet = searchAction.doSearch(params)
        self.postDoSearch(resultSet)
    
    #検索後処理
    def postDoSearch(self, resultSet):
        self.nowDitailSet = resultSet
        self.imcomeExpenditureDic = getImcomeExpenditureDic()
        #比率計算部の合計、比率をクリア
        self.view.getWidgetDic(self.ratioCalcFrame, getRatioItemName("sum")).configure(state = "normal")
        self.view.getWidgetDic(self.ratioCalcFrame, getRatioItemName("ratio")).configure(state = "normal")
        self.view.getWidgetDic(self.ratioCalcFrame, getRatioItemName("sum")).delete(0, tk.END)
        self.view.getWidgetDic(self.ratioCalcFrame, getRatioItemName("ratio")).delete(0, tk.END)
        self.view.getWidgetDic(self.ratioCalcFrame, getRatioItemName("sum")).configure(state = "readonly")
        self.view.getWidgetDic(self.ratioCalcFrame, getRatioItemName("ratio")).configure(state = "readonly")
        if resultSet["count"]:
            self.view.getWidgetDic(self.ratioCalcFrame, getSearchAButtonName("ratioCalc"))['state'] = tk.NORMAL
            self.editDetail(resultSet)
        else:
            self.detailDoClear()
            self.view.getWidgetDic(self.ratioCalcFrame, getSearchAButtonName("ratioCalc"))['state'] = tk.DISABLED
            messagebox.showerror('エラーメッセージ', getErrorMessage("er-001"))
    
    #新規登録　バインド用
    def loadEditViewBind(self, event):
        self.loadEditView()
    
    #新規登録
    def  loadEditView(self):
        record = {
            "id": '',
            "date": myDate.getToday("date"),
            "store": '',
            "money": '',
            "remarks": '',
            "imcomeExpenditure": '支出',
            "draft": False
        }
        self.reSearchFlg = True
        searchViewA.pulldownUpdateFlg = True
        editView("insert", record)
    
    #編集画面
    def preViewEditBind(self, event):
        data = event.widget.item(event.widget.selection())['values']
        record = {
            "id": data[0],
            "date": data[1][:10],
            "store": data[2],
            "money": data[3].replace('\\',''),
            "remarks": data[4],
            "imcomeExpenditure": data[5],
            "draft": data[6]
        }
        self.reSearchFlg = True
        searchViewA.pulldownUpdateFlg = True
        editView("update", record)

    #検索条件保存画面　バインド用
    def loadConditionKeepPopupViewBind(self, event):
        self.loadConditionKeepPopupView
    
    #検索条件保存画面
    def loadConditionKeepPopupView(self):
        conditionParams = self.getParams()
        conditionName = self.view.getWidgetDic(self.buttonFrame, getConditionKeepPopupViewItemName("conditionName")).get()
        searchViewA.pulldownUpdateFlg = True
        conditionKeepPopupView(conditionName, conditionParams)
    
    #戻る処理
    def returnBind(self, event):
        self.view.getFrame(searchViewA.mainFrame).destroy()
    
    #自動再検索
    def reDoSearch(self, event):
        if self.reSearchFlg:
            self.reSearchFlg = False
            self.preDoSearch()
    
    #検索画面フォーカス時の処理
    def forcusInFunc(self, event):
        self.pulldownUpdate()
        self.reDoSearch(event)

def main():
    searchViewA()

if __name__ == "__main__":
    print("start pprogram")
    main()