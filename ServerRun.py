from lib.lib import *
import typer
import Server


app = typer.Typer(help="Tool to run your own private (and non-real accepting cash) bank server.")

@app.command(help="Tool to run your own private (and non-real accepting cash) bank server.")
def run(config: str = typer.Argument(..., help="The configuration file for the server. Example file found in the GitHub. Make sure the file isn't empty!")):
    # to do the shit now
    configFile = jsonLIB.read(config)
    IP = configFile["IP"]
    PORT = configFile["Port"]
    encryptionKey = configFile["Encryption Key"]
    credsFile = configFile["Credentials File"]
    loansFile = configFile["Loans File"]
    moneyFile = configFile["Balance File"]
    identFile = configFile["ID File"]
    customBankName = configFile["Custom Bank Name"]
    customBankColor = configFile["Custom Bank Name Color"]
    if customBankName == "":
        server = Server.Server(IP, PORT, encryptionKey, credsFile, loansFile, moneyFile, identFile)
    else:
        server = Server.Server(IP, PORT, encryptionKey, credsFile, loansFile, moneyFile, identFile, customBankName, customBankColor)
    server.loop()

if __name__ == "__main__":
    app()

