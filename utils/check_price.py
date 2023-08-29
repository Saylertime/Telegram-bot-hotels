def check_price(price):
    if price.isdigit() and int(price) > 0:
        return True
    return False
