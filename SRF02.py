import time
from smbus import SMBus # Þetta er pakkinn sem sér um fjarlægðarskynjarana
from __init__ import lock, SRF02_data # Þetta er threads

# ------------ LÝSING -----------------
# Þetta skjal er bara fall sem sér um að nota fjarlægðarskynjarana (SRF02).
# Þeir eru I2C skynjarar og tengjast beint við SCL(GPIO 3) og SDA(GPIO 2) pin'a á Pi'inu
# Það sem forritið gerir er að lesa gögn frá skynjurum, sem hægt er að láta skila fjarlægð í sentímetrum (skv. bækling SRF02)
# Fjarlægðin er skrifuð inná þráð (thread) sem main.py skjalið vinnur síðan úr

# ---------- GLOBAL BREYTUR ------------
SAMPLE_COUNT = 0 # Til þess að telja hver margar mælingar hafa verið teknar í viðkomandi umferð (ef safnað er fleirum en einni)
N_SAMPLES = 1 # Hægt að velja hve mörgum mælingum á að safna
I2C_ADDRESSES = [0X70, 0X71] # Listi yfir addressur á sensorum (fundið með i2cdetect -y 1, en þeir þurfa þá væntanlega að vera tengdir)


def distance_scan():
    bus = SMBus(1) # Þetta notar physical SDA og SCL pinnana á PI. allt með bus héðan frá er að nota smbus pakkann
    distance_h = 0
    distance_v = 0
    # Hér eru þráða breyturnar, en þær geyma mælda fjarlægð skynjara
    SRF02_data["left"] = distance_v
    SRF02_data["right"] = distance_h
    while True:
        # Logic fyrir hægri skynjara
        try:
            bus.write_byte_data(I2C_ADDRESSES[0], 0, 0x51) # Kveikji á vinstri skynjara
            time.sleep(0.07)
            high_h = bus.read_byte_data(I2C_ADDRESSES[0],2) # Mikilvægari hluti merkis sem kemur útkomu upp að "tuginum" eins og 4*10 í 45
            low_h  = bus.read_byte_data(I2C_ADDRESSES[0],3) # Einingarnar í útkomutöluni, eins og 5 í 45
            distance_h += high_h * 256 + low_h # Virkar eins og 4*10 + 2, þar sem high er 4 margf. m. 10 og low er 2, eða, einingarnar (nota 256 af því er með 8-bytes, 2^8 = 256)
            #print(distance_h) # ----Debug
        except Exception as e:
            print(f"Sensor error {hex(I2C_ADDRESSES[0])}: {e}")

        # Logic fyrir vinstri skynjara (allt það sama og með hægri)
        try:
            bus.write_byte_data(I2C_ADDRESSES[1], 0, 0x51) # Kveikji á hægri skynjara
            time.sleep(0.07)
            high_v = bus.read_byte_data(I2C_ADDRESSES[1],2)
            low_v = bus.read_byte_data(I2C_ADDRESSES[1],3)
            distance_v += high_v * 256 + low_v
            #print(distance_v) # ----Debug
        except Exception as e:
            print(f"Sensor error {hex(I2C_ADDRESSES[1])}: {e}")

        SAMPLE_COUNT += 1
        if SAMPLE_COUNT != 0 and SAMPLE_COUNT%N_SAMPLES == 0: # Þetta lætur "distance" breyturnar safna nokkrum mælingum upp að völdum fjölda, og skilar síðan meðaltali
            with lock:
                SRF02_data["left"] = distance_v/N_SAMPLES
                SRF02_data["right"] = distance_h/N_SAMPLES
            distance_v = 0
            distance_h = 0
            SAMPLE_COUNT = 0
        else:
            pass
            