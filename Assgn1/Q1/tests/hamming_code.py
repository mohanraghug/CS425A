from PIL import Image
import sys


def LeftShiftRotate(oldstate):  								# please Don't Modified it :)
	
	leftbit = oldstate[0]
	
	for i in range(0,14):
		oldstate[i] = oldstate[i+1]

	oldstate[14] = leftbit
	newstate = oldstate

	return newstate
	 
 
def hamming_decode(bitstring):

												# do something #
		

def hamming_encode(bitstring):
	
												# do something #


def ReadImage():

	image_name = # same as above        
	flip_bits = # read as command line argrument    					        
	
	image_ = Image.open(image_name)
	pixel_ = image_.load()
	width, height = image_.size

	for y in range (0, height):
		for x in range (0, width):  


		# add code here #
  
		
		
		flip_bits = LeftShiftRotate(flip_bits)
			

ReadImage()


												# file ends here #
