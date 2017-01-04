'''
The MIT License
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''

'''
Usage:  In a linux terminal, go to the location of the script
    	and type the following: 

    	python conv.py "image_name" size_of_filter number_of_convolutions
    	example: python conv.py cat.jpg 16 3

    	The script will process the image and will create the image files
    	for the convolutions. In the above example, the following files are
    	created: cat_conv1.jpg, cat_conv2.jpg, cat_conv3.jpg

'''

import numpy as np
import matplotlib.image as mpimg
import matplotlib.pyplot as plt 
from skimage import io
import sys
from datetime import datetime as dt

def conv(img_name, filter_size, convs_number=1):
	filter_size = int(filter_size)
	convs_number = int(convs_number)
	if convs_number > 6: # 6 convs at most, to avoid to much computation
		convs_number = 6
	if convs_number < 1: # at least one conv
		convs_number = 1

	image = mpimg.imread(img_name)

	for c in range(1, convs_number + 1):
		start = dt.now()

		image = conv_array(image, filter_size)

		# rescale to be a valid RGB value [0 - 1] to save in disk
		image = rescale_rgb(image)
		save_image(image, image_name_no_ext(img_name) + "_conv" + str(c) + ".jpg")
		
		end = dt.now()
		delta = end - start
		total = round(delta.seconds + delta.microseconds/1E6, 2) # from http://stackoverflow.com/a/2880735/1065981

		print("Convolution " + str(c) + ": " + str(total) + " seconds")

def conv_array(image_array, filter_size):
	# rescale to be a valid RGB value [0 - 255] for better precision
	image_array = rescale_rgb(image_array, False)
	shape = image_array.shape

	filter_width = filter_size
	filter_height = filter_size
	filter_depth = shape[2]
	filters_number = 3 # To display the output as image

	# Weights and biases for the filters
	# TODO: Any other idea for the weights and biases?
	weights = np.random.normal(0, 1, (filters_number, filter_depth, filter_height, filter_width))
	biases = np.random.normal(0, 1, (filters_number, 1))

	stride = 1 # witdh and height
	# TODO: Add padding

	# convolve
	# TODO: I am sure there are numpy functions or tricks to avoid the while loops
	output_height = []

	height_counter = 0 # Moving vertically
	while height_counter < shape[0] - filter_height:
		
		output_width = []

		width_counter = 0 # Moving horizontally
		while width_counter < shape[1] - filter_width:
			
			output_depth = [] # elements of the new features map

			depth_counter = 0 # iterating the channels
			while depth_counter < shape[2]:
				
				patch = image_array[height_counter:height_counter + filter_height, width_counter:width_counter + filter_width, depth_counter]
				output_element = 0 # each filter results in an element in the depth direction

				filter_counter = 0 # applying filters
				while filter_counter < filters_number:
					filter_ = weights[filter_counter, depth_counter, :, :]
					output_element += np.sum(patch * filter_) + biases[filter_counter][0]

					filter_counter += 1

				output_depth.append(output_element)

				depth_counter += 1

			output_width.append(output_depth)
			width_counter += 1

		output_height.append(output_width)
		height_counter += 1

	output = np.array(output_height)
	return output

def rescale_rgb(x, isfloat=True):
	max_i = np.max(x)
	min_i = np.min(x)
	max_o = 1
	min_o = -1

	if isfloat is False:
		max_o = 255
		min_o = 0

	return ((x - min_i) * (max_o - min_o) / (max_i - min_i)) + min_o

def save_image(pixels_array, file_name):
   	io.imsave(file_name, pixels_array)

def image_name_no_ext(img_name):
	name = str(img_name)
	r = name[::-1]       		# reverse name
	n = r[r.index(".") + 1:]    # reverse name extensionless
	return n[::-1]

conv(sys.argv[1], sys.argv[2], sys.argv[3])
