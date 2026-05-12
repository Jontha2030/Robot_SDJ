from evdev import InputDevice, ecodes
from motor import forward, backwards, right, left, stop
from play import play_random, stop_playing
from __init__ import Button_Press
import avoid_obstacles
from fpv_server_webxr_headlocked import start_server
from servo import cameraservominus, cameraservoplus
from SRF02 import distance_scan
import threading


# -------- LÝSING ---------
# Þetta er aðal forritið fyrir róbótinn sem kallar á öll undir forritin 
# Því er stýrt af notanda með PS4 fjarstýringu. 
# Það er hægt að 
# 1) Keyra frjálst
# 2) Láta róbót keyra sjálfan og forðast hindarnir
# 3) Spila lög

# -------- FASTAR ---------
SPEED_R = 200
SPEED_L = 180

# Þetta fall sér um að ræsa hluta forritsins sem eiga að vera í gangi alltaf.
# Það eru SRF02 fjarlægðarskynjararnir og allt sem er á bakvið Pi myndavélina.
def initialize_components():
    SRF02Thread = threading.Thread(target=distance_scan, daemon=True) # SRF02 forritið er keyrt á sér þráð þar sem það
    # virkar sem endalaus while loopa sem er stanslaust að mæla fjarlæg. Síðan er hægt að virkja önnur forrit sem nýta
    # þessar mælingar
    fpvThread = threading.Thread(target=start_server, daemon=True) # Þessi þráður er fyrir vefsíðuna sem Pi'in hýsir og
    # sendir stanslaust á myndir frá Pi myndavélinni
    SRF02Thread.start()
    fpvThread.start()

#Fall fyrir controllerinn sem er aðal partur kerfisns
def controller_sturcture():
    try:
        # Sæki tengingu við fjarstýringu (þarf að vera búið að tengjast við hana með Bluetooth)
        dev = InputDevice("/dev/input/event4")

        #Skillgreini takka
        BTN_X = 304   
        BTN_CIRCLE = 305
        BTN_TRIANGLE = 307
        BTN_SQUARE = 308

        BTN_L1 = 310
        BTN_R1 = 311
        BTN_L2 = 312
        BTN_R2 = 313
        BTN_R3 = 318

        print("Controller ready")

            #Ef ýtt er á taka þá gerist eitthvað
        for event in dev.read_loop():
            if event.type == ecodes.EV_KEY and event.value == 1:
                if event.code == BTN_X:
                    # Bakkar
                    backwards(SPEED_L-8, SPEED_R) # Þurfum mað laga hraðan hér af þvi hann fer ekki eins afturábak og áfram
                elif event.code == BTN_CIRCLE:
                    # Beygjir til hægri
                    right(SPEED_L, SPEED_R)
                elif event.code == BTN_TRIANGLE:
                    # Keyrir beint áfram
                    forward(SPEED_L, SPEED_R)
                elif event.code == BTN_SQUARE:
                    # Beygjir til vinstri
                    left(SPEED_L, SPEED_R)
                elif event.code == BTN_R1:
                    # Stoppar mótóra
                    stop()
                elif event.code == BTN_R2:
                    print("R2 pressed")
                elif event.code == BTN_L1:
                    # Ef ýtt er á þennan takka er sjálfstýringar forritið keyrt 
                    Button_Press["state"] = False
                    print("Entering AUTO-MODE...")
                    automodeThread = threading.Thread(target=avoid_obstacles.avoid_obstacles, daemon=True) # Þá er bara kveikt á sér
                    # þræði til þess að það sé ennþá hægt að hlusta á takka fjarstýringar
                    automodeThread.start()
                elif event.code == BTN_L2:
                    # Ef ýtt er á þennan takka er slökkt á sjálfstýringu
                    Button_Press["state"] = True
                    stop()
                    stop_playing()
                    automodeThread.join(timeout=2) # Geng frá þræði
                    
                elif event.code == BTN_R3:
                    print("R3 pressed")


            #Þetta er fyrir D-pad
            elif event.type == ecodes.EV_ABS:
                if event.code == ecodes.ABS_HAT0Y:
                    if event.value == -1: # D-pad up
                        # Kveikir á lagi
                        play_random()
                    elif event.value == 1: # D-pad down
                        # Slekkur á lagi
                        stop_playing()

                elif event.code == ecodes.ABS_HAT0X:
                    if event.value == -1: # D-pad left
                        # Færir servo fyrir myndavél 30 gráður til vinstri
                        cameraservoplus()
                    elif event.value == 1: # D-pad right
                        # Færir servo fyrir myndavél 30 gráður til hægri
                        cameraservominus()
                        
    # Hér er gripið það þegar notandi slekkur á forriti og séð til þess að öllum ferlum sé hætt
    except KeyboardInterrupt:
        print("Notandi slökkti á forriti")
        stop_playing()
        stop()
        Button_Press["state"] = False
    # Hér er gripið það þegar einhvað ófyrirséð fer úrskeiðis og séð til þess að öllu ferlum sé hætt
    except Exception as mainVilla:
        print("Einhvað fór úrskeiðis\n", mainVilla)
        stop_playing()
        stop()
        Button_Press["state"] = False


if __name__ == "__main__":
    initialize_components()
    controller_sturcture()
