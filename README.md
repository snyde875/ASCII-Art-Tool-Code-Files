# Image Art Creator
A basic, Python 3-based application that'll currently allow you to do 3 things
* Create ASCII Art (Examples given below)
* Convert between image file types (Supported formats given below)
* Average the colors of an image to create a new image (Examples given below, known as "Group Colors" on the application)

As of now, these are the only functions the application is capable of executing. The brighten, blur detection, and warp colors buttons currently do nothing when clicked. I may or may not add these on a later date.

## Getting Set Up
In order to use the application, all you have to do is download the files above as a zip. Once donwloaded, browse into the "dist" folder and locate the "image-art-creator.exe" executable. Create a shortcut of this executable to your desktop, task bar, or wherever you'd like to have it. Moving the executable out of the "dist" folder will NOT create a shortcut! The executable will not be able to launch if you do, so the best thing you can do for yourself is to create a shortcut!

In order to use the convert file format option, you must download ImageMagick and set MAGICK_HOME enviornment variable to the path of ImageMagick. Note that you do not need to download ImageMagick in order to create ASCII art or use any other of the applications functionalities; only the convert file format option requires ImageMagick. An installation of ImageMagick is required because Wand, one of the dependencies of this application, uses ImageMagick as a dependency. Below is a step-by-step, easy-to-follow walkthrough of getting ImageMagick set up.

