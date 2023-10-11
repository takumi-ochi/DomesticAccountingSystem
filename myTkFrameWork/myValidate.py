import tkinter as tk
import tkinter.ttk as ttk
from .myConst import *

class myValidate():
    #入力桁最大数制限
    def limitChar(string, maxLength):
        return len(string) <= int(maxLength)
    
    #入力制限(整数のみ)
    def limitInt(string, maxLength, minusFlg = False):
        if string == '':
            return True
        #数値評価
        try:
            int(string)
        except Exception:
            return False
        #マイナス値判定
        if minusFlg and myValidate.isNegNum(int(string)): return False
        #入力桁数評価
        if not(myValidate.limitChar(string, maxLength)):
            return False
        
        return True
    
    #入力制限(数値のみ)
    def limitNum(string, maxLength, minusFlg = False):
        string = string.replace('.', '')
        if string == '':
            return True
        #数値評価
        try:
            float(string)
        except Exception:
            return False
        #マイナス値判定
        if minusFlg and myValidate.isNegNum(int(string)): return False
        #入力桁数評価
        if not(myValidate.limitChar(string, maxLength)):
            return False
        
        return True
    
    #入力制限(マイナス値判定)　負の数ならTrue
    def isNegNum(number):
        return number < 0
    
    #入力制限(日付のみ)
    def limitDate(string, maxLength):
        repStr = string.replace('/', '')
        return myValidate.limitInt(repStr, maxLength, True)

    
    #入力制御(金額)
    def limitMoney(string, maxLength):
        string = string.replace(',', '')
        return myValidate.limitInt(string, maxLength, True)

    #入力制御(?と,を入力不可)
    def limitInput(string, maxLength):
        if string in ['?',',']:
            return False
        
        #入力桁数評価
        if not(myValidate.limitChar(string, maxLength)):
            return False
        
        return True