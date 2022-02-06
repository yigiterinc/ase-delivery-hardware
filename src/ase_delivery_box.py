import RPi.GPIO as GPIO
import json

from mfrc522 import SimpleMFRC522
from box_controller import BoxController


def main() -> None:
    # GPIO initial configuration
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    
    # Define GPIO outputs, namely LEDs
    led_red = 38
    led_green = 40
    photo_res = 36

    # Initialize box controller
    box_controller = BoxController(led_green, led_red, photo_res)

    # Initialize RFID reader
    reader = SimpleMFRC522()

    # Load configuration file
    id, name, address = '', '', ''
    with open("resources/config.json") as config_json:
        data = json.load(config_json)
        box_id = data["ID"]
        box_name = data["NAME"]
        box_address = data["ADDRESS"]
    
    try:
        # Control loop
        while True:

            # Welcome message
            print(f"Welcome to the {box_name} {box_id} of {box_address}.\nPlease scan your RFID card.")

            # Read RFID card
            rfid_user_id = None
            while True:
                _, rfid_user_id = reader.read()
                if rfid_user_id != '':
                    break
                print("\nPlease scan your card again!")


            # Authentication
            box_controller.handle_new_customer(rfid_user_id.split()[0])
            
    # Handle keyboard interrupt and clean GPIOs
    except KeyboardInterrupt:
        GPIO.cleanup()
        raise 
        
    
if __name__ == "__main__":
    main()
    