# Fictional CLI Banking Server for Python
Horribly made fake custom bank you can host locally with Python.
Using Socket, you can make deposits, withdrawls and loans, with an easy to customize configuration.

## Features
- A system to request data from the server.
- A full fledged Client file to interact with the server.
- Only a command line interface created with Python.

## How to setup
### Building


1. Clone the repository with the command and cd to it.

``
git clone https://github.com/MinaRoblox/BankAccount.git && BankAccount
``

2.- Create the neccesary JSON files for this utilities and what it shoud contain:
- Credentials file .json // {}
- Loans file .json // {}
- Money .json // {}
- Maximun ID .txt // 0

3.- Place the paths of each one of your puts in their respective spots:

``
"Credentials File": "db/cred.json",
"Loans File": "db/loan.json",
"Balance File": "db/money.json",
"ID File": "db/maxID.txt"
``

4.- Change any neccesary configurations you want, like the IP, port or the Encryptation Key.

5.- With/without a virtual enviroment activated, install the required libraries.

``
pip install -r requirements.txt
``


6.- Run ServerRun.py with:

``
python3 ServerRun.py config.json
``

7.- In another terminal in the same network run:

``
python3 ClientRun.py "IP" port
``

### Releases