


"""
SCPI commands good to know:

SENS - used for data retrival
CALC - used for data processing



znb commands:


znb.instrument_status_checking = True  # Error check after each command, can be True or False

znb.clear_status()  # Clear status register

znb.close() # close session

znb.query_str('*IDN?') # check VNA id

RsInstrument.assert_minimum_version('1.50.0') # check version

resource = 'TCPIP0::10.33.38.33::INSTR'  # VISA resource string for the device

znb = RsInstrument(resource, True, True, "SelectVisa='rs'") # select rs VISA and other configs.


"""