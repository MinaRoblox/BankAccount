from lib.lib import *

class Server():
    def __init__(self, ip, port, encryptionKey, CRED_FILE, LOAN_FILE, MONEY_FILE, MAXIDFILE, bankName="MinaRoblox's Bank", bankColor=""):
        self.IP = ip
        self.PORT = port
        self.KEY = encryptionKey
        self.CREDENTIALS_FILE = CRED_FILE
        self.LOANS_FILE = LOAN_FILE
        self.MONEY_FILE = MONEY_FILE
        self.SERVER = SocketAPI.Server(self.IP, self.PORT)
        self.MAXIDFILE = MAXIDFILE
        self.ENCRYPTER = DataSaver.Encrypter(self.KEY, self.CREDENTIALS_FILE, self.LOANS_FILE, self.MONEY_FILE, self.MAXIDFILE)
        self.BANKNAME = bankName
        self.BANKCOLOR = bankColor

    def registerUser(self, username, password, securityPin):
        self.ENCRYPTER.saveUserData(username, password, securityPin)
    
    def checkCredentialsLOGIN(self, username, password, securityPin, userID):
        currentData = self.ENCRYPTER.loadUserData(userID)
        givenData = {
            "Username": f"{username}",
            "Password": f"{password}",
            "Security Pin": f"{securityPin}"
        }
        if givenData == currentData:
            return True
        else:
            return False
    
    def addBalanceByATM(self, userID: int, balance: float):
        self.ENCRYPTER.addDepositedByATMBalance(userID, balance)
    
    def withdrawMoney(self, userID: int, amount: float):
        self.ENCRYPTER.withdrawnMoney(userID, amount)
    
    def takeOutLoan(self, userid: int, quantity: float):
        self.ENCRYPTER.takeOutLoan(userid, quantity)

    def payDebt(self, userID: int, quantity: float):
        self.ENCRYPTER.payDebt(userID, quantity)
    
    def getUserData(self, userID: int):
        return self.ENCRYPTER.loadUserData(userID)

    def getLoanData(self, userID: int):
        fullData = jsonLIB.read(self.LOANS_FILE)
        userData = fullData[f"{userID}"]
        ownedEncrypted = userData["Owned"]
        timeLeftEncrypted = userData["Time Left"]   
        loanLimitEncrypted = userData["Loan Limit"]

        ownedDecrypted = float(Encryption.Decrypt(self.KEY, ownedEncrypted))
        timeToPayDecrypted = Encryption.Decrypt(self.KEY, timeLeftEncrypted)
        loanLimitDecrypted = float(Encryption.Decrypt(self.KEY, loanLimitEncrypted))

        return (ownedDecrypted, timeToPayDecrypted, loanLimitDecrypted)

    def getBalanceData(self, userID: int):
        fullData = jsonLIB.read(self.MONEY_FILE)
        userData = fullData[f"{userID}"]

        balanceEncrypted = userData["Balance"]
        depositedEncrypted = userData["Deposited"]
        withdrawnEncrypted = userData["Withdrawn"]

        balanceDecrypted = float(Encryption.Decrypt(self.KEY, balanceEncrypted))
        depositedDecrypted = float(Encryption.Decrypt(self.KEY, depositedEncrypted))
        withdrawnDecrypted = float(Encryption.Decrypt(self.KEY, withdrawnEncrypted))

        return (balanceDecrypted, depositedDecrypted, withdrawnDecrypted)

    def handleCommand(self, commandFull: str):
        print(f"Command received: {commandFull}")
        command = commandFull.split()
        if command[0] == "credentials":
            if command[1] == "register":
                userName = command[2]
                passWord = command[3]
                secuPin = command[4]
                self.registerUser(userName, passWord, secuPin)
            elif command[1] == "login":
                userName = command[2]
                passWord = command[3]
                secuPin = command[4]
                userID = int(command[5])
                if self.checkCredentialsLOGIN(userName, passWord, secuPin, userID):
                    return True
                else:
                    return False
            elif command[1] == "id":
                userName = command[2]
                passWord = command[3]
                secuPin = command[4]
                return self.getUserID(userName, passWord, secuPin)
                
        elif command[0] == "bank":
            if command[1] == "deposit":
                usID = int(command[2])
                amount = float(command[3])
                self.addBalanceByATM(usID, amount)
            elif command[1] == "withdraw":
                useID = int(command[2])
                alount = float(command[3])
                self.withdrawMoney(useID, alount)
        elif command[0] == "loan":
            if command[1] == "get":
                uID = int(command[2])
                quantit = float(command[3])
                a = self.takeOutLoan(uID, quantit)

            elif command[1] == "pay":
                userIdentity = int(command[2])
                quantityAgain = float(command[3])
                self.payDebt(userIdentity, quantityAgain)
        elif command[0] == "request":
            if command[1] == "loan":
                userID = command[2]
                return self.getLoanData(userID)
            elif command[1] == "balance":
                userIDentityfication = command[2]
                return self.getBalanceData(userIDentityfication)
            elif command[1] == "name":
                return self.BANKNAME
            elif command[1] == "color":
                if self.BANKCOLOR == "":
                    return "None"
                else:
                    colorsAvailible = ["BLACK", "BLUE", "CYAN", "GREEN", "LIGHTBLACK_EX", "LIGHTBLUE_EX", "LIGHTCYAN_EX", "LIGHTGREEN_EX", "LIGHTMAGENTA_EX", "LIGHTRED_EX", "LIGHTWHITE_EX",
                   "LIGHTYELLOW_EX", "MAGENTA", "RED", "RESET", "WHITE", "YELLOW"]
                    if self.BANKCOLOR.upper() in colorsAvailible:
                        return self.BANKCOLOR
                    else:
                        return "None"

        else:
            return "Invalid command."
        
    def getUserID(self, username, password, spin):
        ALLDATA = jsonLIB.read(self.CREDENTIALS_FILE)
        for i in range(9999):
            try:
                USERDATA = ALLDATA[str(i + 1)]
                USERDATA["Username"] = Encryption.Decrypt(self.KEY, USERDATA["Username"])
                USERDATA["Password"] = Encryption.Decrypt(self.KEY, USERDATA["Password"])
                USERDATA["Security Pin"] = Encryption.Decrypt(self.KEY, USERDATA["Security Pin"])
                if USERDATA["Username"] == username and USERDATA["Password"] == password and USERDATA["Security Pin"] == spin:
                    print("ID Obtaining successful!")
                    return i + 1
                else:
                    continue
            except:
                return False
        return False
    
    def loop(self):
        def serverLoop():
            con = self.SERVER.acceptConection()
            while True:
                mes = self.SERVER.receiveMSG()
                if mes == "No user here.":
                    break
                Boolean = self.handleCommand(mes)
                print(f"Returning to client: {Boolean}")
                self.SERVER.sendMSG(f"{Boolean}")
        while True:
            serverLoop()