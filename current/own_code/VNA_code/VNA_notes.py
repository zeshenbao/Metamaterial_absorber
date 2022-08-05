


"""
SCPI commands good to know:
* SENS # used for data measurement
* CALC # used for data retrieval/processing
page 1592 for sync



Specific SCPI commands:

calibration:
* 7.3.1.2 CALCulate:CALValidate:CHARacteriza <String> # Selects the CalU characterization to be used for the cal validation.
* CALCulate:CALValidate:RUN # Runs the cal validation with its configured settings.
* We can also select limits to magnitude and phase

data:
* 7.3.1.3 CALCulate:DATA... 3 used to get data
* We can also select which data to get. FDAT, SDAT, CONT sweep off.
* CALCulate<Ch>:DATA:CHANnel:ALL? <Format> # Reads the current response values of **all traces** of the selected channel.
* CALCulate<Chn>:DATA? <Format> # The query reads the response values of the selected channel's **active** trace or reads
error terms of the selected channel.

znb commands:

* znb.close() # close session
* znb.query_str('*IDN?') # check VNA id
* RsInstrument.assert_minimum_version('1.50.0') # check version
* resource = 'TCPIP0::10.33.38.33::INSTR'  # VISA resource string for the device
* znb = RsInstrument(resource, True, True, "SelectVisa='rs'") # select rs VISA and other configs.


"""