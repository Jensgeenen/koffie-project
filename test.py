import RPi.GPIO as GPIO
import time
import busio
import digitalio
import board
import adafruit_pcd8544
import sys
# import mysql.connector as mariadb
import mariadb


import sqlite3

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from mfrc522 import SimpleMFRC522

import spidev

GPIO.setmode (GPIO.BCM)
GPIO.setup (17, GPIO.IN) # GPIO 17 input knop 1
GPIO.setup (27, GPIO.IN) # GPIO 27 input knop 2
GPIO.setup (5, GPIO.IN) # GPIO 5 input knop 3
GPIO.setup (6, GPIO.IN) # GPIO 6 input knop 4


complete = 0
land = ' Ethiopië'
land_thee = ' China'


# conn = sqlite3.connect("Koffie.db")
# print(conn)
# cursor = conn.execute("SELECT firstName from Koffie.User")
# print(cusrsor)

conn = mariadb.connect(user='user', password='user', host='localhost', database='Koffie')
cursor = conn.cursor()
print(cursor)

# Connect to the database
# conn = mysql.connector.connect(
#   host="localhost",
#   user="user",
#   password="user",
#   database="Koffie"
# )
# # Create a cursor object
# cursor = conn.cursor()

# # Execute a SELECT statement
# cursor.execute("SELECT * FROM User")
# for row in rows:
# print(row)

# Initialize SPI bus
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

# Initialize display
dc = digitalio.DigitalInOut(board.D23)  # data/command
cs1 = digitalio.DigitalInOut(board.CE1)  # chip select CE1 for display
reset = digitalio.DigitalInOut(board.D24)  # reset
display = adafruit_pcd8544.PCD8544(spi, dc, cs1, reset, baudrate= 1000000)
display.bias = 4
display.contrast = 60
display.invert = True

#  Clear the display.  Always call show after changing pixels to make the display update visible!
display.fill(0)
display.show()
font = ImageFont.load_default()

reader = SimpleMFRC522()

statement = "SELECT firstName FROM User "

cursor.execute(statement)
for i in cursor:
    print(i)

