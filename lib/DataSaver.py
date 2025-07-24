import lib
from lib import jsonLIB
from datetime import datetime, timedelta
# this is here because python fucking hates datetime and timedelta
def day_in_future():
    today = datetime.today()
    one_week_later = today + timedelta(days=7)
    return one_week_later.strftime("%A, %d %B %Y")

class Encrypter():
    def __init__(self, key: int, credFile: str, loanFile: str, moneyFile: str, maxIDFile: str):
        self.KEY = key
        self.CREDFILE = credFile
        self.LOANFILE = loanFile
        self.MONEYFILE = moneyFile
        self.MAXIDFILE = maxIDFile
    
    ### BALANCE FUNCTIONS
    # money.json {
    #   userID {
    #     balance: float
    #     deposited: float
    #     withdrawn: float
    #   }
    # }
    def setupBalance(self, userID: int):
        balanceEncrypted = lib.Encryption.Encrypt(self.KEY, "0")
        depositedEncrypted = lib.Encryption.Encrypt(self.KEY, "0")
        withdrawnEncrypted = lib.Encryption.Encrypt(self.KEY, "0")
        dataToSave = {
            f"{userID}": {
                "Balance": balanceEncrypted,
                "Deposited": depositedEncrypted,
                "Withdrawn": withdrawnEncrypted
            }
        }
        fullData = jsonLIB.read(self.MONEYFILE)
        fullData.update(dataToSave)
        jsonLIB.write(fullData, self.MONEYFILE)
    
    def addDepositedByATMBalance(self, userID: int, amount: float):
        """
        Add balance by deposital in ATM.
        """
        fullData = jsonLIB.read(self.MONEYFILE)
        userData = fullData[f"{userID}"]
        ## DATA GETTER
        balanceEncrypted = userData["Balance"]
        balanceDecrypted = float(lib.Encryption.Decrypt(self.KEY, balanceEncrypted))
        depositedEncrypted = userData["Deposited"]
        depositedDecrypted = float(lib.Encryption.Decrypt(self.KEY, depositedEncrypted))

        ## ADD BALANCE
        balanceDecrypted += amount
        ## ADD DATA STUFF
        depositedDecrypted += amount
        ## REENCRYPT DATA
        balance = lib.Encryption.Encrypt(self.KEY, str(balanceDecrypted))
        deposited = lib.Encryption.Encrypt(self.KEY, str(depositedDecrypted))
        ## REWRITE DATA
        rewrittenData = {
            f"{userID}": {
                "Balance": balance,
                "Deposited": deposited,
                "Withdrawn": userData["Withdrawn"]
            }
        }
        
        fullData.update(rewrittenData)
        jsonLIB.write(fullData, self.MONEYFILE)

    def withdrawnMoney(self, userID: int, amount: float):
        fullData = jsonLIB.read(self.MONEYFILE)
        userData = fullData[f"{userID}"]
        ## DATA GETTER
        balanceEncrypted = userData["Balance"]
        balanceDecrypted = float(lib.Encryption.Decrypt(self.KEY, balanceEncrypted))
        withdrawnEncrypted = userData["Withdrawn"]
        withdrawnDecrypted = float(lib.Encryption.Decrypt(self.KEY, withdrawnEncrypted))
        
        ## DO THE CHANGES
        if balanceDecrypted < amount:
            return False # Insufficient funds
        else:
            balanceDecrypted -= amount
            withdrawnDecrypted += amount
        
        balance = lib.Encryption.Encrypt(self.KEY, str(balanceDecrypted))
        withdrawn = lib.Encryption.Encrypt(self.KEY, str(withdrawnDecrypted))
        ## REWRITE DATA
        rewrittenData = {
            f"{userID}": {
                "Balance": balance,
                "Deposited": userData["Deposited"],
                "Withdrawn": withdrawn
            }
        }
        fullData.update(rewrittenData)
        jsonLIB.write(fullData, self.MONEYFILE)

    ### CREDENTIALS FUNCTIONS
    def saveUserData(self, username: str, password: str, securitypin: str):
        userEncrypt = lib.Encryption.Encrypt(self.KEY, username)
        passwordEncrypt = lib.Encryption.Encrypt(self.KEY, password)
        secPinEncrypt = lib.Encryption.Encrypt(self.KEY, securitypin)
        ####### GET ID
    
        currentID = None
        with open(self.MAXIDFILE, "r") as IDFILE:
            currentID = IDFILE.read()

        newID = int(currentID) + 1
        with open(self.MAXIDFILE, "w") as IDFILE:
            IDFILE.write(str(newID))

        ####### FINISH GET ID
        dataToSave = {
            f"{newID}": {
                "Username": f"{userEncrypt}",
                "Password": f"{passwordEncrypt}",
                "Security Pin": f"{secPinEncrypt}"
            }
        }
        fullData = jsonLIB.read(self.CREDFILE)
        fullData.update(dataToSave)
        jsonLIB.write(fullData, self.CREDFILE)
        self.setupBalance(newID)
        self.setupLoanSystem(newID)
    
    def loadUserData(self, userID: int):
        ALLDATA = jsonLIB.read(self.CREDFILE)
        USERDATA = ALLDATA[str(userID)]
        USERDATA["Username"] = lib.Encryption.Decrypt(self.KEY, USERDATA["Username"])
        USERDATA["Password"] = lib.Encryption.Decrypt(self.KEY, USERDATA["Password"])
        USERDATA["Security Pin"] = lib.Encryption.Decrypt(self.KEY, USERDATA["Security Pin"])
        return USERDATA
    
    ### DEBT FUNCTIONS
    # loans.json {
    #   userID {
    #     owned: float,
    #     timeleft: int (days),
    #     loanLimit: float
    #   }
    # }
    # timeleft: you can only take out 1 loan per time, when this finishes, if you dont pay, your account shall be removed from
    # the money taken out, if you dont have any money, your account shall be frozen, with only the deposital feature being allowed.

    def setupLoanSystem(self, userID: int):
        ownedEncrypted = lib.Encryption.Encrypt(self.KEY, "0")
        timeleftEncrypted = lib.Encryption.Encrypt(self.KEY, "None")
        loanLimitEncrypted = lib.Encryption.Encrypt(self.KEY, "20000")
        dataToSave = {
            f"{userID}": {
                "Owned": ownedEncrypted,
                "Time Left": timeleftEncrypted,
                "Loan Limit": loanLimitEncrypted
            }
        }
        fullData = jsonLIB.read(self.LOANFILE)
        fullData.update(dataToSave)
        jsonLIB.write(fullData, self.LOANFILE)

    def takeOutLoan(self, userID: int, amount: float):
        fullData = jsonLIB.read(self.LOANFILE)
        userData = fullData[f"{userID}"]
        ownedEncrypted = userData["Owned"]
        timeLeftEncrypted = userData["Time Left"]   
        loanLimitEncrypted = userData["Loan Limit"]

        ownedDecrypted = float(lib.Encryption.Decrypt(self.KEY, ownedEncrypted))
        timeLeftDecrypted = lib.Encryption.Decrypt(self.KEY, timeLeftEncrypted)
        loanLimitDecrypted = float(lib.Encryption.Decrypt(self.KEY, loanLimitEncrypted))

        # do the stuff
        if loanLimitDecrypted < amount:
            return False
        else:
            loanLimitDecrypted -= amount
            ownedDecrypted += amount
            timeLeftDecrypted = day_in_future()
        
        # actually adding the fucking balance // adding this way too late for it to be excusable
        fullDataMoney = jsonLIB.read(self.MONEYFILE)
        userData = fullDataMoney[f"{userID}"]
        ## DATA GETTER
        balanceEncrypted = userData["Balance"]
        balanceDecrypted = float(lib.Encryption.Decrypt(self.KEY, balanceEncrypted))
        # adding the balance
        balanceDecrypted += ownedDecrypted
        
        # Reencrypt
        owned = lib.Encryption.Encrypt(self.KEY, str(ownedDecrypted))
        timeLeft = lib.Encryption.Encrypt(self.KEY, str(timeLeftDecrypted))
        loanLimit = lib.Encryption.Encrypt(self.KEY, str(loanLimitDecrypted))
        balance = lib.Encryption.Encrypt(self.KEY, str(balanceDecrypted))

        dataToSave = {
            f"{userID}": {
                "Owned": owned,
                "Time Left": timeLeft,
                "Loan Limit": loanLimit
            }
        }

        secondDataToSave = {
            f"{userID}": {
                "Balance": balance,
                "Deposited": userData["Deposited"],
                "Withdrawn": userData["Withdrawn"]
            }
        }
        fullData = jsonLIB.read(self.LOANFILE)
        fullData.update(dataToSave)
        fullDataMoney = jsonLIB.read(self.MONEYFILE)
        fullDataMoney.update(secondDataToSave)
        jsonLIB.write(fullData, self.LOANFILE)
        jsonLIB.write(fullDataMoney, self.MONEYFILE)
    

    def payDebt(self, userID: int, amountGiven: float):
        fullData = jsonLIB.read(self.LOANFILE)
        userData = fullData[f"{userID}"]
        ownedEncrypted = userData["Owned"]
        timeLeftEncrypted = userData["Time Left"]   
        loanLimitEncrypted = userData["Loan Limit"]

        ownedDecrypted = float(lib.Encryption.Decrypt(self.KEY, ownedEncrypted))
        timeLeftDecrypted = lib.Encryption.Decrypt(self.KEY, timeLeftEncrypted)
        loanLimitDecrypted = float(lib.Encryption.Decrypt(self.KEY, loanLimitEncrypted))

        if ownedDecrypted > amountGiven:
            ownedDecrypted -= amountGiven
            loanLimitDecrypted += amountGiven
        if ownedDecrypted <= amountGiven:
            # Include system to make warning that overpaying will not pay for other loans and
            # may break the system until warning.
            ownedDecrypted = 0
            loanLimitDecrypted = 20000
            timeLeftDecrypted = "None"

        # actually adding the fucking balance // adding this way too late for it to be excusable
        fullDataMoney = jsonLIB.read(self.MONEYFILE)
        userData = fullDataMoney[f"{userID}"]
        ## DATA GETTER
        balanceEncrypted = userData["Balance"]
        balanceDecrypted = float(lib.Encryption.Decrypt(self.KEY, balanceEncrypted))
        # getting rid of the balance
        balanceDecrypted -= amountGiven
        
        # Reencrypt
        owned = lib.Encryption.Encrypt(self.KEY, str(ownedDecrypted))
        timeLeft = lib.Encryption.Encrypt(self.KEY, str(timeLeftDecrypted))
        loanLimit = lib.Encryption.Encrypt(self.KEY, str(loanLimitDecrypted))
        balance = lib.Encryption.Encrypt(self.KEY, str(balanceDecrypted))

        dataToSave = {
            f"{userID}": {
                "Owned": owned,
                "Time Left": timeLeft,
                "Loan Limit": loanLimit
            }
        }

        secondDataToSave = {
            f"{userID}": {
                "Balance": balance,
                "Deposited": userData["Deposited"],
                "Withdrawn": userData["Withdrawn"]
            }
        }

        fullData = jsonLIB.read(self.LOANFILE)
        fullData.update(dataToSave)
        fullDataMoney = jsonLIB.read(self.MONEYFILE)
        fullDataMoney.update(secondDataToSave)
        jsonLIB.write(fullData, self.LOANFILE)
        jsonLIB.write(fullDataMoney, self.MONEYFILE)