from sys import *
from os import *
from tkinter import messagebox

from myTkFrameWork.myTk import *
from myTkFrameWork.myConst import *
from myTkFrameWork.mySession import *

from menu.menu import *
from searchA.searchViewA import *

from loginConst import *
from loginAction import *

class login:
    view = None

    def __init__(self):
        loginFrame = "login"
        self.view = myTk(getTitle(), getDefaultWindowSetting(), "root", loginFrame)

        #タイトル部
        self.view.createFrame("title", loginFrame, 400, 10)
        self.view.titleLabel("title", getTitleName())
        self.view.getWidgetDic("title", getTitleName()).bind('<ButtonPress>', self.inputLoginIdPass)

        #入力項目
        itemFrame = "item"
        self.view.createFrame(itemFrame, loginFrame, 320, 100)
        #ID
        inputName = getInputValue("id")
        self.view.nameLabel(itemFrame, inputName)
        self.view.createEntry(itemFrame, inputName)
        self.view.getWidgetDic(itemFrame, inputName).focus_set()
        #パスワード
        inputName = getInputValue("pass")
        self.view.nameLabel(itemFrame, inputName, True)
        self.view.passwordEntry(itemFrame, inputName)

        #ログインボタン
        buttonFrame = "button"
        self.view.createFrame(buttonFrame, loginFrame, 440, 170)
        self.view.createButton(buttonFrame, loginFrame, self.openSearchView, 20)
        self.view.getWidgetDic(buttonFrame, loginFrame).bind('<Return>', self.openSearchViewBind)

        self.view.root.mainloop()
    
    def openSearchViewBind(self, event):
        self.openSearchView()
    
    def openSearchView(self):
        params = {}
        params["id"] = self.view.getWidgetDic("item", getInputValue("id"))
        params["pass"] = self.view.getWidgetDic("item", getInputValue("pass"))
        if loginAction.getSession(params):
            self.view.getWidgetDic("item", getInputValue("id")).delete(0, tk.END)
            self.view.getWidgetDic("item", getInputValue("pass")).delete(0, tk.END)
            if mySession.getUserId() in ["test", "takumi"]:
                searchViewA()
            else:
                menu()
        else:
            messagebox.showerror('エラーメッセージ', "IDかパスワードが間違っています。")
    
    def inputLoginIdPass(self, event):
        self.view.getWidgetDic("item", getInputValue("id")).delete(0, tk.END)
        self.view.getWidgetDic("item", getInputValue("pass")).delete(0, tk.END)
        self.view.getWidgetDic("item", getInputValue("id")).insert(0, 'takumi')
        self.view.getWidgetDic("item", getInputValue("pass")).insert(0, 'takumi')
        self.openSearchView()
        
    
def main():
    login()

if __name__ == "__main__":
    print("start program")
    main()