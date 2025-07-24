from lib.lib import *
import typer
import Client

app = typer.Typer()

@app.command(help="Application to connect to a users server.")
def run(ip: str = typer.Argument(..., help="IP Address of the server"), port: int = typer.Argument(..., help="Port of the server")):
    client = Client.Client(ip, port)
    client.connect()
    client.accessPortal()

if __name__ == "__main__":
    app()

