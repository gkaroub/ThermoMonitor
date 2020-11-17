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
dbLocation = './db/sensorData.db'
# This is the color for alert visualization of sensors pages
alertColor = 'rgb(255, 20, 20)'
# This is the color for normal visualization of sensors pages
normalColor ='rgb(0, 100, 255)'
# Maximum allowed absolute difference between succesive temperature samples 
maxaad=5
# Default number of samples to plot at historical data
numOfSamples = 240
# Mail parameters
sender = "ALARM xxxxxxxxxxxxxxx"
receiver = "<xxxxxxxx@gmail.com>"
usr="xxxxxxxxx@gmail.com"
usrpasswd="xxxxxxxxxxxxxxxxxxxx"
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
recipients=["6xxxxxxxxx","6xxxxxxxxx","6xxxxxxxxx"]
# port in which the serial device (usb to serial) is attached
serPort="/dev/ttyUSB0"
# Twilio account data.  
#-- Onle one set of AccSID/AccTOK must be uncommented!!!!
# ************************************************
# Test Account -- use this not to get charged. No real actions happening though...
#AccSID="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
#AccTOK="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
# ************************************************
# Real Account  -- charging occurs but also actions happen
#AccSID="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
#AccTOK="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
AccSID="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
AccTOK="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
# ************************************************
# Telephone numbers for notification. Call_to is the number to be called
# and call_from is the number from you are calling. Perhaps it is Concealed 
call_to="+306xxxxxxxxx"
call_from="+1xxxxxxxxxxx"
smsBody="NOC ALERTS"
twimlData='<Response><Say>Alert Alert Alert</Say></Response>'
# Global switches -- equals to 'YES'or 'NO', control related notification actions 
send_email='NO'
send_sms='NO'
send_call='NO'
