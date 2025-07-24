from lib.lib import *
from datetime import datetime, timedelta
from colorama import Fore
from colorama import init as colorama_init

# this is here because python fucking hates this
def day_in_future():
    today = datetime.today()
    one_week_later = today + timedelta(days=7)
    return one_week_later.strftime("%A, %d %B %Y")

# python also fucking hates str to tuple so this is here
def str_to_tuple(s: str) -> tuple:
    s = s.strip().strip("()")
    if not s:
        return ()

    def parse_value(x: str):
        x = x.strip()

        # Handle booleans
        if x == "True":
            return True
        if x == "False":
            return False
        
        # Handle None
        if x == "None":
            return None

        # Handle quoted strings
        if (x.startswith("'") and x.endswith("'")) or (x.startswith('"') and x.endswith('"')):
            return x[1:-1]

        # Handle numbers
        try:
            return int(x)
        except ValueError:
            try:
                return float(x)
            except ValueError:
                return x

    # Custom split respecting quotes
    items = []
    current = []
    in_quotes = False
    quote_char = ''
    
    for char in s:
        if char in ("'", '"'):
            if in_quotes and char == quote_char:
                in_quotes = False
            elif not in_quotes:
                in_quotes = True
                quote_char = char
            current.append(char)
        elif char == ',' and not in_quotes:
            items.append(''.join(current).strip())
            current = []
        else:
            current.append(char)
    if current:
        items.append(''.join(current).strip())

    return tuple(parse_value(item) for item in items)
# thanks ai and this is more of a fucking necessity
# btw this function has grown from 20 lines to like 60

