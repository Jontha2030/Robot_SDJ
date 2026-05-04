Til þess að geta keyrt róbótinn þarf eftirfarandi Python pakka:

1) smbus
2) evdev
3) pygame
4) adafruit_servokit


Til þess að hlaða þeim inn í tölvuna sína er best að vera í "virtual environment".
(Skiptir í raun ekki máli í hvaða möppu það er búið til)
```bash
python -m venv "Nafn á virtual environemnt"
```
Síðan þarf að "activate'a" það
```bash
source "Nafn á virtual environemnt"/bin/activate
```
Síðan er hægt að hlaða inn öllum pökkunum með pip:
```bash
pip install smbus
pip install evdev
pip install pygame
pip install adafruit_servokit
```

Þá ætti að vera hægt að keyra alla kóðana hérna.
(Muna bara alltaf að "activate'a" þegar maður opnar tölvuna aftur)
