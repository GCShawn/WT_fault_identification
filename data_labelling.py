import pandas as pd
import numpy as np
import datetime


def data_labels (scada_data, status_data_rtu, status_data_wec, warning_data_rtu, warning_data_wec,  filter_type):

    if filter_type == 'no faults':
        corr_time_wec_s=status_data_wec.loc[(status_data_wec['Full Status']=='2 : 1')|
        (status_data_wec['Full Status']=='0 : 0')|(status_data_wec['Full Status']=='3 : 12'),
        'Time'] 
        
        selected_wec_status_indices = np.where ((status_data_wec['Full Status']=='2 : 1')|(status_data_wec['Full Status']=='3 : 12')|
        (status_data_wec['Full Status']=='0 : 0')) 
        selected_wec_status_indices = selected_wec_status_indices[0]
        
        # Convert datatimes to strings
        time_scada = scada_data ['Time']
        t_scada = []
        t_wec_s = []
        for i in range(0,len(time_scada)):
            t_scada.append(datetime.datetime.strptime(time_scada[i], "%d/%m/%Y %H:%M:%S")) #saves every iteration

        t_wec_s = [datetime.datetime.strptime(x, "%d/%m/%Y %H:%M:%S") for x in corr_time_wec_s]

        # Operational data w/ timestamps that corresponds to the at least 30 minutes after these statuses came into effect
        # and 120 before they changed were chosen
        op_data_tmstmps_1 = []
        for i in range (len(t_scada)):
            for j in range (len(t_wec_s)):
                if (t_scada[i] >= t_wec_s[j] - datetime.timedelta(seconds=7200 )) & (t_scada[i] < t_wec_s[j] + datetime.timedelta(seconds=1800)):
                    op_data_tmstmps_1.append(t_scada[i])


        # All operational data corresponding to RTU statuses where power output was being curtailed were filtered out. That leaves only
        corr_time_rtu_s=status_data_rtu.loc[(status_data_rtu['Full Status']=='0 : 0'), 'Time']
        #indices
        selected_rtu_status_indices = np.where(status_data_rtu['Full Status']=='0 : 0') # if I put comma, I get true/false. if I put | I get values but in tuple format
        selected_rtu_status_indices = selected_rtu_status_indices[0]
        # Convert datatimes to strings
        t_rtu_s = []
        t_rtu_s = [datetime.datetime.strptime(x, "%d/%m/%Y %H:%M:%S") for x in corr_time_rtu_s]

        op_data_tmstmps_2 = []
        for i in range (len(t_scada)):
            for j in range (len(t_rtu_s)):
                if (t_scada[i] >= t_rtu_s[j] - datetime.timedelta(seconds=600)) & (t_scada[i] < t_rtu_s[j] + datetime.timedelta(seconds=600)): # Corresponds to the paper
                    op_data_tmstmps_2.append(t_scada[i])

        # Times corresponding to a single specific warning message (230 - Power Limitation) filtered out.
        corr_time_except_single_warning = warning_data_wec.loc[(warning_data_wec['Main Warning']!=230), 'Time']
        t_wec_w = []
        t_wec_w = [datetime.datetime.strptime(x, "%d/%m/%Y %H:%M:%S") for x in corr_time_except_single_warning]

        op_data_tmstmps_3 = []
        for i in range (len(t_scada)):
            for j in range (len(t_wec_w)):
                if (t_scada[i] >= t_wec_w[j] - datetime.timedelta(seconds=600)) & (t_scada[i] < t_wec_w[j] + datetime.timedelta(seconds=600)): # Corresponds to the paper
                    op_data_tmstmps_3.append(t_scada[i])

        combined_timestamps =  sorted(op_data_tmstmps_1 + op_data_tmstmps_2 + op_data_tmstmps_3)

        nofault_dataset = pd.DataFrame(columns = scada_data.columns)
        for i in range (len(scada_data)):
            for j in range (len(combined_timestamps)):
                if t_scada[i] == combined_timestamps[j]:
                    nofault_dataset = nofault_dataset.append(scada_data.loc[i,:])

        return nofault_dataset
