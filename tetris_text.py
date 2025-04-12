#!/usr/bin/env python
import time
import sys
import os
import argparse

# Add parent directory to path so we can import tetris_animation
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from tetris_animation import TetrisMatrixDraw

class TetrisText:
    def __init__(self):
        # Configure command line arguments for the RGB matrix
        parser = argparse.ArgumentParser()
        parser.add_argument("-r", "--led-rows", action="store", help="Display rows (default: 32)", default=32, type=int)
        parser.add_argument("--led-cols", action="store", help="Display columns (default: 64)", default=64, type=int)
        parser.add_argument("-c", "--led-chain", action="store", help="Daisy-chained boards (default: 1)", default=1, type=int)
        parser.add_argument("-P", "--led-parallel", action="store", help="Parallel chains (default: 1)", default=1, type=int)
        parser.add_argument("-b", "--led-brightness", action="store", help="Brightness (default: 100)", default=100, type=int)
        parser.add_argument("-m", "--led-gpio-mapping", help="Hardware mapping", default="regular", 
                           choices=['regular', 'adafruit-hat', 'adafruit-hat-pwm'])
        parser.add_argument("--text", help="Text to display (default: HELLO)", default="HELLO", type=str)
        
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
        if self.args.led_rows >= 64:
            self.tetris.scale = 2
        else:
            self.tetris.scale = 1

    def run(self):
        try:
            print(f"Displaying text: {self.args.text}")
            print("Press CTRL-C to exit")
            
            # Set the text
            self.tetris.set_text(self.args.text.upper(), True)
            animation_complete = False
            
            while True:
                # Clear the matrix
                self.matrix.Clear()
                
                # Draw the animated text
                # Center it on the display
                x_pos = (self.matrix.width - self.tetris.calculate_width()) // 2
                y_pos = self.matrix.height - 2
                
                animation_complete = self.tetris.draw_text(x_pos, y_pos)
                
                if animation_complete:
                    # Wait a bit before restarting the animation
                    time.sleep(3)
                    self.tetris.set_text(self.args.text.upper(), True)
                    animation_complete = False
                
                # Small delay before next animation frame
                time.sleep(0.05)
                
        except KeyboardInterrupt:
            print("Exiting...")
            sys.exit(0)

# Main function
if __name__ == "__main__":
    tetris_text = TetrisText()
    tetris_text.run()