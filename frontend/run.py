from flask import Flask,render_template,request

from client.sendbtc import SendBitcoin

app = Flask(__name__)

@app.route("/",methods = ["GET","POST"])
def wallet():
    message = ""
    if request.method == "POST":
        from_address = request.form.get("fromAddress")
        toAddress = request.form.get("toAddress")
        Amount = request.form.get("Amount",type=int)
        sendCoin = SendBitcoin(fromAccount=from_address,toAccount=toAddress,Amount=Amount,UTOxS=UTXOS)
        if not sendCoin.prepareTransaction():
            message = "Insufficient balance"
    return render_template("wallet.html",message= message)
def main(utoxs):
    global UTXOS 
    UTXOS = utoxs
    app.run()