""" 
@author: Joao Periquito 
iBEAt Rename Scrpit
2022
Pulse sequence name standardization for iBEAt MR Protcol
"""

import os

import pandas as pd

def check(database):

    results_path = database.path() + '_output'
    if not os.path.exists(results_path):
        os.mkdir(results_path)

    df = pd.DataFrame([
        ['T2w',0,''],
        ['Dixon_out_phase',0,''],           #TE
        ['Dixon_in_phase',0,''],            #TE
        ['Dixon_fat',0,''],
        ['Dixon_water',0,''],
        ['DCE',0,''],               # time resolution (difference between acqui time)
        ['Dixon_post_contrast_out_phase',0,''],
        ['Dixon_post_contrast_in_phase',0,''],
        ['Dixon_post_contrast_fat',0,''],
        ['Dixon_post_contrast_water',0,'']
        ], columns=['MRI Sequence','Checked','Notes'])

    list_of_series = database.series()
    list_of_series_description = []
    for series in (list_of_series):
        list_of_series_description.append(series['SeriesDescription'])
    
    # Loop through the rows and update the second column based on the condition
    dims = ['AcquisitionTime']
    for index, row in df.iterrows():
        if row['MRI Sequence'] in list_of_series_description:
            df.at[index, 'Checked'] = 1

            if row['MRI Sequence'] == 'Dixon_out_phase':
                series = database.series(SeriesDescription='Dixon_out_phase')
                if series[0]['EchoTime'] == 1.34:
                    continue
                else:
                    df.at[index, 'Notes'] = 'Echo time (1.34ms) = ' + str(series[0]['EchoTime'])
                    df.at[index, 'Checked'] = 2
            
            if row['MRI Sequence'] == 'Dixon_in_phase':
                series = database.series(SeriesDescription='Dixon_in_phase')
                if series[0]['EchoTime'] == 2.57:
                    continue
                else:
                    df.at[index, 'Notes'] = 'Echo time (2.57ms) = ' + str(series[0]['EchoTime'])
                    df.at[index, 'Checked'] = 2
     

    def color_rule(val):
        return ['background-color: red' if x == 0 else 'background-color: orange' if x == 2 else 'background-color: green' for x in val]

    iBEAt_column = df.style.apply(color_rule, axis=1, subset=['Checked'])
    iBEAt_column.to_excel(os.path.join(results_path,'iBEAt_checklist.xlsx'), engine='openpyxl', index=False)

    

def Philips_rename(series):
        
    SeqName = series["SeriesDescription"]
    
    if SeqName is None:
        return
    
    if SeqName == 'T1w_abdomen_dixon_cor_bh' or SeqName == 'T1W-abdomen-Dixon-post-coronal-BH':
        TE = series.EchoTime

        inphase = series.subseries(EchoTime=TE[0])
        inphase.SeriesDescription = 'Dixon_in_phase'

        outphase = series.subseries(EchoTime=TE[1])
        outphase.SeriesDescription = 'Dixon_out_phase'
        
        return 'Dixon'
    
    if SeqName == 'DCE_kidneys_cor-oblique_fb_wet_pulse':
        return 'DCE'
    
    if SeqName == 'T1w_abdomen_post_contrast_dixon_cor_bh':
        TE = series.EchoTime

        inphase = series.subseries(EchoTime=TE[1])
        inphase.SeriesDescription = 'Dixon_post_contrast_in_phase'

        outphase = series.subseries(EchoTime=TE[0])
        outphase.SeriesDescription = 'Dixon_post_contrast_out_phase'
        
        return 'Dixon_post_contrast'

            

def Siemens_rename(series): 
    """
    The sequence names in Leeds have been removed by the anonymisation
    procedure and must be recovered from other attributes
    """
    SeqName = series["SequenceName"]

    if SeqName == '*fl3d2':
        sequence = 'Dixon'
        imType = series["ImageType"]
        if imType[3] == 'OUT_PHASE' or imType[4] == 'OUT_PHASE': 
            return sequence + '_out_phase'
        if imType[3] == 'IN_PHASE'  or imType[4] == 'IN_PHASE': 
            return sequence + '_in_phase'
        if imType[3] == 'FAT'       or imType[4] == 'FAT': 
            return sequence + '_fat'
        if imType[3] == 'WATER'     or imType[4] == 'WATER': 
            return sequence + '_water'

    if SeqName == '*tfl2d1_16': 
        return 'DCE'
    
    if SeqName == '*fl3d2': 
        return 'Dixon'

def GE_rename(series): 
    """
    The sequence names in Leeds have been removed by the anonymisation
    procedure and must be recovered from other attributes
    """
    SeqName = series["SeriesDescription"]
    print(SeqName)

    if SeqName == 'InPhase: T1_abdomen_dixon_cor_bh':
        return 'Dixon_in_phase'
    if SeqName == 'OutPhase: T1_abdomen_dixon_cor_bh':
        return 'Dixon_out_phase'
    if SeqName == 'WATER: T1_abdomen_dixon_cor_bh':
        return 'Dixon_water'
    if SeqName == 'FAT: T1_abdomen_dixon_cor_bh':
        return 'Dixon_fat'
    if SeqName == 'InPhase: T1_abdomen_post_contrast_dixon_cor_bh':
        return 'Dixon_post_contrast_in_phase'
    if SeqName == 'OutPhase: T1_abdomen_post_contrast_dixon_cor_bh':
        return 'Dixon_post_contrast_out_phase'
    if SeqName == 'WATER: T1_abdomen_post_contrast_dixon_cor_bh':
        return 'Dixon_post_contrast_water'
    if SeqName == 'FAT: T1_abdomen_post_contrast_dixon_cor_bh':
        return 'Dixon_post_contrast_fat'

def all_series(folder):

    DCE_count = 0
    all_series = folder.series()
    Manufacturer = all_series[0]['Manufacturer']

    for i, series in enumerate(all_series):
        folder.progress(i+1, len(all_series), 'Renaming...')

        if Manufacturer == 'SIEMENS':
            imDescription = Siemens_rename(series)
            if imDescription is None:
                continue
            series.SeriesDescription = imDescription

            if imDescription == 'DCE':
                DCE_count = 1
            if DCE_count == 1 and imDescription[0:5] == 'Dixon':
                series.SeriesDescription = imDescription.split('_')[0] + '_post_contrast' + imDescription.split('Dixon')[-1]

        elif Manufacturer == 'Philips' or Manufacturer == 'Philips Medical Systems':
            imDescription = Philips_rename(series)
            if imDescription is None: 
                continue
            series.SeriesDescription = imDescription

        elif Manufacturer == 'GE MEDICAL SYSTEMS':
            imDescription = GE_rename(series)
            if imDescription is None:
                continue
            series.SeriesDescription = imDescription


