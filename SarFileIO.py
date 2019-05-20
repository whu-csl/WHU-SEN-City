import struct
import numpy as np
from numpy.lib.stride_tricks import as_strided
import cv2
import scipy.io as scio

def ReadFile(fileName,width,height,byte_order = "<"):
    binfile = open(fileName,'rb')
    data = binfile.read();
    format = byte_order + str(width*height) + 'f'
    image = struct.unpack_from(format,data,0)
    image = np.reshape(image,[1,height,width])
    print("Read file complete : %s" % fileName)
    return image

def ReadHDRFile(fileName):
    hdr = open(fileName, 'rb')
    lines = hdr.readlines()
    for line in lines:
        line = str(line,encoding='utf-8')
        values = line.split('=')
        if(line.__contains__('samples')):
            width = values[1]
            width = width.strip()
            width = int(width)
        if(line.__contains__('lines')):
            height = values[1]
            height = height.strip()
            height = int(height)
        if(line.__contains__('byte order')):
            byte_order = values[1]
            byte_order = byte_order.strip()
            byte_order = float(byte_order)
            if(byte_order == 0):
                byte_order = "<"
            else:
                byte_order = ">"
    return height, width, byte_order

def ReadBinFiles(fileNames, width, height, byte_order = "<"):
    for i in range(len(fileNames) ):
        image = ReadFile(fileNames[i],width,height,byte_order)
        #saveimage = image * 255;
        #saveimage = saveimage.reshape(height,width,1)
        #cv2.imwrite("test" + str(i) + ".jpg",saveimage)
        if i == 0:
            imgs =image
        else:
            imgs = np.concatenate((imgs, image), 0)
            print(np.shape(imgs))
    return imgs
