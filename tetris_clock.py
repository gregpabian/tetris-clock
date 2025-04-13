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
        parser.add_argument("--fps", action="store", help="Frames per second (default: 20)", default=20, type=int)
        
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
        
        # Create the first canvas that we'll draw into and then swap
        self.offscreen_canvas = self.matrix.CreateFrameCanvas()
        
        # Initialize the Tetris animation
        self.tetris = TetrisMatrixDraw(self.offscreen_canvas)
        
        # Set scale based on matrix size
        self.tetris.scale = 2
        
        # Calculate sleep time based on desired FPS
        self.sleep_time = 1.0 / self.args.fps

    def run(self):
        try:
            print("Press CTRL-C to stop the clock")
            
            last_time = ""
            colon_time = 0
            show_colon = True
            
            # Initial setup - force animation on first run
            now = datetime.datetime.now()
            current_time = now.strftime("%H:%M")
            self.tetris.set_time(current_time, True)
            animation_active = True
            
            while True:
                # Get current time
                now = datetime.datetime.now()
                current_time = now.strftime("%H:%M")
                
                # Check if time has changed
                if current_time != last_time:
                    # Time has changed, start a new animation
                    self.tetris.set_time(current_time, True)
                    last_time = current_time
                    animation_active = True
                
                # Clear the offscreen canvas
                self.offscreen_canvas.Clear()

                # Update colon blinking
                colon_time += self.sleep_time
                if colon_time >= 1:
                    show_colon = not show_colon
                    colon_time = 0
                
                # Draw the current state
                animation_complete = self.tetris.draw_numbers(2, 26, show_colon)
                
                # If animation just completed, update state
                if animation_active and animation_complete:
                    animation_active = False
                
                # Swap buffers
                self.offscreen_canvas = self.matrix.SwapOnVSync(self.offscreen_canvas)
                
                # Determine sleep time - shorter during animation for smoother motion
                # Longer when static to save CPU
                if animation_active:
                    time.sleep(self.sleep_time)
                else:
                    # When not animating, we only need to update to blink the colon
                    # We can sleep longer, but still need to wake up to check time changes
                    time.sleep(0.25)  # Check for time changes and update colon 4 times per second
                
        except KeyboardInterrupt:
            print("Exiting...")
            sys.exit(0)

# Main function
if __name__ == "__main__":
    tetris_clock = TetrisClock()
    tetris_clock.run()