# DiCaLum Software
Digital Camera Luminance measurements.

http://dicalum.eu/

https://pypi.org/project/dicalum/

Note: this is an unofficial copy of the freely available code at the above links.

The official links are given above.

Below is an excrept from the official website:
___
# About DiCaLum
DiCaLum is a collection of Python routines and a GUI to convert digital camera raw images to radiance maps. The code is freely available as a Python package by:

pip3 install dicalum

DiCaLum depends on several standard packages: numpy, matplotlib, rawpy, exifread, Pillow and scipy. It is recommended to install or upgrade these packages before installing DiCaLum.

When DiCaLum is installed, it can be used with the simple Python code:

import dicalum  
dicalum.dclinst.camera=2  
program = dicalum.DclGui()  
program.window.mainloop()

For testing purposes a standalone Windows executable is also available: http://dicalum.eu/rundicalum.exe

Please note that the Python version of  DiCaLum is still in development, it is a Beta version of the code. Even calibration updates will be performed. More details on the code and its extensions will be available soon.

# A brief description of DiCalum:
The metrics used in DiCaLum was introduced in this paper:

Zoltán Kolláth, Andrew Cool, Andreas Jechow, Kornél Kolláth, Dénes Száz, Kai Pong Tong: Introducing the dark sky unit for multi-spectral measurement of the night sky quality with commercial digital cameras, Journal of Quantitative Spectroscopy and Radiative Transfer,
Volume 253, (2020) 107162,    https://doi.org/10.1016/j.jqsrt.2020.107162.


# Some related publications:
Zoltán Kolláth, Dénes Száz, Kai Pong Tong, Kornél Kolláth: The Colour of the Night Sky. Journal of Imaging. 2020; 6(9):90. https://doi.org/10.3390/jimaging6090090

Zoltán Kolláth, Dénes Száz, Kornél Kolláth, Kai Pong Tong:  Light Pollution Monitoring and Sky Colours. J. Imaging 2020, 6, 104. https://doi.org/10.3390/jimaging6100104

Zoltán Kolláth & Anita Dömény: "Night sky quality monitoring in existing and planned dark sky parks by digital cameras", International Journal of Sustainable Lighting, Vol 19 No 1 61-68 (2017)

Andreas Jechow, Zoltán Kolláth, Salvador J. Ribas, Henk Spoelstra, Franz Hölker & Christopher C. M. Kyba: "Imaging and mapping the impact of clouds on skyglow with all-sky photometry",
Scientific Reports 7, Article number: 6741 (2017)

