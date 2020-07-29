# emd-converter
EMD Converter is a convenient and lightweight tool to convert the FEI Velox emd files to the common image formats including tiff, jpg, png, and bmp. The tool was written by Dr. Tao Ma. For questions and suggestions, please send a message to taoma@umich.edu.

## 1. Installation
The tool requires Python 3 environment. I recommend to install Anaconda which is the most straightforward way. Download and install the Python 3 version of Anaconda from here: https://www.anaconda.com/.

After the Anaconda is installed, open the Anaconda prompt console. First, install the [Hyperspy](https://hyperspy.org/):  ``conda install hyperspy -c conda-forge``. Then, simply navigate to the ``EMD Converter\`` folder with ``cd [PATH]`` and run ``pip install ./``. The pip should install the package automatically. 

## 2. Usage
Simply type "emd-con" in the Anaconda prompt console. A GUI will pop up. Just load the emd files, set the output directory, select the output format, and click "Let's go!". 

## 3. Formats
When selecting '.tif' format, the software converts the images into 16-bit tif files containing the pixel resolution. For DigitalMicrograph users, you can simply drag the converted tif files into GMS, which should be able to read the data including the pixel size losslessly. This is the most convenient way to convert emd files into GMS I have found so far.

PNG files are lossless, too, and can be imported into many other software like Microsoft Office, ImageJ, LaTeX, etc. Note that GMS does not take png files.

The jpg and bmp files are lossy conversion, which convert the original data into unsigned 8-bit int. These formats are good for direct use, but or ideal for image analysis as some data are lost in the conversion. Also, the pixel size information is not kept in these formats.

## 4. About the emd format
Velox saves all types of data, including simple images, image stacks, SI data, DPC, etc, into a single emd format. While these files share the same format, the data structures are quite different. This converter has been tested for simple images, image stacks, DPC images, and EDS mapping data. For simple images, the converter just makes the conversion in the selected output directory. For image stacks and DPC images, the converter first makes a folder with the file name and converts all the image frames into that folder. For EDS mapping data, the converter converts all the image data, e.g., maps for each element, and ignores the spectra data.
