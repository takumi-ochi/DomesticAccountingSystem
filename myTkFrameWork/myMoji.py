class myMoji:
    zenHanDic = str.maketrans({chr(0xFF01 + i): chr(0x21 + i) for i in range(94)})
    hanZenDic = str.maketrans({chr(0x0021 + i): chr(0xFF01 + i) for i in range(94)})
    
    #全角＞半角
    def zenToHan(text):
        text = text.translate(myMoji.zenHanDic)
        return text

    #半角＞全角
    def hanToZen(text):
        text = text.translate(myMoji.hanZenDic)
        return text

if __name__ == "__main__":
    myMoji.zenToHan("１")