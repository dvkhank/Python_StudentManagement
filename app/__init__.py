from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from urllib.parse import quote


app = Flask(__name__)
app.secret_key = '21137affa59a4dd08b708dcf106c724f9'
app.config["SQLALCHEMY_DATABASE_URI"] ="mysql+pymysql://root:%s@localhost/studentmanagement?charset=utf8mb4" % quote('123456789')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["PAGE_SIZE"] = 2

db = SQLAlchemy(app=app)
login = LoginManager(app=app)

momo = {
    "endpoint": "https://test-payment.momo.vn/gw_payment/transactionProcessor",
    "partnerCode": "MOMO",
    "accessKey": "F8BBA842ECF85",
    "secretKey": "K951B6PE1waDMi640xX08PD3vg6EkVlz",
    "orderInfo": "pay with MoMo",
    "returnUrl": "http://127.0.0.1:5000/momo/payment-result",
    "notifyUrl": "http://127.0.0.1:5000/momo/payment-result",
    "amount": "",
    "orderId": "",
    "requestId": "",
    "requestType": "captureMoMoWallet",
    "extraData": ""
}
