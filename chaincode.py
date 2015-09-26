#extract chain code from objects in an image file

from scipy import misc
import numpy as np
import copy
import matplotlib.pyplot as plt
import feature_extraction

img = misc.imread('alfabet.jpg')
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
    if bpixel not in borderElm:
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
    histOfDir[direction] += 1
    return bpixel, wpixel

#slice array than contains object
def slice(img, border):
    lowerBound = map(min, zip(*borderElm)) #bottom-right index
    upperBound = map(max, zip(*borderElm)) #top-left index
    #set sliced-array value to 0
    return lowerBound, upperBound

#delete object
def delObject(img, lowerBound, upperBound):
    img[lowerBound[0]:upperBound[0]+1, lowerBound[1]:upperBound[1]+1] = 0
    return img

def getChainCode(chainCode):
    curInd = (0, 0) #store current black pixel index
    backtrack = (0, 0) #store former white pixel index
    curInd, backtrack = findPixel(curInd, backtrack)
    flag = copy.copy(curInd)
    countFlag = 0

    while countFlag < 2:
        curInd, backtrack = getBorderElm(bw, curInd, backtrack)
        if curInd == flag:
            countFlag += 1
    return chainCode

if __name__ == '__main__':
    getBW()
    imgplot = plt.imshow(bw, cmap = 'Greys')
    plt.show()
    count = 0

    chainCodes = [] #save string of chain code
    features = [] #save histogram of each object

    #get list of chain codes
    while np.any(bw) == True:
        chainCode = [] #save chain code of one object
        borderElm = [] #save border elements of one object
        histOfDir = [0]*8 #make histogram of direction
        amtOfPix = 0 #will store amount of border elements

        chainCode = getChainCode(chainCode)
        #convert chain code to string
        strcc = ''.join(str(e) for e in chainCode)
        #append string to list of chaincodes
        chainCodes.append(strcc)
        amtOfPix = len(borderElm)

        #slice array that contains object
        lowerBound, upperBound = slice(bw, borderElm)
        #delete that object
        bw = delObject(bw, lowerBound, upperBound)

        histOfDir = np.asarray(histOfDir)
        histOfDir = histOfDir*1.0 / amtOfPix*1.0
        features.append(histOfDir)
        count += 1
        #imgplot = plt.imshow(bw, cmap = 'Greys')
        #plt.show()

    #convert features to array
    #save it to .txt file
    features = np.asarray(features)
    features.tofile('D:\Codes\pengenalan pola\chaincode\larik', sep='||',
    format = "%.2f")
    float_formatter = lambda x: "%.2f" %x
    np.set_printoptions(formatter={'float_kind':float_formatter})
    print "\n" + str(chainCodes)
    print "\n" + str(features)
    print "\n there are " + str(count) + " objects"
    #plot histogram of each letter
    #for n in xrange(len(features)):
    #    plt.plot(features[n])
    #    plt.show()
