#
# Used to implement AlexNet for Mnist
# date:2018-5-9
# a  : zhonghy
#
#

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

#AlexNet
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
import numpy


"""input dataset"""
mnist = input_data.read_data_sets("E:/data/MNIST_data", one_hot=True)

#define hyperparameters of net
learning_rate = 0.001
training_iters = 200000   #200000
batch_size = 128
display_step = 10

#define parameters of net
n_input = 784    #dimension of input(image shape:28 x 28)
n_classes = 10   #dimension of labels(0-9 digits)
dropout = 0.75   #probability of dropout and output

#input placeholder
x = tf.placeholder(tf.float32, [None, n_input])
y = tf.placeholder(tf.float32, [None, n_classes])
keep_prob = tf.placeholder(tf.float32) #dropout

"""define conv, pool, normal function for AlexNet"""
#define convolution operations
def conv2d(name, x, w, b, strides=1):
    x = tf.nn.conv2d(x, w, strides = [1, strides, strides, 1], padding = 'SAME')
    x = tf.nn.bias_add(x, b)
    return tf.nn.relu(x, name=name) #utilize relu active function

#define pool operations
def maxpool2d(name, x, k=2):
    return tf.nn.max_pool(x, ksize=[1, k, k, 1], strides=[1, k, k, 1],
                          padding='SAME', name=name)

#nomorlize operations
def norm(name, l_input, lsize=4):
    return tf.nn.lrn(l_input, lsize, bias=1.0, alpha=0.001 / 9.0,
                     beta=0.75, name=name)

#define all parameters of net
weights = {
    'wc1': tf.Variable(tf.random_normal([11, 11, 1, 96])),
    'wc2': tf.Variable(tf.random_normal([5, 5, 96, 256])),
    'wc3': tf.Variable(tf.random_normal([3, 3, 256, 384])),
    'wc4': tf.Variable(tf.random_normal([3, 3, 384, 384])),
    'wc5': tf.Variable(tf.random_normal([3, 3, 384, 256])),
    'wd1': tf.Variable(tf.random_normal([4*4*256, 4096])),
    'wd2': tf.Variable(tf.random_normal([4096, 4096])),
    'out': tf.Variable(tf.random_normal([4096, 10]))
    }

biases = {
    'bc1': tf.Variable(tf.random_normal([96])),
    'bc2': tf.Variable(tf.random_normal([256])),
    'bc3': tf.Variable(tf.random_normal([384])),
    'bc4': tf.Variable(tf.random_normal([384])),
    'bc5': tf.Variable(tf.random_normal([256])),
    'bd1': tf.Variable(tf.random_normal([4096])),
    'bd2': tf.Variable(tf.random_normal([4096])),
    'out': tf.Variable(tf.random_normal([n_classes]))
    }

"""define AlexNet model"""
def alex_net(x, weights, biases, dropout):
    #Reshape input picture
    x = tf.reshape(x, shape=[-1, 28, 28, 1])
    
    """first layer conv"""
    #convolution
    conv1 = conv2d('conv1', x, weights['wc1'], biases['bc1'])
    #downsampling
    pool1 = maxpool2d('pool1', conv1, k=2)
    #normalization
    norm1 = norm('norml', pool1, lsize=4)
    norm1 = tf.nn.dropout(norm1, dropout)

    """second layer conv"""
    #convolutin
    conv2 = conv2d('conv2', conv1, weights['wc2'], biases['bc2'])
    #maxpool(downsampling)
    pool2 = maxpool2d('pool2', conv2, k=2)
    #normalize
    norm2 = norm('norm2', pool2, lsize=4)
    norm2 = tf.nn.dropout(norm2, dropout)

    """third layer conv"""
    conv3 = conv2d('conv3', norm2, weights['wc3'], biases['bc3'])
    #downsample
    pool3 = maxpool2d('pool3', conv3, k=2)
    #normalize
    norm3 = norm('norm3', pool3, lsize=4)
    norm3 = tf.nn.dropout(norm3, dropout)

    """fourth layer conv"""
    conv4 = conv2d('conv4', norm3, weights['wc4'], biases['bc4'])
    """fifth layer conv"""
    conv5 = conv2d('conv5', norm3, weights['wc5'], biases['bc5'])
    #downsample
    pool5 = maxpool2d('pool5', conv5, k=2)
    #normlize
    norm5 = norm('norm5', pool5, lsize=4)
    norm5 = tf.nn.dropout(norm5, dropout)

    """full connect layer1"""
    fc1 = tf.reshape(norm5, [-1, weights['wd1'].get_shape().as_list()[0]])
    fc1 = tf.add(tf.matmul(fc1, weights['wd1']), biases['bd1'])
    fc1 = tf.nn.relu(fc1)
    #dropout
    fc1 = tf.nn.dropout(fc1, dropout)

    """full connect layer2"""
    fc2 = tf.reshape(fc1, [-1, weights['wd1'].get_shape().as_list()[0]])
    fc2 = tf.add(tf.matmul(fc2, weights['wd1']), biases['bd1'])
    fc2 = tf.nn.relu(fc2)
    #dropout
    fc2 = tf.nn.dropout(fc2, dropout)

    """output layer"""
    out = tf.add(tf.matmul(fc2, weights['out']), biases['out'])
    return out



"""construct loss function, optimizer, model"""
#construct model
pred = alex_net(x, weights, biases, keep_prob)

#define loss function and optimizer
cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits = pred,
                                                              labels = y))
optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cost)

#estimate function
correct_pred = tf.equal(tf.argmax(pred, 1), tf.argmax(y, 1))
accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

"""training and estimate"""
#initialize variables
init = tf.global_variables_initializer()

with tf.Session() as sess:
    sess.run(init)
    step = 1
    #launch training, until training_iters = 200000
    while step * batch_size < training_iters:
        batch_x, batch_y = mnist.train.next_batch(batch_size)
        sess.run(optimizer, feed_dict={x: batch_x, y: batch_y, #errors here
                                       keep_prob: dropout})
        if step % display_step == 0:
            #calculate accuracy and loss value
            loss, acc = sess.run([cost, accuracy], feed_dict={x: batch_x,
                                                              y: batch_y,
                                                              keep_prob: 1.})
            print("Iter" + str(step*batch_size) + ", Minibatch Loss= " + \
                  "{:.6f}".format(loss) + ", Training Accuracy= " + \
                  "{:.5f}".format(acc))
        step += 1
        
    print("Optimization Finished!")

    #calculate accucary of test sets
    print("Testing Accuracy:", \
          sess.run(accuracy, feed_dict={x: mnist.test.images[:256],
                                        y: mnist.test.labels[:256],
                                        keep_prob:1.}))


