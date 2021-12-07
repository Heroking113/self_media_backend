from decimal import Decimal

if __name__ == '__main__':

    s = '123.357832348'
    d = Decimal(str(round(float(s), 2)))
    # t = round(float(d)*100, 1)
    print(d, type(d), str(d), float(d))
