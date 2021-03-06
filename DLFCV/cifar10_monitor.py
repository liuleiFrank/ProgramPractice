#
# Train MiniVGGNet with monitor on cifar10 dataset
# a: zhonghy
# date: 2018-7-24
#
#

# set the matplotlib backend so figures can be saved in the background
import matplotlib
matplotlib.use("Agg")

# import the necessary packages
from pyimagesearch.callbacks.trainingmonitor import TrainingMonitor
from sklearn.preprocessing import LabelBinarizer
from pyimagesearch.nn.conv.minivggnet import MiniVGGNet
from keras.optimizers import SGD
from keras.datasets import cifar10
import argparse
import os

### construct the argument parse and parse the arguments
##ap = argparse.ArgumentParser()
##ap.add_argument("-o", "--output", required=True,
##                help="path to the output directory")
##args = vars(ap.parse_args())

# show information on the process ID
print("[INFO] process ID: {}".format(os.getpid()))

# load the training and testing data, then scale it into the
# range [0, 1]
print("[INFO] loading CIFAR-10 data...")
((trainX, trainY), (testX, testY)) = cifar10.load_data()
trainX = trainX.astype("float") / 255.0
testX = testX.astype("float") / 255.0

# convert the labels from integers to vectors
lb = LabelBinarizer()
trainY = lb.fit_transform(trainY)
testY = lb.fit_transform(testY)

# initialize the label names for the CIFAR-10 dataset
labelNames = ["airplane", "automobile", "bird", "cat", "deer",
              "dog", "frog", "horse", "ship", "truck"]

# initialize the optimizer and model
print("[INFO] compiling model...")
opt = SGD(lr=0.01, momentum=0.9, nesterov=True) # attention
model = MiniVGGNet.build(width=32, height=32, depth=3, classes=10)
model.compile(loss="categorical_crossentropy", optimizer=opt,
              metrics=["accuracy"])

# construct the set of callbacks
figPath = os.path.sep.join(["F:\\data", "{}.png".format(
    os.getpid())]) #args["output"]
jsonPath = os.path.sep.join(["F:\\data", "{}.json".format(
    os.getpid())])# [args["output"]
callbacks = [TrainingMonitor(figPath, jsonPath=jsonPath)]

# train the network
print("[INFO] training network...")
model.fit(trainX, trainY, validation_data=(testX, testY),
              batch_size=64, epochs=100, callbacks=callbacks, verbose=1)

#########################################
# save the network to disk
print("[INFO] serializing network...")
model.save("MiniVGGNet_on_cifar10_without_decay.hdf5")
#########################################
##
### evaluate the network
##print("[INFO] evaluating network...")
##predictions = model.predict(testX, batch_size=64)
##print(classification_report(testY.argmax(axis=1),
##                            predictions.argmax(axis=1),
##                            target_names=labelNames))
##
### plot the training loss and accuarcy
##plt.style.use("ggplot")
##plt.figure()
##plt.plot(np.arange(0, 40), H.history["loss"], label="train_loss")
##plt.plot(np.arange(0, 40), H.history["val_loss"], label="val_loss")
##plt.plot(np.arange(0, 40), H.history["acc"], label="train_acc")
##plt.plot(np.arange(0, 40), H.history["val_acc"], label="val_acc")
##plt.title("Training Loss and Accuarcy")
##plt.xlabel("Epoch #")
##plt.ylabel("Loss/Accuarcy")
##plt.legend()
##plt.show()
####plt.savefig(args["output"])


