from basic_utils import *
#from pynput.keyboard import Key, Listener
#from pynput import keyboard
import csv
#from datetime import datetime
from ctypes import cdll,c_long, c_ulong, c_uint32,byref,create_string_buffer,c_bool,c_char_p,c_int,c_int16,c_double, sizeof, c_voidp
from TLPMX import TLPMX
import time
import os

from TLPMX import TLPM_DEFAULT_CHANNEL


def app():
    CYCLE_CHAR = 'c' # Input for cycling settings
    SET_CHAR = 's'   # Input for setting angles
    TIME_CHAR = 't'  # Input for setting the wait time between movements
    RES_CHAR = 'r'   # Input for setting resolution

    WAIT_TIME = 0.3    # Wait time
    RESOLUTION = 1   # Resolution

    # start and stop of motor 1, start and stop of motor 2
    ranges = [-200, 200, -200, 200]


    port = input("Enter port: ")

    # Setup
    if not init(port):
        print("Failed to open serial")
        return 1
    setup()
    print("\n")


    # Loop variables
    a = 'a'


    while a[0] != 'q':
        print("\n")
        print(CYCLE_CHAR, "- Cycle various settings")
        print(SET_CHAR, "- Set an angle for each motor")
        print(TIME_CHAR, "- Wait time between angles (currently ", WAIT_TIME, ")")
        print(RES_CHAR, "- Set angular resolution of cycling (currently ", RESOLUTION, ")")
        print("q - Quit\n")

        a = input(">> ")

        if a[0] == CYCLE_CHAR:


            #######         TLPM SETUP            #########
            # Find connected power meter devices.
            tlPM = TLPMX()
            deviceCount = c_uint32()
            tlPM.findRsrc(byref(deviceCount))

            print("Number of found devices: " + str(deviceCount.value))
            print("")

            resourceName = create_string_buffer(1024)

            for i in range(0, deviceCount.value):
                tlPM.getRsrcName(c_int(i), resourceName)
                print("Resource name of device", i, ":", c_char_p(resourceName.raw).value)
            print("")
            tlPM.close()

            # Connect to last device.
            tlPM = TLPMX()
            tlPM.open(resourceName, c_bool(True), c_bool(True))

            message = create_string_buffer(1024)
            tlPM.getCalibrationMsg(message,TLPM_DEFAULT_CHANNEL)
            print("Connected to device", i)
            print("Last calibration date: ",c_char_p(message.raw).value)
            print("")

            time.sleep(2)

            # Set wavelength in nm.
            wavelength = c_double(1550)
            tlPM.setWavelength(wavelength,TLPM_DEFAULT_CHANNEL)

            # Enable auto-range mode.
            # 0 -> auto-range disabled
            # 1 -> auto-range enabled
            tlPM.setPowerAutoRange(c_int16(1),TLPM_DEFAULT_CHANNEL)

            # Set power unit to Watt.
            # 0 -> Watt
            # 1 -> dBm
            tlPM.setPowerUnit(c_int16(0),TLPM_DEFAULT_CHANNEL)

            ####                MOTOR CYCLING           ########
            time.sleep(2)
            print("Important note! \nTo abort, press and hold any key until main menu appears")
            ans = input("Use custom range? (y/n)")
            while True:
                if ans == 'y':
                    ranges[0] = float(input("Motor 1 lower bound"))
                    ranges[1] = float(input("Motor 1 upper bound"))
                    if ranges[0] > ranges[1]:
                        print("Lower bound and upper bound incorrect order")
                        continue
                    ranges[2] = float(input("Motor 2 lower bound"))
                    ranges[3] = float(input("Motor 2 upper bound"))
                    if ranges[2] > ranges[3]:
                        print("Lower bound and upper bound incorrect order")
                        continue
                    break
                if ans == 'n':
                    break


            abort = False 

            path = r"C:\Users\admin\Documents\Data\hwp"
            filename = "dataV_t0.3_r0.05_mot2_0807.csv"
            filepath = os.path.join(path, filename)

            ###                 CREATE CSV              #######
            with open(filepath, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                #writer.writerow(["Time","Motor 2 Angle (deg)", "Motor 1 Angle (deg)","Wavelength(nm)","Power (W)"])
                writer.writerow(["Motor 2 Angle (deg)","Power (W)"])
                csvfile.flush()

            try:
                # Move to beginning
                move(ranges[0], 1)
                move(ranges[2], 2)
                time.sleep(5)

                #Time of Experiment
                time_offset = 0.165
                time_per_point = (WAIT_TIME+time_offset)/RESOLUTION
                total_time = (float(ranges[1])-float(ranges[0]))*(float(ranges[3])-float(ranges[2]))*time_per_point
                end_time = time.strftime("%I:%M:%S %p", time.localtime(time.time() + total_time))
                print("Estimated Completion Time:", end_time)

                i = ranges[0]
                while i < ranges[1]:
                    move(i, 1)             
                    time.sleep(WAIT_TIME)

                    j = ranges[2]
                    while j < ranges[3]:
                        move(j, 2)
                        time.sleep(WAIT_TIME)

                        # built in wait for 360 spin
                        #if j == -180:
                        #    time.sleep(0.8)
                            
                        power =  c_double()
                        tlPM.measPower(byref(power),TLPM_DEFAULT_CHANNEL)
                        with open(filepath, 'a', newline='') as csvfile:
                            writer = csv.writer(csvfile, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
                            #writer.writerow([datetime.now()] + [i] + [j] + [wavelength.value] + [power.value])
                            writer.writerow([j] + [power.value])

                        j += RESOLUTION
                    break

                    if abort:
                        break
                    
                    i += RESOLUTION

            except KeyboardInterrupt:
                print("\nAborted by user (Ctrl+C)")

            finally:
                tlPM.close()
                ### End fors

            

        elif a[0] == SET_CHAR:
            x = input("Motor 1 angle < ")
            y = input("Motor 2 angle < ")

            move(float(x), 1)
            move(float(y), 2)

        elif a[0] == TIME_CHAR:
            WAIT_TIME = float(input("Wait time < "))

        elif a[0] == RES_CHAR:
            RESOLUTION = float(input("Resolution < "))

        elif a[0] == 'q':
            break

        elif a[0] == 'r':
            print(read_one())

        else:
            print("Invalid input\n")
    ### End while
        
    

    print("\nFinished")
    deinit()
    return 0
### End app()


# Execution
app()