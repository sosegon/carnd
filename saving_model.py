'''
    DEFINE THE MODEL
'''
import tensorflow as tf
# Remove previous Tensors and Operations
tf.reset_default_graph()

from tensorflow.examples.tutorials.mnist import input_data
import numpy as np

learning_rate = 0.001
n_input = 784  # MNIST data input (img shape: 28*28)
n_classes = 10  # MNIST total classes (0-9 digits)

# Import MNIST data
mnist = input_data.read_data_sets('.', one_hot=True)

# Features and Labels
features = tf.placeholder(tf.float32, [None, n_input])
labels = tf.placeholder(tf.float32, [None, n_classes])

# Weights & bias
weights = tf.Variable(tf.random_normal([n_input, n_classes]))
bias = tf.Variable(tf.random_normal([n_classes]))

# Logits - xW + b
logits = tf.add(tf.matmul(features, weights), bias)

# Define loss and optimizer
cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits, labels))
optimizer = tf.train.GradientDescentOptimizer(learning_rate=learning_rate).minimize(cost)

# Calculate accuracy
correct_prediction = tf.equal(tf.argmax(logits, 1), tf.argmax(labels, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

'''
    TRAIN THE MODEL
'''
import math
import os.path
from datetime import datetime as dt

start =  dt.now()

save_file = 'train_model.ckpt'
batch_size = 128
n_epochs = 100

saver = tf.train.Saver()

# Launch the graph
with tf.Session() as sess:
    # Initialize all the Variables
    if os.path.exists(save_file):
        saver.restore(sess, save_file)
        test_accuracy = sess.run(accuracy, feed_dict={features: mnist.test.images, labels: mnist.test.labels})
        print('Test Accuracy: {}'.format(test_accuracy))
    else:
        sess.run(tf.initialize_all_variables())

        # Training cycle
        for epoch in range(n_epochs):
            total_batch = math.ceil(mnist.train.num_examples / batch_size)

            # Loop over all batches
            for i in range(total_batch):
                batch_features, batch_labels = mnist.train.next_batch(batch_size)
                sess.run(
                    optimizer,
                    feed_dict={features: batch_features, labels: batch_labels})

            # Print status for every 10 epochs
            if epoch % 10 == 0:
                valid_accuracy = sess.run(
                    accuracy,
                    feed_dict={
                        features: mnist.validation.images,
                        labels: mnist.validation.labels})
                print('Epoch {:<3} - Validation Accuracy: {}'.format(
                    epoch,
                    valid_accuracy))

        # Save the model
        saver.save(sess, save_file)
        print('Trained Model Saved.')

end = dt.now()
delta = end - start
total = round(delta.seconds + delta.microseconds/1E6, 2) # from http://stackoverflow.com/a/2880735/1065981

print("Total training time: " + str(total) + " seconds")