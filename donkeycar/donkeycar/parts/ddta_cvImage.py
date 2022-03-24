import cv2 as cv


class DDTA_CvImage(object):

    def __init__(self):
        #self.trapezoidal_mask = None
        print("DDTA : Image OpenCV Part activated")


    def run(self, image):
        if image is None or image[0] is None:
            return image
        
        image = image.copy()
        originalimage = image
        
        #crop basé sur original_2k22 dimensions : 216*162
        y=43
        x=0
        h=76
        w=216
        crop_img = image[y:y+h, x:x+w]

        ##ajout masque
        #wMask = cv.bitwise_and(origin,mask)
        #cv.imshow("1 - mask", wMask)

        ##niveau de gris
        gray = cv.cvtColor(crop_img, cv.COLOR_BGR2GRAY)

        ##noir & blanc
        (thresh, blackAndWhiteImage) = cv.threshold(gray, 127, 255, cv.THRESH_BINARY)

        ##erosion
        kernel_size = 3     #3,5,7 aua choix
        #kernel = np.ones((kernel_size,kernel_size),np.uint8)
        #kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE,(kernel_size,kernel_size))
        kernel = cv.getStructuringElement(cv.MORPH_CROSS,(kernel_size,kernel_size))

        erosion = cv.erode(blackAndWhiteImage,kernel,iterations = 1)
        #erosion = cv.erode(blackAndWhiteImage,cv.MORPH_OPEN,kernel)
        
        return erosion
