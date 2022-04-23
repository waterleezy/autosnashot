import numpy
import cv2
from PIL import Image


def calculatedif(img1, img2):
    img1 = cv2.cvtColor(numpy.asarray(img1), cv2.COLOR_RGB2BGR)
    img2 = cv2.cvtColor(numpy.asarray(img2), cv2.COLOR_RGB2BGR)
    hist1 = cv2.calcHist([img1],[0],None,[255],[0.0, 255.0])
    hist2 = cv2.calcHist([img2],[0],None,[255],[0.0, 255.0])

    degree = 0
    for i in range(len(hist1)):
        if hist1[i] != hist2[i]:
            degree = degree + (1-abs(hist1[i]-hist2[i])/max(hist1[i],hist2[i]))
        else:
            degree = degree + 1
    degree = degree / len(hist1)
    return degree

def classify_hist_with_split(imgf1, imgf2, size=(256,256)):
    #img1 = Image.open(imgf1)
    #img2 = Image.open(imgf2)
    img1 = imgf1
    img2 = imgf2
    #they will do resize to reduce calcuate.
    img1 = cv2.cvtColor(numpy.asarray(img1), cv2.COLOR_RGB2BGR)
    img2 = cv2.cvtColor(numpy.asarray(img2), cv2.COLOR_RGB2BGR)

    img1 = cv2.resize(img1, size)
    img2 = cv2.resize(img2, size)

    sub_img1 = cv2.split(img1)
    sub_img2 = cv2.split(img2)

    sub_data=0

    for im1, im2 in zip(sub_img1, sub_img2):
        sub_data += calculatedif(im1, im2)
    sub_data = sub_data / 3

    return sub_data




    
