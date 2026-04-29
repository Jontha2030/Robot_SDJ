import time
from smbus import SMBus

def distance_scan():
    bus = SMBus(1) # Þetta notar physical SDA og SCL pinnana á PI
    # (GPIO 2 og 3)
    i2c_addresses = [0x70, 0x71] # Listi yfir addressur á sensorum
    while True:
        bus.write_byte_data(i2c_addresses[0], 0, 81) # Kveikji á vinstri skynjara
        bus.write_byte_data(i2c_addresses[1], 0, 81) # Kveikji á hægri skynjara
        high_v = bus.read_byte_data(i2c_addresses[0],2)
        high_h = bus.read_byte_data(i2c_addresses[1],2)

        low_v = bus.read_byte_data(i2c_addresses[0],3)
        low_h = bus.read_byte_data(i2c_addresses[1],3)
        print("Vinstri:",high_v * 256 + low_v, 3," Hægri:", high_h * 256 + low_h)
        time.sleep(0.1)

distance_scan()
