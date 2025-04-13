#!/usr/bin/env python
class FallInstruction:
    """Type that describes how a brick is falling down"""
    def __init__(self, blocktype, color, x_pos, y_stop, num_rot):
        self.blocktype = blocktype  # Number of the block type
        self.color = color          # Color of the brick
        self.x_pos = x_pos          # x-position where the brick should be placed
        self.y_stop = y_stop        # y-position where the brick should stop falling
        self.num_rot = num_rot      # Number of 90-degree rotations applied to the brick


class NumState:
    """Type that describes the current state of a drawn number or character"""
    def __init__(self):
        self.num_to_draw = -1      # Number/character to draw (ASCII value)
        self.blockindex = 0        # Index of the currently falling brick
        self.fallindex = 0         # y-position that the brick already has
        self.x_shift = 0           # x-position relative to the starting point


# Constants
TETRIS_MAX_NUMBERS = 9
TETRIS_DISTANCE_BETWEEN_DIGITS = 7
TETRIS_Y_DROP_DEFAULT = 16


class TetrisMatrixDraw:
    """Python port of the TetrisMatrixDraw library"""
    def __init__(self, canvas):
        """Initialize with an RGB matrix canvas instance"""
        self.canvas = canvas
        self.numstates = [NumState() for _ in range(TETRIS_MAX_NUMBERS)]
        self.sizeOfValue = 0
        self._debug = False
        self.scale = 1
        self.drawOutline = False
        self.outLineColour = (0, 0, 0)  # RGB black
        
        # Define Tetris colors (RGB)
        self.tetrisRED = (255, 0, 0)
        self.tetrisGREEN = (0, 255, 0)
        self.tetrisBLUE = (0, 50, 255)
        self.tetrisWHITE = (255, 255, 255)
        self.tetrisYELLOW = (255, 255, 0)
        self.tetrisCYAN = (0, 255, 255)
        self.tetrisMAGENTA = (255, 0, 255)
        self.tetrisORANGE = (255, 128, 0)
        self.tetrisBLACK = (0, 0, 0)
        
        self.tetrisColors = [
            self.tetrisRED, 
            self.tetrisGREEN, 
            self.tetrisBLUE, 
            self.tetrisWHITE, 
            self.tetrisYELLOW, 
            self.tetrisCYAN, 
            self.tetrisMAGENTA, 
            self.tetrisORANGE,
            self.tetrisBLACK
        ]
        
        # Initialize the fall instruction data for numbers and characters
        self._init_fall_instructions()

    def _init_fall_instructions(self):
        """Initialize all fall instructions for numbers and letters"""
        # Number 0 fall instructions
        self.num_0 = [
            FallInstruction(2, 5, 4, 16, 0),
            FallInstruction(4, 7, 2, 16, 1),
            FallInstruction(3, 4, 0, 16, 1),
            FallInstruction(6, 6, 1, 16, 1),
            FallInstruction(5, 1, 4, 14, 0),
            FallInstruction(6, 6, 0, 13, 3),
            FallInstruction(5, 1, 4, 12, 0),
            FallInstruction(5, 1, 0, 11, 0),
            FallInstruction(6, 6, 4, 10, 1),
            FallInstruction(6, 6, 0, 9, 1),
            FallInstruction(5, 1, 1, 8, 1),
            FallInstruction(2, 5, 3, 8, 3)
        ]
        
        # Number 1 fall instructions
        self.num_1 = [
            FallInstruction(2, 5, 4, 16, 0),
            FallInstruction(3, 4, 4, 15, 1),
            FallInstruction(3, 4, 5, 13, 3),
            FallInstruction(2, 5, 4, 11, 2),
            FallInstruction(0, 0, 4, 8, 0)
        ]
        
        # Number 2 fall instructions
        self.num_2 = [
            FallInstruction(0, 0, 4, 16, 0),
            FallInstruction(3, 4, 0, 16, 1),
            FallInstruction(1, 2, 1, 16, 3),
            FallInstruction(1, 2, 1, 15, 0),
            FallInstruction(3, 4, 1, 12, 2),
            FallInstruction(1, 2, 0, 12, 1),
            FallInstruction(2, 5, 3, 12, 3),
            FallInstruction(0, 0, 4, 10, 0),
            FallInstruction(3, 4, 1, 8, 0),
            FallInstruction(2, 5, 3, 8, 3),
            FallInstruction(1, 2, 0, 8, 1)
        ]
        
        # Number 3 fall instructions
        self.num_3 = [
            FallInstruction(1, 2, 3, 16, 3),
            FallInstruction(2, 5, 0, 16, 1),
            FallInstruction(3, 4, 1, 15, 2),
            FallInstruction(0, 0, 4, 14, 0),
            FallInstruction(3, 4, 1, 12, 2),
            FallInstruction(1, 2, 0, 12, 1),
            FallInstruction(3, 4, 5, 12, 3),
            FallInstruction(2, 5, 3, 11, 0),
            FallInstruction(3, 4, 1, 8, 0),
            FallInstruction(1, 2, 0, 8, 1),
            FallInstruction(2, 5, 3, 8, 3)
        ]
        
        # Number 4 fall instructions
        self.num_4 = [
            FallInstruction(0, 0, 4, 16, 0),
            FallInstruction(0, 0, 4, 14, 0),
            FallInstruction(3, 4, 1, 12, 0),
            FallInstruction(1, 2, 0, 12, 1),
            FallInstruction(2, 5, 0, 10, 0),
            FallInstruction(2, 5, 3, 12, 3),
            FallInstruction(3, 4, 4, 10, 3),
            FallInstruction(2, 5, 0, 9, 2),
            FallInstruction(3, 4, 5, 10, 1)
        ]
        
        # Number 5 fall instructions
        self.num_5 = [
            FallInstruction(0, 0, 0, 16, 0),
            FallInstruction(2, 5, 2, 16, 1),
            FallInstruction(2, 5, 3, 15, 0),
            FallInstruction(3, 4, 5, 16, 1),
            FallInstruction(3, 4, 1, 12, 0),
            FallInstruction(1, 2, 0, 12, 1),
            FallInstruction(2, 5, 3, 12, 3),
            FallInstruction(0, 0, 0, 10, 0),
            FallInstruction(3, 4, 1, 8, 2),
            FallInstruction(1, 2, 0, 8, 1),
            FallInstruction(2, 5, 3, 8, 3)
        ]
        
        # Number 6 fall instructions
        self.num_6 = [
            FallInstruction(2, 5, 0, 16, 1),
            FallInstruction(5, 1, 2, 16, 1),
            FallInstruction(6, 6, 0, 15, 3),
            FallInstruction(6, 6, 4, 16, 3),
            FallInstruction(5, 1, 4, 14, 0),
            FallInstruction(3, 4, 1, 12, 2),
            FallInstruction(2, 5, 0, 13, 2),
            FallInstruction(3, 4, 2, 11, 0),
            FallInstruction(0, 0, 0, 10, 0),
            FallInstruction(3, 4, 1, 8, 0),
            FallInstruction(1, 2, 0, 8, 1),
            FallInstruction(2, 5, 3, 8, 3)
        ]
        
        # Number 7 fall instructions
        self.num_7 = [
            FallInstruction(0, 0, 4, 16, 0),
            FallInstruction(1, 2, 4, 14, 0),
            FallInstruction(3, 4, 5, 13, 1),
            FallInstruction(2, 5, 4, 11, 2),
            FallInstruction(3, 4, 1, 8, 2),
            FallInstruction(2, 5, 3, 8, 3),
            FallInstruction(1, 2, 0, 8, 1)
        ]
        
        # Number 8 fall instructions
        self.num_8 = [
            FallInstruction(3, 4, 1, 16, 0),
            FallInstruction(6, 6, 0, 16, 1),
            FallInstruction(3, 4, 5, 16, 1),
            FallInstruction(1, 2, 2, 15, 3),
            FallInstruction(4, 7, 0, 14, 0),
            FallInstruction(1, 2, 1, 12, 3),
            FallInstruction(6, 6, 4, 13, 1),
            FallInstruction(2, 5, 0, 11, 1),
            FallInstruction(4, 7, 0, 10, 0),
            FallInstruction(4, 7, 4, 11, 0),
            FallInstruction(5, 1, 0, 8, 1),
            FallInstruction(5, 1, 2, 8, 1),
            FallInstruction(1, 2, 4, 9, 2)
        ]
        
        # Number 9 fall instructions
        self.num_9 = [
            FallInstruction(0, 0, 0, 16, 0),
            FallInstruction(3, 4, 2, 16, 0),
            FallInstruction(1, 2, 2, 15, 3),
            FallInstruction(1, 2, 4, 15, 2),
            FallInstruction(3, 4, 1, 12, 2),
            FallInstruction(3, 4, 5, 12, 3),
            FallInstruction(5, 1, 0, 12, 0),
            FallInstruction(1, 2, 2, 11, 3),
            FallInstruction(5, 1, 4, 9, 0),
            FallInstruction(6, 6, 0, 10, 1),
            FallInstruction(5, 1, 0, 8, 1),
            FallInstruction(6, 6, 2, 8, 2)
        ]
        
        # Store sizes of each number's fall instruction array
        self.blocks_per_number = [12, 5, 11, 11, 9, 11, 12, 7, 13, 12]
        
        # Store references to number arrays for easy access
        self.number_arrays = [
            self.num_0, self.num_1, self.num_2, self.num_3, self.num_4,
            self.num_5, self.num_6, self.num_7, self.num_8, self.num_9
        ]
        
        # Initialize letter arrays (simplified version - in a full implementation, 
        # you would include all letters from TetrisLetters.h)
        self.letter_arrays = {}
        self.blocks_per_char = {}
        
        # As a simple example, define letter 'A' (ASCII 65)
        self.letter_arrays[65] = [
            FallInstruction(0, 2, 0, 16, 0),
            FallInstruction(0, 1, 4, 16, 0),
            FallInstruction(5, 5, 3, 14, 1),
            FallInstruction(4, 2, 0, 14, 1),
            FallInstruction(4, 1, 4, 13, 0),
            FallInstruction(5, 0, 0, 13, 0),
            FallInstruction(4, 3, 4, 11, 0),
            FallInstruction(5, 2, 0, 11, 0),
            FallInstruction(0, 1, 2, 10, 0)
        ]
        self.blocks_per_char[65] = 9
        
        # Add more letters as needed for your application

    def reset_num_states(self):
        """Reset the state of all digits"""
        for i in range(TETRIS_MAX_NUMBERS):
            self.numstates[i].num_to_draw = -1
            self.numstates[i].fallindex = 0
            self.numstates[i].blockindex = 0
            self.numstates[i].x_shift = 0

    def set_num_state(self, index, value, x_shift):
        """Set the state of a digit at a given index"""
        if index < TETRIS_MAX_NUMBERS:
            if self._debug:
                print(f"Setting digit {index} to value {value}")
            self.numstates[index].num_to_draw = value
            self.numstates[index].x_shift = x_shift
            self.numstates[index].fallindex = 0
            self.numstates[index].blockindex = 0

    def set_time(self, time_str, force_refresh=False):
        """Set the time to display (format: "12:34")"""
        self.sizeOfValue = 4
        time_str = time_str.replace(":", "")
        for pos in range(4):
            x_offset = pos * TETRIS_DISTANCE_BETWEEN_DIGITS * self.scale
            if pos >= 2:
                x_offset += (3 * self.scale)
            
            individual_number = time_str[pos] if pos < len(time_str) else " "
            number = int(individual_number) if individual_number.isdigit() else -1
            
            # Only change the number if it's different or being forced
            if force_refresh or number != self.numstates[pos].num_to_draw:
                self.set_num_state(pos, number, x_offset)

    def set_numbers(self, value, force_refresh=False):
        """Set numeric value to display"""
        str_value = str(value)
        if len(str_value) <= TETRIS_MAX_NUMBERS:
            self.sizeOfValue = len(str_value)
            for pos in range(self.sizeOfValue):
                current_x_shift = TETRIS_DISTANCE_BETWEEN_DIGITS * self.scale * pos
                number = int(str_value[pos])
                
                # Only change the number if it's different or being forced
                if force_refresh or number != self.numstates[pos].num_to_draw:
                    self.set_num_state(pos, number, current_x_shift)
                else:
                    self.numstates[pos].x_shift = current_x_shift
        else:
            print("Number too long")

    def set_text(self, txt, force_refresh=False):
        """Set text to display"""
        self.sizeOfValue = len(txt)
        for pos in range(self.sizeOfValue):
            current_x_shift = TETRIS_DISTANCE_BETWEEN_DIGITS * self.scale * pos
            letter = txt[pos]
            
            # Only change the letter if it's different or being forced
            if force_refresh or ord(letter) != self.numstates[pos].num_to_draw:
                self.set_num_state(pos, ord(letter), current_x_shift)
            else:
                self.numstates[pos].x_shift = current_x_shift

    def draw_pixel(self, x, y, color):
        """Draw a single pixel on the canvas with the specified color"""
        if 0 <= x < self.canvas.width and 0 <= y < self.canvas.height:
            self.canvas.SetPixel(x, y, color[0], color[1], color[2])

    def draw_shape(self, blocktype, color, x_pos, y_pos, num_rot):
        """Draw a tetris shape at the specified position"""
        # Square
        if blocktype == 0:
            self.draw_pixel(x_pos, y_pos, color)
            self.draw_pixel(x_pos + 1, y_pos, color)
            self.draw_pixel(x_pos, y_pos - 1, color)
            self.draw_pixel(x_pos + 1, y_pos - 1, color)
        
        # L-Shape
        elif blocktype == 1:
            if num_rot == 0:
                self.draw_pixel(x_pos, y_pos, color)
                self.draw_pixel(x_pos + 1, y_pos, color)
                self.draw_pixel(x_pos, y_pos - 1, color)
                self.draw_pixel(x_pos, y_pos - 2, color)
            elif num_rot == 1:
                self.draw_pixel(x_pos, y_pos, color)
                self.draw_pixel(x_pos, y_pos - 1, color)
                self.draw_pixel(x_pos + 1, y_pos - 1, color)
                self.draw_pixel(x_pos + 2, y_pos - 1, color)
            elif num_rot == 2:
                self.draw_pixel(x_pos + 1, y_pos, color)
                self.draw_pixel(x_pos + 1, y_pos - 1, color)
                self.draw_pixel(x_pos + 1, y_pos - 2, color)
                self.draw_pixel(x_pos, y_pos - 2, color)
            elif num_rot == 3:
                self.draw_pixel(x_pos, y_pos, color)
                self.draw_pixel(x_pos + 1, y_pos, color)
                self.draw_pixel(x_pos + 2, y_pos, color)
                self.draw_pixel(x_pos + 2, y_pos - 1, color)
        
        # L-Shape (reverse)
        elif blocktype == 2:
            if num_rot == 0:
                self.draw_pixel(x_pos, y_pos, color)
                self.draw_pixel(x_pos + 1, y_pos, color)
                self.draw_pixel(x_pos + 1, y_pos - 1, color)
                self.draw_pixel(x_pos + 1, y_pos - 2, color)
            elif num_rot == 1:
                self.draw_pixel(x_pos, y_pos, color)
                self.draw_pixel(x_pos + 1, y_pos, color)
                self.draw_pixel(x_pos + 2, y_pos, color)
                self.draw_pixel(x_pos, y_pos - 1, color)
            elif num_rot == 2:
                self.draw_pixel(x_pos, y_pos, color)
                self.draw_pixel(x_pos, y_pos - 1, color)
                self.draw_pixel(x_pos, y_pos - 2, color)
                self.draw_pixel(x_pos + 1, y_pos - 2, color)
            elif num_rot == 3:
                self.draw_pixel(x_pos, y_pos - 1, color)
                self.draw_pixel(x_pos + 1, y_pos - 1, color)
                self.draw_pixel(x_pos + 2, y_pos - 1, color)
                self.draw_pixel(x_pos + 2, y_pos, color)
        
        # I-Shape
        elif blocktype == 3:
            if num_rot == 0 or num_rot == 2:  # Horizontal
                self.draw_pixel(x_pos, y_pos, color)
                self.draw_pixel(x_pos + 1, y_pos, color)
                self.draw_pixel(x_pos + 2, y_pos, color)
                self.draw_pixel(x_pos + 3, y_pos, color)
            else:  # Vertical
                self.draw_pixel(x_pos, y_pos, color)
                self.draw_pixel(x_pos, y_pos - 1, color)
                self.draw_pixel(x_pos, y_pos - 2, color)
                self.draw_pixel(x_pos, y_pos - 3, color)
        
        # S-Shape
        elif blocktype == 4:
            if num_rot == 0 or num_rot == 2:
                self.draw_pixel(x_pos + 1, y_pos, color)
                self.draw_pixel(x_pos, y_pos - 1, color)
                self.draw_pixel(x_pos + 1, y_pos - 1, color)
                self.draw_pixel(x_pos, y_pos - 2, color)
            else:
                self.draw_pixel(x_pos, y_pos, color)
                self.draw_pixel(x_pos + 1, y_pos, color)
                self.draw_pixel(x_pos + 1, y_pos - 1, color)
                self.draw_pixel(x_pos + 2, y_pos - 1, color)
        
        # S-Shape (reversed)
        elif blocktype == 5:
            if num_rot == 0 or num_rot == 2:
                self.draw_pixel(x_pos, y_pos, color)
                self.draw_pixel(x_pos, y_pos - 1, color)
                self.draw_pixel(x_pos + 1, y_pos - 1, color)
                self.draw_pixel(x_pos + 1, y_pos - 2, color)
            else:
                self.draw_pixel(x_pos + 1, y_pos, color)
                self.draw_pixel(x_pos + 2, y_pos, color)
                self.draw_pixel(x_pos, y_pos - 1, color)
                self.draw_pixel(x_pos + 1, y_pos - 1, color)
        
        # Half cross
        elif blocktype == 6:
            if num_rot == 0:
                self.draw_pixel(x_pos, y_pos, color)
                self.draw_pixel(x_pos + 1, y_pos, color)
                self.draw_pixel(x_pos + 2, y_pos, color)
                self.draw_pixel(x_pos + 1, y_pos - 1, color)
            elif num_rot == 1:
                self.draw_pixel(x_pos, y_pos, color)
                self.draw_pixel(x_pos, y_pos - 1, color)
                self.draw_pixel(x_pos, y_pos - 2, color)
                self.draw_pixel(x_pos + 1, y_pos - 1, color)
            elif num_rot == 2:
                self.draw_pixel(x_pos + 1, y_pos, color)
                self.draw_pixel(x_pos, y_pos - 1, color)
                self.draw_pixel(x_pos + 1, y_pos - 1, color)
                self.draw_pixel(x_pos + 2, y_pos - 1, color)
            elif num_rot == 3:
                self.draw_pixel(x_pos + 1, y_pos, color)
                self.draw_pixel(x_pos, y_pos - 1, color)
                self.draw_pixel(x_pos + 1, y_pos - 1, color)
                self.draw_pixel(x_pos + 1, y_pos - 2, color)
        
        # Corner-Shape
        elif blocktype == 7:
            if num_rot == 0:
                self.draw_pixel(x_pos, y_pos, color)
                self.draw_pixel(x_pos + 1, y_pos, color)
                self.draw_pixel(x_pos, y_pos - 1, color)
            elif num_rot == 1:
                self.draw_pixel(x_pos, y_pos, color)
                self.draw_pixel(x_pos, y_pos - 1, color)
                self.draw_pixel(x_pos + 1, y_pos - 1, color)
            elif num_rot == 2:
                self.draw_pixel(x_pos + 1, y_pos, color)
                self.draw_pixel(x_pos + 1, y_pos - 1, color)
                self.draw_pixel(x_pos, y_pos - 1, color)
            elif num_rot == 3:
                self.draw_pixel(x_pos, y_pos, color)
                self.draw_pixel(x_pos + 1, y_pos, color)
                self.draw_pixel(x_pos + 1, y_pos - 1, color)

    def fill_rect(self, x, y, w, h, color):
        """Draw a filled rectangle"""
        for i in range(w):
            for j in range(h):
                self.draw_pixel(x + i, y + j, color)

    def draw_rect(self, x, y, w, h, color):
        """Draw a rectangle outline"""
        for i in range(w):
            self.draw_pixel(x + i, y, color)
            self.draw_pixel(x + i, y + h - 1, color)
        for j in range(h):
            self.draw_pixel(x, y + j, color)
            self.draw_pixel(x + w - 1, y + j, color)

    def draw_larger_block(self, x_pos, y_pos, scale, color):
        """Draw a scaled block"""
        self.fill_rect(x_pos, y_pos, scale, scale, color)
        if self.drawOutline:
            self.draw_rect(x_pos, y_pos, scale, scale, self.outLineColour)

    def draw_larger_shape(self, scale, blocktype, color, x_pos, y_pos, num_rot):
        """Draw a scaled shape"""
        offset1 = 1 * scale
        offset2 = 2 * scale
        offset3 = 3 * scale
        
        # Square
        if blocktype == 0:
            self.draw_larger_block(x_pos, y_pos, scale, color)
            self.draw_larger_block(x_pos + offset1, y_pos, scale, color)
            self.draw_larger_block(x_pos, y_pos - offset1, scale, color)
            self.draw_larger_block(x_pos + offset1, y_pos - offset1, scale, color)
            return
        
        # L-Shape
        elif blocktype == 1:
            if num_rot == 0:
                self.draw_larger_block(x_pos, y_pos, scale, color)
                self.draw_larger_block(x_pos + offset1, y_pos, scale, color)
                self.draw_larger_block(x_pos, y_pos - offset1, scale, color)
                self.draw_larger_block(x_pos, y_pos - offset2, scale, color)
            elif num_rot == 1:
                self.draw_larger_block(x_pos, y_pos, scale, color)
                self.draw_larger_block(x_pos, y_pos - offset1, scale, color)
                self.draw_larger_block(x_pos + offset1, y_pos - offset1, scale, color)
                self.draw_larger_block(x_pos + offset2, y_pos - offset1, scale, color)
            elif num_rot == 2:
                self.draw_larger_block(x_pos + offset1, y_pos, scale, color)
                self.draw_larger_block(x_pos + offset1, y_pos - offset1, scale, color)
                self.draw_larger_block(x_pos + offset1, y_pos - offset2, scale, color)
                self.draw_larger_block(x_pos, y_pos - offset2, scale, color)
            elif num_rot == 3:
                self.draw_larger_block(x_pos, y_pos, scale, color)
                self.draw_larger_block(x_pos + offset1, y_pos, scale, color)
                self.draw_larger_block(x_pos + offset2, y_pos, scale, color)
                self.draw_larger_block(x_pos + offset2, y_pos - offset1, scale, color)
        
        # L-Shape (reverse)
        elif blocktype == 2:
            if num_rot == 0:
                self.draw_larger_block(x_pos, y_pos, scale, color)
                self.draw_larger_block(x_pos + offset1, y_pos, scale, color)
                self.draw_larger_block(x_pos + offset1, y_pos - offset1, scale, color)
                self.draw_larger_block(x_pos + offset1, y_pos - offset2, scale, color)
            elif num_rot == 1:
                self.draw_larger_block(x_pos, y_pos, scale, color)
                self.draw_larger_block(x_pos + offset1, y_pos, scale, color)
                self.draw_larger_block(x_pos + offset2, y_pos, scale, color)
                self.draw_larger_block(x_pos, y_pos - offset1, scale, color)
            elif num_rot == 2:
                self.draw_larger_block(x_pos, y_pos, scale, color)
                self.draw_larger_block(x_pos, y_pos - offset1, scale, color)
                self.draw_larger_block(x_pos, y_pos - offset2, scale, color)
                self.draw_larger_block(x_pos + offset1, y_pos - offset2, scale, color)
            elif num_rot == 3:
                self.draw_larger_block(x_pos, y_pos - offset1, scale, color)
                self.draw_larger_block(x_pos + offset1, y_pos - offset1, scale, color)
                self.draw_larger_block(x_pos + offset2, y_pos - offset1, scale, color)
                self.draw_larger_block(x_pos + offset2, y_pos, scale, color)
        
        # I-Shape
        elif blocktype == 3:
            if num_rot == 0 or num_rot == 2:  # Horizontal
                self.draw_larger_block(x_pos, y_pos, scale, color)
                self.draw_larger_block(x_pos + offset1, y_pos, scale, color)
                self.draw_larger_block(x_pos + offset2, y_pos, scale, color)
                self.draw_larger_block(x_pos + offset3, y_pos, scale, color)
            else:  # Vertical
                self.draw_larger_block(x_pos, y_pos, scale, color)
                self.draw_larger_block(x_pos, y_pos - offset1, scale, color)
                self.draw_larger_block(x_pos, y_pos - offset2, scale, color)
                self.draw_larger_block(x_pos, y_pos - offset3, scale, color)
        
        # S-Shape
        elif blocktype == 4:
            if num_rot == 0 or num_rot == 2:
                self.draw_larger_block(x_pos + offset1, y_pos, scale, color)
                self.draw_larger_block(x_pos, y_pos - offset1, scale, color)
                self.draw_larger_block(x_pos + offset1, y_pos - offset1, scale, color)
                self.draw_larger_block(x_pos, y_pos - offset2, scale, color)
            else:
                self.draw_larger_block(x_pos, y_pos, scale, color)
                self.draw_larger_block(x_pos + offset1, y_pos, scale, color)
                self.draw_larger_block(x_pos + offset1, y_pos - offset1, scale, color)
                self.draw_larger_block(x_pos + offset2, y_pos - offset1, scale, color)
        
        # S-Shape (reversed)
        elif blocktype == 5:
            if num_rot == 0 or num_rot == 2:
                self.draw_larger_block(x_pos, y_pos, scale, color)
                self.draw_larger_block(x_pos, y_pos - offset1, scale, color)
                self.draw_larger_block(x_pos + offset1, y_pos - offset1, scale, color)
                self.draw_larger_block(x_pos + offset1, y_pos - offset2, scale, color)
            else:
                self.draw_larger_block(x_pos + offset1, y_pos, scale, color)
                self.draw_larger_block(x_pos + offset2, y_pos, scale, color)
                self.draw_larger_block(x_pos, y_pos - offset1, scale, color)
                self.draw_larger_block(x_pos + offset1, y_pos - offset1, scale, color)
        
        # Half cross
        elif blocktype == 6:
            if num_rot == 0:
                self.draw_larger_block(x_pos, y_pos, scale, color)
                self.draw_larger_block(x_pos + offset1, y_pos, scale, color)
                self.draw_larger_block(x_pos + offset2, y_pos, scale, color)
                self.draw_larger_block(x_pos + offset1, y_pos - offset1, scale, color)
            elif num_rot == 1:
                self.draw_larger_block(x_pos, y_pos, scale, color)
                self.draw_larger_block(x_pos, y_pos - offset1, scale, color)
                self.draw_larger_block(x_pos, y_pos - offset2, scale, color)
                self.draw_larger_block(x_pos + offset1, y_pos - offset1, scale, color)
            elif num_rot == 2:
                self.draw_larger_block(x_pos + offset1, y_pos, scale, color)
                self.draw_larger_block(x_pos, y_pos - offset1, scale, color)
                self.draw_larger_block(x_pos + offset1, y_pos - offset1, scale, color)
                self.draw_larger_block(x_pos + offset2, y_pos - offset1, scale, color)
            elif num_rot == 3:
                self.draw_larger_block(x_pos + offset1, y_pos, scale, color)
                self.draw_larger_block(x_pos, y_pos - offset1, scale, color)
                self.draw_larger_block(x_pos + offset1, y_pos - offset1, scale, color)
                self.draw_larger_block(x_pos + offset1, y_pos - offset2, scale, color)
        
        # Corner-Shape
        elif blocktype == 7:
            if num_rot == 0:
                self.draw_larger_block(x_pos, y_pos, scale, color)
                self.draw_larger_block(x_pos + offset1, y_pos, scale, color)
                self.draw_larger_block(x_pos, y_pos - offset1, scale, color)
            elif num_rot == 1:
                self.draw_larger_block(x_pos, y_pos, scale, color)
                self.draw_larger_block(x_pos, y_pos - offset1, scale, color)
                self.draw_larger_block(x_pos + offset1, y_pos - offset1, scale, color)
            elif num_rot == 2:
                self.draw_larger_block(x_pos + offset1, y_pos, scale, color)
                self.draw_larger_block(x_pos + offset1, y_pos - offset1, scale, color)
                self.draw_larger_block(x_pos, y_pos - offset1, scale, color)
            elif num_rot == 3:
                self.draw_larger_block(x_pos, y_pos, scale, color)
                self.draw_larger_block(x_pos + offset1, y_pos, scale, color)
                self.draw_larger_block(x_pos + offset1, y_pos - offset1, scale, color)

    def calculate_width(self):
        """Calculate the width of the displayed content"""
        return (self.sizeOfValue * TETRIS_DISTANCE_BETWEEN_DIGITS * self.scale) - 1

    def draw_colon(self, x, y, colon_color):
        """Draw the colon for the clock display"""
        colon_size = 2 * self.scale
        x_colon_pos = x + (TETRIS_DISTANCE_BETWEEN_DIGITS * 2 * self.scale)
        self.fill_rect(x_colon_pos, y + (12 * self.scale), colon_size, colon_size, colon_color)
        self.fill_rect(x_colon_pos, y + (8 * self.scale), colon_size, colon_size, colon_color)
   
    def get_fall_instr_by_num(self, num, blockindex):
        """Return the fall instruction for a digit"""
        if 0 <= num < 10:
            return self.number_arrays[num][blockindex]
        return None
        
    def get_fall_instr_by_ascii(self, ascii_code, blockindex):
        """Return the fall instruction for an ASCII character"""
        if ascii_code in self.letter_arrays and blockindex < self.blocks_per_char.get(ascii_code, 0):
            return self.letter_arrays[ascii_code][blockindex]
        return None
            
    def draw_numbers(self, x=0, y=0, display_colon=False):
        """Draw numbers with tetris animation"""
        finished_animating = True
        
        scaled_y_offset = self.scale if self.scale > 1 else 1
        base_y = y - (TETRIS_Y_DROP_DEFAULT * self.scale)
        
        for numpos in range(self.sizeOfValue):
            if self.numstates[numpos].num_to_draw >= 0 and self.numstates[numpos].num_to_draw < 10:
                # Draw falling shape
                if self.numstates[numpos].blockindex < self.blocks_per_number[self.numstates[numpos].num_to_draw]:
                    finished_animating = False
                    current_fall = self.get_fall_instr_by_num(self.numstates[numpos].num_to_draw, 
                                                          self.numstates[numpos].blockindex)
                    
                    # Handle rotations
                    rotations = current_fall.num_rot
                    if rotations == 1:
                        if self.numstates[numpos].fallindex < int(current_fall.y_stop / 2):
                            rotations = 0
                    elif rotations == 2:
                        if self.numstates[numpos].fallindex < int(current_fall.y_stop / 3):
                            rotations = 0
                        elif self.numstates[numpos].fallindex < int(current_fall.y_stop / 3 * 2):
                            rotations = 1
                    elif rotations == 3:
                        if self.numstates[numpos].fallindex < int(current_fall.y_stop / 4):
                            rotations = 0
                        elif self.numstates[numpos].fallindex < int(current_fall.y_stop / 4 * 2):
                            rotations = 1
                        elif self.numstates[numpos].fallindex < int(current_fall.y_stop / 4 * 3):
                            rotations = 2
                    
                    color = self.tetrisColors[current_fall.color]
                    
                    if self.scale <= 1:
                        self.draw_shape(
                            current_fall.blocktype,
                            color,
                            x + current_fall.x_pos + self.numstates[numpos].x_shift,
                            base_y + self.numstates[numpos].fallindex - scaled_y_offset,
                            rotations
                        )
                    else:
                        self.draw_larger_shape(
                            self.scale,
                            current_fall.blocktype,
                            color,
                            x + (current_fall.x_pos * self.scale) + self.numstates[numpos].x_shift,
                            base_y + (self.numstates[numpos].fallindex * scaled_y_offset) - scaled_y_offset,
                            rotations
                        )
                    
                    self.numstates[numpos].fallindex += 1
                    
                    if self.numstates[numpos].fallindex > current_fall.y_stop:
                        self.numstates[numpos].fallindex = 0
                        self.numstates[numpos].blockindex += 1
                
                # Draw already dropped shapes
                if self.numstates[numpos].blockindex > 0:
                    for i in range(self.numstates[numpos].blockindex):
                        fallen_block = self.get_fall_instr_by_num(self.numstates[numpos].num_to_draw, i)
                        color = self.tetrisColors[fallen_block.color]
                        
                        if self.scale <= 1:
                            self.draw_shape(
                                fallen_block.blocktype, 
                                color, 
                                x + fallen_block.x_pos + self.numstates[numpos].x_shift,
                                base_y + fallen_block.y_stop - 1,
                                fallen_block.num_rot
                            )
                        else:
                            self.draw_larger_shape(
                                self.scale,
                                fallen_block.blocktype, 
                                color,
                                x + (fallen_block.x_pos * self.scale) + self.numstates[numpos].x_shift,
                                base_y + (fallen_block.y_stop * scaled_y_offset) - scaled_y_offset,
                                fallen_block.num_rot
                            )
        
        if display_colon:
            self.draw_colon(x, base_y, self.tetrisWHITE)
        
        return finished_animating

    def draw_text(self, x=0, y=0):
        """Draw text with tetris animation"""
        finished_animating = True
        
        scaled_y_offset = self.scale if self.scale > 1 else 1
        base_y = y - (TETRIS_Y_DROP_DEFAULT * self.scale)
        
        for numpos in range(self.sizeOfValue):
            ascii_code = self.numstates[numpos].num_to_draw
            if ascii_code >= 33:  # Valid ASCII character
                blocks_in_char = self.blocks_per_char.get(ascii_code, 0)
                
                # Draw falling shape
                if self.numstates[numpos].blockindex < blocks_in_char:
                    finished_animating = False
                    current_fall = self.get_fall_instr_by_ascii(ascii_code, self.numstates[numpos].blockindex)
                    
                    if current_fall:
                        # Handle rotations
                        rotations = current_fall.num_rot
                        if rotations == 1:
                            if self.numstates[numpos].fallindex < int(current_fall.y_stop / 2):
                                rotations = 0
                        elif rotations == 2:
                            if self.numstates[numpos].fallindex < int(current_fall.y_stop / 3):
                                rotations = 0
                            elif self.numstates[numpos].fallindex < int(current_fall.y_stop / 3 * 2):
                                rotations = 1
                        elif rotations == 3:
                            if self.numstates[numpos].fallindex < int(current_fall.y_stop / 4):
                                rotations = 0
                            elif self.numstates[numpos].fallindex < int(current_fall.y_stop / 4 * 2):
                                rotations = 1
                            elif self.numstates[numpos].fallindex < int(current_fall.y_stop / 4 * 3):
                                rotations = 2
                        
                        color = self.tetrisColors[current_fall.color]
                        
                        if self.scale <= 1:
                            self.draw_shape(
                                current_fall.blocktype,
                                color,
                                x + current_fall.x_pos + self.numstates[numpos].x_shift,
                                base_y + self.numstates[numpos].fallindex - scaled_y_offset,
                                rotations
                            )
                        else:
                            self.draw_larger_shape(
                                self.scale,
                                current_fall.blocktype,
                                color,
                                x + (current_fall.x_pos * self.scale) + self.numstates[numpos].x_shift,
                                base_y + (self.numstates[numpos].fallindex * scaled_y_offset) - scaled_y_offset,
                                rotations
                            )
                        
                        self.numstates[numpos].fallindex += 1
                        
                        if self.numstates[numpos].fallindex > current_fall.y_stop:
                            self.numstates[numpos].fallindex = 0
                            self.numstates[numpos].blockindex += 1
                
                # Draw already dropped shapes
                if self.numstates[numpos].blockindex > 0:
                    for i in range(self.numstates[numpos].blockindex):
                        fallen_block = self.get_fall_instr_by_ascii(ascii_code, i)
                        if fallen_block:
                            color = self.tetrisColors[fallen_block.color]
                            
                            if self.scale <= 1:
                                self.draw_shape(
                                    fallen_block.blocktype,
                                    color,
                                    x + fallen_block.x_pos + self.numstates[numpos].x_shift,
                                    base_y + fallen_block.y_stop - 1,
                                    fallen_block.num_rot
                                )
                            else:
                                self.draw_larger_shape(
                                    self.scale,
                                    fallen_block.blocktype,
                                    color,
                                    x + (fallen_block.x_pos * self.scale) + self.numstates[numpos].x_shift,
                                    base_y + (fallen_block.y_stop * scaled_y_offset) - scaled_y_offset,
                                    fallen_block.num_rot
                                )
        
        return finished_animating