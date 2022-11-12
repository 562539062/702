def datacheck():
    #Sig 
    for i in O_Nright:
        if np.sum(np.abs(p_Sig[i]-val_data['Sig']['Sig'][i][0].squeeze()))>0.001:
            print('error')
    #len
    print('Len:',np.sum(np.abs((O_Len-val_data['Len']['Len'].squeeze()))))
    
    #Nright 
    val = np.array(list((val_data['Nright']['Nright'].squeeze()-1)))
    print('Nright:',set(val)-set(O_Nright))
            
    #DSigraw-Segment3
    # print(np.sum(np.abs((DSig-val_data['DSig_raw']['DSig']))))
    
    ##DDSig
    print('DDSig:',np.sum(np.abs((DDSig-val_data['DDSig']['DDSig']))))
    
    

    #foreDSig-Segment3 #略微误差 round和浮点数导致 
    print('DSig_before:',np.sum(np.abs((DSig_before-np.round(val_data['DSig_before']['DSig'],12)))))
    
    
    #afterDSig-Segment3 #略微误差 round和浮点数、foreDSig导致
    print('DSig_after',np.sum(np.abs((DSig-val_data['DSig_after']['DSig']))))
    
    
    #temp #略微误差 round和浮点数、foreDSig导致
    print('temp:',np.sum(np.abs((temp-val_data['temp']['temp']))))
    
    #'Z21' 'Z22'
    print('Z21:',np.sum(np.abs((Z21-np.array(val_data['Z21']['Z21']).reshape(-1)))))
    print('Z22:',np.sum(np.abs((Z22-np.array(val_data['Z22']['Z22']).reshape(-1)))))

    #'resultZ' #略微误差
    print('resultZ:',np.sum(np.abs((resultZ-np.array(val_data['resultZ']['resultZ'])))))

    #'resultD' #略微误差
    print('resultD:',np.sum(np.abs((resultD-np.array(val_data['resultD']['resultD']).reshape(-1)))))

    #'resultS' #略微误差
    print('resultS:',np.sum(np.abs((resultS-np.array(val_data['resultS']['resultS']).reshape(-1)))))

    #'resultA' #略微误差
    print('resultA:',np.sum(np.abs((resultA-np.array(val_data['resultA']['resultA']).reshape(-1)))))


    'Result_Sample'
    for i in range(170):
        print('Result_Sample:',np.sum(np.abs((Result_Sample[i]-np.array(val_data['Result_Sample']['Result_Sample'][0][i])))))
        err = np.sum(np.abs(np.round(Result_Sample[i],9)-np.round(val_data['Result_Sample']['Result_Sample'][0][i],9)))
        if err>1:
            print(err,i) 