# ******************************************************************************
# This is the confiuration file for all variables 
# with explanation for their use
# ************************************************

# Temperature Notification Threshold
# this the temperature above which the application
# background will turn to red. 
NTemp = 25
# Seconds between succesive samples above which the application
# background will turn to red. 
NTime = 50
# This is the location of the sensors database
dbLocation = '/nfs/Databases/sensorData.db'
# This is the color for alert visualization of sensors pages
alertColor = 'rgb(255, 20, 20)'
# This is the color for normal visualization of sensors pages
normalColor ='rgb(0, 100, 255)'
# Maximum allowed absolute difference between succesive temperature samples 
maxaad=5
# Default number of samples to plot at historical data
numOfSamples = 240
# Mail parameters
sender = "ALARM nocnimits@gmail.com"
receiver = "<g.karoub@gmail.com>"
usr="nocnimits@gmail.com"
usrpasswd="rcpcwlnmcprrlnia"
message1 = f"""\
Subject: Attention. Temperature RISE in NOC
To: {receiver}
From: {sender}

Temperature has risen to """
SMTPserver="smtp.gmail.com"
SMTPport=587
# Calls from serial port through PSTN modem
# change to 'NO' if there is no serial connection to PSTN modem
PSTN_calls='NO'
recipients=["6956024579","6956024584","6956024581"]
# port in which the serial device (usb to serial) is attached
serPort="/dev/ttyUSB0"
# Twilio account data.  
#-- Onle one set of AccSID/AccTOK must be uncommented!!!!
# ************************************************
# Test Account -- use this not to get charged. No real actions happening though...
#AccSID="ACf177001a2d039c9b765fb2c98f984172"
#AccTOK="f83dd514e849274f6c677f5988ed08c6"
# ************************************************
# Real Account  -- charging occurs but also actions happen
#AccSID="AC0261d2ed0e8651b93150698de1d75d7e"
#AccTOK="c25d7a76a684b91b63123c0bdf0773aa"
AccSID="AC0d79db44e338bce0936f2d6334ddd037"
AccTOK="2fe27baf6fb0e3d5c24958a4a77a6a1b"
# ************************************************
# Telephone numbers for notification. Call_to is the number to be called
# and call_from is the number from you are calling. Perhaps it is Concealed 
call_to="+306956024579"
call_from="+12052365074"
smsBody="NOC ALERTS"
twimlData='<Response><Say>Alert Alert Alert</Say></Response>'
# Global switches -- equals to 'YES'or 'NO', control related notification actions 
send_email='NO'
send_sms='NO'
send_call='NO'
