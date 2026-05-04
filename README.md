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
pip install adafruit_circuitpython_servokit
```

Síðan, til þess að tengjast fjarstýringu, þarf að nota bluetoothctl:
```bash
bluetoothctl
```
<<<<<<< HEAD
Þá keyrist umhverfi sem byrtir fullt af tölum en þar er einnig hægt að keyra skipanir.
Keyrið eftirfarandi:
=======
>>>>>>> 0f79371 (Update README with Bluetooth connection instructions)
```bash
power on
agent on
default-agent
scan on
```
Síðan er ehv. veginn fundið addressuna á controller'num og gert
```bash
pair "Address'a"
connect "Address'a"
trust "Address'a"
quit
```


Þá ætti að vera hægt að keyra alla kóðana hérna.
(Muna bara alltaf að "activate'a" þegar maður opnar tölvuna aftur)
