def count_fee(fee):
    total_fee = 0

    if fee:
        for c in fee.values():
            total_fee += c['fee']
    return {
        "total_fee" : total_fee
    }