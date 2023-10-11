from tkinter import messagebox

from myTkFrameWork.myTk import *
from myTkFrameWork.myConst import *
from myTkFrameWork.mySession import *
from myTkFrameWork.db.myDao import *
from myTkFrameWork.Error import *

from edit.editAction import *

class editView:
    view = None
    mainFrame = "edit"

    def __init__(self, mode, record = {}):
        self.record = record
        self.view = myTk(getEditTitle(), getEditWindowSetting(), "top", editView.mainFrame, True)

        #タイトル部
        self.view.createFrame("title", editView.mainFrame, 120, 0)
        self.view.titleLabel("title", getEditTitle())

        #ボタン部
        buttonFontSize = 15
        buttonFrame = "button"
        self.buttonFrame = buttonFrame
        self.view.createFrame(buttonFrame, editView.mainFrame, 20, 50)
        buttonDisableFlg = False
        buttonBackGroundColor = 'SystemButtonFace' #ボタンの基本背景色
        
        #検索モード(検索/更新切り替え)
        self.view.createCheckButton(buttonFrame, getButtonName("changeMode"), mode == "insert", False, 12, "登録モード", self.editModeChange)
        if mode == "insert": self.view.getWidgetDic(self.buttonFrame, getButtonName("changeMode"))['state'] = tk.DISABLED

        #登録
        insetButtonDisableFlg = not self.view.getCheck(self.buttonFrame, getButtonName("changeMode"))
        self.view.createButton(buttonFrame, getButtonName("insert"), self.preDoInsert, buttonFontSize, '', '', insetButtonDisableFlg)

        #更新ボタンの設定
        buttonDisableFlg = self.view.getCheck(self.buttonFrame, getButtonName("changeMode"))
        if not buttonDisableFlg: buttonBackGroundColor = getUpdateButtonBGColor()
        #更新
        self.view.createButton(buttonFrame, getButtonName("update"), self.preDoUpdate, buttonFontSize, '', '', buttonDisableFlg, buttonBackGroundColor)

        #削除ボタンの設定
        if not buttonDisableFlg: buttonBackGroundColor = getDeleteButtonBGColor()
        #削除
        self.view.createButton(buttonFrame, getButtonName("delete"), self.preDoDelete, buttonFontSize, '', '', buttonDisableFlg, buttonBackGroundColor)
        #クリア
        self.view.createButton(buttonFrame, getButtonName("clear"), self.preDoClear, buttonFontSize)

        #入力項目部
        itemFrame = "item"
        self.itemFrame = itemFrame
        self.view.createFrame(itemFrame, editView.mainFrame, 20, 100)

        #ドラフト
        self.view.createCheckButton(itemFrame, getDetailValue("draft"), False, False, 12)

        #日付ボタン
        self.view.createButton(itemFrame, getButtonName("yesterDay"), self.setYesterday, 11)
        self.view.createButton(itemFrame, getButtonName("toDay"), self.setToday, 11)
        self.view.createButton(itemFrame, getButtonName("tomorrow"), self.setTomorrow, 11)

        #日付
        self.view.nameLabel(itemFrame, getDetailValue("date"), True)
        self.view.dateEntry(itemFrame, getDetailValue("date"), 8, 15, 8)
        self.view.setWidgetParam(itemFrame, "column", self.view.getWidgetParam(itemFrame, "column") - 1)
        self.view.myGrid(itemFrame, getDetailValue("date"), False, 1, 3)

        #店舗・用途
        self.view.nameLabel(itemFrame, getDetailValue("store"), True)
        self.view.createEntry(itemFrame, getDetailValue("store"), "top", 30, 15, 30)
        self.view.setWidgetParam(itemFrame, "column", self.view.getWidgetParam(itemFrame, "column") - 1)
        self.view.myGrid(itemFrame, getDetailValue("store"), False, 1, 3)

        #金額
        self.view.nameLabel(itemFrame, getDetailValue("money"), True)
        self.view.moneyEntory(itemFrame, getDetailValue("money"))
        self.view.setWidgetParam(itemFrame, "column", self.view.getWidgetParam(itemFrame, "column") - 1)
        self.view.myGrid(itemFrame, getDetailValue("money"), False, 1, 3)


        #収入・支出
        self.view.nameLabel(itemFrame, getDetailValue("imcomeExpenditure"), True)
        self.view.createCombobox(itemFrame, getDetailValue("imcomeExpenditure"), 20, tuple(getImcomeExpenditureDic().values()))
        self.view.setWidgetParam(itemFrame, "column", self.view.getWidgetParam(itemFrame, "column") - 1)
        self.view.myGrid(itemFrame, getDetailValue("imcomeExpenditure"), False, 1, 3)

        #備考
        self.view.nameLabel(itemFrame, getDetailValue("remarks"), True)
        self.view.setWidgetParam(itemFrame, "column", self.view.getWidgetParam(itemFrame, "column") - 1)
        self.view.myGrid(itemFrame, getDetailValue("remarks"), False, 1, 4)
        self.view.createText(itemFrame, getDetailValue("remarks"), True, 20, 8, "15")
        self.view.setWidgetParam(itemFrame, "column", self.view.getWidgetParam(itemFrame, "column") - 1)
        self.view.myGrid(itemFrame, getDetailValue("remarks"), False, 1, 4)

        #初期表示
        self.preDoClear()

        self.view.top.mainloop()

    #入力項目取得
    def getItems(self):
        return {
            "id": self.record["id"],
            "draft": self.view.getCheckButton(self.itemFrame, getDetailValue("draft")),
            "date": self.view.getWidgetDic(self.itemFrame, getDetailValue("date")),
            "store": self.view.getWidgetDic(self.itemFrame, getDetailValue("store")),
            "money": self.view.getWidgetDic(self.itemFrame, getDetailValue("money")),
            "imcomeExpenditure": self.view.getWidgetDic(self.itemFrame, getDetailValue("imcomeExpenditure")),
            "remarks": self.view.getWidgetDic(self.itemFrame, getDetailValue("remarks"))
        }
    
    #日付(前日)ボタン
    def setYesterday(self):
        yesterdayStr = myDate.dateYesterdayText(self.view.getWidgetDic(self.itemFrame, getDetailValue("date")).get())
        self.view.getWidgetDic(self.itemFrame, getDetailValue("date")).delete(0, tk.END)
        self.view.getWidgetDic(self.itemFrame, getDetailValue("date")).insert(0, yesterdayStr)

    #日付(今日)ボタン
    def setToday(self):
        self.view.getWidgetDic(self.itemFrame, getDetailValue("date")).delete(0, tk.END)
        self.view.getWidgetDic(self.itemFrame, getDetailValue("date")).insert(0, myDate.getToday("date"))
    
    #日付(翌日)ボタン
    def setTomorrow(self):
        tomorrowStr = myDate.dateTomorrowText(self.view.getWidgetDic(self.itemFrame, getDetailValue("date")).get())
        self.view.getWidgetDic(self.itemFrame, getDetailValue("date")).delete(0, tk.END)
        self.view.getWidgetDic(self.itemFrame, getDetailValue("date")).insert(0, tomorrowStr)

    #登録モード切り替え
    def editModeChange(self, event):
        #登録モードチェックボックスが非活性の場合は処理しない
        if self.view.getWidgetDic(self.buttonFrame, getButtonName("changeMode"))['state'] == tk.DISABLED: return

        #登録者モードのチェックが切り替わる前に処理が入ってくるため、分岐条件のnotを使用している
        if not self.view.getCheck(self.buttonFrame, getButtonName("changeMode")):
            #登録ボタン活性化
            self.view.getWidgetDic(self.buttonFrame, getButtonName("insert"))['state'] = tk.NORMAL
            #更新ボタン非活性化
            self.view.getWidgetDic(self.buttonFrame, getButtonName("update"))['state'] = tk.DISABLED
            self.view.getWidgetDic(self.buttonFrame, getButtonName("update")).config(bg='#f5f5f5')
            #更新ボタン非活性化
            self.view.getWidgetDic(self.buttonFrame, getButtonName("delete"))['state'] = tk.DISABLED
            self.view.getWidgetDic(self.buttonFrame, getButtonName("delete")).config(bg='#f5f5f5')
        else:
            #登録ボタン非活性化
            self.view.getWidgetDic(self.buttonFrame, getButtonName("insert"))['state'] = tk.DISABLED
            #更新ボタン活性化
            self.view.getWidgetDic(self.buttonFrame, getButtonName("update"))['state'] = tk.NORMAL
            self.view.getWidgetDic(self.buttonFrame, getButtonName("update")).config(bg=getUpdateButtonBGColor())
            #削除ボタン活性化
            self.view.getWidgetDic(self.buttonFrame, getButtonName("delete"))['state'] = tk.NORMAL
            self.view.getWidgetDic(self.buttonFrame, getButtonName("delete")).config(bg=getDeleteButtonBGColor())
    
    #登録前処理
    def preDoInsert(self):
        params = self.getItems()

        #チェック処理
        Error.errorReset()

        #日付
        Error.validateRequired(params["date"], getDetailValue("date"))
        Error.validateDateCheck(params["date"], getDetailValue("date"))

        #店舗・用途
        Error.validateRequired(params["store"], getDetailValue("store"))

        #金額
        Error.validateRequired(params["money"], getDetailValue("money"))

        #備考
        Error.limitInput(params["remarks"].get("1.0", "end -1c"), getDetailValue("remarks"))

        if Error.isError():
            Error.showError()
            return

        self.view.getWidgetDic(self.buttonFrame, getButtonName("update"))['state'] = tk.DISABLED
        self.view.getWidgetDic(self.buttonFrame, getButtonName("delete"))['state'] = tk.DISABLED
        self.view.getWidgetDic(self.buttonFrame, getButtonName("changeMode"))['state'] = tk.DISABLED

        editAction.doInsert(params)
        self.postDoInsert()

    #登録後処理
    def postDoInsert(self):
        self.view.getWidgetDic(self.buttonFrame, getButtonName("update")).config(bg='#f5f5f5')
        self.view.getWidgetDic(self.buttonFrame, getButtonName("delete")).config(bg='#f5f5f5')
        if not messagebox.askyesno('確認', getMessage("msg-001") + "。\n" + getMessage("msg-005")):
            self.viewDelete()
        return
    
    #更新前処理
    def preDoUpdate(self):
        params = self.getItems()

        #チェック処理
        Error.errorReset()

        #日付
        Error.validateRequired(params["date"], getDetailValue("date"))
        Error.validateDateCheck(params["date"], getDetailValue("date"))

        #店舗・用途
        Error.validateRequired(params["store"], getDetailValue("store"))

        #金額
        Error.validateRequired(params["money"], getDetailValue("money"))

        #備考
        Error.limitInput(params["remarks"].get("1.0", "end -1c"), getDetailValue("remarks"))

        if Error.isError():
            Error.showError()
            return
        
        editAction.doUpdate(params)
        self.postDoUpdate()
    
    #更新後処理
    def postDoUpdate(self):
        messagebox.showinfo('メッセージ', getMessage("msg-002"))
        self.viewDelete()
    
    #削除前処理
    def preDoDelete(self):
        if messagebox.askyesno('確認', getMessage("msg-004")):
            editAction.doDelete(self.getItems())
            self.postDoDelete()
    
    #削除後処理
    def postDoDelete(self):
        messagebox.showinfo('メッセージ', getMessage("msg-003"))
        self.viewDelete()
    
    #初期表示・クリア処理
    def preDoClear(self):
        #ドラフト
        self.view.setCheck(self.itemFrame, getDetailValue("draft"), self.record["draft"])
        
        #日付
        self.view.getWidgetDic(self.itemFrame, getDetailValue("date")).delete(0, tk.END)
        self.view.getWidgetDic(self.itemFrame, getDetailValue("date")).insert(0, self.record["date"])
        
        #店舗・用途
        self.view.getWidgetDic(self.itemFrame, getDetailValue("store")).delete(0, tk.END)
        self.view.getWidgetDic(self.itemFrame, getDetailValue("store")).insert(0, self.record["store"])

        #金額
        self.view.getWidgetDic(self.itemFrame, getDetailValue("money")).delete(0, tk.END)
        self.view.getWidgetDic(self.itemFrame, getDetailValue("money")).insert(0, self.record["money"])

        #収入・支出
        self.view.getWidgetDic(self.itemFrame, getDetailValue("imcomeExpenditure")).set(self.record["imcomeExpenditure"])

        #備考
        self.view.getWidgetDic(self.itemFrame, getDetailValue("remarks")).delete("1.0", 'end')
        self.view.getWidgetDic(self.itemFrame, getDetailValue("remarks")).insert("1.0", self.record["remarks"])
    
    def viewDelete(self):
        self.view.top.destroy()