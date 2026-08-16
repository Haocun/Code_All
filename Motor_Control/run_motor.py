from basic_utils import *
from pynput.keyboard import Key, Listener
from pynput import keyboard

abort = False

def on_press(key):
    if key == 'q':
        global abort 
        abort = True

def app():
    CYCLE_CHAR = 'a' # Input for cycling settings
    SET_CHAR = 'b'   # Input for setting angles
    TIME_CHAR = 'c'  # Input for setting the wait time between movements
    RES_CHAR = 'd'   # Input for setting resolution

    WAIT_TIME = 2    # Wait time
    RESOLUTION = 5   # Resolution


    # Setup
    if not init():
        print("Failed to open serial")
        return 1
    setup()
    print("\n")


    # Loop variables
    a = 'a'


    while a != 'q':
        print("\n")
        print(CYCLE_CHAR, "- Cycle various settings")
        print(SET_CHAR, "- Set an angle for each motor")
        print(TIME_CHAR, "- Wait time between angles (currently ", WAIT_TIME, ")")
        print(RES_CHAR, "- Set angular resolution of cycling (currently ", RESOLUTION, ")")
        print("q - Quit\n")

        a = input(">> ")

        if a == CYCLE_CHAR:
            print("Important note! \nTo abort, press and hold any key until main menu appears")
            input("(Enter anything or nothing to continue)")

            global abort 
            abort = False 

            
            # Move to beginning
            move(-180, 1)
            move(-180, 2)
            time.sleep(5)

            for i in range(-180, 180, RESOLUTION):
                move(i, 1)
                time.sleep(WAIT_TIME)

                for j in range(-180, 180, RESOLUTION):
                    move(j, 2)
                    time.sleep(WAIT_TIME)

                    # The event listener will be running in this block
                    with keyboard.Events() as events:
                        # Block at most one second
                        event = events.get(0.05)
                        if event is None:
                            1
                        else:
                            print('Aborting!')
                            abort = True

                    # Check for abort
                    if abort:
                        break

                    # built in wait for 360 spin
                    if j == -180:
                        time.sleep(0.8)

                if abort:
                    break
            ### End fors


            

        elif a == SET_CHAR:
            x = input("Motor 1 angle < ")
            y = input("Motor 2 angle < ")

            move(float(x), 1)
            move(float(y), 2)

        elif a == TIME_CHAR:
            WAIT_TIME = float(input("Wait time < "))

        elif a == RES_CHAR:
            RESOLUTION = int(input("Resolution < "))

        elif a == 'q':
            break

        else:
            print("Invalid input\n")
    ### End while
        
    

    print("\nFinished")
    deinit()
    return 0
### End app()


# Execution
app()