# Wind Turbine Fault Identification using Machine Learning Techniques applied to SCADA data
Due to the unscheduled maintenance, wind farms can loss precious time and that results in the loss of revenue. To this end, it is imporant to perform maintenance before it becomes too late. By continiously monitoring, turbine health, it is possible to detect the faults and schedule maintenance as needed. In this project, SCADA data collected from the wind farm in Ireland is used to evaluate the turbine performance.
Fault and alarm data are filtered and analysed in conjunction with the power curve to identify periods of normal and faulty operation. Also, the specific fault is identified.
The data consists of: Operational data, Status data, Warning data.
## Description of Data
### Operational Data:
The turbine control system monitors many parameters such as wind speed and ambient temperature, power characteristics and others. The data is collected every 10 minutes and stored as _scada_data_. 
### Status Data:
Number of normal and abnormal (faulty) operation states are saved in two separate datasets: WEC Status data and RTU Status data. The WEC (Wind Energy Converter) status data corresponds to status message directly related to the turbine itself. RTU data corresponds to power control data at the point of connection to the grid, such as active and reactive power. Each status has a "main status" and "sub-status" code associated with it. Any main WEC status code above 0 indicates a faulty behaviour, however that does not mean that there is fault, e.g. status code 2 indicates "lack of wind". In RTU, statuses exclusive deal with active and reactive power set-points, e.g., status 100:82 corresponds to limiting the active power output to 82% of its actual current output.
### Warning Data:
This data corresponds to the general information about the turbine and are not directly related to the turbine operation or safety. Sometimes, warning messages correspond to a potentially developing fault on the turbine, as if the same warning message persists for a set amount of time and is not cleared soon, a fault might develop and a new status message is generated. 
## Description of .py Files
_main.py_ - Run this file. At certain point you will be asked to decide if we want to classify all-faults or a specific fault. The options are: _all faults, fault 62, fault 80, fault 228, fault 60, fault 9_

_data_labelling.py_ - labels datapoints as "all faults" or a specific fault

_feature_selection.py_ - as not all of the features in the SCADA dataset (63 features in total) are useful, 27 features are chosen based on the author's domain expertise. In addition, _'CS101 : Blade B temp.', 'CS101 : Blade C temp.', 'RTU: ava. Setpoint 1', 'CS101 : Sys 1 inverter 1 cabinet temp.', 'CS101 : Sys 1 inverter 2 cabinet temp.', 'CS101 : Sys 1 inverter 3 cabinet temp.', 'CS101 : Sys 1 inverter 4 cabinet temp.', 'CS101 : Sys 1 inverter 5 cabinet temp.', 'CS101 : Sys 1 inverter 6 cabinet temp.', 'CS101 : Sys 1 inverter 7 cabinet temp.', 'CS101 : Sys 2 inverter 1 cabinet temp.', 'CS101 : Sys 2 inverter 2 cabinet temp.',  'CS101 : Sys 2 inverter 3 cabinet temp.', 'CS101 : Sys 2 inverter 4 cabinet temp.', 'CS101 : Sys 2 inverter 5 cabinet temp.', 'CS101 : Sys 2 inverter 6 cabinet temp.', 'CS101 : Sys 2 inverter 7 cabinet temp.'_ are combined to get the inverter average and inverted standard deviation. In addition, here the dataset is normalized.

_dataset_split.py_ - The data is split into training and testing split with 80/20 ratio. The training data is balanced using undersampling technique.

_model.py_ - The model is trained using either SVM or Decision Tree algorithms
