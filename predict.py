import numpy as np
import keras
from PIL import Image

from model import SegNet
 
import dataset

height = 360
width = 480
classes = 12
epochs = 100
batch_size = 1
log_filepath='./logs_100/'

data_shape = 360*480

def writeImage(image, filename):
    """ label data to colored image """
    Sky = [128,128,128]
    Building = [128,0,0]
    Pole = [192,192,128]
    Road_marking = [255,69,0]
    Road = [128,64,128]
    Pavement = [60,40,222]
    Tree = [128,128,0]
    SignSymbol = [192,128,128]
    Fence = [64,64,128]
    Car = [64,0,128]
    Pedestrian = [64,64,0]
    Bicyclist = [0,128,192]
    Unlabelled = [0,0,0]
    r = image.copy()
    g = image.copy()
    b = image.copy()
    label_colours = np.array([Sky, Building, Pole, Road_marking, Road, Pavement, Tree, SignSymbol, Fence, Car, Pedestrian, Bicyclist, Unlabelled])
    for l in range(0,12):
        r[image==l] = label_colours[l,0]
        g[image==l] = label_colours[l,1]
        b[image==l] = label_colours[l,2]
    rgb = np.zeros((image.shape[0], image.shape[1], 3))
    rgb[:,:,0] = r/1.0
    rgb[:,:,1] = g/1.0
    rgb[:,:,2] = b/1.0
    im = Image.fromarray(np.uint8(rgb))
    # im.save('/Users/koheiyamamoto/Desktop/SegNet/out/' + filename)
    im.save('./out/' + filename)
    
def getfilename(l):
    newnames = []
    for name in l:
        newnames.append(name[0].lstrip("/SegNet/CamVid/test/").rstrip(".png") + '_out.png' )
    return newnames

def main():
    print("loading data...")

    print('loading model... this part is gonna take a while')
    model = keras.models.load_model('./seg.h5')
    print('loaded model...')

    # ds = dataset.Dataset(test_file='val.txt', classes=classes)
    ds = dataset.Dataset(test_file='test.txt', classes=classes)
    print("data loaded...")
    filenames, test_X, test_y = ds.load_data_test('test') # need to implement, y shape is (None, 360, 480, classes)
    test_X = ds.preprocess_inputs(test_X)
    test_Y = ds.reshape_labels(test_y)
    # print('---------')
    # print(len(test_X))
    # print('---------')
    # print(len(test_Y))
    # print(filenames)
    # print(len(filenames))

    files = getfilename(filenames)

    print("predicting...")
    probs = model.predict(test_X, batch_size=1)
    # print('probs---------')
    # print(probs)
    # print(len(probs))
    for index,name in enumerate(files):
        prob = probs[index].reshape((height, width, classes)).argmax(axis=2)
        # print('prob---------')
        # print(prob)
        # print(len(prob))
        print('step: ', index, '/', len(files))
        print(prob)
        # print(len(prob))
        print("writing...")  
        writeImage(prob, name)

# def predict(test):
#     print('loading model... this part is gonna take a while')
#     model = keras.models.load_model('./seg.h5')
#     print('loaded model...')
#     probs = model.predict(test, batch_size=1)

#     prob = probs[0].reshape((height, width, classes)).argmax(axis=2)    
#     return prob

# def main():
#     print("loading data...")
#     # ds = dataset.Dataset(test_file='val.txt', classes=classes)
#     ds = dataset.Dataset(test_file='test.txt', classes=classes)
#     print("data loaded...")
#     test_X, test_y = ds.load_data('test') # need to implement, y shape is (None, 360, 480, classes)
#     test_X = ds.preprocess_inputs(test_X)
#     test_Y = ds.reshape_labels(test_y)

#     print("predicting...")
#     prob = predict(test_X)
#     print("writing...")    
#     writeImage(prob, 'val.png')

if __name__ == '__main__':
    main()