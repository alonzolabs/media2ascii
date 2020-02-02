import numpy as np
import cv2

import time

from PIL import Image, ImageDraw, ImageFont

# No command line options yet

# Specify the input text file here
txt_file_name = "yourfile.txt"
txt_file = open(txt_file_name, 'r')
art = txt_file.readlines()
txt_file.close()

line_length = int(art[0])

num_frames = int((len(art) - 1) / line_length)

### Animate the file in the command line at ~24 FPS
# for i in range(num_frames):
    # chunk_start = (i * line_length) + 1
    # frame = "".join(art[chunk_start:chunk_start + 36])
    # print(frame)
    # time.sleep(0.042)

### Convert every text frame to an image
# Toggle these params to make the text "fit" your desired frame size
width = 1280
height = 720
font_size = 18
line_height = 21
top_margin = 3
background_color = 'black'
text_color = 'white'
fnt = ImageFont.truetype('consola.ttf', font_size)
for i in range(num_frames):
    print(i)
    chunk_start = (i * line_length) + 1

    img = Image.new('RGB', (width, height), color=background_color)
    d = ImageDraw.Draw(img)
    for l in range(37):
        d.text((0, l * line_height + top_margin), art[chunk_start + l], font=fnt, fill=text_color)
    img.save('your_name' + str(i) + '.png') # I recommend outputting these to a seperate folder
