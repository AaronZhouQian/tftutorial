#!/usr/bin/python
import numpy as np
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
mnist=input_data.read_data_sets('MNIST_data',one_hot=True)

#The hyperparameters 
#strides for the max pooling layer is 2 in this case
#we only use 1 convolution layer and 1 max pooling layer

def weight_variable(shape):
  initial = tf.truncated_normal(shape, stddev=0.1)
  return tf.Variable(initial)
  
def bias_variable(shape):
  initial = tf.constant(0.1, shape=shape)
  return tf.Variable(initial)
  
def conv2d(x,W,stride_length=1):
    return tf.nn.conv2d(x,W,strides=[1,stride_length,stride_length,1],padding='SAME')

def max_pool_2x2(x):
    return tf.nn.max_pool(x,ksize=[1,2,2,1],strides=[1,2,2,1],padding='SAME')

def routine(conv2d_stride_length=2,W1_dim=[5,5,1,32],b1_dim=[32],W2_dim=[5, 5, 32, 64],b2_dim=[64]):
    sess=tf.InteractiveSession()
    W_conv1_weight_variable_dim = W1_dim
    b_conv1_bias_variable_dim = b1_dim
    W_conv2_weight_variable_dim = W2_dim
    b_conv2_bias_variable_dim = b2_dim
    #input data
    x=tf.placeholder(tf.float32,shape=[None,784])
    #correct labels
    y_=tf.placeholder(tf.float32,shape=[None,10])

    x_image=tf.reshape(x,[-1,28,28,1])

    #first layer
    W_conv1=weight_variable(W_conv1_weight_variable_dim)
    b_conv1=bias_variable(b_conv1_bias_variable_dim)

    h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1, conv2d_stride_length) + b_conv1)
    h_pool1 = max_pool_2x2(h_conv1)


    #second layer
#    W_conv2 = weight_variable(W_conv2_weight_variable_dim)
#    b_conv2 = bias_variable(b_conv2_bias_variable_dim)

#    h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2, conv2d_stride_length) + b_conv2)
#    h_pool2 = max_pool_2x2(h_conv2)


    #Densely Connected Layer
    #the first division is the number of pixels in the width/height of
    #the output of the conv layer while the second division gives those
    #in the output after the max pooling
    output_img_dim=(28/conv2d_stride_length)/2
    W_fc1 = weight_variable([output_img_dim * output_img_dim * b1_dim[0], 1024])
    b_fc1 = bias_variable([1024])

    h_pool1_flat = tf.reshape(h_pool1, [-1, output_img_dim * output_img_dim * b1_dim[0]])
    h_fc1 = tf.nn.relu(tf.matmul(h_pool1_flat, W_fc1) + b_fc1)

    #dropout
    keep_prob = tf.placeholder(tf.float32)
    h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

    #readout layer
    W_fc2 = weight_variable([1024, 10])
    b_fc2 = bias_variable([10])

    y_conv=tf.nn.softmax(tf.matmul(h_fc1_drop, W_fc2) + b_fc2)

    cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(y_conv), reduction_indices=[1]))
    train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)
    correct_prediction = tf.equal(tf.argmax(y_conv,1), tf.argmax(y_,1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

    sess.run(tf.initialize_all_variables())
    for i in range(20000):
        batch = mnist.train.next_batch(50)
        if i%1000 == 0:
            train_accuracy = accuracy.eval(feed_dict={x:batch[0], y_: batch[1], keep_prob: 1.0})
            print("step %d, training accuracy %g"%(i, train_accuracy))
        
        train_step.run(feed_dict={x: batch[0], y_: batch[1], keep_prob: 0.5})

    print("test accuracy %g"%accuracy.eval(feed_dict={
        x: mnist.test.images, y_: mnist.test.labels, keep_prob: 1.0}))


def main():
    for c2stride_length in [3,4,5,6]:
        routine(conv2d_stride_length=2)
        print("the conv2d_stride_length is %d" %conv2d_stride_length)


if __name__ == '__main__':
  main()







































