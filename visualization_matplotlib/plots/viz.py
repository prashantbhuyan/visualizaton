__author__ = 'Prashant B. Bhuyan'

import numpy as np
import pandas as pd
import scipy
import csv
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy import stats
from scipy import misc
from scipy import ndimage
import pylab
import Tkinter
import tkFileDialog
import glob
import re


import sys


# For Problem 3
def applyThreshold(img):

    # apply gaussian_filter to simplify the image.  The parameter value of 3 gave me the most logical results.
    filtered_image = ndimage.gaussian_filter(img,3)

    # apply threshold by partitioning the data based on the filtered image's mean.
    binaryData = filtered_image > filtered_image.mean()

    # save the array data for filtered, binary image with threshold.
    misc.imsave('convertedImage.jpg',binaryData)

    # return true false data that has the threshold in place.
    return(binaryData)

# For Problem 3
def countObjects(img):


    # label object instances and object slices.
    slices, instances = ndimage.label(applyThreshold(img))

    # return number of object instances.
    return(instances)

# for problem 3
def getObjectSlices(img):

    # label objects in the binary image.
    slices, instances = ndimage.label(applyThreshold(img))

    # return object slices.
    return(slices)

# for problem 3
def centerOfMass(img):

    # find coordinates for the center of mass of all objects in the image.
    coords = ndimage.center_of_mass(img, getObjectSlices(img), range(1,countObjects(img)+1))

    # return center of mass coordinates.
    return(coords)



# for problem 2
def fit(x,y):
    m,b = np.polyfit(x,y,1)

    return m*x+b




if __name__ == "__main__":

    # initialize a counter for problem 3
    count = 0

    # Create output file for image processing
    sys.stdout = open("/Users/MicrostrRes/Desktop/hw10_logfile.txt", "w")

    # get file for car feature data (for problem 1)
    cars_file = tkFileDialog.askopenfile(title = 'Choose File That Contains Car Data . . .')
    # create data frame for car feature data (for problem 1)
    cars_df = pd.read_table(cars_file, sep = ',')

    # get file for brain body data (for problem 2)
    brainbody_file = tkFileDialog.askopenfile(title = 'Choose File That Contains Brain/Body Data . . .')
    # create a data frame for brain and body data (for problem 2)
    brainbody_df = pd.read_table(brainbody_file, sep = ',')

    # get file for http request data (for problem 4)
    http_requestdata = tkFileDialog.askopenfile(title = 'Choose File That Contains HTTP Request Data . . . ')
    # create data frame for http request data (for problem 4)
    http_requestdata_df = pd.read_table(http_requestdata, sep = ',', header = None)

    # prompt the user for path to raw images (for problem 3)
    pathtoimages = tkFileDialog.askdirectory(title='Select Directory Containing Your Images . . .')

    # glob png formatted images together and save to variable imagefiles (for problem 3)
    imagefiles = glob.glob1(pathtoimages, '*.png')

    # create an array that stores each of the images (for problem 3)
    image_arr = [misc.imread(pathtoimages + '/' + img).astype(np.float32) for img in imagefiles]


    # slice data car data frame into a selected data frame with 4 variables (for problem 1)
    selected_df = cars_df[['Buying','Maint','Safety','Doors']]

    # Problem 1 - Create Sub Plots of Frequencies vs Feature

    p1 = selected_df.apply(pd.value_counts).plot(kind = 'bar', subplots=True).any()
    plt.suptitle('Car Features Distribution')
    plt.ylabel('Frequency')
    plt.show(p1)


    # slice brain body data frame into two variables (for problem 2)
    body = brainbody_df['body']
    brain = brainbody_df['brain']

    # Problem 2a - Create a scatter plot of the two variables
    plt.title('Scatter Brain vs Body')
    plt.xlabel('Brain')
    plt.ylabel('Body')
    p2 = plt.scatter(brain,body)
    plt.show(p2)


    # Problem 2b - Create a regression line between the variable values
    r = fit(brain,body)
    plt.title('Regression Line Brain vs Body')
    plt.xlabel('Brain')
    plt.ylabel('Body')
    p3 = plt.plot(brain,r,'-')
    plt.show(p3)


    # Problem 2c -
    plt.title('Regression Line on Scatter Brain vs Body')
    plt.xlabel('Brain')
    plt.ylabel('Body')
    plt.scatter(brain,body)
    r2 = fit(brain,body)
    p4 = plt.plot(brain,r2,'-')
    plt.show(p4)

    plt.show()

    # Problem 3- iterate through each image in the image_arr and output only the values of coordinates for
    # center points for objects.png (for problem 3)
    for i in image_arr:

        count += 1

        if count == 2:

            # Print out the raw image data (without threshold) for each image.
            print '\n', 'Raw Image #', count, 'W/O Threshold:\n'
            print '\n',i,'\n'

            # Print the converted image data (with threshold) for each image.
            print '\n', 'Binary Conversion of Image #', count,'W/ Threshold:\n'
            print '\n', applyThreshold(i), '\n'

            # Print the number of objects in each image.
            print '\n', 'There are', countObjects(i), 'objects in image #', count, 'above. \n'

            # Print the objects themselves
            print '\n', 'Here are Objects (Slices) for image #', count, 'above. \n', getObjectSlices(i)

            # Print the coordinates of the center of mass for each of the objects in each image.
            print 'The Coordinates for the Center of Mass for each of the', countObjects(i), 'objects in image #', count, 'above are: \n', centerOfMass(i)
            print '********BREAK******** \n'



            implot = plt.imshow(i)

            plt.scatter(*zip(*centerOfMass(i)),color = "red")
            plt.title('Center-Points of Objects Overlaid Upon Image')

            plt.show()


    # Problem 4- sort http request data by hour bin
    http_requestdata_df.columns = ['timeint','requests']
    sorted_http_reqdf = http_requestdata_df.sort(['timeint'],ascending = [True])

    # Problem 4- plot HTTP Server Requests by Hour (Hour on x-axis and Requests on y-axis)
    plt.plot(sorted_http_reqdf['timeint'],sorted_http_reqdf['requests'])
    plt.title('Number of HTTP Requests by Hour')
    plt.xlabel('Hours (24 Hour Scale)')
    plt.ylabel('# of Requests')
    plt.show()
    print sorted_http_reqdf







