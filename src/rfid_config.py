import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from time import sleep


GPIO.setwarnings(False)
reader = SimpleMFRC522()

try:
    while True:
        print("\n\nPlease scan your RFID tag.")
        id, text = reader.read()
        print(f"ID: {id}; Text: {text}")

        ans = input("Do you want to overwrite it? [Y/n] ").lower()
        if ans == "y" or ans == "yes":
            ans = input("New text: ")
            reader.write(ans)
            print("Succeeded to write new data.")

        sleep(3)

except KeyboardInterrupt:
    GPIO.cleanup()
    raise