###############################################################################################################################################################
    if filter_type == 'all faults':
        af_corr_time_wec_s = status_data_wec.loc[(status_data_wec['Main Status']==62)|(status_data_wec['Main Status']==80)|
        (status_data_wec['Main Status']==228)|(status_data_wec['Main Status']==60)|(status_data_wec['Main Status']==9),
        'Time']

        time_scada = scada_data ['Time']
        t_scada = []
        for i in range(0,len(time_scada)):
            t_scada.append(datetime.datetime.strptime(time_scada[i], "%d/%m/%Y %H:%M:%S")) #saves every iteration
        af_time_wec_s = []
        af_time_wec_s = [datetime.datetime.strptime(x, "%d/%m/%Y %H:%M:%S") for x in af_corr_time_wec_s]

        af_op_data_tmstmp = []
        for i in range(len(t_scada)):
            for j in range(len(af_time_wec_s)):
                if (t_scada[i] >= af_time_wec_s[j] - datetime.timedelta(seconds=600)) & (t_scada[i] < af_time_wec_s[j] + datetime.timedelta(seconds = 600)):
                    af_op_data_tmstmp.append(t_scada[i])


        allfault_dataset = pd.DataFrame(columns = scada_data.columns)
        for i in range (len(scada_data)):
            for j in range (len(af_op_data_tmstmp)):
                if t_scada[i] == af_op_data_tmstmp[j]:
                    allfault_dataset = allfault_dataset.append(scada_data.loc[i,:])

        return allfault_dataset
###############################################################################################################################################################
    if filter_type == 'fault 62': 
        sf_corr_time_wec_s_62 = status_data_wec.loc[(status_data_wec['Main Status']==62), 'Time']
        time_scada = scada_data ['Time']
        t_scada = []
        for i in range(0,len(time_scada)):
            t_scada.append(datetime.datetime.strptime(time_scada[i], "%d/%m/%Y %H:%M:%S")) #saves every iteration
        sf_time_wec_s_62 = []
        sf_time_wec_s_62 = [datetime.datetime.strptime(x, "%d/%m/%Y %H:%M:%S") for x in sf_corr_time_wec_s_62]

        sf_op_data_tmstmp_62 = []
        for i in range(len(t_scada)):
            for j in range(len(sf_time_wec_s_62)):
                if (t_scada[i] >= sf_time_wec_s_62[j] - datetime.timedelta(seconds=600)) & (t_scada[i] < sf_time_wec_s_62[j] + datetime.timedelta(seconds = 600)):
                    sf_op_data_tmstmp_62.append(t_scada[i])

        sf_62_dataset = pd.DataFrame(columns = scada_data.columns)
        for i in range(len(scada_data)):
            for j in range(len(sf_op_data_tmstmp_62)):
                if t_scada[i] == sf_op_data_tmstmp_62[j]:
                    sf_62_dataset = sf_62_dataset.append(scada_data.loc[i,:])
            
        return sf_62_dataset
    
###############################################################################################################################################################
    if filter_type == 'fault 80': 
        sf_corr_time_wec_s_80 = status_data_wec.loc[(status_data_wec['Main Status']==80), 'Time']
        time_scada = scada_data ['Time']
        t_scada = []
        for i in range(0,len(time_scada)):
            t_scada.append(datetime.datetime.strptime(time_scada[i], "%d/%m/%Y %H:%M:%S")) #saves every iteration
        sf_time_wec_s_80 = []
        sf_time_wec_s_80 = [datetime.datetime.strptime(x, "%d/%m/%Y %H:%M:%S") for x in sf_corr_time_wec_s_80]

        sf_op_data_tmstmp_80 = []
        for i in range(len(t_scada)):
            for j in range(len(sf_time_wec_s_80)):
                if (t_scada[i] >= sf_time_wec_s_80[j] - datetime.timedelta(seconds=600)) & (t_scada[i] < sf_time_wec_s_80[j] + datetime.timedelta(seconds = 600)):
                    sf_op_data_tmstmp_80.append(t_scada[i])  

        sf_80_dataset = pd.DataFrame(columns = scada_data.columns)
        for i in range(len(scada_data)):
            for j in range(len(sf_op_data_tmstmp_80)):
                if t_scada[i] == sf_op_data_tmstmp_80[j]:
                    sf_80_dataset = sf_80_dataset.append(scada_data.loc[i,:])
            
        return sf_80_dataset
