import hashlib
import hmac
from datetime import datetime
from random import randint
import logging

class VNPAY:
    def __init__(self, tmn_code, hash_secret_key, test_url):
        self.request_data = {
            'vnp_Version': '2.1.0',
            'vnp_Command': 'pay',
            'vnp_TmnCode': tmn_code,
            'vnp_CreateDate': datetime.now().strftime('%Y%m%d%H%M%S'),
            'vnp_IpAddr': '192.168.1.102',
            'vnp_CurrCode': 'VND',
            'vnp_Locale': 'vn',
        }
        self.hash_secret_key = hash_secret_key
        self.test_url = test_url

    def set_order_info(self, amount, info, order_type, return_url):
        self.request_data['vnp_Amount'] = amount * 100  # Convert amount to cents
        self.request_data['vnp_OrderInfo'] = info
        self.request_data['vnp_OrderType'] = order_type
        self.request_data['vnp_ReturnUrl'] = return_url
        self.request_data['vnp_TxnRef'] = randint(1, 999)

    def get_payment_url(self):
        try:
            data_str = "&".join(f"{k}={v}" for k, v in sorted(self.request_data.items()))
            secure_hash = self.create_secure_hash(data_str)

            # Thêm chữ ký vào requestData
            self.request_data['vnp_SecureHash'] = secure_hash

            # Tạo URL thanh toán
            payment_url = self.test_url + '?' + "&".join(f"{k}={v}" for k, v in sorted(self.request_data.items()))

            # Log thông tin gửi đi
            logging.debug("Payment URL: %s", payment_url)

            return payment_url
        except Exception as e:
            logging.error("Error generating payment URL: %s", str(e))
            raise

    def create_secure_hash(self, data_str):
        try:
            key = bytes(self.hash_secret_key, 'utf-8')
            data = bytes(data_str, 'utf-8')
            secure_hash = hmac.new(key, msg=data, digestmod=hashlib.sha512).hexdigest().upper()
            logging.debug("Generated Secure Hash: %s", secure_hash)
            return secure_hash
        except Exception as e:
            logging.error("Error creating secure hash: %s", str(e))
            raise
