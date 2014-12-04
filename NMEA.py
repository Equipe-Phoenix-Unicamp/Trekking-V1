class NMEA:
    NMEA_GGA = "00";
    NMEA_GLL = "01";
    NMEA_GSA = "02";
    NMEA_GSV = "03";
    NMEA_RMC = "04";
    NMEA_VTG = "05";
    NMEA_SET = "00";
    NMEA_QUERY = "01";
    NMEA_RATE_QUERY = "00";
    NMEA_QUERY_RATE_MINIMUN = "00";
    NMEA_QUERY_RATE_RMC = "01";
    @staticmethod
    def createData103(code, mode, rate):
        returnString = "$PSRF103,"+code+","+mode+","+rate+",01"
        charArray = list(returnString)
        byteXor=0
        for char in charArray:
            byteXor ^=ord(char)

        returnString += "*"+"%02X" % byteXor+"\r\n"+chr(0) 
        return returnString
