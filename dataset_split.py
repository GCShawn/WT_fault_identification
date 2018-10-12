import numpy as np
from sklearn.model_selection import train_test_split
import numpy.lib.recfunctions as rf
from sklearn import utils



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

def split (final_data_set, fault_type, balanced_type):
    
    y = final_data_set['label']
    # all-fault: 62, 80, 228, 60, 9 were combined under the common 30 fault code
    if fault_type == 'all faults':
        y = np.where((y==9)|(y==60)|(y==62)|(y==80)|(y==228),30,y) 
        y = np.where((y!=0)&(y!=30), 40, y) 
    
          
    X = rf.drop_fields(final_data_set, ['label'], False).view(np.float64).reshape(len(final_data_set),
                                    len(final_data_set.dtype) - 1)
    
    # Partition into training and testing dataset with 80/20 ratio
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    X_train, y_train = utils.shuffle(X_train, y_train)
    
    if balanced_type == 'balanced':
        #all faults
        X_train_fault_bal = X_train[np.where(y_train == 30)]
        y_train_fault_bal = y_train[np.where(y_train == 30)]
        #no faults
        X_train_nf_bal = X_train[np.where(y_train == 0)][0:len(X_train_fault_bal)]
        y_train_nf_bal = y_train[np.where(y_train == 0)][0:len(X_train_fault_bal)]
        #other faults
        X_train_other_bal = X_train[np.where(y_train == 40)][0:len(X_train_fault_bal)]
        y_train_other_bal = y_train[np.where(y_train == 40)][0:len(X_train_fault_bal)]
        
        X_train_bal = np.concatenate([X_train_fault_bal, X_train_nf_bal, X_train_other_bal])
        y_train_bal = np.concatenate([y_train_fault_bal, y_train_nf_bal,y_train_other_bal])
        
        X_train, y_train = utils.shuffle(X_train_bal, y_train_bal)
       
        
    return X_train, y_train, X_test, y_test