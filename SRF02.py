import time
from smbus import SMBus

def distance_scan():
    bus = SMBus(1) # Þetta notar physical SDA og SCL pinnana á PI
    # (GPIO 2 og 3)
    i2c_addresses = [0x70, 0x71] # Listi yfir addressur á sensorum
    while True:
        bus.write_byte_data(i2c_addresses[0], 0, 0x51) # Kveikji á vinstri skynjara
        time.sleep(0.07)
        high_h = bus.read_byte_data(i2c_addresses[1],2) # Mikilvægari hluti merkis sem kemur útkomu upp að "tuginum" eins og 4*10 í 45
        low_h  = bus.read_byte_data(i2c_addresses[1],3) # Einingarnar í útkomutöluni, eins og 5 í 45
        distance_h = high_h * 256 + low_h # Virkar eins og 4*10 + 2, þar sem high er 4 margf. m. 10 og low er 2, eða, einingarnar (nota 256 af því er með 8-bytes, 2^8 = 256)
        #print(distance_h) # ----Debug

        bus.write_byte_data(i2c_addresses[1], 0, 0x51) # Kveikji á hægri skynjara
        time.sleep(0.07)
        high_v = bus.read_byte_data(i2c_addresses[0],2)
        low_v = bus.read_byte_data(i2c_addresses[0],3)
        distance_v = high_v * 256 + low_v
        #print(distance_v) # ----Debug
        print("Vinstri:", distance_v," Hægri:", distance_h) # ----Debug
        if distance_v < 25:
            print("Stop vinstri!!!")
        elif distance_h < 25:
            print("Stop hægri!!!")

distance_scan()
