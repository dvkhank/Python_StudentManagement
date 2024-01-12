import hashlib


class VNPAY:
    def __init__(self):
        self.requestData = {}
        self.responseData = {}

    def get_payment_url(self, payment_url, hash_secret_key):
        # Xử lý dữ liệu và tạo chuỗi để tạo chữ ký
        data_str = "&".join(f"{key}={value}" for key, value in sorted(self.requestData.items()))
        secure_hash = self.create_secure_hash(data_str, hash_secret_key)

        # Thêm chữ ký vào requestData
        self.requestData['vnp_SecureHash'] = secure_hash

        # Tạo URL thanh toán
        payment_url += '?' + "&".join(f"{key}={value}" for key, value in sorted(self.requestData.items()))
        return payment_url

    def create_secure_hash(self, data_str, hash_secret_key):
        data_str = hash_secret_key + data_str
        secure_hash = hashlib.sha256(data_str.encode('utf-8')).hexdigest()
        return secure_hash

    def validate_response(self, hash_secret_key):
        # Xác minh chữ ký từ VNPAY
        secure_hash = self.responseData['vnp_SecureHash']
        data_str = "&".join(
            f"{key}={value}" for key, value in sorted(self.responseData.items()) if key != 'vnp_SecureHash')
        calculated_hash = self.create_secure_hash(data_str, hash_secret_key)

        return secure_hash == calculated_hash
