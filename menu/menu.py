from myTkFrameWork.myTk import *
from myTkFrameWork.myConst import *
from myTkFrameWork.mySession import *

from searchA.searchViewA import *

class menu:
    mainFrame = "menu"

    def __init__(self):
        self.view = myTk("", "", "frame", menu.mainFrame)

        #ヘッダー部
        headFrame = "head"
        self.view.createFrame(headFrame, menu.mainFrame, 0, 0)
        self.view.titleLabel(headFrame, 'ユーザー名:' + mySession.getUserName(), 15)

        #ヘッダーリンク
        headLinkFrame = "headLink"
        self.view.createFrame(headLinkFrame, menu.mainFrame, 930, 0)
        self.view.linkLabel(headLinkFrame, getHeadDic("logout"))
        self.view.getWidgetDic(headLinkFrame, getHeadDic("logout")).focus_set()
        self.view.getWidgetDic(headLinkFrame, getHeadDic("logout")).bind('<ButtonPress>', self.logout)

        #タイトル部
        self.view.createFrame("title", menu.mainFrame, 350, 10)
        self.view.titleLabel("title", getTitle())

        #メニューリンク
        menuLinkFrame = "menuLink"
        self.view.createFrame(menuLinkFrame, menu.mainFrame, 300, 100)
        self.view.linkLabel(menuLinkFrame, '家計簿検索')
        self.view.getWidgetDic(menuLinkFrame, '家計簿検索').bind('<ButtonPress>', self.fowardSearchA)
        if mySession.getAutho() == "A": self.view.linkLabel(menuLinkFrame, 'ユーザーマスターメンテナンス')

    def fowardSearchA(self, event):
        searchViewA()

    
    def logout(self, event):
        mySession.clearSesson()
        self.view.getFrame(menu.mainFrame).destroy()