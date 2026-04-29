import time
from smbus import SMBus

def distance_scan():
    bus = SMBus(1) # Þetta notar physical SDA og SCL pinnana á PI
    # (GPIO 2 og 3)
    i2c_addresses = [0x70, 0x71] # 
    while True:
        bus.write_byte_data(i2c_addresses[0], 0, 81) # Kveikji á vinstri skynjara
        bus.write_byte_data(i2c_addresses[1], 0, 81) # Kveikji á hægri skynjara
        print("Vinstri:",bus.read_byte_data(i2c_addresses[0], 2)," Hægri:",bus.read_byte_data(i2c_addresses[1],2))
    

distance_scan()
