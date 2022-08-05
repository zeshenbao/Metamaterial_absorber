
from RsInstrument import *
from time import sleep
from matplotlib import pyplot as plt
import numpy as np




RsInstrument.assert_minimum_version('1.50.0')
resource = 'TCPIP0::10.33.38.33::INSTR'  # VISA resource string for the device
znb = RsInstrument(resource, True, False, "SelectVisa='rs'")


def comprep():
    """Preparation of the communication (termination, etc...)"""

    print(f'VISA Manufacturer: {znb.visa_manufacturer}')  # Confirm VISA package to be chosen
    znb.visa_timeout = 600000  # Timeout for VISA Read Operations
    znb.opc_timeout = 600000  # Timeout for opc-synchronised operations
    znb.instrument_status_checking = True  # Error check after each command, can be True or False
    znb.clear_status()  # Clear status register

def close():
    """Close the VISA session"""

    znb.close()


def comcheck():
    """Check communication with the device"""

    # Just knock on the door to see if instrument is present
    idnResponse = znb.query_str('*IDN?')
    print('Hello, I am ' + idnResponse)

def file_write():
    # open logfile
    logfile = open(PcFile, "w")
    # write table headline
    logfile.write("Frequ / Hz; Atten. / db; Atten.2 / db")
    logfile.write("\n")
    points_count = znb.query_int('SENSe1:SWEep:POINts?')  # Request number of frequency points
    trace_data = znb.query_str('CALC1:DATA:TRAC? "Trc1", FDAT')  # Get measurement values for complete trace
    trace_data2 = znb.query_str('CALC1:DATA:TRAC? "Trc2", FDAT')  # Get measurement values for complete trace
    trace_tup = tuple(map(str, trace_data.split(',')))  # Convert the received string into a tuple
    trace_tup2 = tuple(map(str, trace_data2.split(',')))  # Convert the received string into a tuple
    freq_list = znb.query_str('CALC:DATA:STIM?')  # Get frequency list for complete trace
    freq_tup = tuple(map(str, freq_list.split(',')))  # Convert the received string into a tuple

    # Now write frequency and magnitude for each point and close the file if done
    x = 0
    while x < points:
        logfile.write(freq_tup[x] + ";")
        logfile.write(trace_tup[x] + ";")
        logfile.write(trace_tup2[x] + "\n")
        x = x + 1
    logfile.close()



pc_file = r'/Users/zeshen/Desktop/Wband_setup_pc.znxml'
instrument_file = r'C:\Users\Instrument\Desktop\Wband_setup.znxml'




points = 50000


comcheck()
comprep()

for i in range(10):

    print("sweep nr" +str(i))
    znb.write_str_with_opc("SYSTEM:DISPLAY:UPDATE ON")

    znb.write('SENSe1:SWEep:POINts ' + str(points))  # Set number of sweep points to the defined number
    znb.write_str('CALCulate1:PARameter:MEASure "Trc1", "b4"')  # Measurement now is S21
    znb.write_str('CALCulate1:PARameter:MEASure "Trc2", "b2"')  # Measurement now is S21


    znb.write_str("INIT1:IMMediate; *OPC")


    PcFile = r'/Users/zeshen/Desktop/static_test1_csv/csv_file' +str(i) +'.CSV'  # Name and path of the logfile

    file_write()

    data = np.genfromtxt('/Users/zeshen/Desktop/static_test1_csv/csv_file' + str(i) + '.CSV', delimiter=";",
                         names=["x", "y", "z"])

    plt.plot(data['x'], data['y'])
    plt.plot(data['x'], data['z'])

    plt.xlabel("freq [Hz]")
    plt.ylabel("Intensity [dB]")

    plt.savefig('/Users/zeshen/Desktop/static_test1_plot/plot_file' + str(i) + '.png', bbox_inches='tight')
    plt.clf()




    ## Reset might not be needed
    #znb.reset()  # reset session
    #znb.write_str_with_opc(f'MMEM:LOAD:STAT 1,"{instrument_file}"')


    #znb.get_total_time()
    # reset_time_statistics()
    # Load the transferred setup

    print(znb.get_total_time())

znb.close()

print()
print("I'm done. Data is written to ", PcFile)