import time
from smbus import SMBus
from __init__ import lock, SRF02_data


def distance_scan():
    bus = SMBus(1) # Þetta notar physical SDA og SCL pinnana á PI
    # (GPIO 2 og 3)
    i2c_addresses = [0x70, 0x71] # Listi yfir addressur á sensorum
    sample_count = 1
    distance_h = 0
    distance_v = 0
    SRF02_data["left"] = distance_v
    SRF02_data["right"] = distance_h
    while True:
        # Logic fyrir hægri skynjara
        try:
            bus.write_byte_data(i2c_addresses[0], 0, 0x51) # Kveikji á vinstri skynjara
            time.sleep(0.07)
            high_h = bus.read_byte_data(i2c_addresses[1],2) # Mikilvægari hluti merkis sem kemur útkomu upp að "tuginum" eins og 4*10 í 45
            low_h  = bus.read_byte_data(i2c_addresses[1],3) # Einingarnar í útkomutöluni, eins og 5 í 45
            distance_h += high_h * 256 + low_h # Virkar eins og 4*10 + 2, þar sem high er 4 margf. m. 10 og low er 2, eða, einingarnar (nota 256 af því er með 8-bytes, 2^8 = 256)
            #print(distance_h) # ----Debug
        except Exception as e:
            print(f"Sensor error {hex(i2c_addresses[0])}: {e}")

        # Logic fyrir vinstri skynjara
        try:
            bus.write_byte_data(i2c_addresses[1], 0, 0x51) # Kveikji á hægri skynjara
            time.sleep(0.07)
            high_v = bus.read_byte_data(i2c_addresses[0],2)
            low_v = bus.read_byte_data(i2c_addresses[0],3)
            distance_v += high_v * 256 + low_v
            #print(distance_v) # ----Debug
            sample_count += 1
        except Exception as e:
            print(f"Sensor error {hex(i2c_addresses[1])}: {e}")

        if sample_count%10 == 0:
            with lock:
                SRF02_data["left"] = distance_v
                SRF02_data["right"] = distance_h
            distance_v = 0
            distance_h = 0
        else:
            pass
            