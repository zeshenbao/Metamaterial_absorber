from RsInstrument import *
from time import sleep
from matplotlib import pyplot as plt
import numpy as np




def com_prep():
    """Preparation of the communication (termination, etc...)"""

    print(f'VISA Manufacturer: {znb.visa_manufacturer}')  # Confirm VISA package to be chosen
    znb.visa_timeout = 500000  # Timeout for VISA Read Operations
    znb.opc_timeout = 500000  # Timeout for opc-synchronised operations
    znb.instrument_status_checking = True  # Error check after each command, can be True or False
    znb.clear_status()  # Clear status register


def close():
    """Close the VISA session"""

    znb.close()


def com_check():
    """Check communication with the device"""
    print("test")
    # Just knock on the door to see if instrument is present
    idnResponse = znb.query_str('*IDN?')
    sleep(1)
    print('Hello, I am ' + idnResponse)


def meas_setup():
    """Assign more detailed settings and segments to the channels"""
    print("start measure")
    #
    # Setup for CH1
    #

    #znb.write_int('SWEEP:COUNT ', 10)
    znb.write_str('SENSe1:FREQuency:STARt 0.10GHZ')  # Start frequency to 10 MHz
    znb.write_str('SENSe1:FREQuency:STOP 2.0GHZ')  # Stop frequency to 1 GHz
    znb.write('SENSe1:SWEep:POINts ' + str(points))  # Set number of sweep points to the defined number
    #znb.write_str('DISPlay:WINDow1:TRACe1:Y:SCALe:AUTO ONCE')  # Enable auto scaling for trace 1
    #znb.write_str('*WAI')
    znb.write_str_with_opc('SENSe:SWEep:TIME:AUTO ON')
    znb.write_str('CALCulate1:PARameter:MEASure "Trc1", "S21"')  # Measurement now is S21
    #sleep(10)  # It will take some time to perform a complete sweep - wait for it

    znb.write_str_with_opc("INIT1")  # Set single sweep mode and stop acquisition

    print("end measure")

def file_write():
    # open logfile

    print("start writing")
    logfile = open(PcFile, "w")
    # write table headline
    logfile.write("Frequ / Hz; Atten. / db")
    logfile.write("\n")
    points_count = znb.query_int('SENSe1:SWEep:POINts?')  # Request number of frequency points
    trace_data = znb.query_str('CALC1:DATA? FDAT')  # Get measurement values for complete trace
    trace_tup = tuple(map(str, trace_data.split(',')))  # Convert the received string into a tuple
    freq_list = znb.query_str('CALC:DATA:STIM?')  # Get frequency list for complete trace
    freq_tup = tuple(map(str, freq_list.split(',')))  # Convert the received string into a tuple

    # Now write frequency and magnitude for each point and close the file if done
    x = 0
    while x < points:
        logfile.write(freq_tup[x] + ";")
        logfile.write(trace_tup[x] + "\n")
        x = x + 1
    logfile.close()

    print("finished writing")






RsInstrument.assert_minimum_version('1.50.0')
resource = 'TCPIP0::10.33.38.33::INSTR'  # VISA resource string for the device
#resource = 'TCPIP0::test::INSTR'
points = 50001  # Number of sweep points
znb = RsInstrument(resource, True, True, "SelectVisa='rs'")

for i in range(10):
    print(i)

    sleep(1)  # Eventually add some waiting time when reset is performed during initialization

    PcFile = r'/Users/zeshen/Desktop/measurements/test_VNA' +str(i) +'.CSV'  # Name and path of the logfile
    com_prep()
    #com_check()
    meas_setup()
    file_write()

    data = np.genfromtxt('/Users/zeshen/Desktop/measurements/test_VNA' +str(i) +'.CSV', delimiter=";", names=["x", "y"])

    plt.plot(data['x'], data['y'])

    plt.xlabel("freq [Hz]")
    plt.ylabel("Intensity [dB]")

    plt.savefig('/Users/zeshen/Desktop/measurementspic/test_VNA_pic' +str(i) +'.png', bbox_inches='tight')
    plt.clf()

    znb.get_total_time()

    znb.reset() #reset session
    znb.get_total_time()
    #reset_time_statistics()
close()

print()
print("I'm done. Data is written to ", PcFile)
