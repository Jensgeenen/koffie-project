import RPi.GPIO as GPIO
import time
import busio
import digitalio
import board
import adafruit_pcd8544
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

GPIO.setmode (GPIO.BCM)
GPIO.setup (17, GPIO.IN) # GPIO 17 input knop 1
GPIO.setup (27, GPIO.IN) # GPIO 27 input knop 2
GPIO.setup (5, GPIO.IN) # GPIO 5 input knop 3
GPIO.setup (6, GPIO.IN) # GPIO 6 input knop 4

value = 1
complete = 0

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

# Load default font.
font = ImageFont.load_default()
#font=ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSansBold.ttf", 10)

# Get drawing object to draw on image
image = Image.new('1', (display.width, display.height))
draw = ImageDraw.Draw(image)

# Draw a white filled box to clear the image.
draw.rectangle((0, 0, display.width, display.height), outline=255, fill=255)

# Write some text.
draw.text((1,0), '', font=font)
draw.text((1,8), 'Scan je kaart', font=font)
draw.text((1,16), 'HIER', font=font)
draw.text((1,24), '', font=font)
draw.text((1,32), '', font=font)
display.image(image)
display.show()
try:
    while True:
        complete = 0
        if (value == 1 ):
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


            if (GPIO.input (17)==1): #input high active
                while complete != 1:
                    image = Image.new('1', (display.width, display.height))
                    draw = ImageDraw.Draw(image)
                    draw.rectangle((0, 0, display.width, display.height), outline=255, fill=255)
                    draw.text((1,0),'Opties', font=font)
                    draw.text((1,8), (str(1)+ ' Koffie'), font=font)
                    draw.text((1,16), (str(2)+ 'Latte macchiato'), font=font)
                    draw.text((1,24), (str(3)+ 'Cappuccino'), font=font)
                    draw.text((1,32), (str(4)+ 'Espresso'), font=font)
                    display.image(image)
                    display.show()
                    time.sleep (0.3)
                    complete = 1


            if (GPIO.input (5)==1): #input high active
                while complete != 1:
                    image = Image.new('1', (display.width, display.height))
                    draw = ImageDraw.Draw(image)
                    draw.rectangle((0, 0, display.width, display.height), outline=255, fill=255)
                    draw.text((1,0),'Opties', font=font)
                    draw.text((1,8), (str(1)+ ' Citroen'), font=font)
                    draw.text((1,16), (str(2)+ 'Rooibos'), font=font)
                    draw.text((1,24), '', font=font)
                    draw.text((1,32), '', font=font)
                    display.image(image)
                    display.show()
                    time.sleep (0.3)
                    complete = 1
                
except KeyboardInterrupt:
	#cleanup
	GPIO.cleanup()
	print("clean closed")
