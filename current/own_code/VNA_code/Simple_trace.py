
from RsInstrument import *
from time import sleep
from matplotlib import pyplot as plt
import numpy as np




RsInstrument.assert_minimum_version('1.50.0')
resource = 'TCPIP0::10.33.38.33::INSTR'  # VISA resource string for the device
znb = RsInstrument(resource, True, True, "SelectVisa='rs'")



for i in range(10):

    print(f'VISA Manufacturer: {znb.visa_manufacturer}')  # Confirm VISA package to be chosen
    znb.visa_timeout = 5000  # Timeout for VISA Read Operations
    znb.opc_timeout = 50000  # Timeout for opc-synchronised operations
    znb.instrument_status_checking = True  # Error check after each command, can be True or False
    znb.clear_status()  # Clear status register


    idnResponse = znb.query_str('*IDN?')
    print('Hello, I am ' + idnResponse)

    #znb.write_str("SWE:COUN 10000")
    #znb.write_str('SENSe1:FREQuency:STARt 1.0GHZ')  # Start frequency to 10 MHz
    #znb.write_str('SENSe1:FREQuency:STOP 1.5GHZ')  # Stop frequency to 1 GHz
    znb.write('SENSe1:SWEep:POINts ' + str(10000))

    znb.write_str("INIT1:IMMediate; *WAI")


    PcFile = r'/Users/zeshen/Desktop/static_test1_csv/csv_file' +str(i) +'.CSV'  # Name and path of the logfile


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
    while x < 10000:
        logfile.write(freq_tup[x] + ";")
        logfile.write(trace_tup[x] + "\n")
        x = x + 1
    logfile.close()

    print("finished writing")

    data = np.genfromtxt('/Users/zeshen/Desktop/static_test1_csv/csv_file' + str(i) + '.CSV', delimiter=";",
                         names=["x", "y"])

    plt.plot(data['x'], data['y'])

    plt.xlabel("freq [Hz]")
    plt.ylabel("Intensity [dB]")

    plt.savefig('/Users/zeshen/Desktop/static_test1_plot/plot_file' + str(i) + '.png', bbox_inches='tight')
    plt.clf()

    znb.get_total_time()

    znb.reset()  # reset session
    znb.get_total_time()
    # reset_time_statistics()

znb.close()

print()
print("I'm done. Data is written to ", PcFile)
