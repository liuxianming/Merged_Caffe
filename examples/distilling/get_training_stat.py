import lmdb
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import sys
CAFFE_ROOT = '/mnt/ilcompf0d0/user/xliu/code/caffe/python'
sys.path.append(CAFFE_ROOT)
import caffe
from caffe.io import caffe_pb2


"""This script is basically used to calculate the label distribution and plot
"""

def calculate_label_dist(db_name, num_label, compact=True):
    db = lmdb.open(db_name)
    print "Database {} opened, and begin processing".format(db_name)
    label_dist = np.zeros((num_label,))
    conf_matrix = np.zeros((num_label, num_label))
    with db.begin() as txn:
        cur = txn.cursor()
        datum = caffe_pb2.Datum()
        for key, value in cur:
            datum.ParseFromString(value)
            labels = caffe.io.datum_to_array(datum).flatten()
            if compact:
                label_vec = np.zeros((1, num_label))
                for idx in labels:
                    label_vec[0, idx] = 1
            else:
                label_vec = labels.reshape((1,num_label))
            label_dist += label_vec.flatten()
            conf_matrix += label_vec.transpose().dot(label_vec)
        # for compact case, scan one by one
        # for non-compact case, just add the fetech vector to label_dist
    return label_dist, conf_matrix

if __name__ == "__main__":
    training_field_lmdb = '/mnt/ilcompf2d1/data/be/prepared-2015-06-15/Encoded_LMDB/TRAINING/field'
    num_labels = 67
    label_dist, conf_matrix = calculate_label_dist(training_field_lmdb, num_labels)
    #save to file
    np.save('./training_label_distribution', label_dist)
    np.save('./training_label_confusion_mat', conf_matrix)
