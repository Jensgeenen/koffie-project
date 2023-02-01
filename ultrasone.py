#Libraries
import RPi.GPIO as GPIO
import time
import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

GPIO.setwarnings(False)

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

#set GPIO Pins
GPIO_TRIGGER1 = 18
GPIO_ECHO1 = 24
GPIO_TRIGGER2 = 17
GPIO_ECHO2 = 23
GPIO_TRIGGER3 = 22
GPIO_ECHO3 = 25
GPIO_TRIGGER4 = 27
GPIO_ECHO4 = 5

value1 = False
value2 = False
value3 = False
value4 = False
sonicSpeed = 34300
tiggerLow = 0.00001
low = 10
high = 15
timeBetweenMeasurements = 5

#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER1, GPIO.OUT)
GPIO.setup(GPIO_ECHO1, GPIO.IN)
GPIO.setup(GPIO_TRIGGER2, GPIO.OUT)
GPIO.setup(GPIO_ECHO2, GPIO.IN)
GPIO.setup(GPIO_TRIGGER3, GPIO.OUT)
GPIO.setup(GPIO_ECHO3, GPIO.IN)
GPIO.setup(GPIO_TRIGGER4, GPIO.OUT)
GPIO.setup(GPIO_ECHO4, GPIO.IN)

# Define the HTML document
html1 = '''
<!DOCTYPE html>
<html>
<head>
  <style>
    body {
      font-family: Arial, sans-serif;
      background-color: #F2F2F2;
      padding: 30px;
    }
    .container {
      background-color: #FFFFFF;
      box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
      border-radius: 10px;
      padding: 20px;
    }
    h1 {
      text-align: center;
      color: #8B0000;
      margin-bottom: 20px;
    }
    p {
      font-size: 16px;
      line-height: 1.5;
      color: #333;
      text-align: center;
      margin-bottom: 20px;
    }
    a {
      display: block;
      background-color: #8B0000;
      color: #FFFFFF;
      padding: 10px 20px;
      border-radius: 20px;
      text-align: center;
      text-decoration: none;
      margin: 0 auto;
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>Melding Koffiemachine</h1>
    <p>De melk is bijna op en moet worden bijgevuld.</p>
    <a href="http://192.168.161.156:3000/login">Meer informatie, bekijk het dashboard</a>
  </div>
</body>
</html>
'''
html2 = '''
<!DOCTYPE html>
<html>
<head>
  <style>
    body {
      font-family: Arial, sans-serif;
      background-color: #F2F2F2;
      padding: 30px;
    }
    .container {
      background-color: #FFFFFF;
      box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
      border-radius: 10px;
      padding: 20px;
    }
    h1 {
      text-align: center;
      color: #8B0000;
      margin-bottom: 20px;
    }
    p {
      font-size: 16px;
      line-height: 1.5;
      color: #333;
      text-align: center;
      margin-bottom: 20px;
    }
    a {
      display: block;
      background-color: #8B0000;
      color: #FFFFFF;
      padding: 10px 20px;
      border-radius: 20px;
      text-align: center;
      text-decoration: none;
      margin: 0 auto;
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>Melding Koffiemachine</h1>
    <p>De suiker is bijna op en moet worden bijgevuld.</p>
    <a href="http://192.168.161.156:3000/login">Meer informatie, bekijk het dashboard</a>
  </div>
</body>
</html>
'''
html3 = '''
<!DOCTYPE html>
<html>
<head>
  <style>
    body {
      font-family: Arial, sans-serif;
      background-color: #F2F2F2;
      padding: 30px;
    }
    .container {
      background-color: #FFFFFF;
      box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
      border-radius: 10px;
      padding: 20px;
    }
    h1 {
      text-align: center;
      color: #8B0000;
      margin-bottom: 20px;
    }
    p {
      font-size: 16px;
      line-height: 1.5;
      color: #333;
      text-align: center;
      margin-bottom: 20px;
    }
    a {
      display: block;
      background-color: #8B0000;
      color: #FFFFFF;
      padding: 10px 20px;
      border-radius: 20px;
      text-align: center;
      text-decoration: none;
      margin: 0 auto;
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>Melding Koffiemachine</h1>
    <p>De koffie is bijna op en moet worden bijgevuld.</p>
    <a href="http://192.168.161.156:3000/login">Meer informatie, bekijk het dashboard</a>
  </div>
</body>
</html>
'''
html4 = '''
<!DOCTYPE html>
<html>
<head>
  <style>
    body {
      font-family: Arial, sans-serif;
      background-color: #F2F2F2;
      padding: 30px;
    }
    .container {
      background-color: #FFFFFF;
      box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
      border-radius: 10px;
      padding: 20px;
    }
    h1 {
      text-align: center;
      color: #8B0000;
      margin-bottom: 20px;
    }
    p {
      font-size: 16px;
      line-height: 1.5;
      color: #333;
      text-align: center;
      margin-bottom: 20px;
    }
    a {
      display: block;
      background-color: #8B0000;
      color: #FFFFFF;
      padding: 10px 20px;
      border-radius: 20px;
      text-align: center;
      text-decoration: none;
      margin: 0 auto;
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>Melding Koffiemachine</h1>
    <p>De thee is bijna op en moet worden bijgevuld.</p>
    <a href="http://192.168.161.156:3000/login">Meer informatie, bekijk het dashboard</a>
  </div>
</body>
</html>
'''

