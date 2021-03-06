from communication_controller import CommunicationController
from led_controller import LEDController
from photo_resistor_controller import PhotoResistorController

from time import time_ns


class BoxController:
    
    def __init__(self, led_green : int, led_red : int, photo_res : int) -> None:
        # Save LEDs, photo resistor and time configurations
        self.led_green = led_green
        self.led_red = led_red
        self.photo_res = photo_res
        self.open_secs = 0
        
        # Constant value configurations
        self.led_blinking_secs = 1
        self.led_confirmation_secs = 3
        self.opening_secs = 1e10
        self.brightness_closed = 0

        # Setup controllers for LEDs and photoresistor
        self.led_controller = LEDController([led_green, led_red])
        self.photo_resistor_controller = PhotoResistorController(photo_res)

        # Setup communication controller to perform authentication
        params = {
            "mode": "cors",
            "cache": "no-chache",
            "credentials": "include",
            "redirect": "follow",
            "referrerPolicy": "origin-when-cross-origin"
        }
        self.communication_controller = CommunicationController(params)


    def __unlock(self) -> None:
        # Set absolute starting time
        while self.photo_resistor_controller.read_brightness() == self.brightness_closed:
            pass
        self.open_secs = time_ns()


    def __lock(self) -> None:
        # As long as the brightness level does not embodies a closed box
        while self.photo_resistor_controller.read_brightness() != self.brightness_closed:
            # Check if allowed opening time is exceeded and if yes toggle red LED
            if time_ns() - self.open_secs > self.opening_secs:
                self.led_controller.toggle(self.led_red, self.led_blinking_secs)   


    def handle_new_customer(self, user_id : int) -> None:
        # Check if customer is authenticated and if yes toggle green LED
        if self.communication_controller.authenticate(user_id):
            self.led_controller.toggle(self.led_green, self.led_confirmation_secs)
            self.__unlock()
            self.__lock()
        # Otherwise toggle red LED
        else:
            self.led_controller.toggle(self.led_red, self.led_confirmation_secs) 
