"""
多态继承版本
"""

# 规范接口, 不实现任何功能
class Pay():
    def pay(self):
        pass


# 支付宝支付
class AliPay(Pay):
    def pay(self):
        print('阿里Pay')


# 微信支付
class WeixinPay(Pay):
    def pay(self):
        print('微信Pay')


# 银联支付
class YinlianPay(Pay):
    def pay(self):
        print('银联Pay')


if __name__ == '__main__':
    # 测试支付多态应用

    a = AliPay()
    w = WeixinPay()
    y = YinlianPay()

    a.pay()
    w.pay()
    y.pay()
