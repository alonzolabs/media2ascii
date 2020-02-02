# media2ascii
media2ascii aims to convert all forms of visual media to sparse ASCII representations. Most image to ASCII programs convert every piece of the image to a character based on brightness which produces a wall of text,
but media2ascii uses canny edge detection in hopes of selecting only the most essential visual information from images. By applying this to each frame of a video, we can also produce ascii videos.

# Requirements
- Python 3
- Scikit
- Numpy
- Matplotlib
- Pillow (For video)
- FFmpeg (For video)
- opencv (For video)

# Converting an Image
convert.py can be run using Python 3. It can take an image and parameters using:
```
python3 convert.py <filename> <params>
```
Params only work if a filename is explicitly given. You can learn more about them in convert.py

Sigma affects the gaussian blur applied to the image. Increasing sigma will reduce the amount of fine-detail edges, but will speed up runtime and, to an extent, clarity.

Images under 1000x1000px take under 10 seconds on my computer. This figure goes up as the image gets larger, and more detailed. Increasing sigma reduces the edges and thus the runtime. Shading should have trivial effect on runtime.


# Converting a Video
Converting a video is more complicated and can take many hours of runtime. Run video/vconvert.py:
```
python3 vconvert.py <videofilename> --sigma=# --lines=#
```
This will convert the video to a text file that specifies the number of lines in each frame and the text for each frame. I *strongly* recommend playing with sigma values before doing a full run, because converting the full video can take hours, so you want to make sure it looks good.

Now that we have a text file, we use text_to_images.py to convert our text file to a series of pngs using Pillow. All the parameters for this are currently hardcoded, so change the code and run:
```
python3 text_to_images.py
```
This took about a half an hour for me on a ~4000 frame video. 

text_to_images.py also can animate your file in the command line using some code that needs to be uncommented. This is immediate gratification if you don't care about having a video file.

Now we have images, and use FFmpeg's command line to knit all the images into a video, learn more at [this URL.](https://hamelot.io/visualization/using-ffmpeg-to-convert-a-set-of-images-into-a-video/)

We now have a silent video, if you want to map audio from an mp3 or another video, FFmpeg can do that too! For more info on this you can look [here](https://superuser.com/questions/590201/add-audio-to-video-using-ffmpeg), but also Google will be your friend.

# Versions
v0.1: Basic image and video converting functionality. 2/2/2020

# TODO
- Improve image preprocessing and stop relying on the built in Gaussian blur
- Allow the use to directly input an edge map
- Explore supervised learning to convert edges more quickly/open-endedly
- Put more parameters in the UI to make it easier to use
- Expand readme, including how to add custom fonts

# Other references
Also checkout Brian MacIntosh's converter, it's the only other feature-based image converter I've seen and it takes some really cool (and sometimes more effective) approaches: https://www.brianmacintosh.com/asciiart/