###############################################################################################################################################################
    if filter_type == 'fault 228':            
        sf_corr_time_wec_s_228 = status_data_wec.loc[(status_data_wec['Main Status']==228), 'Time']
        time_scada = scada_data ['Time']
        t_scada = []
        for i in range(0,len(time_scada)):
            t_scada.append(datetime.datetime.strptime(time_scada[i], "%d/%m/%Y %H:%M:%S")) #saves every iteration
        sf_time_wec_s_228 = []
        sf_time_wec_s_228 = [datetime.datetime.strptime(x, "%d/%m/%Y %H:%M:%S") for x in sf_corr_time_wec_s_228]

        sf_op_data_tmstmp_228 = []
        for i in range(len(t_scada)):
            for j in range(len(sf_time_wec_s_228)):
                if (t_scada[i] >= sf_time_wec_s_228[j] - datetime.timedelta(seconds=600)) & (t_scada[i] < sf_time_wec_s_228[j] + datetime.timedelta(seconds = 600)):
                    sf_op_data_tmstmp_228.append(t_scada[i])

        sf_228_dataset = pd.DataFrame(columns = scada_data.columns)
        for i in range(len(scada_data)):
            for j in range(len(sf_op_data_tmstmp_228)):
                if t_scada[i] == sf_op_data_tmstmp_228[j]:
                    sf_228_dataset = sf_228_dataset.append(scada_data.loc[i,:])
                    
        return sf_228_dataset

###############################################################################################################################################################
    if filter_type == 'fault 60':            
        sf_corr_time_wec_s_60  = status_data_wec.loc[(status_data_wec['Main Status']==60), 'Time']
        time_scada = scada_data ['Time']
        t_scada = []
        for i in range(0,len(time_scada)):
            t_scada.append(datetime.datetime.strptime(time_scada[i], "%d/%m/%Y %H:%M:%S")) #saves every iteration
        sf_time_wec_s_60 = []
        sf_time_wec_s_60 = [datetime.datetime.strptime(x, "%d/%m/%Y %H:%M:%S") for x in sf_corr_time_wec_s_60]

        sf_op_data_tmstmp_60 = []
        for i in range(len(t_scada)):
            for j in range(len(sf_time_wec_s_60)):
                if (t_scada[i] >= sf_time_wec_s_60[j] - datetime.timedelta(seconds=600)) & (t_scada[i] < sf_time_wec_s_60[j] + datetime.timedelta(seconds = 600)):
                    sf_op_data_tmstmp_60.append(t_scada[i])                 

        sf_60_dataset = pd.DataFrame(columns = scada_data.columns)
        for i in range(len(scada_data)):
            for j in range(len(sf_op_data_tmstmp_60)):
                if t_scada[i] == sf_op_data_tmstmp_60[j]:
                    sf_60_dataset = sf_60_dataset.append(scada_data.loc[i,:])
        
        return sf_60_dataset

###############################################################################################################################################################
    if filter_type == 'fault 9':            
        sf_corr_time_wec_s_9 = status_data_wec.loc[(status_data_wec['Main Status']==9), 'Time']        
        time_scada = scada_data ['Time']
        t_scada = []
        for i in range(0,len(time_scada)):
            t_scada.append(datetime.datetime.strptime(time_scada[i], "%d/%m/%Y %H:%M:%S")) #saves every iteration
        sf_time_wec_s_9 = []
        sf_time_wec_s_9 = [datetime.datetime.strptime(x, "%d/%m/%Y %H:%M:%S") for x in sf_corr_time_wec_s_9]

        sf_op_data_tmstmp_9 = []
        for i in range(len(t_scada)):
            for j in range(len(sf_time_wec_s_9)):
                if (t_scada[i] >= sf_time_wec_s_9[j] - datetime.timedelta(seconds=600)) & (t_scada[i] < sf_time_wec_s_9[j] + datetime.timedelta(seconds = 600)):
                    sf_op_data_tmstmp_9.append(t_scada[i])  
            
        sf_9_dataset = pd.DataFrame(columns = scada_data.columns)
        for i in range(len(scada_data)):
            for j in range(len(sf_op_data_tmstmp_9)):
                if t_scada[i] == sf_op_data_tmstmp_9[j]:
                    sf_9_dataset = sf_9_dataset.append(scada_data.loc[i,:])
        
        return sf_9_dataset

       
        