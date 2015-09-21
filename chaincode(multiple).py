#extract chain code from objects in an image file
#problem: chain codes are already obtained
#but detected chain codes cannot be saved on list

from scipy import misc
import numpy as np
import copy
#import matplotlib.pyplot as plt
#used for checking if traced element(s) is deleted succesfully

img = misc.imread('c:/Users/User/Pictures/alfabet.jpg')
bw = np.zeros((img.shape[0], img.shape[1]))

#create black and white representation of image
#1 = black, 0 = white
def getBW():
    for row in xrange(img.shape[0]):
        for col in xrange(img.shape[1]):
            if (np.sum(img[row][col]))/3 > 128:
                bw[row][col] = 0
            else:
                bw[row][col] = 1

#find first pixel of object
def findPixel(bpixel, wpixel):
    for row in xrange(bpixel[0], bw.shape[0]):
        for col in xrange(bpixel[1], bw.shape[1]):
            if bw[row][col] == 1:
                bpixel = (row, col)
                wpixel = (row, col-1)
                #borderElm.append(bpixel)
                return bpixel, wpixel

#get starting direction from neighboring current index
#param: current black pixel index, former white pixel index
#will be used later for backtracking
def getDirection(bpixel, wpixel):
    dir = 0
    row = bpixel[0]
    col = bpixel[1]
    if wpixel == (row, col+1):
        dir = 0
    if wpixel == (row-1, col+1):
        dir = 1
    if wpixel == (row-1, col):
        dir = 2
    if wpixel == (row-1, col-1):
        dir = 3
    if wpixel == (row, col-1):
        dir = 4
    if wpixel == (row+1, col-1):
        dir = 5
    if wpixel == (row+1, col):
        dir = 6
    if wpixel == (row+1, col+1):
        dir = 7

    return dir

#get index of moore neighbor
#param: rotating direction and current pixel index
def getIndex(dir, bpixel):
    row = bpixel[0]
    col = bpixel[1]
    if dir == 0:
        #grid = (row, col)
        grid = (row, col+1)
    if dir == 1:
        grid = (row-1, col+1)
    if dir == 2:
        grid = (row-1, col)
    if dir == 3:
        grid = (row-1, col-1)
    if dir == 4:
        grid = (row, col-1)
    if dir == 5:
        grid = (row+1, col-1)
    if dir == 6:
        grid = (row+1, col)
    if dir == 7:
        grid = (row+1, col+1)

    return grid

#get border elements + chain code of an object
#using eight connectivity
#will rotate anti-clockwise
#param: image array, current black pixel, former white pixel
def getBorderElm(img, bpixel, wpixel):
    borderElm.append(bpixel)
    pixVal = img[wpixel[0]][wpixel[1]]
    direction = getDirection(bpixel, wpixel) #get initial direction
    index = (0, 0)

    while pixVal != 1:
        index = getIndex(direction, bpixel)
        pixVal = img[index[0], index[1]]
        if pixVal == 0:
            wpixel = copy.copy(index)
            direction = (direction+1) % 8
        else:
            bpixel = copy.copy(index)
    chainCode.append(direction)
    return bpixel, wpixel

#slice array than contains object
def slice(img, border):
    lowerBound = map(min, zip(*borderElm)) #bottom-right index
    upperBound = map(max, zip(*borderElm)) #top-left index
    #set sliced-array value to 0
    return lowerBound, upperBound

#delete object
def delObject(img, lowerBound, upperBound):
    img[lowerBound[0]:upperBound[0]+5, lowerBound[1]:upperBound[1]+5] = 0
    return img

def getChainCode():
    curInd = (0, 0) #store current black pixel index
    backtrack = (0, 0) #store former white pixel index
    curInd, backtrack = findPixel(curInd, backtrack)

    while curInd not in borderElm:
        curInd, backtrack = getBorderElm(bw, curInd, backtrack)

if __name__ == '__main__':
    getBW()
    count = 0
    chainCode = [] #save chain code of one object
    chainCodes = [] #suppossedly save chain codes of all objects in file
    borderElm = [] #save border elements of one object
    borderElms = [] #supposedly save border elms of all objects in file

    #get list of chain codes
    while np.any(bw) == True:
        getChainCode()
        chainCodes.append(chainCode)
        borderElms.append(borderElm)
        print "chain code: " + str(chainCode)
        print "border elements: " + str(borderElm)
        print "\n"
        lowerBound, upperBound = slice(bw, borderElm)
        bw = delObject(bw, lowerBound, upperBound)
        del borderElm[:]
        del chainCode[:]
        count += 1

    #chain code and border elements can be obtained but only append empty list
    #to chainCodes and borderElms
    #shown below
    print "\n" + str(chainCodes)
    print "\n" + str(borderElms)
    print "\n there are " + str(count) + " objects"
