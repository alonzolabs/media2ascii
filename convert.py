import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
from scipy import ndimage as ndi
from sklearn.neural_network import MLPClassifier
import sys

from skimage import feature
from skimage import io
from skimage.transform import rescale

### FOR CONVERTING IMAGES TO ASCII ###

# PARAMS
# python convert.py <filename> <options>
# Use brightness of the original image to "shade" the ASCII
shade = False #--shade
reverse_shade = False #--reverse_shade
# Clean up certain common patterns
clean = True #--no_clean
lines = 0  #--lines=#
progress = False # --progress
# Sets Gaussian sigma, also setting disables UI
sigma = -1.0
# Skip anything brighter than this when shading, useful for images with white
# backgrounds.
background_threshold = 1.01 # --background_threshold=#, --bgt=#

file = "image.png"

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
        for e in range(c_h * c_w): # Compare characters 
            if lvisual[e] == subset[e]:
                likeness += 1
        if likeness == (c_w * c_h): # Character is a perfect match
            if letter == ' ' and len(original_subset) != 0: # Shading
                average = np.average(original_subset)
                if average >= background_threshold:
                    return ' '
                if shade:
                    return shades[int((len(shades) - 1) * average)]
                elif reverse_shade:
                    return reverse_shades[int((len(reverse_shades) - 1) * average)]
            return letter
        # Character is the current best match
        elif likeness > curr_max_likeness and letter != ' ':
            curr_max_likeness = likeness
            curr_letter = letter
    return curr_letter

# Run through all the subsets of the edge image
def convert(img, canny_sigma):
    image = feature.canny(img, sigma=canny_sigma)

    print("Running Sigma=", canny_sigma)
    h_i = image.shape[0] // c_h # Number of lines
    w_i = image.shape[1] // c_w # Number of chars in a line

    string = ""
    for r in range(h_i):
        for c in range(w_i):
            sub = image[r*c_h:r*c_h+c_h,c*c_w:c*c_w+c_w]
            if not shade and not reverse_shade:
                string += predict(sub.flatten())
            else:
                original = img[r*c_h:r*c_h+c_h,c*c_w:c*c_w+c_w]
                string += predict(sub.flatten(), original.flatten())        
        string += "\n"
        if progress:
            print(100 * r / h_i)

    if clean:
        string = string.replace("_` ", " / ")
        string = string.replace("_' ", " / ")
        string = string.replace(" '_", " \\ ")
        string = string.replace(" `_", " \\ ")

    print(string)

### Load image
im = io.imread(file, flatten=True)

if lines != 0:
    im = rescale(im, lines / (im.shape[0] // c_h), anti_aliasing=False)

### UI and Running
if sigma >= 0.0: # No UI option
    convert(im, sigma)
else:
    ### UI
    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(8, 3),
                                        sharex=True, sharey=True)

    ax1.imshow(im, cmap=plt.cm.gray)
    ax1.axis('off')
    ax1.set_title('image', fontsize=20)

    edges = feature.canny(im, sigma=1)
    ax2.imshow(edges, cmap=plt.cm.gray)
    ax2.axis('off')
    ax2.set_title('edges', fontsize=20)

    axcolor = 'lightgoldenrodyellow'
    axis_sigma = plt.axes([0.1, 0.1, 0.8, 0.03], facecolor=axcolor)

    ssigma = Slider(axis_sigma, 'sigma', 0.5, 10.0, valinit=1.0, valstep=0.05)

    def update_sigma(sigma):
        edges = feature.canny(im, sigma=ssigma.val)
        ax2.imshow(edges, cmap=plt.cm.gray)

    ssigma.on_changed(update_sigma)

    convertax = plt.axes([0.8,0.025, 0.1, 0.04])
    convert_button = Button(convertax, "convert", color=axcolor, hovercolor='0.975')

    def convert_button_clicked(event):
        convert(im, ssigma.val)

    convert_button.on_clicked(convert_button_clicked)

    fig.tight_layout()

    plt.show()