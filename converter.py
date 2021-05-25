import cryptocompare

diction = cryptocompare.get_price('BTC')

print(type(diction['BTC']['EUR']))

hello = ''

if not hello:
    print("Empty is falsy!")

if not cryptocompare.get_price('DOES NOT EXIST'):
    print("Got an Error")
else:
    print("Success!")