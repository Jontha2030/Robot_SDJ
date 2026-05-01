import time
from smbus import SMBus

bus = SMBus(1)
i2c_addresses = [0x70, 0x71]
while True:
    # Hægri skynjari
    bus.write_byte_data(i2c_addresses[0], 0, 0x51) # Segji hægri skynjara að byrja mælingu og skila cm (0x51 gerir það)
    # Nú getur i2c aðeins tekið við 8-bytes í einu, en SRF02 skylar 16-bytes fyrir hverja mælingu svo, henni er skipt í tvent, high og low
    time.sleep(0.07) # Þarf að bíða í a.m.k 65ms skv. datahseet á SRF02 til þess að hljóð hafi tíma til að ferðast
    high_h = bus.read_byte_data(i2c_addresses[0], 2) # Næ í high byte sem er fyrri partur merkis og er mikilvægastur (eins og 4*10 í 43)
    low_h = bus.read_byte_data(i2c_addresses[0], 3) # Næ í low hlutan sem er minna mikilvægur, oftast bara einingar (eins og 4 í 44)
    distance_h = high_h * 256 + low_h # Eins og að leggja saman 4*10 + 4, sem væri í base-10 (vinn í base-256 af því ég er með 8-bytes, 2^8 = 256)
    #print(distance_h) # ----- Debug

    # Vinstri skynjari. Fræðin er öll eins hér
    bus.write_byte_data(i2c_addresses[1], 0, 0x51)
    time.sleep(0.07)
    high_v = bus.read_byte_data(i2c_addresses[1], 2)
    low_v =  bus.read_byte_data(i2c_addresses[1], 3)
    distance_v = high_v * 256 + low_h
    
    print("Vinstri:",distance_v," Hægri:",distance_h) 
    
