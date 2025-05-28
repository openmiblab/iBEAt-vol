import pandas as pd
import os
import pydmr



def convert_to_dmr(path, file):
    df = pd.read_csv(os.path.join(path, file + '.csv'))

    df['SeriesDescription'] = df['SeriesDescription'].str.replace('LK_ed', 'LK')
    df['SeriesDescription'] = df['SeriesDescription'].str.replace('RK_ed', 'RK')
    df['PatientID'] = file

    pars = {}
    data = {}
    columns = ['category', 'ROI']
    rois = {
        'LK': 'Left kidney',
        'RK': 'Right kidney',
        'BK': 'Both kidneys',
    }
    for index, row in df.iterrows():
        if 'baseline' in row.PatientID:
            subject = row.PatientID.replace('_baseline', '')
            study = 'baseline'
        elif 'followup' in row.PatientID:
            subject = row.PatientID.replace('_followup', '')
            study = 'followup'
        else:
            subject = row.PatientID
            study = 'baseline'
        pars[subject, study, row.Biomarker] = row.Value

        data[row.Biomarker] = [
            row.Biomarker, 
            row.Unit, 
            'float', 
            row.StudyDescription, 
            rois[row.SeriesDescription],
        ]

    dmr = {
        'data': data,
        'pars': pars,
        'columns': columns,
    }
    pydmr.write(os.path.join(path, file + '.dmr'), dmr)



if __name__=='__main__':
    path = os.path.join("C:\\Users\\md1jdsp\\Downloads\\Volumetry_3_csvBiomarkers")
    # file = 'combined'
    # convert_to_dmr(path, file)

    for filename in os.listdir(path):
        if filename.endswith(".csv"):
            file_name_without_ext = os.path.splitext(filename)[0]
            convert_to_dmr(path, file_name_without_ext)

    file_list = []
    for filename in os.listdir(path):
        if filename.endswith(".dmr.zip"):
            file_list.append(filename)

    pydmr.concat(file_list, os.path.jpoin(path, 'master'), cleanup=False)