### Installing ImageMagick
First, you will need to download "ImageMagick-7.0.10-24-Q16-x86-dll.exe" from [here](http://www.imagemagick.org/download/binaries/) and then run the installation. When installing ImageMagick, make sure you install development headers and libraries for C and C++ as shown in the image below. If the version specified above is not available, pick a version that is at least version 7 (so ImageMagick-7.0.10 and up) and that has "Q16-x86" following it. Q8 and x64 will not work. 

![alt text](https://docs.wand-py.org/en/0.4.1/_images/windows-setup.png)

When installing ImageMagick from the installer, make sure you remember the location of where you're saving ImageMagick. Once ImageMagick has been saved to your computer, you will need to navigate to control panel -> system and security -> system -> advanced system settings. Afterwards, select "Enviornment Variables," and then under "System Variables," hit "new." The variable name should be MAGICK_HOME, and for the variable value, hit "browse directory" and then select your download of ImageMagick. Alternatively, you can search "View Advanced System Settings" from the Windows Search bar and select the Enviornment Variables option from there. 

![alt text](https://docs.wand-py.org/en/0.4.1/_images/windows-envvar.png)

Once ImageMagick has been successfully downloaded and the enviornment variable has been set up, you should be able use the convert file format option of the application.

## Program Abilities
Next, I'll go over the three different things that this can application can do for you a bit more in depth with some examples.

### Creating ASCII Art

| Original Image | Default ASCII Art | Inverting White and Black | Blue to Orange Gradients |
| ----- | ----- | ----- | ----- |
| ![](https://user-images.githubusercontent.com/46146906/88861163-01f6c980-d1c3-11ea-981a-fa588532e730.png) | ![](https://user-images.githubusercontent.com/46146906/88860771-1b4b4600-d1c2-11ea-86ea-277e1bdf331e.png) | ![](https://user-images.githubusercontent.com/46146906/88860780-1e463680-d1c2-11ea-9eeb-5f0e1e6d206b.png) | ![](https://user-images.githubusercontent.com/46146906/88860785-20a89080-d1c2-11ea-8c4a-fa98b2931027.png) |

The images provided above are some examples of the type of ASCII art you can create with this image application. Many ASCII art creators out there recreate the input image with a white background and black ASCII characters as seen in the Default ASCII Art example, but with this application you have a bit more customization. You can specify the background color as well as the starting and ending colors (from top to bottom) of the ASCII art. The application takes your starting color and creates a series of gradients that eventually blends into your ending color, as seen in the Blue to Orange Gradients example. 

### Converting between formats
In order to use this part of the application, an installation of ImageMagick is required. See the section "Installing ImageMagick" for a quick and easy guide for how to do this.

Currently, you can upload and convert between any of these file formats given below:
* png
* jpg
* ppm (P6, binary)
* ppm (P3, ASCII)
* bmp
* pgm

I've given users the option to convert images to a ppm ASCII format because most file type converters online only give the option to convert an image to a compressed binary ppm. In other words, should you open a ppm ASCII image with notepad, for example, all of the image data will be represented in ASCII RGB values. It's my hope that this will be useful to anyone on windows needing to work with ppm images with a magic number of P3. 

### Averaging colors of an image
This function of the application can create some pretty interesting and unique images. Essentially, the user chooses a number between 2 and 10 (inclusive), and the application will recreate that image with only the number of colors that they chose. So if the number you picked was six, then you image is recreated with only six colors. The colors chosen, however, are not random. The application utilizes an algorithm that first selects six random colors (had you chosen six as your number) and then determines which color is closest to the six random colors for every color in your image, placing them in one of six different bins. Afterwards, all the colors in the bins are averaged to create six new colors, and the process repeats until the six new colors are the same as the previous six. Essentially, the application takes your image and averages its colors to a number that you specify. Some examples are given below.

| Original | Averaged to 5 Colors |
| ----- | ----- |
| ![](https://user-images.githubusercontent.com/46146906/88862553-30c26f00-d1c6-11ea-9169-f498f61bde44.jpg) | ![](https://user-images.githubusercontent.com/46146906/88862552-2e601500-d1c6-11ea-855c-1db38e28adf8.png) |

| Original | Averaged to 3 Colors |
| ----- | ----- |
| ![](https://user-images.githubusercontent.com/46146906/88977129-eb17ac00-d282-11ea-9d8a-f865828877ea.jpg) | ![](https://user-images.githubusercontent.com/46146906/88977136-eeab3300-d282-11ea-8649-e96a5955ccb5.png) |

| Original | Averaged to 6 Colors |
| ----- | ----- | 
| ![](https://user-images.githubusercontent.com/46146906/88977603-d7b91080-d283-11ea-8fae-a5ed119b5930.jpg) | ![](https://user-images.githubusercontent.com/46146906/88977611-da1b6a80-d283-11ea-8d34-85997aaf34cc.png) |

| Original | Averaged to 4 Colors | Averaged to 10 Colors |
| ----- | ----- | ----- |
| ![](https://user-images.githubusercontent.com/46146906/88977193-113d4c00-d283-11ea-8789-7edacbc1d866.png) | ![](https://user-images.githubusercontent.com/46146906/88977151-f4a11400-d282-11ea-9bd9-70731f46c04d.png) | ![](https://user-images.githubusercontent.com/46146906/88977142-f1a62380-d282-11ea-883a-5af19012308b.png) | ![](https://user-images.githubusercontent.com/46146906/88977611-da1b6a80-d283-11ea-8d34-85997aaf34cc.png) |

Please note that the algorithm used to create these images is a brute-force algorithm that will take a while depending on how many colors you select, the size of your image, and your computer's processing speed. It's best to execute the process and then simply let it run until it's finished. 

If you know how to speed up this process while providing consistent results, I'd love to know! 

## Purpose
The purpose of this project was to gain experience in GUI programming while also providing a program that might be useful to some people. A project in one of my computer science classes relied on ppm P3 images as input, and at the time, I had a lot of trouble finding a way to convert jpg and png images to this style of image formatting. Consequently, I wanted to provide people with a simple application that could allow them to convert to this file format with ease. 

One of the reasons I started programming was because I found it interesting and wanted to build things that could be of use to myself and others. That being said, not everyone has a Python IDE on their computer, or even Python itself for that matter. On top of that, while it might be easy for me to navigate and use Python files that I've created, the same isn't necessarily true for someone with zero programming experience. Thus, it's only natural to learn a bit of GUI programming if you want friends and family to use the things you've made. The "Group Colors" function of my application is actually something I had to do for a class project, and many of my friends found it to be pretty cool. I wanted them to be able to use it easily and without any trouble, and I thought the best way to do that would be to create a simple UI for them to navigate. 

## Built With
* [Python 3](https://www.python.org/downloads/) - The primary programming language used
* [Pillow](https://pillow.readthedocs.io/en/stable/) - Mainly used for opening, saving, and converting images to and from a numpy array format
* [NumPy](https://numpy.org/) - Used to represent images in array form
* [Colour](https://pypi.org/project/colour/) - Used to create smooth gradients between two colors
* [PyQt5](https://pypi.org/project/PyQt5/) - The GUI framework
* [Wand](https://docs.wand-py.org/en/0.6.2/) - Used to allow conversion to formats not supported by Pillow, such as PPM P3
* [PyInstaller](https://pypi.org/project/PyInstaller/) - Used to package the Python 3 files into an executable 

## Acknowledgements 
After packaging the python files through PyInstaller to create the executable for the application, I ran into an error stating "ImportError: unable to find Qt5Core.dll." After doing some research on how to solve this problem, I ran into a [stack overflow answer](https://stackoverflow.com/questions/56949297/how-to-fix-importerror-unable-to-find-qt5core-dll-on-path-after-pyinstaller-b) that solved my problem. Sofair R. provided a code snippet that I imported into my main python file and the import error was fixed. 

In addition, while programming the ASCII art creator, I used two articles for reference:
* [Convert Photos to ASCII Arts with Python](https://wshanshan.github.io/python/asciiart/)
* [Converting an Image to ASCII Image in Python](https://www.geeksforgeeks.org/converting-image-ascii-image-python/)

The first article is also what gave me the idea to create ASCII art using color gradients. 

I also taught myself how to use PyQt5 using a series of articles hosted [here.](https://www.learnpyqt.com/)

Finally, the k-means algorithm used in the "Group Colors" functionality of the application was originally a class project for my CSCI 1913 Data Structures and Algorithms class taught by Daniel Kluver. I made slight modifications to the original code, such as using python PIL to open images and numpy to represent images, but the algorithm as a whole is largely still the original algorithm used for that class. 
