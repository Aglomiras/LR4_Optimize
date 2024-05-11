capacity = 16000  # емкость персонального энергоблока (ПЭБ)
initCharge = 6000  # уровень заряда ПЭБ

'''Почасовая цена за электроэнергию'''
priceSchedule = [1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
                 2.0, 3.0, 5.0, 5.0, 5.0, 4.5,
                 3.0, 3.0, 3.0, 3.0, 4.5, 5.0,
                 7.0, 9.0, 11.0, 12.0, 8.0, 4.0]

'''Почасовое потребление электроэнергии'''
loadSchedule = [480, 320, 320, 360, 360, 360,
                420, 920, 1200, 720, 680, 720,
                800, 820, 960, 1200, 1380, 1380,
                1520, 1800, 1920, 1920, 1640, 1020]

constantLoad = 400  # потребитель с постоянной нагрузкой
targetCharge = 4800  # конечный заряд аккумулятора

basis = 0
for i in range(len(priceSchedule)):
    basis = basis + loadSchedule[i]

basis1 = 0
for i in range(len(priceSchedule)):
    basis1 = basis1 - -4000*priceSchedule[i]

print(basis)
print(basis1)

asdfgh = [1,1,1,1,1]
qwerty = [2,2,2,2,2]
zxcvbn = [3,3,3,3,3]
ppoopo = [4,4,4,4,4]

ofdsa = []
ofdsa.append(asdfgh)
ofdsa.append(qwerty)
ofdsa.append(zxcvbn)
ofdsa.append(ppoopo)

for ch1, ch2 in zip(ofdsa[::2], ofdsa[1::2]):
    print(ch1, ch2)