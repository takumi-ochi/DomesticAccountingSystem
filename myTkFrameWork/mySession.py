class mySession:
    userId = ""
    userName = ""
    Autho = ""

    def setUserId(userId):
        mySession.userId = userId
    
    def getUserId():
        return mySession.userId
    
    def setUserName(userName):
        mySession.userName = userName
    
    def getUserName():
        return mySession.userName
    
    def setAutho(Autho):
        mySession.Autho = Autho
    
    def getAutho():
        return mySession.Autho
    
    def clearSesson():
        mySession.userId = ""
        mySession.userName = ""
        mySession.Autho = ""
