from tkinter import messagebox

from myTkFrameWork.myTk import *
from myTkFrameWork.myConst import *
from myTkFrameWork.mySession import *
from myTkFrameWork.db.myDao import *
from myTkFrameWork.Error import *

from conditionKeepPopup.conditionKeepPopupAction import *

class conditionKeepPopupView:
    view = None
    mainFrame = "keepPupup"
    keepConditionParams = {} #保存する検索条件

    #検索条件保存ポップアップ画面の項目名辞書
    itemNamedic = {"conditionName":"検索名"}
    
    def __init__(self, conditionName, conditionParams = {}):
        conditionKeepPopupView.keepConditionParams = conditionParams
        self.view = myTk(self.getConditionKeepPopupViewTitle(), getConditionKeepWindowSetting(), "top", conditionKeepPopupView.mainFrame, True)

        #タイトル部
        self.view.createFrame("title", conditionKeepPopupView.mainFrame, 55, 0)
        self.view.titleLabel("title", self.getConditionKeepPopupViewTitle())
    
        #入力項目部
        itemFrame = "item"
        self.itemFrame = itemFrame
        self.view.createFrame(itemFrame, conditionKeepPopupView.mainFrame, 90, 60)

        #検索名
        self.view.nameLabel(itemFrame, getConditionKeepPopupViewItemName("conditionName"), True)
        self.view.createEntry(itemFrame, getConditionKeepPopupViewItemName("conditionName"), "top", 20, 15, 20)
        if conditionName:
            self.view.getWidgetDic(itemFrame, getConditionKeepPopupViewItemName("conditionName")).insert(0, conditionName)
            self.view.getWidgetDic(itemFrame, getConditionKeepPopupViewItemName("conditionName")).configure(state = "readonly")

        #ボタン部
        buttonFontSize = 15
        buttonFrame = "button"
        self.buttonFrame = buttonFrame
        self.view.createFrame(buttonFrame, conditionKeepPopupView.mainFrame, 200, 90)
        buttonDisableFlg = False
        buttonBackGroundColor = 'SystemButtonFace' #ボタンの基本背景色

        #保存
        if conditionName: buttonDisableFlg = True
        self.view.createButton(buttonFrame, getButtonName("keep"), self.preDoSave, buttonFontSize, '', '', buttonDisableFlg)
        #更新
        if conditionName == '': 
            buttonDisableFlg = True
        else:
            buttonDisableFlg = False
        if conditionName: buttonBackGroundColor = 'deep sky blue'
        self.view.createButton(buttonFrame, getButtonName("update"), self.preDoUpdate, buttonFontSize, '', '', buttonDisableFlg, buttonBackGroundColor)
        #削除
        if conditionName == '': 
            buttonDisableFlg = True
        else:
            buttonDisableFlg = False
        if conditionName: buttonBackGroundColor = 'indian red'
        self.view.createButton(buttonFrame, getButtonName("delete"), self.preDoDelete, buttonFontSize, '', '', buttonDisableFlg, buttonBackGroundColor)

        self.view.top.mainloop()

    def getConditionKeepPopupViewTitle(self):
        return "検索条件保存画面"

    def preDoSave(self):
        params = conditionKeepPopupView.keepConditionParams
        params["conditionName"] = self.view.getWidgetDic(self.itemFrame, getConditionKeepPopupViewItemName("conditionName"))

        #チェック処理
        Error.errorReset()

        #検索名
        Error.validateRequired(params["conditionName"], getConditionKeepPopupViewItemName("conditionName"))

        if Error.isError():
            Error.showError()
            return
        
        #重複チェック
        whereSetList = [
            {
                "columun": 'conditionName',
                "value": params["conditionName"].get(),
                "where": 'conditionName = :conditionName',
            }
        ]
        Error.doubleCheck(conditionKeepPopupAction.getMainTable(), whereSetList)

        if Error.isError():
            Error.showError()
            return

        conditionKeepPopupAction.doSave(params)
        self.postDoSave()
    
    def postDoSave(self):
        messagebox.showinfo('メッセージ', getMessage("msg-006"))
        self.viewDelete()
    
    def preDoDelete(self):
        if messagebox.askyesno('確認', getMessage("msg-004")):
            conditionName = self.view.getWidgetDic(self.itemFrame, getConditionKeepPopupViewItemName("conditionName")).get()
            conditionKeepPopupAction.doDelete(conditionName)
            self.postDoDelete()
    
    def postDoDelete(self):
        messagebox.showinfo('メッセージ', getMessage("msg-003"))
        self.viewDelete()
    
    def preDoUpdate(self):
        if messagebox.askyesno('確認', getMessage("msg-007")):
            params = conditionKeepPopupView.keepConditionParams
            params["conditionName"] = self.view.getWidgetDic(self.itemFrame, getConditionKeepPopupViewItemName("conditionName"))
            conditionKeepPopupAction.doUpdate(params)
            self.postDoUpdate()
    
    def postDoUpdate(self):
        messagebox.showinfo('メッセージ', getMessage("msg-002"))
        self.viewDelete()
    
    def viewDelete(self):
        self.view.top.destroy()