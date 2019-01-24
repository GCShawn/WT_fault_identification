import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix
# Custom functions: 
from data_labelling import data_labels #labelling data
from features_selection import feature_selection
from dataset_split import preparation_for_splitting, split
from model import model_train
##### Data Loading #####
scada_data = pd.read_csv('data/SCADA_data.csv')
status_data_rtu = pd.read_csv('data/status_data_rtu.csv')
status_data_wec = pd.read_csv('data/status_data_wec.csv')
warning_data_rtu = pd.read_csv('data/warning_data_rtu.csv')
warning_data_wec = pd.read_csv('data/warning_data_wec.csv')


##### Data Labelling #####
output_nf = pd.DataFrame (columns = scada_data.columns) #always keep nofault dataset
output_nf = data_labels(scada_data, status_data_rtu, status_data_wec, warning_data_rtu, warning_data_wec, 'no faults')

fault_input = input(" Enter the fault. Options are: all faults, fault 62, fault 80, fault 228, fault 60, fault 9: ")
output_faults = pd.DataFrame (columns = scada_data.columns) # this one will take either 
output_faults = data_labels(scada_data, status_data_rtu, status_data_wec, warning_data_rtu, warning_data_wec, fault_input)

##### Feature Selection #####
# We will normalize the dataset here as well
selected_features = ['WEC: ava. windspeed',
                    'WEC: ava. Rotation',
                    'WEC: ava. Power',
                    'WEC: ava. reactive Power',
                    'WEC: ava. blade angle A',
                    'CS101 : Spinner temp.', 
                    'CS101 : Front bearing temp.',  
                    'CS101 : Rear bearing temp.',  
                    'CS101 : Pitch cabinet blade A temp.',  
                    'CS101 : Pitch cabinet blade B temp.',  
                    'CS101 : Pitch cabinet blade C temp.',  
                    'CS101 : Rotor temp. 1',  
                    'CS101 : Rotor temp. 2',   
                    'CS101 : Stator temp. 1',  
                    'CS101 : Stator temp. 2',  
                    'CS101 : Nacelle ambient temp. 1',  
                    'CS101 : Nacelle ambient temp. 2',  
                    'CS101 : Nacelle temp.',  
                    'CS101 : Nacelle cabinet temp.',  
                    'CS101 : Main carrier temp.',  
                    'CS101 : Rectifier cabinet temp.',  
                    'CS101 : Yaw inverter cabinet temp.',  
                    'CS101 : Fan inverter cabinet temp.',  
                    'CS101 : Ambient temp.',  
                    'CS101 : Tower temp.',  
                    'CS101 : Control cabinet temp.',  
                    'CS101 : Transformer temp.' ]


output_nfs = feature_selection(scada_data, output_nf, selected_features) # features are selected in no fault dataset
output_ffs = feature_selection(scada_data, output_faults, selected_features) #features are selected in faulty dataset

##### Convert to record array #####
output_nfs_rec_array = output_nfs.to_records(index = False)
output_ffs_rec_array = output_ffs.to_records(index = False)

##### Prepartion for splitting #####
final_data_set = preparation_for_splitting (output_nfs_rec_array, output_ffs, output_ffs_rec_array)    
X_train, y_train, X_test, y_test = split (final_data_set, 'all faults', 'balanced')

##### Training a model #####
# First argument is string: Decision Tree or SVM
y_pred, best_param = model_train('SVM', X_train, y_train, X_test, y_test)
labels = ['no-fault','fault']
clfreport = classification_report(y_test, y_pred, target_names=labels)
cm = confusion_matrix(y_test, y_pred)