# send the email via Gmail server
email_from = '<Your email address>'
password = '<Your password>'
email_to = '<Your email address>'

# Create a MIMEMultipart class, and set up the From, To, Subject fields
email_message1 = MIMEMultipart()
email_message1['From'] = email_from
email_message1['To'] = email_to
email_message1['Subject'] = 'De melk moet worden bijgevuld | Koffiemachine'
# Create a MIMEMultipart class, and set up the From, To, Subject fields
email_message2 = MIMEMultipart()
email_message2['From'] = email_from
email_message2['To'] = email_to
email_message2['Subject'] = 'De suiker moet worden bijgevuld | Koffiemachine'
# Create a MIMEMultipart class, and set up the From, To, Subject fields
email_message3 = MIMEMultipart()
email_message3['From'] = email_from
email_message3['To'] = email_to
email_message3['Subject'] = 'De koffie moet worden bijgevuld | Koffiemachine'
# Create a MIMEMultipart class, and set up the From, To, Subject fields
email_message4 = MIMEMultipart()
email_message4['From'] = email_from
email_message4['To'] = email_to
email_message4['Subject'] = 'De thee moet worden bijgevuld | Koffiemachine'



# Connect to the Gmail SMTP server and Send Email
context = ssl.create_default_context()
def send_email1():
    # Attach the html doc defined earlier, as a MIMEText html content type to the MIME message
    email_message1.attach(MIMEText(html1, "html"))
    # Convert it as a string
    email_string1 = email_message1.as_string()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(email_from, password)
        server.sendmail(email_from, email_to, email_string1)
        print("Email sent 1 !")
        server.quit()
def send_email2():
    # Attach the html doc defined earlier, as a MIMEText html content type to the MIME message
    email_message2.attach(MIMEText(html2, "html"))
    # Convert it as a string
    email_string2 = email_message2.as_string()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(email_from, password)
        server.sendmail(email_from, email_to, email_string2)
        print("Email sent 2 !")
        server.quit()
def send_email3():
    # Attach the html doc defined earlier, as a MIMEText html content type to the MIME message
    email_message3.attach(MIMEText(html3, "html"))
    # Convert it as a string
    email_string3 = email_message3.as_string()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(email_from, password)
        server.sendmail(email_from, email_to, email_string3)
        print("Email sent 3 !")
        server.quit()
def send_email4():
    # Attach the html doc defined earlier, as a MIMEText html content type to the MIME message
    email_message4.attach(MIMEText(html4, "html"))
    # Convert it as a string
    email_string4 = email_message4.as_string()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(email_from, password)
        server.sendmail(email_from, email_to, email_string4)
        print("Email sent 4 !")
        server.quit()

def distance1():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER1, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(tiggerLow)
    GPIO.output(GPIO_TRIGGER1, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO1) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO1) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * sonicSpeed) / 2
 
    return distance

def distance2():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER2, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(tiggerLow)
    GPIO.output(GPIO_TRIGGER2, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO2) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO2) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * sonicSpeed) / 2
 
    return distance

def distance3():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER3, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(tiggerLow)
    GPIO.output(GPIO_TRIGGER3, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO3) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO3) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * sonicSpeed) / 2
 
    return distance

def distance4():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER4, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(tiggerLow)
    GPIO.output(GPIO_TRIGGER4, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO4) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO4) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * sonicSpeed) / 2
    return distance
while True:
    dist1 = distance1()
    dist2 = distance2()
    dist3 = distance3()
    dist4 = distance4()
    print("---------------------------------------")
    print ("Measured Distance 1 = %.1f cm" % dist1)
    print ("Measured Distance 2 = %.1f cm" % dist2)
    print ("Measured Distance 3 = %.1f cm" % dist3)
    print ("Measured Distance 4 = %.1f cm" % dist4)
    if dist1 < low and value1 == False:
        print('There is = %.1f milk left' % dist1)
        send_email1()
        value1 = True
    if dist1 > high and value1 == True:
        value1 = False
    if dist2 < low and value2 == False:
        print('There is = %.1f suiker left' % dist2)
        send_email2()
        value2 = True
    if dist2 > high and value2 == True:
        value2 = False
    if dist3 < low and value3 == False:
        print('There is = %.1f coffee left' % dist3)
        send_email3()
        value3 = True
    if dist3 > high and value3 == True:
        value3 = False
    if dist4 < low and value4 == False:
        print('There is = %.1f thee left' % dist4)
        send_email4()
        value4 = True
    if dist4 > high and value4 == True:
        value4 = False
    time.sleep(timeBetweenMeasurements)
