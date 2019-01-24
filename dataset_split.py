import numpy as np
from sklearn.model_selection import train_test_split
import numpy.lib.recfunctions as rf
from sklearn import utils
import random
from imblearn.over_sampling import SMOTE


def preparation_for_splitting (output_nfs_rec_array, output_ffs, output_ffs_rec_array):
    
    fault_free_labels = np.zeros(len(output_nfs_rec_array), dtype = int)
    final_data_set = rf.append_fields(output_nfs_rec_array, ['label'], data=[fault_free_labels], usemask=False)
    i = 1
    for fault_data_set in output_ffs.columns:
        labels = np.array([i]).repeat(len(output_ffs_rec_array))
        fault_data_set = rf.append_fields(output_ffs_rec_array, ['label'], data = [labels], usemask=False)
        final_data_set = np.concatenate([final_data_set, fault_data_set])
        i += 1

    np.random.shuffle(final_data_set)
     
    return final_data_set

def split (final_data_set, balanced_type):
    
    y = final_data_set['label']
    y = np.where(y!=0, 30, y)          
    X = rf.drop_fields(final_data_set, ['label'], False).view(np.float64).reshape(len(final_data_set),
                       len(final_data_set.dtype) - 1)
    
    # Partition into training and testing dataset with 80/20 ratio
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    X_train, y_train = utils.shuffle(X_train, y_train)
    
    if balanced_type == 'undersample':
        #all faults
        X_train_fault_bal = X_train[np.where(y_train != 0)]
        y_train_fault_bal = y_train[np.where(y_train != 0)]
        #no faults
        X_train_nf_bal = X_train[np.where(y_train == 0)][0:len(X_train_fault_bal)]
        y_train_nf_bal = y_train[np.where(y_train == 0)][0:len(X_train_fault_bal)]
             
        X_train_bal = np.concatenate([X_train_fault_bal, X_train_nf_bal])
        y_train_bal = np.concatenate([y_train_fault_bal, y_train_nf_bal])
        
        X_train, y_train = utils.shuffle(X_train_bal, y_train_bal)

    if balanced_type == 'oversample':
              
        sm = SMOTE (random_state = 12)
        X_train, y_train = sm.fit_sample (X_train, y_train)
       
        X_train, y_train = utils.shuffle(X_train, y_train)
        
    return X_train, y_train, X_test, y_test