import numpy as np
import platform
import SarFileIO as sarIO
import cv2 as cv
import os
import scipy.io as scio

dataset_path = './WHU-SEN-City/'
sample_step = 128
sample_size = 256

def Create_SAR_RGB(sar_data, minmax = []):
    minmax = np.reshape(minmax,[6])
    #if(len(minmax) < 6):
    #    print('Error, no invalid min and max value')
    #    return
    t11 = sar_data[0, :, :]
    t22 = sar_data[1, :, :]
    t33 = sar_data[2, :, :]

    eps = 0.0000000000000001

    pb = 10 * np.log10(t11 + eps)
    pc = 10 * np.log10(t22 + eps)
    pa = 10 * np.log10(t33 + eps)

    maxpb = minmax[0]
    minpb = minmax[1]

    maxpc = minmax[2]
    minpc = minmax[3]

    maxpa = minmax[4]
    minpa = minmax[5]

    r = (pb - minpb) / (maxpb - minpb)
    g = (pc - minpc) / (maxpc - minpc)
    b = (pa - minpa) / (maxpa - minpa)

    r = np.clip(r, 0, 1)
    g = np.clip(g, 0, 1)
    b = np.clip(b, 0, 1)

    r = np.float32(255 * r)
    g = np.float32(255 * g)
    b = np.float32(255 * b)

    t3Shape = np.shape(sar_data)
    image = [b, g, r]
    image = np.reshape(image, [3, t3Shape[1], t3Shape[2]])
    image = np.transpose(image, [1, 2, 0])
    return image

def ReadS1Data(filePath):
    hdr_file = os.path.join(filePath,'Amplitude_VH.hdr')
    height, width, byte_order = sarIO.ReadHDRFile(hdr_file)

    binfileslist = [os.path.join(filePath,'Amplitude_VH.img'),os.path.join(filePath,'Amplitude_VV.img')]
    binfiles = sarIO.ReadBinFiles(binfileslist, width, height, byte_order)

    div = binfiles[0,:,:] / binfiles[1,:,:]
    div = np.reshape(div,[1,height,width])
    binfiles = np.append(binfiles,div,axis=0)

    minmaxfile = scio.loadmat(os.path.join(dataset_path, 'total_minmax.mat'))
    minmax = minmaxfile['minmax']

    binfiles = Create_SAR_RGB(binfiles,minmax)

    return binfiles

def SampleCount(length):
    count = (length - sample_step) * 1.0 / sample_step
    count = int(count)
    return count

def ReadSENData(dataset_path):
    total_count = 0
    paths = os.listdir(dataset_path)
    for path in paths:
        path = os.path.join(dataset_path,path)
        if(os.path.isdir(path)):
            print(path)
            sub_files = os.listdir(path)
            for sub in sub_files:
                sub = os.path.join(path,sub)
                print('--' + sub)
                if(os.path.isfile(sub) and sub.__contains__('_of_S2')):
                    print("--read s2 data: %s" % sub)
                    img = cv.imread(sub)

                elif(os.path.isdir(sub) and sub.__contains__('_of_S1')):
                    print("--read s1 data: %s" % sub)
                    binfiles = ReadS1Data(sub)
                    #cv.imwrite(os.path.basename(path) + ".png", binfiles)

            width = np.shape(img)[1]
            height = np.shape(img)[0]
            w_count = SampleCount(width)
            h_count = SampleCount(height)
            total_count = total_count + w_count * h_count

            binfiles = cv.resize(binfiles, (width, height), 0, 0, cv.INTER_CUBIC)

            city_count = 0
            for h_c in range(0,h_count):
                for w_c in range(0,w_count):
                    h = h_c * sample_step
                    w = w_c * sample_step
                    sub_s2 = img[h:h + sample_size, w:w + sample_size,:]
                    sub_s1 = binfiles[h:h + sample_size, w:w + sample_size,:]
                    scio.savemat(path + '/' + str(city_count) +'.mat', {'s1': sub_s1, 's2': sub_s2})
                    city_count = city_count + 1

    print("Total count %d" % total_count)

ReadSENData(dataset_path + '/train')