import numpy as np
import cv2
import os
from skimage import exposure

def toGray(images):
    # rgb2gray converts RGB values to grayscale values by forming a weighted sum of the R, G, and B components:
    # 0.2989 * R + 0.5870 * G + 0.1140 * B 
    # source: https://www.mathworks.com/help/matlab/ref/rgb2gray.html
    
    images = 0.2989*images[:,:,:,0] + 0.5870*images[:,:,:,1] + 0.1140*images[:,:,:,2]
    return images

def normalizeImages(images):
    # use Histogram equalization to get a better range
    # source http://scikit-image.org/docs/dev/api/skimage.exposure.html#skimage.exposure.equalize_hist
    images = (images / 255.).astype(np.float32)
    
    for i in range(images.shape[0]):
        images[i] = exposure.equalize_hist(images[i])
    
    images = images.reshape(images.shape + (1,)) 
    return images

def normalizeImages2(images):
    for i in range(images.shape[0]):
        cv2.normalize(images[i],images[i], alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
    
    # if convert to gray scale use this after
    print("images has shape before", images.shape)
    #images = images.reshape(images.shape + (1,)) 
    #print("images has shape after", images.shape)
    return images

def preprocessData(images):
    grayImages = toGray(images)
    return normalizeImages(grayImages)

def rotateImage(img, angle):
    (rows, cols, ch) = img.shape
    M = cv2.getRotationMatrix2D((cols/2,rows/2), angle, 1)
    return cv2.warpAffine(img, M, (cols,rows))

def loadBlurImg(path, imgSize):
    img = cv2.imread(path)
    if img is None:
        print("Invalid Image")
        return None
    #angle = np.random.randint(-180, 180)
    #img = rotateImage(img, angle)
    img = cv2.blur(img,(5,5))
    img = cv2.resize(img, imgSize)
    #showImage(img)
    return img

def load_img(img_path):
    x = []
    if not os.path.exists(img_path):
        print("Image not found!")
        return None
    
    img = loadBlurImg(img_path, (64, 64))

    if img is None:
        return None
    
    x.append(img)
    y = np.array(x)
    return y

def classify(img_path):

    if not os.path.exists(os.getcwd() + '/car.h5'):
        print("Cannot find pre-trained model")
        return None

    print(img_path)
    img = load_img(img_path)

    if img is None:
        return None

    img = preprocessData(img)

    import tensorflow as tf
    sess = tf.Session()
    from keras import backend as K
    K.set_session(sess)

    from keras.models import load_model
    model = load_model(os.getcwd() + '/car.h5')

    predictions = model.predict_classes(img)

    cleanup(img_path)
    
    if predictions[0] == 0:
        return True
    else:
        return False

def save_file(f):
    from django.core.files.storage import FileSystemStorage
    fs = FileSystemStorage()
    filename = fs.save(f.name, f)
    return fs.path(filename)

def cleanup(path):
    if os.path.isfile(path):
        print("is file")
        os.remove(path)