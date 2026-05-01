import time
from smbus import SMBus

bus = SMBus(1)
i2c_addresses = [0x70, 0x71]
while 1:
	bus.write_byte_data(i2c_addresses[0], 0, 0x51) # Tell sensor to scan in mm
        # Nú getur i2c aðeins tekið við 8-bytes í einu, en SRF02 skylar 16-bytes fyrir hverja mælingu
        # svo, henni er skipt í tvent, high og low
        time.sleep(0.07) # Þarf að bíða í a.m.k 65ms skv. datahseet á SRF02 til þess að hljóð hafi tíma til að ferðast
	high_h = bus.read_byte_data(i2c_addresses[0], 2) # Næ í high byte sem er fyrri partur merkis og er mikilvægastur (eins og 4*10 í 43)
	low_h = bus.read_byte_data(i2c_addresses[0], 3) # Næ í low hlutan sem er minna mikilvægur, oftast bara einingar (eins og 4 í 44)
	distance_h = high_h * 256 + low_h # Eins og að leggja saman 4*10 + 4, sem væri í base-10 (vinn í base-256 af því ég er með 8-bytes, 2^8 = 256)
	#print(distance_h) # ----- Debug

	bus.write_byte_data(i2c.
