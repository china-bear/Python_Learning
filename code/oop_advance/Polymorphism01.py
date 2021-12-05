# 多态普通版本
class Pay():
    def pay(self, obj):
        obj.pay()


# 支付宝支付
class AliPay():
    def pay(self):
        print('阿里Pay')


# 微信支付
class WeixinPay():
    def pay(self):
        print('微信Pay')


# 银联支付
class YinlianPay():
    def pay(self):
        print('银联Pay')


if __name__ == '__main__':
    # 测试支付多态应用
    pay = Pay()
    pay.pay(AliPay())
    pay.pay(WeixinPay())
    pay.pay(YinlianPay())