try:
    
    while True:
        complete = 0
        text = 0
        image = Image.new('1', (display.width, display.height))
        draw = ImageDraw.Draw(image)
        draw.rectangle((0, 0, display.width, display.height), outline=255, fill=255)
        draw.text((1,0), '', font=font)
        draw.text((1,8), 'Scan je kaart', font=font)
        draw.text((1,16), 'HIER', font=font)
        draw.text((1,24), '', font=font)
        draw.text((1,32), '', font=font)
        display.image(image)
        display.show()
        id, text = reader.read()
        print(id)
        print(text)
        if (text != 0 ):
            while complete != 1:
                image = Image.new('1', (display.width, display.height))
                draw = ImageDraw.Draw(image)
                draw.rectangle((0, 0, display.width, display.height), outline=255, fill=255)
                draw.text((1,0),'Opties', font=font)
                draw.text((1,8),(str(1)+ ' Koffie'), font=font)
                draw.text((1,16),(str(2)+ ' Thee'), font=font)
                draw.text((1,24), '', font=font)
                draw.text((1,32), '', font=font)
                display.image(image)
                display.show()
                time.sleep (0.3)


                if (GPIO.input (17)==1): #koffie
                    while complete != 1:
                        image = Image.new('1', (display.width, display.height))
                        draw = ImageDraw.Draw(image)
                        draw.rectangle((0, 0, display.width, display.height), outline=255, fill=255)
                        draw.text((1,0),'Opties', font=font)
                        draw.text((1,8), (str(1)+ ' Koffie'), font=font)
                        draw.text((1,16), (str(2)+ ' Latte macchiato'), font=font)
                        draw.text((1,24), (str(3)+ ' Cappuccino'), font=font)
                        draw.text((1,32), (str(4)+ ' Espresso'), font=font)
                        display.image(image)
                        display.show()
                        time.sleep (0.3)

                        if (GPIO.input (17)==1):
                            while complete != 1:
                                image = Image.new('1', (display.width, display.height))
                                draw = ImageDraw.Draw(image)
                                draw.rectangle((0, 0, display.width, display.height), outline=255, fill=255)
                                draw.text((1,0),'Formaat', font=font)
                                draw.text((1,8),(str(1)+ ' Groot'), font=font)
                                draw.text((1,16),(str(2)+ ' Klein'), font=font)
                                draw.text((1,24), '', font=font)
                                draw.text((1,32), '', font=font)
                                display.image(image)
                                display.show()
                                time.sleep (0.3)

                                if (GPIO.input (17)==1):
                                    while complete != 1:
                                        image = Image.new('1', (display.width, display.height))
                                        draw = ImageDraw.Draw(image)
                                        draw.rectangle((0, 0, display.width, display.height), outline=255, fill=255)
                                        draw.text((1,0),"Extra's", font=font)
                                        draw.text((1,8), (str(1)+ ' Naturel'), font=font)
                                        draw.text((1,16), (str(2)+ ' Melk'), font=font)
                                        draw.text((1,24), (str(3)+ ' Suiker'), font=font)
                                        draw.text((1,32), (str(4)+ ' Melk+Suiker'), font=font)
                                        display.image(image)
                                        display.show()
                                        time.sleep (0.3)

                                        if (GPIO.input (17)==1):
                                            image = Image.new('1', (display.width, display.height))
                                            draw = ImageDraw.Draw(image)
                                            draw.rectangle((0, 0, display.width, display.height), outline=255, fill=255)
                                            draw.text((1,0),' Keuze', font=font)
                                            draw.text((1,8),(' Koffie groot '), font=font)
                                            draw.text((1,16),(' Naturel'), font=font)
                                            draw.text((1,24), ' Herkomst', font=font)
                                            draw.text((1,32), land, font=font)
                                            display.image(image)
                                            display.show()
                                            cursor.execute("select Card.cardID, userID, drinkPrice from Koffie.Card join Koffie.User on Card.cardID = User.cardID join Koffie.Drink on User.userID = Drink.drinkID where uidCardNumber = "+ str(id) +" and drinkID = 1;")
                                            cursor.execute("select drinkPrice from Koffie.Drink where drinkID = '1';")
                                            result = cursor.fetchone()
                                            drinkPrice = result[0]
                                            print(drinkPrice)
                                            cursor.execute("select userID from Koffie.Card join Koffie.User on Card.cardID = User.cardID where uidCardNumber = '219196986759';")
                                            result = cursor.fetchone()
                                            userID = result[0] 

                                            cursor.execute("INSERT INTO Koffie.Order(drinkID, userID, cardID, orderDate, orderTime, orderPrice) VALUES (1 , "+ str(userID) +" , 1, CURRENT_DATE(), CURRENT_TIME(),"+ str(drinkPrice) +" );")
                                            
                                            
                                            conn.commit()
                                            time.sleep (15.0)
                                            complete = 1

                                        if (GPIO.input (27)==1):
                                            image = Image.new('1', (display.width, display.height))
                                            draw = ImageDraw.Draw(image)
                                            draw.rectangle((0, 0, display.width, display.height), outline=255, fill=255)
                                            draw.text((1,0),' Keuze', font=font)
                                            draw.text((1,8),(' Koffie groot '), font=font)
                                            draw.text((1,16),(' Melk'), font=font)
                                            draw.text((1,24), ' Herkomst', font=font)
                                            draw.text((1,32), land, font=font)
                                            display.image(image)
                                            display.show()
                                            cursor.execute("select drinkPrice from Koffie.Drink where drinkID = '3';")
                                            result = cursor.fetchone()
                                            drinkPrice = result[0]
                                            print(drinkPrice)
                                            cursor.execute("select userID from Koffie.Card join Koffie.User on Card.cardID = User.cardID where uidCardNumber = "+ str(id) +";")
                                            result = cursor.fetchone()
                                            userID = result[0] 

                                            cursor.execute("INSERT INTO Koffie.Order(drinkID, userID, cardID, orderDate, orderTime, orderPrice) VALUES (3 , "+ str(userID) +" , "+ str(text) +", CURRENT_DATE(), CURRENT_TIME(),"+ str(drinkPrice) +" );")
                                            
                                            
                                            conn.commit()
                                            time.sleep (15.0)
                                            complete = 1

                                        if (GPIO.input (5)==1):
                                            image = Image.new('1', (display.width, display.height))
                                            draw = ImageDraw.Draw(image)
                                            draw.rectangle((0, 0, display.width, display.height), outline=255, fill=255)
                                            draw.text((1,0),' Keuze', font=font)
                                            draw.text((1,8),(' Koffie groot '), font=font)
                                            draw.text((1,16),(' Suiker'), font=font)
                                            draw.text((1,24), ' Herkomst', font=font)
                                            draw.text((1,32), land, font=font)
                                            display.image(image)
                                            display.show()
                                            cursor.execute("select Card.cardID, userID, drinkPrice from Koffie.Card join Koffie.User on Card.cardID = User.cardID join Koffie.Drink on User.userID = Drink.drinkID where uidCardNumber = "+ str(id) +" and drinkID = 5;")
                                            cursor.execute("select drinkPrice from Koffie.Drink where drinkID = '1';")
                                            result = cursor.fetchone()
                                            drinkPrice = result[0]
                                            print(drinkPrice)
                                            cursor.execute("select userID from Koffie.Card join Koffie.User on Card.cardID = User.cardID where uidCardNumber = '219196986759';")
                                            result = cursor.fetchone()
                                            userID = result[0] 

                                            cursor.execute("INSERT INTO Koffie.Order(drinkID, userID, cardID, orderDate, orderTime, orderPrice) VALUES (1 , "+ str(userID) +" , 1, CURRENT_DATE(), CURRENT_TIME(),"+ str(drinkPrice) +" );")
                                            
                                            
                                            conn.commit()
                                            time.sleep (15.0)
                                            complete = 1

                                        if (GPIO.input (6)==1):
                                            image = Image.new('1', (display.width, display.height))
                                            draw = ImageDraw.Draw(image)
                                            draw.rectangle((0, 0, display.width, display.height), outline=255, fill=255)
                                            draw.text((1,0),' Keuze', font=font)
                                            draw.text((1,8),(' Koffie groot '), font=font)
                                            draw.text((1,16),(' Melk+Suiker'), font=font)
                                            draw.text((1,24), ' Herkomst', font=font)
                                            draw.text((1,32), land, font=font)
                                            display.image(image)
                                            display.show()
                                            cursor.execute("select Card.cardID, userID, drinkPrice from Koffie.Card join Koffie.User on Card.cardID = User.cardID join Koffie.Drink on User.userID = Drink.drinkID where uidCardNumber = "+ str(id) +" and drinkID = 7;")
                                            cursor.execute("select drinkPrice from Koffie.Drink where drinkID = '1';")
                                            result = cursor.fetchone()
                                            drinkPrice = result[0]
                                            print(drinkPrice)
                                            cursor.execute("select userID from Koffie.Card join Koffie.User on Card.cardID = User.cardID where uidCardNumber = '219196986759';")
                                            result = cursor.fetchone()
                                            userID = result[0] 

                                            cursor.execute("INSERT INTO Koffie.Order(drinkID, userID, cardID, orderDate, orderTime, orderPrice) VALUES (1 , "+ str(userID) +" , 1, CURRENT_DATE(), CURRENT_TIME(),"+ str(drinkPrice) +" );")
                                            
                                            
                                            conn.commit()
                                            time.sleep (15.0)
                                            complete = 1

                                if (GPIO.input (27)==1):
                                    while complete != 1:
                                        image = Image.new('1', (display.width, display.height))
                                        draw = ImageDraw.Draw(image)
                                        draw.rectangle((0, 0, display.width, display.height), outline=255, fill=255)
                                        draw.text((1,0),"Extra's", font=font)
                                        draw.text((1,8), (str(1)+ ' Naturel'), font=font)
                                        draw.text((1,16), (str(2)+ ' Melk'), font=font)
                                        draw.text((1,24), (str(3)+ ' Suiker'), font=font)
                                        draw.text((1,32), (str(4)+ ' Melk+Suiker'), font=font)
                                        display.image(image)
                                        display.show()
                                        time.sleep (0.3)
                                        if (GPIO.input (17)==1):
                                            image = Image.new('1', (display.width, display.height))
                                            draw = ImageDraw.Draw(image)
                                            draw.rectangle((0, 0, display.width, display.height), outline=255, fill=255)
                                            draw.text((1,0),' Keuze', font=font)
                                            draw.text((1,8),(' Koffie klein '), font=font)
                                            draw.text((1,16),(' Naturel'), font=font)
                                            draw.text((1,24), ' Herkomst', font=font)
                                            draw.text((1,32), land, font=font)
                                            display.image(image)
                                            display.show()
                                            cursor.execute("select Card.cardID, userID, drinkPrice from Koffie.Card join Koffie.User on Card.cardID = User.cardID join Koffie.Drink on User.userID = Drink.drinkID where uidCardNumber = "+ str(id) +" and drinkID = 2;")
                                            cursor.execute("select drinkPrice from Koffie.Drink where drinkID = '1';")
                                            result = cursor.fetchone()
                                            drinkPrice = result[0]
                                            print(drinkPrice)
                                            cursor.execute("select userID from Koffie.Card join Koffie.User on Card.cardID = User.cardID where uidCardNumber = '219196986759';")
                                            result = cursor.fetchone()
                                            userID = result[0] 

                                            cursor.execute("INSERT INTO Koffie.Order(drinkID, userID, cardID, orderDate, orderTime, orderPrice) VALUES (1 , "+ str(userID) +" , 1, CURRENT_DATE(), CURRENT_TIME(),"+ str(drinkPrice) +" );")
                                            
                                            
                                            conn.commit()
                                            time.sleep (15.0)
                                            complete = 1

                                        if (GPIO.input (27)==1):
                                            image = Image.new('1', (display.width, display.height))
                                            draw = ImageDraw.Draw(image)
                                            draw.rectangle((0, 0, display.width, display.height), outline=255, fill=255)
                                            draw.text((1,0),' Keuze', font=font)
                                            draw.text((1,8),(' Koffie klein '), font=font)
                                            draw.text((1,16),(' Melk'), font=font)
                                            draw.text((1,24), ' Herkomst', font=font)
                                            draw.text((1,32), land, font=font)
                                            display.image(image)
                                            display.show()
                                            cursor.execute("select Card.cardID, userID, drinkPrice from Koffie.Card join Koffie.User on Card.cardID = User.cardID join Koffie.Drink on User.userID = Drink.drinkID where uidCardNumber = "+ str(id) +" and drinkID = 4;")
                                            cursor.execute("select drinkPrice from Koffie.Drink where drinkID = '1';")
                                            result = cursor.fetchone()
                                            drinkPrice = result[0]
                                            print(drinkPrice)
                                            cursor.execute("select userID from Koffie.Card join Koffie.User on Card.cardID = User.cardID where uidCardNumber = '219196986759';")
                                            result = cursor.fetchone()
                                            userID = result[0] 

                                            cursor.execute("INSERT INTO Koffie.Order(drinkID, userID, cardID, orderDate, orderTime, orderPrice) VALUES (1 , "+ str(userID) +" , 1, CURRENT_DATE(), CURRENT_TIME(),"+ str(drinkPrice) +" );")
                                            
                                            
                                            conn.commit()
                                            time.sleep (15.0)
                                            complete = 1

                                        if (GPIO.input (5)==1):
                                            image = Image.new('1', (display.width, display.height))
                                            draw = ImageDraw.Draw(image)
                                            draw.rectangle((0, 0, display.width, display.height), outline=255, fill=255)
                                            draw.text((1,0),' Keuze', font=font)
                                            draw.text((1,8),(' Koffie klein '), font=font)
                                            draw.text((1,16),(' Suiker'), font=font)
                                            draw.text((1,24), ' Herkomst', font=font)
                                            draw.text((1,32), land, font=font)
                                            display.image(image)
                                            display.show()
                                            cursor.execute("select Card.cardID, userID, drinkPrice from Koffie.Card join Koffie.User on Card.cardID = User.cardID join Koffie.Drink on User.userID = Drink.drinkID where uidCardNumber = "+ str(id) +" and drinkID = 6;")
                                            cursor.execute("select drinkPrice from Koffie.Drink where drinkID = '1';")
                                            result = cursor.fetchone()
                                            drinkPrice = result[0]
                                            print(drinkPrice)
                                            cursor.execute("select userID from Koffie.Card join Koffie.User on Card.cardID = User.cardID where uidCardNumber = '219196986759';")
                                            result = cursor.fetchone()
                                            userID = result[0] 

                                            cursor.execute("INSERT INTO Koffie.Order(drinkID, userID, cardID, orderDate, orderTime, orderPrice) VALUES (1 , "+ str(userID) +" , 1, CURRENT_DATE(), CURRENT_TIME(),"+ str(drinkPrice) +" );")
                                            
                                            
                                            conn.commit()
                                            time.sleep (15.0)
                                            complete = 1

                                        if (GPIO.input (6)==1):
                                            image = Image.new('1', (display.width, display.height))
                                            draw = ImageDraw.Draw(image)
                                            draw.rectangle((0, 0, display.width, display.height), outline=255, fill=255)
                                            draw.text((1,0),' Keuze', font=font)
                                            draw.text((1,8),(' Koffie klein '), font=font)
                                            draw.text((1,16),(' Melk+Suiker'), font=font)
                                            draw.text((1,24), ' Herkomst', font=font)
                                            draw.text((1,32), land, font=font)
                                            display.image(image)
                                            display.show()
                                            cursor.execute("select Card.cardID, userID, drinkPrice from Koffie.Card join Koffie.User on Card.cardID = User.cardID join Koffie.Drink on User.userID = Drink.drinkID where uidCardNumber = "+ str(id) +" and drinkID = 8;")
                                            cursor.execute("select drinkPrice from Koffie.Drink where drinkID = '1';")
                                            result = cursor.fetchone()
                                            drinkPrice = result[0]
                                            print(drinkPrice)
                                            cursor.execute("select userID from Koffie.Card join Koffie.User on Card.cardID = User.cardID where uidCardNumber = '219196986759';")
                                            result = cursor.fetchone()
                                            userID = result[0] 

                                            cursor.execute("INSERT INTO Koffie.Order(drinkID, userID, cardID, orderDate, orderTime, orderPrice) VALUES (1 , "+ str(userID) +" , 1, CURRENT_DATE(), CURRENT_TIME(),"+ str(drinkPrice) +" );")
                                            
                                            
                                            conn.commit()
                                            time.sleep (15.0)
                                            complete = 1

                        if (GPIO.input (27)==1):
                            image = Image.new('1', (display.width, display.height))
                            draw = ImageDraw.Draw(image)
                            draw.rectangle((0, 0, display.width, display.height), outline=255, fill=255)
                            draw.text((1,0),' Keuze', font=font)
                            draw.text((1,8),(' Latte macchiato '), font=font)
                            draw.text((1,16),(''), font=font)
                            draw.text((1,24), ' Herkomst', font=font)
                            draw.text((1,32), land, font=font)
                            display.image(image)
                            display.show()
                            cursor.execute("select Card.cardID, userID, drinkPrice from Koffie.Card join Koffie.User on Card.cardID = User.cardID join Koffie.Drink on User.userID = Drink.drinkID where uidCardNumber = "+ str(id) +" and drinkID = 9;")
                            cursor.execute("select drinkPrice from Koffie.Drink where drinkID = '1';")
                            result = cursor.fetchone()
                            drinkPrice = result[0]
                            print(drinkPrice)
                            cursor.execute("select userID from Koffie.Card join Koffie.User on Card.cardID = User.cardID where uidCardNumber = '219196986759';")
                            result = cursor.fetchone()
                            userID = result[0] 

                            cursor.execute("INSERT INTO Koffie.Order(drinkID, userID, cardID, orderDate, orderTime, orderPrice) VALUES (1 , "+ str(userID) +" , 1, CURRENT_DATE(), CURRENT_TIME(),"+ str(drinkPrice) +" );")
                                            
                                            
                            conn.commit()
                            time.sleep (15.0)
                            complete = 1

                        if (GPIO.input (5)==1):
                            image = Image.new('1', (display.width, display.height))
                            draw = ImageDraw.Draw(image)
                            draw.rectangle((0, 0, display.width, display.height), outline=255, fill=255)
                            draw.text((1,0),' Keuze', font=font)
                            draw.text((1,8),(' Cappuccino '), font=font)
                            draw.text((1,16),(''), font=font)
                            draw.text((1,24), ' Herkomst', font=font)
                            draw.text((1,32), land, font=font)
                            display.image(image)
                            display.show()
                            cursor.execute("select Card.cardID, userID, drinkPrice from Koffie.Card join Koffie.User on Card.cardID = User.cardID join Koffie.Drink on User.userID = Drink.drinkID where uidCardNumber = "+ str(id) +" and drinkID = 17;")
                            cursor.execute("select drinkPrice from Koffie.Drink where drinkID = '1';")
                            result = cursor.fetchone()
                            drinkPrice = result[0]
                            print(drinkPrice)
                            cursor.execute("select userID from Koffie.Card join Koffie.User on Card.cardID = User.cardID where uidCardNumber = '219196986759';")
                            result = cursor.fetchone()
                            userID = result[0] 

                            cursor.execute("INSERT INTO Koffie.Order(drinkID, userID, cardID, orderDate, orderTime, orderPrice) VALUES (1 , "+ str(userID) +" , 1, CURRENT_DATE(), CURRENT_TIME(),"+ str(drinkPrice) +" );")
                                            
                                            
                            conn.commit()
                            time.sleep (15.0)
                            complete = 1

                        if (GPIO.input (6)==1):
                            image = Image.new('1', (display.width, display.height))
                            draw = ImageDraw.Draw(image)
                            draw.rectangle((0, 0, display.width, display.height), outline=255, fill=255)
                            draw.text((1,0),' Keuze', font=font)
                            draw.text((1,8),(' Espresso '), font=font)
                            draw.text((1,16),(''), font=font)
                            draw.text((1,24), ' Herkomst', font=font)
                            draw.text((1,32), land, font=font)
                            display.image(image)
                            display.show()
                            cursor.execute("select Card.cardID, userID, drinkPrice from Koffie.Card join Koffie.User on Card.cardID = User.cardID join Koffie.Drink on User.userID = Drink.drinkID where uidCardNumber = "+ str(id) +" and drinkID = 25;")
                            cursor.execute("select drinkPrice from Koffie.Drink where drinkID = '1';")
                            result = cursor.fetchone()
                            drinkPrice = result[0]
                            print(drinkPrice)
                            cursor.execute("select userID from Koffie.Card join Koffie.User on Card.cardID = User.cardID where uidCardNumber = '219196986759';")
                            result = cursor.fetchone()
                            userID = result[0] 

                            cursor.execute("INSERT INTO Koffie.Order(drinkID, userID, cardID, orderDate, orderTime, orderPrice) VALUES (1 , "+ str(userID) +" , 1, CURRENT_DATE(), CURRENT_TIME(),"+ str(drinkPrice) +" );")
                                            
                                            
                            conn.commit()
                            time.sleep (15.0)
                            complete = 1    


                if (GPIO.input (27)==1): #thee
                    while complete != 1:
                        image = Image.new('1', (display.width, display.height))
                        draw = ImageDraw.Draw(image)
                        draw.rectangle((0, 0, display.width, display.height), outline=255, fill=255)
                        draw.text((1,0),'Opties', font=font)
                        draw.text((1,8), (str(1)+ ' Citroen'), font=font)
                        draw.text((1,16), (str(2)+ ' Rooibos'), font=font)
                        draw.text((1,24), '', font=font)
                        draw.text((1,32), '', font=font)
                        display.image(image)
                        display.show()
                        time.sleep (0.3)
                        if (GPIO.input (17)==1):
                            while complete != 1:
                                image = Image.new('1', (display.width, display.height))
                                draw = ImageDraw.Draw(image)
                                draw.rectangle((0, 0, display.width, display.height), outline=255, fill=255)
                                draw.text((1,0),"Extra's", font=font)
                                draw.text((1,8), (str(1)+ ' Naturel'), font=font)
                                draw.text((1,16), (str(2)+ ' Melk'), font=font)
                                draw.text((1,24), (str(3)+ ' Suiker'), font=font)
                                draw.text((1,32), (str(4)+ ' Melk+Suiker'), font=font)
                                display.image(image)
                                display.show()
                                time.sleep (0.3)
                                if (GPIO.input (17)==1):
                                    image = Image.new('1', (display.width, display.height))
                                    draw = ImageDraw.Draw(image)
                                    draw.rectangle((0, 0, display.width, display.height), outline=255, fill=255)
                                    draw.text((1,0),' Keuze', font=font)
                                    draw.text((1,8),(' Citroen thee '), font=font)
                                    draw.text((1,16),(' Naturel'), font=font)
                                    draw.text((1,24), ' Herkomst', font=font)
                                    draw.text((1,32), land_thee, font=font)
                                    display.image(image)
                                    display.show()
                                    cursor.execute("select Card.cardID, userID, drinkPrice from Koffie.Card join Koffie.User on Card.cardID = User.cardID join Koffie.Drink on User.userID = Drink.drinkID where uidCardNumber = "+ str(id) +" and drinkID = 41;")
                                    cursor.execute("select drinkPrice from Koffie.Drink where drinkID = '1';")
                                    result = cursor.fetchone()
                                    drinkPrice = result[0]
                                    print(drinkPrice)
                                    cursor.execute("select userID from Koffie.Card join Koffie.User on Card.cardID = User.cardID where uidCardNumber = '219196986759';")
                                    result = cursor.fetchone()
                                    userID = result[0] 

                                    cursor.execute("INSERT INTO Koffie.Order(drinkID, userID, cardID, orderDate, orderTime, orderPrice) VALUES (1 , "+ str(userID) +" , 1, CURRENT_DATE(), CURRENT_TIME(),"+ str(drinkPrice) +" );")      
                                            
                                    conn.commit()
                                    time.sleep (15.0)
                                    complete = 1
                                
                                if (GPIO.input (27)==1):
                                    image = Image.new('1', (display.width, display.height))
                                    draw = ImageDraw.Draw(image)
                                    draw.rectangle((0, 0, display.width, display.height), outline=255, fill=255)
                                    draw.text((1,0),' Keuze', font=font)
                                    draw.text((1,8),(' Citroen thee '), font=font)
                                    draw.text((1,16),(' Melk'), font=font)
                                    draw.text((1,24), ' Herkomst', font=font)
                                    draw.text((1,32), land_thee, font=font)
                                    display.image(image)
                                    display.show()
                                    cursor.execute("select Card.cardID, userID, drinkPrice from Koffie.Card join Koffie.User on Card.cardID = User.cardID join Koffie.Drink on User.userID = Drink.drinkID where uidCardNumber = "+ str(id) +" and drinkID = 42;")
                                    cursor.execute("select drinkPrice from Koffie.Drink where drinkID = '1';")
                                    result = cursor.fetchone()
                                    drinkPrice = result[0]
                                    print(drinkPrice)
                                    cursor.execute("select userID from Koffie.Card join Koffie.User on Card.cardID = User.cardID where uidCardNumber = '219196986759';")
                                    result = cursor.fetchone()
                                    userID = result[0] 

                                    cursor.execute("INSERT INTO Koffie.Order(drinkID, userID, cardID, orderDate, orderTime, orderPrice) VALUES (1 , "+ str(userID) +" , 1, CURRENT_DATE(), CURRENT_TIME(),"+ str(drinkPrice) +" );")      
                                            
                                    conn.commit()
                                    time.sleep (15.0)
                                    complete = 1

                                if (GPIO.input (5)==1):
                                    image = Image.new('1', (display.width, display.height))
                                    draw = ImageDraw.Draw(image)
                                    draw.rectangle((0, 0, display.width, display.height), outline=255, fill=255)
                                    draw.text((1,0),' Keuze', font=font)
                                    draw.text((1,8),(' Citroen thee '), font=font)
                                    draw.text((1,16),(' Suiker'), font=font)
                                    draw.text((1,24), ' Herkomst', font=font)
                                    draw.text((1,32), land_thee, font=font)
                                    display.image(image)
                                    display.show()
                                    cursor.execute("select Card.cardID, userID, drinkPrice from Koffie.Card join Koffie.User on Card.cardID = User.cardID join Koffie.Drink on User.userID = Drink.drinkID where uidCardNumber = "+ str(id) +" and drinkID = 43;")
                                    cursor.execute("select drinkPrice from Koffie.Drink where drinkID = '1';")
                                    result = cursor.fetchone()
                                    drinkPrice = result[0]
                                    print(drinkPrice)
                                    cursor.execute("select userID from Koffie.Card join Koffie.User on Card.cardID = User.cardID where uidCardNumber = '219196986759';")
                                    result = cursor.fetchone()
                                    userID = result[0] 

                                    cursor.execute("INSERT INTO Koffie.Order(drinkID, userID, cardID, orderDate, orderTime, orderPrice) VALUES (1 , "+ str(userID) +" , 1, CURRENT_DATE(), CURRENT_TIME(),"+ str(drinkPrice) +" );")      
                                            
                                    conn.commit()
                                    time.sleep (15.0)
                                    complete = 1

                                if (GPIO.input (6)==1):
                                    image = Image.new('1', (display.width, display.height))
                                    draw = ImageDraw.Draw(image)
                                    draw.rectangle((0, 0, display.width, display.height), outline=255, fill=255)
                                    draw.text((1,0),' Keuze', font=font)
                                    draw.text((1,8),(' Citroen thee '), font=font)
                                    draw.text((1,16),(' Melk+Suiker'), font=font)
                                    draw.text((1,24), ' Herkomst', font=font)
                                    draw.text((1,32), land_thee, font=font)
                                    display.image(image)
                                    display.show()
                                    cursor.execute("select Card.cardID, userID, drinkPrice from Koffie.Card join Koffie.User on Card.cardID = User.cardID join Koffie.Drink on User.userID = Drink.drinkID where uidCardNumber = "+ str(id) +" and drinkID = 44;")
                                    cursor.execute("select drinkPrice from Koffie.Drink where drinkID = '1';")
                                    result = cursor.fetchone()
                                    drinkPrice = result[0]
                                    print(drinkPrice)
                                    cursor.execute("select userID from Koffie.Card join Koffie.User on Card.cardID = User.cardID where uidCardNumber = '219196986759';")
                                    result = cursor.fetchone()
                                    userID = result[0] 

                                    cursor.execute("INSERT INTO Koffie.Order(drinkID, userID, cardID, orderDate, orderTime, orderPrice) VALUES (1 , "+ str(userID) +" , 1, CURRENT_DATE(), CURRENT_TIME(),"+ str(drinkPrice) +" );")      
                                            
                                    conn.commit()
                                    time.sleep (15.0)
                                    complete = 1


                        if (GPIO.input (27)==1):
                            while complete != 1:
                                image = Image.new('1', (display.width, display.height))
                                draw = ImageDraw.Draw(image)
                                draw.rectangle((0, 0, display.width, display.height), outline=255, fill=255)
                                draw.text((1,0),"Extra's", font=font)
                                draw.text((1,8), (str(1)+ ' Naturel'), font=font)
                                draw.text((1,16), (str(2)+ ' Melk'), font=font)
                                draw.text((1,24), (str(3)+ ' Suiker'), font=font)
                                draw.text((1,32), (str(4)+ ' Melk+Suiker'), font=font)
                                display.image(image)
                                display.show()
                                time.sleep (0.3)
                                if (GPIO.input (17)==1):
                                    image = Image.new('1', (display.width, display.height))
                                    draw = ImageDraw.Draw(image)
                                    draw.rectangle((0, 0, display.width, display.height), outline=255, fill=255)
                                    draw.text((1,0),' Keuze', font=font)
                                    draw.text((1,8),(' Rooibos thee '), font=font)
                                    draw.text((1,16),(' Naturel'), font=font)
                                    draw.text((1,24), ' Herkomst', font=font)
                                    draw.text((1,32), land_thee, font=font)
                                    display.image(image)
                                    display.show()
                                    cursor.execute("select Card.cardID, userID, drinkPrice from Koffie.Card join Koffie.User on Card.cardID = User.cardID join Koffie.Drink on User.userID = Drink.drinkID where uidCardNumber = "+ str(id) +" and drinkID = 45;")
                                    cursor.execute("select drinkPrice from Koffie.Drink where drinkID = '1';")
                                    result = cursor.fetchone()
                                    drinkPrice = result[0]
                                    print(drinkPrice)
                                    cursor.execute("select userID from Koffie.Card join Koffie.User on Card.cardID = User.cardID where uidCardNumber = '219196986759';")
                                    result = cursor.fetchone()
                                    userID = result[0] 

                                    cursor.execute("INSERT INTO Koffie.Order(drinkID, userID, cardID, orderDate, orderTime, orderPrice) VALUES (1 , "+ str(userID) +" , 1, CURRENT_DATE(), CURRENT_TIME(),"+ str(drinkPrice) +" );")      
                                            
                                    conn.commit()
                                    time.sleep (15.0)
                                    complete = 1
                                
                                if (GPIO.input (27)==1):
                                    image = Image.new('1', (display.width, display.height))
                                    draw = ImageDraw.Draw(image)
                                    draw.rectangle((0, 0, display.width, display.height), outline=255, fill=255)
                                    draw.text((1,0),' Keuze', font=font)
                                    draw.text((1,8),(' Rooibos thee '), font=font)
                                    draw.text((1,16),(' Melk'), font=font)
                                    draw.text((1,24), ' Herkomst', font=font)
                                    draw.text((1,32), land_thee, font=font)
                                    display.image(image)
                                    display.show()
                                    cursor.execute("select Card.cardID, userID, drinkPrice from Koffie.Card join Koffie.User on Card.cardID = User.cardID join Koffie.Drink on User.userID = Drink.drinkID where uidCardNumber = "+ str(id) +" and drinkID = 46;")
                                    cursor.execute("select drinkPrice from Koffie.Drink where drinkID = '1';")
                                    result = cursor.fetchone()
                                    drinkPrice = result[0]
                                    print(drinkPrice)
                                    cursor.execute("select userID from Koffie.Card join Koffie.User on Card.cardID = User.cardID where uidCardNumber = '219196986759';")
                                    result = cursor.fetchone()
                                    userID = result[0] 

                                    cursor.execute("INSERT INTO Koffie.Order(drinkID, userID, cardID, orderDate, orderTime, orderPrice) VALUES (1 , "+ str(userID) +" , 1, CURRENT_DATE(), CURRENT_TIME(),"+ str(drinkPrice) +" );")      
                                            
                                    conn.commit()
                                    time.sleep (15.0)
                                    complete = 1

                                if (GPIO.input (5)==1):
                                    image = Image.new('1', (display.width, display.height))
                                    draw = ImageDraw.Draw(image)
                                    draw.rectangle((0, 0, display.width, display.height), outline=255, fill=255)
                                    draw.text((1,0),' Keuze', font=font)
                                    draw.text((1,8),(' Rooibos thee '), font=font)
                                    draw.text((1,16),(' Suiker'), font=font)
                                    draw.text((1,24), ' Herkomst', font=font)
                                    draw.text((1,32), land_thee, font=font)
                                    display.image(image)
                                    display.show()
                                    cursor.execute("select Card.cardID, userID, drinkPrice from Koffie.Card join Koffie.User on Card.cardID = User.cardID join Koffie.Drink on User.userID = Drink.drinkID where uidCardNumber = "+ str(id) +" and drinkID = 47;")
                                    cursor.execute("select drinkPrice from Koffie.Drink where drinkID = '1';")
                                    result = cursor.fetchone()
                                    drinkPrice = result[0]
                                    print(drinkPrice)
                                    cursor.execute("select userID from Koffie.Card join Koffie.User on Card.cardID = User.cardID where uidCardNumber = '219196986759';")
                                    result = cursor.fetchone()
                                    userID = result[0] 

                                    cursor.execute("INSERT INTO Koffie.Order(drinkID, userID, cardID, orderDate, orderTime, orderPrice) VALUES (1 , "+ str(userID) +" , 1, CURRENT_DATE(), CURRENT_TIME(),"+ str(drinkPrice) +" );")      
                                            
                                    conn.commit()
                                    time.sleep (15.0)
                                    complete = 1

                                if (GPIO.input (6)==1):
                                    image = Image.new('1', (display.width, display.height))
                                    draw = ImageDraw.Draw(image)
                                    draw.rectangle((0, 0, display.width, display.height), outline=255, fill=255)
                                    draw.text((1,0),' Keuze', font=font)
                                    draw.text((1,8),(' Rooibos thee '), font=font)
                                    draw.text((1,16),(' Melk+Suiker'), font=font)
                                    draw.text((1,24), ' Herkomst', font=font)
                                    draw.text((1,32), land_thee, font=font)
                                    display.image(image)
                                    display.show()
                                    cursor.execute("select Card.cardID, userID, drinkPrice from Koffie.Card join Koffie.User on Card.cardID = User.cardID join Koffie.Drink on User.userID = Drink.drinkID where uidCardNumber = "+ str(id) +" and drinkID = 48;")
                                    cursor.execute("select drinkPrice from Koffie.Drink where drinkID = '1';")
                                    result = cursor.fetchone()
                                    drinkPrice = result[0]
                                    print(drinkPrice)
                                    cursor.execute("select userID from Koffie.Card join Koffie.User on Card.cardID = User.cardID where uidCardNumber = '219196986759';")
                                    result = cursor.fetchone()
                                    userID = result[0] 

                                    cursor.execute("INSERT INTO Koffie.Order(drinkID, userID, cardID, orderDate, orderTime, orderPrice) VALUES (1 , "+ str(userID) +" , 1, CURRENT_DATE(), CURRENT_TIME(),"+ str(drinkPrice) +" );")      
                                            
                                    conn.commit()
                                    time.sleep (15.0)
                                    complete = 1
                            
                    
                
except KeyboardInterrupt:
	#cleanup
	GPIO.cleanup()
	print("clean closed")
    
