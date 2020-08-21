import numpy as np
from PIL import ImageFont, Image, ImageDraw, ImageEnhance
from colour import Color
from math import floor

SAMPLE_LETTER = "x"  # Used to determine the typical width and height of an ASCII character
BRIGHTNESS_FACTOR = 1.5  # How much to brighten image by
GRAYSCALE_LVLS = "#&B9@?sri:,. "
# GRAYSCALE_LVLS = ' .,:irs?@9B&#' For inverted brightness


def get_width_height(numpy_obj):
    """Returns the width and height of any numpy array"""
    h, w = numpy_obj.shape[0], numpy_obj.shape[1]

    return w, h


def avg_tile_brightness(img_tile):
    """img_tile parameter is a 2 dimensional array representing a tile in a given image;
       the image should be represented using grayscale values rather than rgb values;
       returns the average grayscale value of the image tile"""
    tile_width, tile_height = get_width_height(img_tile)

    grayscale_vals = img_tile.reshape(tile_height * tile_width)  # Reshape 2D array into 1D array

    avg_grayscale = np.average(grayscale_vals)

    return avg_grayscale


def get_num_tiles(img):
    """Determines how many ASCII characters are needed for each row/column in the image"""
    font = ImageFont.load_default()  # Load in default font

    letter_width, letter_height = font.getsize(SAMPLE_LETTER)[0], font.getsize(SAMPLE_LETTER)[1]  # Get width and height of an ASCII character
    img_width, img_height, = get_width_height(img)

    num_letters_per_col = img_height // letter_height
    num_letters_per_row = img_width // letter_width

    return num_letters_per_row, num_letters_per_col, letter_width, letter_height


def get_tile(img, w_start, h_start, w_end, h_end):
    """
    :param img: a 2D array storing image values represented as tuples
    :param w_start: starting width index
    :param h_start: starting height index
    :param w_end:  ending width index
    :param h_end:  ending height index
    :return: a tile of the image from starting width index to ending width index and starting height index to
    ending height index; returned as a numpy array
    """
    tile = []
    i = 0

    for row in range(h_start, h_end):
        tile.append([])
        for col in range(w_start, w_end):
            tile[i].append(img[row][col])

        i += 1

    return np.array(tile)


def brighten(img):
    """Brightens an image object and returns the brightened version as a numpy array"""
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(BRIGHTNESS_FACTOR)

    return np.array(img)


def create_gradients(start_color, end_color, num_lines):
    """
    :param start_color: starting color of the gradient represented as a string
    :param end_color: ending color of the gradient represented as a string
    :param num_lines: the number of colored lines between the starting color and ending color
    :return: an array storing color values that start at start_color and gradually become closer and closer
    to end_color
    """
    start = Color(start_color)
    end = Color(end_color)

    return list(start.range_to(end, num_lines))


def draw_to_image(img, letters_per_row, letters_per_col, letter_width, letter_height, grayscale, color_gradients, draw):
    """
    draws to the new image line by line
    :param img: an image represented as 3-dimensional numpy as grayscale values
    :param letters_per_row: the number of ASCII characters that it takes to represent the original image horizontally
    :param letters_per_col: the number of ASCII characters it takes to represent the original image vertically
    :param letter_width: estimated width of an ASCII character
    :param letter_height: estimated height of an ASCII character
    :param grayscale: A list of ASCII characters representing the different possible levels of grayscale
    from darkest to lightest
    :param color_gradients: A list of colors where the first color in the list gradually becomes more like the last
    color in the list
    :param draw: An ImageDraw.draw object used to draw to the new image
    :return: nothing; the function simply draws to the new image
    """
    line_index = 0  # First line of the image
    y = 0  # The current distance from the very top of the image, starts at 0

    col_pixel_count = 0  # The number of pixels processed vertically
    col_end_count = 0  # Used to determine the value of the last pixel for each given tile, vertically

    for row in range(0, letters_per_col):
        col_end_count += letter_height

        row_pixel_count = 0  # The number of pixels processed horizontally
        row_end_count = 0  # Used to determine the value of the last pixel for each given tile, horizontally

        line = ""  # Begin a new line

        for col in range(0, letters_per_row):
            row_end_count += letter_width

            tile = get_tile(img, row_pixel_count, col_pixel_count, row_end_count, col_end_count)  # Get image tile

            avg_brightness = avg_tile_brightness(tile)  # Determine average brightness of the tile
            i = floor((((len(grayscale) - 1) * avg_brightness) // 255))  # Convert grayscale value as an index

            line += grayscale[i]  # Add one of the ASCII characters in grayscale to the current line of the image

            row_pixel_count += letter_width  # Update the number of pixels processed

        col = color_gradients[line_index]  # Determine the current color gradient
        draw.text((0, y), line, col.hex)  # Draw the line to the image in color col

        y += letter_height  # Update y; next line should be letter_height distance from previous line
        line_index += 1  # Update line index for color_gradients list
        col_pixel_count += letter_height


def check_color(col1, col2, col3):
    """If colors are left blank in the GUI, set them to black and white by default"""
    if col1 == "":
        col1 = "black"

    if col2 == "":
        col2 = "black"

    if col3 == "":
        col3 = "white"

    return col1, col2, col3


def execute_infile(old_name, new_name, start_color, end_color, bgcolor):
    img = Image.open(old_name).convert("L")  # Open the image as grayscale values

    np_img = brighten(img)  # Brighten and convert to numpy array

    w, h = get_width_height(np_img) # Width and height of current image

    lvls_grayscale = list(GRAYSCALE_LVLS) # Turn grayscale lvls into a list
    letters_per_row, letters_per_col, letter_width, letter_height = get_num_tiles(np_img)

    num_lines = h//letter_height # Calculate number of lines in the image (same as # of rows)
    color_gradients = create_gradients(start_color, end_color, num_lines)  # Create a list of colors

    new_img = Image.new("RGBA", (w, h), bgcolor)  # Create a new image
    draw = ImageDraw.Draw(new_img) # Create an object that'll allow us to draw to new_img

    draw_to_image(np_img, letters_per_row, letters_per_col, letter_width, letter_height, lvls_grayscale, color_gradients, draw)
    new_img.save(new_name)
    print("Image created successfully")


def ascii_art(label, path, start_color, end_color, bgcolor):
    start_color, end_color, bgcolor = check_color(start_color, end_color, bgcolor)

    img = Image.open(path).convert("L")  # Open the image as grayscale values
    np_img = brighten(img)  # Brighten and convert to numpy array

    w, h = get_width_height(np_img)  # Width and height of current image

    lvls_grayscale = list(GRAYSCALE_LVLS)  # Turn grayscale lvls into a list
    letters_per_row, letters_per_col, letter_width, letter_height = get_num_tiles(np_img)

    num_lines = h // letter_height  # Calculate number of lines in the image (same as # of rows)
    color_gradients = create_gradients(start_color, end_color, num_lines)  # Create a list of colors

    new_img = Image.new("RGBA", (w, h), bgcolor)  # Create a new image
    draw = ImageDraw.Draw(new_img)  # Create an object that'll allow us to draw to new_img

    draw_to_image(np_img, letters_per_row, letters_per_col, letter_width, letter_height, lvls_grayscale,
                  color_gradients, draw)  # Draw to the image

    return new_img, label


if __name__ == "__main__":
    execute_infile("imgs/abraham.jpeg", "lol.pnp", "blue", "red", "white")