class Client():
    def __init__(self, ip, port):
        self.IP = ip
        self.PORT = port
        self.CLIENT = SocketAPI.Client(self.IP, self.PORT)
        self.userID = None
        self.userName = None
        self.passWord = None
        self.securityPin = None
        colorama_init(autoreset=True)
    
    def connect(self):
        self.CLIENT.connect()
    
    def getLoanData(self):
        self.CLIENT.sendMSG(f"request loan {self.userID}")
        return self.CLIENT.receiveMSG()

    def getBalanceData(self):
        self.CLIENT.sendMSG(f"request balance {self.userID}")
        return self.CLIENT.receiveMSG()
    
    def getBankName(self):
        self.CLIENT.sendMSG("request name")
        return self.CLIENT.receiveMSG()

    def getBankColor(self):
        self.CLIENT.sendMSG("request color")
        return self.CLIENT.receiveMSG()
    
    def bankGUI(self):
        while True:
            loanStatus = str_to_tuple(self.getLoanData())
            balanceStatus = str_to_tuple(self.getBalanceData())
            clear()
            print(f"Welcome to {self.bankName}!")
            print(Fore.LIGHTGREEN_EX + f"If you want to do anything,        Username: {self.userName}")
            print(Fore.LIGHTCYAN_EX + f"please select from one of our      Your User ID: {self.userID}")
            print(Fore.LIGHTRED_EX + f"availible options of their         Owned: {loanStatus[0]}")
            print(Fore.LIGHTGREEN_EX + f"numbers.                           Time to pay: {loanStatus[1]}")
            print(Fore.LIGHTCYAN_EX + f"                                   Loan limit: {loanStatus[2]}")
            print(Fore.LIGHTRED_EX  + f"                                   Account balance: {balanceStatus[0]}")
            print(Fore.LIGHTGREEN_EX + f"                                   ")
            print(Fore.LIGHTGREEN_EX + "1. Deposit.")
            print(Fore.LIGHTGREEN_EX + "2. Withdraw.")
            print(Fore.LIGHTGREEN_EX + "3. Take out a loan.")
            print(Fore.LIGHTGREEN_EX + "4. Pay out your loan.")
            print(Fore.LIGHTGREEN_EX + "5. Quit.")
            try:
                option = int(input(""))
                if option == 0 or option > 5:
                    print(" ")
                    print("That is not a valid command!")
                    time.sleep(1)
                else:
                    # Handle command!
                    match option:
                        # Depositing
                        case 1:
                            print(" ")
                            try:
                                amount = int(input(Fore.LIGHTGREEN_EX + "Amount? > "))
                                if amount == 0 or amount < 0:
                                    print(" ")
                                    print("Try inputting an actual amount!")
                                    time.sleep(1)
                                    continue
                                else:
                                    self.CLIENT.sendMSG(f"bank deposit {self.userID} {amount}")
                                    uselessPieceOf = self.CLIENT.receiveMSG()
                                    time.sleep(1)
                            except:
                                print(" ")
                                print("Don't input a letter as an amount!")
                                time.sleep(1)
                                continue
                        # Withdrawing
                        case 2:
                            print(" ")
                            try:
                                amount = int(input(Fore.LIGHTGREEN_EX + "Amount? > "))
                                if amount == 0 or amount < 0:
                                    print(" ")
                                    print("Try inputting an actual amount!")
                                    time.sleep(1)
                                    continue
                                else:
                                    self.CLIENT.sendMSG(f"bank withdraw {self.userID} {amount}")
                                    anotherUselessPieceOf = self.CLIENT.receiveMSG()
                                    time.sleep(1)
                            except:
                                print(" ")
                                print("Don't input a letter as an amount!")
                                time.sleep(1)
                                continue
                        # Taking out a loan.
                        case 3:
                            print(" ")
                            try:
                                amount = int(input(Fore.LIGHTGREEN_EX + "Amount? > "))
                                if amount == 0 or amount < 0:
                                    print(" ")
                                    print("Try inputting an actual amount!")
                                    time.sleep(1)
                                    continue
                                elif amount > loanStatus[2]:
                                    print(" ")
                                    print("You can't borrow more than what you are limited to.")
                                    time.sleep(2)
        
                                else:
                                    self.CLIENT.sendMSG(f"loan get {self.userID} {amount}")
                                    print(f"You have until {day_in_future()} to pay your loan.")
                                    anotherStupidUselessPieceOf = self.CLIENT.receiveMSG()
                                    time.sleep(3)
                            except:
                                print(" ")
                                print("Don't input a letter as an amount!")
                                time.sleep(1)
                                continue
                        # Paying out a loan
                        case 4:
                            print(" ")
                            try:
                                amount = int(input(Fore.LIGHTGREEN_EX + "Amount? > "))
                                if amount == 0 or amount < 0:
                                    print(" ")
                                    print("Try inputting an actual amount!")
                                    time.sleep(1)
                                    continue
                                elif amount < loanStatus[0]:
                                    print(" ")
                                    print("Pay when you have the full money!")
                                    time.sleep(1)
                                elif amount > loanStatus[0]:
                                    print(" ")
                                    print("Pay the exact amount you own!")
                                    time.sleep(1)
                                else:
                                    self.CLIENT.sendMSG(f"loan pay {self.userID} {amount}")
                                    ohMyLordAnotherOne = self.CLIENT.receiveMSG()
                                    time.sleep(1)
                            except:
                                print(" ")
                                print("Don't input a letter as an amount!")
                                time.sleep(1)
                                continue
                        # Quit
                        case 5:
                            break

            except:
                print(" ")
                print("That is not a valid command!")
                time.sleep(1)

    def setupBankNameColorRequests(self):
        self.bankName = self.getBankName()
        self.bankColor = self.getBankColor()
        self.bankColorChecker = False
        if self.bankColor == "None":
            self.bankColorChecker = False
        else:
            self.bankColorChecker = True
        
        def bankColorGetter(bankColor, bankName):
            if bankColor == "BLACK":
                bankName = Fore.BLACK + bankName
            elif bankColor == "BLUE":
                bankName = Fore.BLUE + bankName
            elif bankColor == "CYAN":
                bankName = Fore.CYAN + bankName
            elif bankColor == "GREEN":
                bankName = Fore.GREEN + bankName
            elif bankColor == "LIGHTBLACK_EX":
                bankName = Fore.LIGHTBLACK_EX + bankName
            elif bankColor == "LIGHTCYAN_EX":
                bankName = Fore.LIGHTCYAN_EX + bankName
            elif bankColor == "LIGHTGREEN_EX":
                bankName = Fore.LIGHTGREEN_EX + bankName
            elif bankColor == "LIGHTMAGENTA_EX":
                bankName = Fore.LIGHTMAGENTA_EX + bankName
            elif bankColor == "LIGHTRED_EX":
                bankName = Fore.LIGHTRED_EX + bankName
            elif bankColor == "LIGHTWHITE_EX":
                bankName = Fore.LIGHTWHITE_EX + bankName
            elif bankColor == "LIGHTYELLOW_EX":
                bankName = Fore.LIGHTYELLOW_EX + bankName
            elif bankColor == "MAGENTA":
                bankName = Fore.MAGENTA + bankName
            elif bankColor == "RED":
                bankName = Fore.RED + bankName
            elif bankColor == "RESET":
                bankName = Fore.RESET + bankName
            elif bankColor == "WHITE":
                bankName = Fore.WHITE + bankName
            elif bankColor == "YELLOW":
                bankName = Fore.YELLOW + bankName
            return bankName
        
        if self.bankColorChecker == True:
            self.bankName = bankColorGetter(self.bankColor, self.bankName)
    
    def login(self):
        print(f"Welcome to {self.bankName}")
        print(Fore.LIGHTGREEN_EX + "Please login to your account with the following details:")
        usernameGiven = input(Fore.LIGHTCYAN_EX + "1. Username >>> ")
        passwordGiven = input(Fore.LIGHTRED_EX + "2. Password >>> ")
        securityGiven = input(Fore.LIGHTGREEN_EX + "3. Security PIN >>> ")
        time.sleep(1)
        self.CLIENT.sendMSG(f"credentials id {usernameGiven} {passwordGiven} {securityGiven}")
        try:
            self.userID = int(self.CLIENT.receiveMSG())
        except:
            return False
        self.CLIENT.sendMSG(f"credentials login {usernameGiven} {passwordGiven} {securityGiven} {self.userID}")
        msg = self.CLIENT.receiveMSG()
        os.system("touch loginBefore.txt")
        if msg == "True":
            self.userName = usernameGiven
            self.passWordGiven = passwordGiven
            self.securityPin = securityGiven
            return True
        else:
            print("Incorrect password!")
            print("Please try again.")
            return False
    
    def register(self):
        print(f"Welcome to {self.bankName}")
        print(Fore.LIGHTCYAN_EX + "As you look like a new user to our platform,")
        print(Fore.LIGHTRED_EX + "you will now be required to create an account")
        print(Fore.LIGHTGREEN_EX + "to start using our services, please insert the")
        print(Fore.LIGHTCYAN_EX + "required credentials to start.")
        print("1. Username")
        print("2. Password")
        print("3. Security PIN")
        usernameGiven = input("1. > ")
        passwordGiven = input("2. > ")
        securityGiven = input("3. > ")
        self.userName = usernameGiven
        self.passWordGiven = passwordGiven
        self.securityPin = securityGiven
        time.sleep(1)
        self.CLIENT.sendMSG(f"credentials register {usernameGiven} {passwordGiven} {securityGiven}")
        a = self.CLIENT.receiveMSG()
        os.system("touch loginBefore.txt")
        self.CLIENT.sendMSG(f"credentials id {usernameGiven} {passwordGiven} {securityGiven}")
        self.userID = self.CLIENT.receiveMSG()
        print(self.userID)
        print(a)
        return True
    def accessPortal(self):
        self.setupBankNameColorRequests()
        clear()
        if os.path.exists("loginBefore.txt"):
            checkLogin = self.login()
            if checkLogin == False:
                pass
            else:
                self.bankGUI()
        else:
            checkRegister = self.register()
            if checkRegister:
                self.bankGUI()
            else:
                print("Incorrect password!")
                print("Please try again.")
