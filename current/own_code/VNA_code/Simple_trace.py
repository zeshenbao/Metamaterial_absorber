
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



def average():
    data1 = np.genfromtxt('/Users/zeshen/Desktop/static_test1_csv/csv_file0.CSV', delimiter=";")

    data1 = np.delete(data1, (0), axis=0)
    data2 = np.genfromtxt('/Users/zeshen/Desktop/static_test1_csv/csv_file1.CSV', delimiter=";")

    data2 = np.delete(data2, (0), axis=0)

    #print(data2["x"])
    sum = (data1+data2)


    PcFile = r'/Users/zeshen/Desktop/static_test1_csv/csv_file0.CSV'

    logfile = open(PcFile, "w")
    logfile.write("Frequ / Hz; Atten. / db; Atten.2 / db")
    logfile.write("\n")
    x = 0
    while x < points:
        logfile.write(str(sum[x][0]) + ";")
        logfile.write(str(sum[x][1]) + ";")
        logfile.write(str(sum[x][2]) + "\n")
        x = x + 1
    logfile.close()

    return sum


pc_file = r'/Users/zeshen/Desktop/Wband_setup_pc.znxml'
instrument_file = r'C:\Users\Instrument\Desktop\Wband_setup.znxml'




points = 201


comcheck()
comprep()

iter = 10000

for i in range(iter):

    if i % 100 == 0:
        print("sweep nr" + str(i))

    znb.write_str_with_opc("SYSTEM:DISPLAY:UPDATE ON")

    znb.write('SENSe1:SWEep:POINts ' + str(points))  # Set number of sweep points to the defined number
    znb.write_str('CALCulate1:PARameter:MEASure "Trc1", "b4"')  # Measurement now is S21
    znb.write_str('CALCulate1:PARameter:MEASure "Trc2", "b2"')  # Measurement now is S21


    znb.write_str("INIT1:IMMediate; *OPC")

    if i == 0:
        PcFile = r'/Users/zeshen/Desktop/static_test1_csv/csv_file0.CSV'  # Name and path of the logfile
        file_write()

        PcFile = r'/Users/zeshen/Desktop/static_test1_csv/csv_file_start.CSV'  # Name and path of the logfile
        file_write()

    elif i >= 1:
        PcFile = r'/Users/zeshen/Desktop/static_test1_csv/csv_file1.CSV'  # Name and path of the logfile
        file_write()
        average()


    #print(znb.get_total_time())
#data_s = np.genfromtxt('/Users/zeshen/Desktop/static_test1_csv/csv_file_start.CSV', delimiter=";")
data = np.genfromtxt('/Users/zeshen/Desktop/static_test1_csv/csv_file0.CSV', delimiter=";")/iter


#plt.plot(data_s[:, 0], data_s[:, 1], "r")
plt.plot(data[:, 0], data[:, 1], "b")
plt.plot(data[:, 0], data[:, 2], "g")

plt.xlabel("freq [Hz]")
plt.ylabel("Intensity [dB]")

plt.savefig('/Users/zeshen/Desktop/static_test1_plot/plot_file_avg.png', bbox_inches='tight')
plt.clf()




    ## Reset might not be needed
    #znb.reset()  # reset session
    #znb.write_str_with_opc(f'MMEM:LOAD:STAT 1,"{instrument_file}"')


    #znb.get_total_time()
    # reset_time_statistics()
    # Load the transferred setup



znb.close()

print()
print("I'm done. Data is written to ", PcFile)
