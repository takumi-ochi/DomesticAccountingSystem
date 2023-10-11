import tkinter as tk
import tkinter.ttk as ttk
from typing import Text

from .myConst import *
from .myValidate import *
from .myMoji import *
from .Error import *

class myTk():
    root = None #メイン画面
    rootWidth = 0 #メイン画面横サイズ
    rootHeight = 0 #メイン画面縦サイズ
    frameDic = {} #フレーム一覧
    widgetDic = {} #パーツ一覧
    widgetParam = {} #ウィジェットパラメーター
    checkList = {} #チェックボックス状態一覧

    def __init__(self, title = "タイトル", state = "zoomed", windowState = "root", frameKey = "frame", modalFlg = False):
        if windowState != "frame":
            if windowState == "top":
                self.top = tk.Toplevel()
                self.top.title(title)
                self.top.bind("<Control-w>", self.bindViewClose)
                if state == "zoomed":
                    self.top.state(state)
                else:
                    self.top.geometry(state)
                #モーダル設定
                if modalFlg:
                    self.top.grab_set() #モーダルにする
                    # self.top.transient(self.master) #タスクバーに表示しない
                self.top.focus_set() #ウィンドをアクティブにする
                self.topWidth = self.top.winfo_screenwidth() #メイン画面横サイズ
                self.topHeight = self.top.winfo_screenheight() #メイン画面縦サイズ
                self.createFrame(frameKey, "top")
            elif windowState == "root":
                myTk.root = tk.Tk()
                myTk.root.title(title)
                myTk.root.bind("<Control-w>", self.bindViewClose)
                if state == "zoomed":
                    myTk.root.state(state)
                else:
                    myTk.root.geometry(state)
                #モーダル設定
                if modalFlg:
                    myTk.root.grab_set() #モーダルにする
                myTk.root.focus_set() #ウィンドをアクティブにする
                myTk.rootWidth = myTk.root.winfo_screenwidth() #メイン画面横サイズ
                myTk.rootHeight = myTk.root.winfo_screenheight() #メイン画面縦サイズ
                self.createFrame(frameKey)
        else:
            self.createFrame(frameKey)
    
    def getRoot(self):
        return myTk.root
    
    def bindViewClose(self, event):
        myTk.root.destroy()
    
    def createFrame(self, frameKey, refDisplay = "root", frameSetX = 0, frameSetY = 0):
        if refDisplay == "root":
            self.frameDic[frameKey] = tk.Frame(myTk.root, width = myTk.rootWidth, height = myTk.rootHeight)
        elif refDisplay == "top":
            self.frameDic[frameKey] = tk.Frame(self.top, width = self.topWidth, height = self.topHeight)
        else:
            self.frameDic[frameKey] = tk.Frame(self.frameDic[refDisplay])
        self.frameDic[frameKey].place(x = frameSetX, y = frameSetY)
        
        self.widgetParam[frameKey + "row"] = 0
        self.widgetParam[frameKey + "column"] = 0
        self.widgetParam[frameKey + "rowspan"] = 1
        self.widgetParam[frameKey + "columnspan"] = 1
        self.widgetParam[frameKey + "x"] = 0
        self.widgetParam[frameKey + "y"] = 0
        self.widgetParam[frameKey + "sticky"] = 'WE'
    
    def getFrame(self, key):
        return self.frameDic[key]
    
    #画面タイトルラベル
    def titleLabel(self, frameKey, name, fontSize = "30"):
        self.widgetDic[frameKey + name] =  tk.Label(self.frameDic[frameKey], text = name, font=("MSゴシック", fontSize, "bold"), relief = tk.FLAT, bd = 2)
        self.myGrid(frameKey, name)
    
    #入力項目ラベル
    def nameLabel(self, frameKey, name, newLine = False, fontSize = "15", fontThick = "normal",  bgColor = "lightskyblue", frameLine = tk.RIDGE, bdType = 2, fontType = "MSゴシック", reName = ''):
        setName = reName if reName else name
        self.widgetDic[frameKey + name] =  tk.Label(self.frameDic[frameKey], text = setName, font=(fontType, fontSize, fontThick), bg = bgColor, relief = frameLine, bd = bdType)
        self.myGrid(frameKey, name, newLine)
    
    #リンクラベル
    def linkLabel(self, frameKey, name, fontSize = "20", newLine = True):
        self.widgetDic[frameKey + name] =  tk.Label(self.frameDic[frameKey], text = name, font=("MSゴシック", fontSize, "normal", "roman", "underline"), fg = 'blue', relief = tk.FLAT, bd = 2)
        self.myGrid(frameKey, name, newLine)
        self.widgetDic[frameKey + name].bind("<Enter>", self.linkLabelInMouseActive) #リンクラベルにマウスがあたったとき
        self.widgetDic[frameKey + name].bind("<Leave>", self.linkLabelOutMouseActive) #リンクラベルからマウスが外れた時

    #リンクラベルを光らせる
    def linkLabelInMouseActive(self, event):
        event.widget["fg"] = 'skyblue'
    
    #リンクラベルを元に戻す
    def linkLabelOutMouseActive(self, event):
        event.widget["fg"] = 'blue'
    
    #テキスト
    def createText(self, frameKey, name, newLine = False, width = 20, height = 10, fontSize = "15"):
        self.widgetDic[frameKey + name] = tk.Text(self.frameDic[frameKey], width = width, height = height, font=("MSゴシック", fontSize, "normal", "roman", "normal"))
        self.myGrid(frameKey, name, newLine)
    
    def textInputComple(self, event):
        inputStr = event.widget.get("1.0", "end -1c")
        for char in ['?', ',']:
            if char in inputStr:
                inputStr = inputStr.replace('?','').replace(',','')
                event.widget.delete("1.0", "end")
                event.widget.insert("1.0", inputStr)
                messagebox.showerror('エラーメッセージ', getErrorMessage("er-002") + '：' + '?,')
                break
    
    #縦スクロールバー　テキスト用
    def createScrolbarText(self, frameKey, name, text):
        self.widgetDic[frameKey + name] = tk.Scrollbar(self.frameDic[frameKey], orient=tk.VERTICAL, command=text.yview)
        text["yscrollcommand"] = self.widgetDic[frameKey + name].set
        self.widgetDic[frameKey + name].grid(row = self.widgetParam[frameKey + "row"], column = self.widgetParam[frameKey + "column"], sticky=(tk.constants.N))
        self.widgetParam[frameKey + "column"] += 1
    
    #エントリー
    def createEntry(self, frameKey, name, view = "root", maxSize = 20, fontSize = "15", maxInput = 20):
        if view == "root":
            vc = myTk.root.register(myValidate.limitInput)
        else:
            vc = self.top.register(myValidate.limitInput)
        self.widgetDic[frameKey + name] = ttk.Entry(self.frameDic[frameKey], width = maxSize, validate = "key", validatecommand = (vc, "%P", maxInput), font=("MSゴシック", fontSize, "normal", "roman", "normal"))
        self.myGrid(frameKey, name)
    
    #リードオンリー
    def readOnlyEntry(self, frameKey, name, maxSize = 20, fontSize = "15", position = "center"):
        self.widgetDic[frameKey + name] = ttk.Entry(self.frameDic[frameKey], width = maxSize, justify = position, font=("MSゴシック", fontSize, "normal", "roman", "normal"))
        self.widgetDic[frameKey + name].configure(state='readonly')
        self.myGrid(frameKey, name)
    
    #エントリー（パスワード)
    def passwordEntry(self, frameKey, name, view = "root", maxSize = 20, fontSize = "15", maxInput = 20):
        if view == "root":
            vc = myTk.root.register(myValidate.limitChar)
        else:
            vc = self.top.register(myValidate.limitChar)
        self.widgetDic[frameKey + name] = ttk.Entry(self.frameDic[frameKey], width = maxSize, validate = "key", validatecommand = (vc, "%P", maxInput), font=("MSゴシック", fontSize, "normal", "roman", "normal"), show = '*')
        self.myGrid(frameKey, name)
    
    #エントリー(整数値入力)
    def intNumberEntry(self, frameKey, name, view = "root", maxSize = 20, fontSize = "15", maxInput = 20, minusFlg = False):
        if view == "root":
            vc = myTk.root.register(myValidate.limitInt)
        else:
            vc = self.top.register(myValidate.limitInt)
        self.widgetDic[frameKey + name] = ttk.Entry(self.frameDic[frameKey], width = maxSize, validate = "key", validatecommand = (vc, "%P", maxInput, minusFlg), font=("MSゴシック", fontSize, "normal", "roman", "normal"))
        self.myGrid(frameKey, name)
        self.widgetDic[frameKey + name].bind("<FocusOut>", self.numComple)

    #エントリー(実数値入力)
    def numberEntry(self, frameKey, name, view = "root", maxSize = 20, fontSize = "15", maxInput = 20, minusFlg = False):
        if view == "root":
            vc = myTk.root.register(myValidate.limitNum)
        else:
            vc = self.top.register(myValidate.limitNum)
        self.widgetDic[frameKey + name] = ttk.Entry(self.frameDic[frameKey], width = maxSize, validate = "key", validatecommand = (vc, "%P", maxInput, minusFlg), font=("MSゴシック", fontSize, "normal", "roman", "normal"))
        self.myGrid(frameKey, name)
        self.widgetDic[frameKey + name].bind("<FocusOut>", self.numComple)
    
    #数値入力補完(大文字を小文字に)
    def numComple(self, event):
        inputStr = myMoji.zenToHan(event.widget.get())
        event.widget.delete(0, tk.END)
        event.widget.insert(0, inputStr)
    
    #エントリー(金額)
    def moneyEntory(self, frameKey, name, view = "root", maxSize = 20, fontSize = "15", maxInput = 20):
        if view == "root":
            vc = myTk.root.register(myValidate.limitMoney)
        else:
            vc = self.top.register(myValidate.limitMoney)
        self.widgetDic[frameKey + name] = ttk.Entry(self.frameDic[frameKey], width = maxSize, validate = "key", validatecommand = (vc, "%P", maxInput), font=("MSゴシック", fontSize, "normal", "roman", "normal"))
        self.myGrid(frameKey, name)
        self.widgetDic[frameKey + name].bind("<FocusIn>", self.moneyCompleCancel)
        self.widgetDic[frameKey + name].bind("<FocusOut>", self.moneyComple)

    #金額入力補完キャンセル(,を削除)
    def moneyCompleCancel(self, event):
        inputStr = event.widget.get().replace(',', '')
        event.widget.delete(0, tk.END)
        event.widget.insert(0, inputStr)
    
    #金額入力補完(大文字を小文字に 3桁毎に,を打つ)
    def moneyComple(self, event):
        self.numComple(event)
        inputStr = event.widget.get()
        if inputStr == '': return
        inputStr = int(inputStr)
        inputStr = "{:,}".format(inputStr)
        event.widget.delete(0, tk.END)
        event.widget.insert(0, inputStr)
    
    #エントリー(日付入力)
    def dateEntry(self, frameKey, name, maxSize = 20, fontSize = "15", maxInput = 20):
        vc = myTk.root.register(myValidate.limitDate)
        self.widgetDic[frameKey + name] = ttk.Entry(self.frameDic[frameKey], width = maxSize, validate = "key", validatecommand = (vc, "%P", maxInput), font=("MSゴシック", fontSize, "normal", "roman", "normal"))
        self.myGrid(frameKey, name)
        self.widgetDic[frameKey + name].bind("<FocusIn>", self.dateCompleCancel)
        self.widgetDic[frameKey + name].bind("<FocusOut>", lambda event: self.dateComple(event, maxInput))
    
    #日付入力補完
    def dateComple(self, event, maxInput):
        inputStr = event.widget.get().replace('/', '')
        if len(inputStr) >= 4:
            event.widget.insert(4, '/')
        if len(inputStr) >= 7:
            event.widget.insert(7, '/')
        if len(inputStr) >= maxInput:
            event.widget.delete(10, tk.END)
        self.numComple(event)
    
    #日付入力補完取り消し
    def dateCompleCancel(self, event):
        inputStr = event.widget.get().replace('/', '')
        event.widget.delete(0, tk.END)
        event.widget.insert(0, inputStr)
    
    #コンボボックス
    def createCombobox(self, frameKey, name, maxSize = 20, pullDown = (), state = "readonly", fontSize = "15"):
        self.widgetDic[frameKey + name] = ttk.Combobox(self.frameDic[frameKey], width = maxSize, justify = "left", values = pullDown, state = state, font = ("MSゴシック", fontSize, "normal", "roman", "normal"))
        self.myGrid(frameKey, name)

    #ウィジェット取得
    def getWidgetDic(self, frameKey, widgetName):
        return self.widgetDic[frameKey + widgetName]
    
    #表
    def createTree(self, frameKey, name, newLine = False, headingSize = 15, detailSize = 15):
        self.widgetDic[frameKey + name] = ttk.Treeview(self.frameDic[frameKey])
        self.myGrid(frameKey, name, newLine)
        self.createScrolbar(frameKey, name + "scrolbar", self.widgetDic[frameKey + name])
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("MSゴシック", headingSize, "bold"))
        style.configure("Treeview", font=("MSゴシック", detailSize))
        style.map('Treeview', foreground=self.fixed_map('foreground', style), background=self.fixed_map('background', style))
    
    #表のバグ取り除き
    def fixed_map(self, option, style):
            return [elm for elm in style.map('Treeview', query_opt=option) if
                    elm[:2] != ('!disabled', '!selected')]
    
    #スクロールバー ツリー用
    def createScrolbar(self, frameKey, name, tree):
        self.widgetDic[frameKey + name] = tk.Scrollbar(self.frameDic[frameKey], orient=tk.constants.VERTICAL, command=tree.yview)
        tree['yscrollcommand'] = self.widgetDic[frameKey + name].set
        self.widgetDic[frameKey + name].grid(row = self.widgetParam[frameKey + "row"], column = self.widgetParam[frameKey + "column"], sticky=(tk.constants.N, tk.constants.S))
        self.widgetParam[frameKey + "column"] += 1
    
    #ボタン
    def createButton(self, frameKey, name, func, fontSize = 11, bindKey = '', rename = '', disabled = False, setBg='SystemButtonFace'):
        buttonName = name
        if rename: buttonName = rename 
        if bindKey: buttonName += '(' + bindKey.upper() + ')'
        state = tk.NORMAL
        if disabled: state = tk.DISABLED
        self.widgetDic[frameKey + name] = tk.Button(self.frameDic[frameKey], text = buttonName, state = state, font=("MSゴシック", fontSize, "normal", "roman", "normal"), command = func, bg=setBg)
        self.myGrid(frameKey, name)
    
    #チェックボックス
    def createCheckButton(self, frameKey, name, chkFlg = False, newLine = False, fontSize = '15', reName = '', func = None):
        self.checkList[frameKey + name + "check"] = tk.BooleanVar()
        self.checkList[frameKey + name + "check"].set(chkFlg)
        setName = reName if reName else name
        self.widgetDic[frameKey + name] = tk.Checkbutton(self.frameDic[frameKey], variable = self.checkList[frameKey + name + "check"], text = setName, font=("MSゴシック", fontSize, "normal", "roman", "normal"))
        if func: #切り替え時の処理設定
            self.widgetDic[frameKey + name].bind("<Button-1>", func)
        self.myGrid(frameKey, name, newLine)
    
    #チェックボックス状態変数取得
    def getCheckButton(self, frameKey, name):
        return self.checkList[frameKey + name + "check"]
    
    #チェックボックス状態設定
    def setCheck(self, frameKey, name, setFlg):
        self.checkList[frameKey + name + "check"].set(setFlg)
    
    #チェックボックス状態取得
    def getCheck(self, frameKey, name):
        return self.checkList[frameKey + name + "check"].get()
    
    #チェックボックス状態逆転
    def setCheckToggle(self, frameKey, name):
        self.checkList[frameKey + name + "check"].set(not self.checkList[frameKey + name + "check"].get())
    
    def myGrid(self, frameKey, widgetName, newLine = False, rowSpan = 1, colSpan = 1, sticky = 'WE', padx = 0, pady = 0):
        if newLine:
            self.widgetParam[frameKey + "row"] += 1
            self.widgetParam[frameKey + "column"] = 0
        
        if rowSpan != 1:
            self.widgetParam[frameKey + "rowspan"] = rowSpan
        else:
            self.widgetParam[frameKey + "rowspan"] = 1
        
        if colSpan != 1:
            self.widgetParam[frameKey + "columnspan"] = colSpan
        else:
            self.widgetParam[frameKey + "columnspan"] = 1
        
        if sticky != 'WE':
            self.widgetParam[frameKey + "sticky"] = sticky
        else:
            self.widgetParam[frameKey + "sticky"] = 'WE'
        
        if padx != 0:
            self.widgetParam[frameKey + "x"] = padx
        else:
            self.widgetParam[frameKey + "x"] = 0

        if pady != 0:
            self.widgetParam[frameKey + "y"] = pady
        else:
            self.widgetParam[frameKey + "y"] = 0
        
        setRow = self.widgetParam[frameKey + "row"]
        setColumn = self.widgetParam[frameKey + "column"]
        setRowspan = self.widgetParam[frameKey + "rowspan"]
        setColumnspan = self.widgetParam[frameKey + "columnspan"]
        setPadx = self.widgetParam[frameKey + "x"]
        setPady = self.widgetParam[frameKey + "y"]
        setSticky = self.widgetParam[frameKey + "sticky"]
        
        self.widgetDic[frameKey + widgetName].grid(
            row = setRow,
            column = setColumn, 
            rowspan = setRowspan, 
            columnspan = setColumnspan, 
            padx = setPadx, 
            pady = setPady, 
            sticky = setSticky)
        if colSpan == 1:
            self.widgetParam[frameKey + "column"] += 1
        else:
            self.widgetParam[frameKey + "column"] += colSpan
    
    def setWidgetParam(self, frameKey, paramKey, value):
        self.widgetParam[frameKey + paramKey] = value
    
    def getWidgetParam(self, frameKey, paramKey):
        return self.widgetParam[frameKey + paramKey]