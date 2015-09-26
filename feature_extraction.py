#extract feature from an object
#feature: histograms of direction
#can only detect object without "satellite" (e.g capital letter)
#no merging and sorting
#source:
#http://www.codeproject.com/Articles/160868/A-C-Project-in-Optical-Character-Recognition-OCR-U

from scipy import misc
import numpy as np
import matplotlib.pyplot as plt
import math

img = misc.imread('A_comic_sans.jpg')
bw = np.zeros((img.shape[0], img.shape[1]))

#binarize image
def getBW():
    for row in xrange(img.shape[0]):
        for col in xrange(img.shape[1]):
            if (np.sum(img[row][col]))/3 > 128:
                bw[row][col] = 0
            else:
                bw[row][col] = 1

#discard all nonborder pixels
def thin (img):
    thinned = np.copy(img)

    for row in xrange(img.shape[0]):
        for col in xrange(img.shape[1]):
            if img[row][col] == 1:
                if np.logical_not(np.all(img[row-1:row+2, col-1:col+2])) == True:
                    continue
                else:
                    thinned[row][col] = 0

    return thinned

# extract chain code using Freeman code
# store it in an ndarray of (track, sector, direction)
# will divide object to 5 tracks and sectors
def extraction(img):
    distances = []
    feature = np.zeros((5, 5, 8), dtype = float) #construct array
    ntrack = feature.shape[0]
    nsector = feature.shape[1]
    #get indices of border pixels
    borderElm = np.transpose(np.nonzero(img))
    #get index of centroid
    yc, xc = np.sum(borderElm, axis = 0)/len(borderElm)
    #get angles
    tan = borderElm - (yc, xc)
    y = tan.transpose()[0]
    x = tan.transpose()[1]
    angles = np.arctan2(y, x)
    # get distances
    for index in borderElm:
        d = math.sqrt(((index[0] - yc)**2) + ((index[1] - xc)**2))
        distances.append(d)

    r = max(distances)

    # evaluate every pixels
    # for every pixels, find: track position, sector position,
    # and amount of each directions of that pixel's neighbor
    for index in xrange(len(borderElm)):
        pixel = borderElm[index]
        row = pixel[0]
        col = pixel[1]
        pi = math.pi
        trackNo = 0
        sectorNo = 0

        if distances[index] < r/ntrack:
            trackNo = 0
        elif r/ntrack <= distances[index] < 2*r/ntrack:
            trackNo = 1
        elif 2*r/ntrack <= distances[index] < 3*r/ntrack:
            trackNo = 2
        elif 3*r/ntrack <= distances[index] < 4*r/ntrack:
            trackNo = 3
        else:
            trackNo = 4

        if angles[index] < (pi*2/5)-pi:
            sectorNo = 0
        elif (pi*2/5)-pi <= angles[index] < (pi*4/5)-pi:
            sectorNo = 1
        elif (pi*4/5)-pi <= angles[index] < (pi*6/5)-pi:
            sectorNo = 2
        elif (pi*6/5)-pi <= angles[index] < (pi*8/5)-pi:
            sectorNo = 3
        else:
            sectorNo = 4

        if img[row][col+1] == 1:
            feature[trackNo][sectorNo][0] += 1
        if img[row-1][col+1] == 1:
            feature[trackNo][sectorNo][1] += 1
        if img[row-1][col] == 1:
            feature[trackNo][sectorNo][2] += 1
        if img[row-1][col-1] == 1:
            feature[trackNo][sectorNo][3] += 1
        if img[row][col-1] == 1:
            feature[trackNo][sectorNo][4] += 1
        if img[row+1][col-1] == 1:
            feature[trackNo][sectorNo][5] += 1
        if img[row+1][col] == 1:
            feature[trackNo][sectorNo][6] += 1
        if img[row+1][col+1] == 1:
            feature[trackNo][sectorNo][7] += 1

    feature = feature/len(borderElm)
    return feature

if __name__ == '__main__':
    #binarize image
    getBW()
    #discard all nonborder pixels
    bw = thin(bw)
    #save feature to .txt file
    feature = extraction(bw)
    feature.tofile('D:\Codes\pengenalan pola\chaincode\A_comic_sans.txt',
    sep='||', format = "%.4f")
