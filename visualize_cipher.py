# requires pip install opencv-python
import cv2
import numpy as np
# import cipher.py, my module in the same directory

import cipher
 

class DumbPRNG (cipher.PRNG):
    def toNormalizedByte(self):
        # generates any random number, as long as it is 42
        return 42
    
def format_image():
    # takes input image and creates a 256x256 greyscale image
    src = cv2.imread('source_image.jpg',0)
    new_width = 256
    # dsize
    dsize = (new_width, 256)

    # resize image
    img = cv2.resize(src, dsize, interpolation = cv2.INTER_AREA)

    cv2.imshow('image',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.imwrite('greyscale.png',img) 






def encrypt_image (prng, src_img, title):
    result_img = np.zeros(src_img.shape, np.uint8)
    width = src_img.shape[0]
    height = src_img.shape[1]
    for i in range(0, width):
        for j in range(0, height):
            result_img [i,j] = src_img[i,j] ^ prng.toNormalizedByte() \

    cv2.imshow(title,result_img)
    
    
def show_original():
    cv2.imshow('image',src)
    cv2.waitKey(0)
    cv2.destroyAllWindows()



if __name__ == '__main__':
    print ('Python Implementation of a Stream Encryption Algorithm')
    print ('Christopher M. LaPonsie')
    print ('IAAS221 Security Foundations')
    print ('------------------------------')
    print ('Instantiating linear congruential generator')
    prngLCG = cipher.lcgPRNG()
    if (prngLCG):
        print ('...OK')
    print ('Instantiating middle square generator')
    prngMS = cipher.MiddleSquarePRNG()
    prngMS.setDigits ( 15 )
    prngMS.setSeed ( 123456 )
    if (prngMS):
        print ('...OK')
    print ('Instantiating number 42 generator')
    dPRNG = DumbPRNG()
    if (dPRNG):
        print ('...OK')
    print ('------------------------------')
    src = cv2.imread('greyscale.png',0)

    
    cv2.imshow('Original',src)
    encrypt_image (dPRNG, src, "XOR 42")
    encrypt_image (prngMS, src, "Middle Square Method")
    encrypt_image (prngLCG, src, "LCG Method")
    cv2.waitKey(0)
    cv2.destroyAllWindows()
