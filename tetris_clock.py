#!/usr/bin/env python
import time
import sys
import os
import datetime
import argparse

# Add parent directory to path so we can import tetris_animation
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from tetris_animation import TetrisMatrixDraw

class TetrisClock:
    def __init__(self):
        # Configure command line arguments for the RGB matrix
        parser = argparse.ArgumentParser()
        parser.add_argument("-r", "--led-rows", action="store", help="Display rows (default: 32)", default=32, type=int)
        parser.add_argument("--led-cols", action="store", help="Display columns (default: 64)", default=64, type=int)
        parser.add_argument("-c", "--led-chain", action="store", help="Daisy-chained boards (default: 1)", default=1, type=int)
        parser.add_argument("-P", "--led-parallel", action="store", help="Parallel chains (default: 1)", default=1, type=int)
        parser.add_argument("-b", "--led-brightness", action="store", help="Brightness (default: 100)", default=50, type=int)
        parser.add_argument("-m", "--led-gpio-mapping", help="Hardware mapping", default="adafruit-hat", 
                           choices=['regular', 'adafruit-hat', 'adafruit-hat-pwm'])
        
        self.args = parser.parse_args()
        
        # Set up the RGB matrix
        options = RGBMatrixOptions()
        options.rows = self.args.led_rows
        options.cols = self.args.led_cols
        options.chain_length = self.args.led_chain
        options.parallel = self.args.led_parallel
        options.brightness = self.args.led_brightness
        options.hardware_mapping = self.args.led_gpio_mapping
        
        self.matrix = RGBMatrix(options=options)
        
        # Initialize the Tetris animation
        self.tetris = TetrisMatrixDraw(self.matrix)
        
        # Set initial scale based on matrix size
        # if self.args.led_rows >= 64:
        #     self.tetris.scale = 2
        # else:
        self.tetris.scale = 2

    def run(self):
        try:
            print("Press CTRL-C to stop the clock")
            
            last_time = ""
            animation_complete = True
            colon_time = 0
            sleep_time = 0.05
            show_colon = True
            
            while True:
                # Get current time
                now = datetime.datetime.now()
                current_time = now.strftime("%H:%M")
                
                # Set new time if changed or animation completed
                if current_time != last_time or animation_complete:
                    self.tetris.set_time(current_time, animation_complete)
                    last_time = current_time
                    animation_complete = False
                
                # Clear the matrix
                self.matrix.Clear()

                colon_time += sleep_time

                if colon_time >= 1:
                    show_colon = not show_colon
                    colon_time = 0
                
                animation_complete = self.tetris.draw_numbers(2, 26, show_colon)
                
                # Small delay before next animation frame
                time.sleep(sleep_time)
                
        except KeyboardInterrupt:
            print("Exiting...")
            sys.exit(0)

# Main function
if __name__ == "__main__":
    tetris_clock = TetrisClock()
    tetris_clock.run()