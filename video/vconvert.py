import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
from scipy import ndimage as ndi
from sklearn.neural_network import MLPClassifier
import sys
import cv2
import time

from skimage import feature
from skimage import io
from skimage.transform import rescale

### FOR CONVERTING IMAGES TO ASCII ###

# RUN PARAMS
# python vconvert.py <filename> <options>
shade = False #--shade
reverse_shade = False #--reverse_shade
clean = True #--no_clean
lines = 30  #--lines=#
progress = False #--progress
sigma = 1.0
background_threshold = 1.01 #--background_threshold=#, --bgt=#

file = "" # No default video yet, please specify one on the command line

if len(sys.argv) >= 2:
    file = sys.argv[1]
    for param in sys.argv[2:]:
        if param == '--shade':
            shade = True
            print("Shading enabled")
        if param == '--reverse_shade':
            reverse_shade = True
            print("Reverse shading enabled")
        if param == "--no_clean":
            clean = False
            print("Cleaning disabled")
        if param[:7] == "--lines":
            lines = int(param[8:])
            print("Fixed # of lines enabled:", lines)
        if param == '--progress':
            progress = True
            print("Progress bar enabled")
        if param[:7] == "--sigma":
            sigma = float(param[8:])
            print("Quick run enabled")
        if param[:22] == "--background_threshold":
            background_threshold = float(param[23:])
            print("Background threshold set:", background_threshold)
        if param[:5] == "--bgt":
            background_threshold = float(param[6:])
            print("Background threshold set:", background_threshold)

values = ' abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*(()_-=+,.<>?/;:\'"\\|]}[{`~'
shades = ' .:-=+*#%@'
reverse_shades = '@%#*+=-:. '

# Default font
visual = (io.imread('default_font.png', flatten=True) > 0.0)
c_h = 10 # Height of each character in the image
c_w = 5  # Width of each character in the image

# Turn font into usable letter to pixel map
x = list(values)
y = []
for i in range(len(values)):
    sub = visual[:,i*c_w:i*c_w+c_w]
    y.append(sub.flatten())
letters = dict(zip(x, y))

### ALGORITHMS ###
# For a subimage of the edge map, find best fit character
def predict(subset, original_subset=[]):
    curr_letter = ""
    curr_max_likeness = -1
    for letter in x:
        lvisual = letters[letter]
        likeness = 0
        for e in range(c_h * c_w):
            if lvisual[e] == subset[e]:
                likeness += 1
        if likeness == (c_w * c_h):
            return letter
        elif likeness > curr_max_likeness and letter != ' ':
            curr_max_likeness = likeness
            curr_letter = letter
    return curr_letter

# Run through all the subsets of the edge image
def convert(img, canny_sigma):
    image = feature.canny(img, sigma=canny_sigma)

    # print("Running Sigma=", canny_sigma)
    h_i = image.shape[0] // c_h
    w_i = image.shape[1] // c_w

    string = ""
    for r in range(h_i):
        for c in range(w_i):
            sub = image[r*c_h:r*c_h+c_h,c*c_w:c*c_w+c_w]
            string += predict(sub.flatten())      
        string += "\n"

    string = string.replace("_` ", " / ")
    string = string.replace("_' ", " / ")
    string = string.replace(" '_", " \\ ")
    string = string.replace(" `_", " \\ ")

    return string

### Set up document
txt_file_name = file + str(time.time()) + ".txt"
txt_file = open(txt_file_name, 'w')
txt_file.write(str(lines))

### LOAD VIDEO
vid = cv2.VideoCapture(file)
success, im = vid.read()
count = 0
while success: # Convert every frame to ASCII
    im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    im = rescale(im, lines / (im.shape[0] // c_h), anti_aliasing=False)
    string = convert(im, sigma)
    txt_file.write(string)
    print(count)
    success, im = vid.read()
    count += 1
txt_file.close()

# text_to_images.py can be used to convert the .txt from this to images
# See the readme for more info.
