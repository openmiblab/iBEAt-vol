import numpy as np
from dbdicom.extensions import sklearn
from dbdicom.pipelines import input_series
from models import UNETR_kidneys_v1, nnUnet_Dixon_v1
import utilities.zenodo_link as UNETR_zenodo
import utilities.zenodo_link_nnunet as nnunet_zenodo
import os
import shutil

export_study = '0: Segmentations'


def kidneys(database):

    # Get weights file and check if valid 
    # if not os.path.isfile(weights):
    #     msg = 'The weights file ' + weights + ' has not been found. \n'
    #     msg += 'Please check that the file with model weights is in the folder, and is named ' + UNETR_kidneys_v1.filename
    #     database.dialog.information(msg)
    #     return

    unetr, unetr_link= UNETR_zenodo.main()
    weights = os.path.join(os.path.dirname(database.path()),unetr)

    database.message('Segmenting kidneys. This could take a few minutes. Please be patient..')

    # Get appropriate series and check if valid
    #series = database.series(SeriesDescription=UNETR_kidneys_v1.trained_on)
    series, study = input_series(database, UNETR_kidneys_v1.trained_on,export_study)
    if series is None:
        msg = 'Cannot autosegment the kidneys: series ' + UNETR_kidneys_v1.trained_on + ' not found.'
        raise RuntimeError(msg)

    if database.PatientName [0:4] == '7128':
    # Loop over the series and create the mask
    #desc = sery.instance().SeriesDescription

        array_out  , header   = series[0].array(['SliceLocation'], pixels_first=True, first_volume=True)
        array_out = array_out[:, :, ::-1,...]
        array_in   , header_in    = series[1].array(['SliceLocation'], pixels_first=True, first_volume=True)
        array_in = array_in[:, :, ::-1,...]
        array_water, header_water = series[2].array(['SliceLocation'], pixels_first=True, first_volume=True)
        array_water = array_water[:, :, ::-1,...]
        array_fat  , header_fat   = series[3].array(['SliceLocation'], pixels_first=True, first_volume=True)
        array_fat = array_fat[:, :, ::-1,...]
        array = np.stack((array_out, array_in, array_water, array_fat), axis=0)
    
    else:

        array_out  , header   = series[0].array(['SliceLocation'], pixels_first=True, first_volume=True)
        array_in   , header_in    = series[1].array(['SliceLocation'], pixels_first=True, first_volume=True)
        array_water, header_water = series[2].array(['SliceLocation'], pixels_first=True, first_volume=True)
        array_fat  , header_fat   = series[3].array(['SliceLocation'], pixels_first=True, first_volume=True)
        array = np.stack((array_out, array_in, array_water, array_fat), axis=0)
    # Calculate predictions 
    masks = UNETR_kidneys_v1.apply(array, weights)
    left_kidney, right_kidney = UNETR_kidneys_v1.kidney_masks(masks)

    # Save UNETR output
    result = study.new_child(SeriesDescription = 'BK')
    result.set_array(masks, header, pixels_first=True)
    # result[['WindowCenter','WindowWidth']] = [1.0, 2.0]

    # Save and display left kidney data
    left = study.new_child(SeriesDescription = 'LK')
    left.set_array(left_kidney, header, pixels_first=True)
    # left[['WindowCenter','WindowWidth']] = [1.0, 2.0]
    
    # Save and display right kidney data
    right = study.new_child(SeriesDescription = 'RK')
    right.set_array(right_kidney, header, pixels_first=True)
    # right[['WindowCenter','WindowWidth']] = [1.0, 2.0]

    database.save()

    kidneys = []
    kidneys.append(left) 
    kidneys.append(right)

    return kidneys

def kidneys_nnunet(database): #ADAPT TO THE nnUet for 

    # Get weights file and check if valid 
    # if not os.path.isfile(weights):
    #     msg = 'The weights file ' + weights + ' has not been found. \n'
    #     msg += 'Please check that the file with model weights is in the folder, and is named ' + UNETR_kidneys_v1.filename
    #     database.dialog.information(msg)
    #     return

    #unetr, unetr_link= UNETR_zenodo.main()
    nnUnet, unetr_link= nnunet_zenodo.main()
    weights = os.path.join(database.path(), nnUnet)

    #copied_folder_path = shutil.copytree(os.path.join(os.path.dirname(database.path()),'Dataset001_Dixon'),os.path.join(database.path(),'Dataset001_Dixon'))
    #copied_folder_path = shutil.copytree(os.path.join(os.path.dirname(database.path()),'nnUNetTrainer__nnUNetPlans__3d_fullres'),os.path.join(database.path(),'nnUNetTrainer__nnUNetPlans__3d_fullres'))

    database.message('Segmenting kidneys. This could take a few minutes. Please be patient..')

    # Get appropriate series and check if valid
    #series = database.series(SeriesDescription=UNETR_kidneys_v1.trained_on)
    sery, study = input_series(database, nnUnet_Dixon_v1.trained_on,export_study)
    if sery is None:
        msg = 'Cannot autosegment the kidneys: series ' + nnUnet_Dixon_v1.trained_on + ' not found.'
        raise RuntimeError(msg)

    array_in,    _      = sery[0].array(['SliceLocation'], pixels_first=True, first_volume=True)
    array_out,   _      = sery[1].array(['SliceLocation'], pixels_first=True, first_volume=True)
    array_water, _      = sery[2].array(['SliceLocation'], pixels_first=True, first_volume=True)
    array_fat,   header = sery[3].array(['SliceLocation'], pixels_first=True, first_volume=True)

    if database.PatientName[0:4] == '7128':
        array_in_temp  = array_in[:, :, ::-1,...]
        array_in = array_in_temp
        array_out_temp = array_out[:, :, ::-1,...]
        array_out = array_out_temp
        array_water_temp = array_water[:, :, ::-1,...]
        array_water = array_water_temp
        array_fat_temp = array_fat[:, :, ::-1,...]
        array_fat = array_fat_temp

    array_to_predict = np.stack([array_in, array_out, array_water, array_fat], axis=0)

    # Calculate predictions 

    masks = nnUnet_Dixon_v1.apply(array_to_predict, weights)

    #shutil.rmtree(weights)
    shutil.rmtree(os.path.join(database.path(),'nnUNetTrainer__nnUNetPlans__3d_fullres'))

    rk, lk = nnUnet_Dixon_v1.kidney_masks(masks)

    if database.PatientName[0:4] == '7128':
        masks = masks[:, :, ::-1,...]
        rk    = rk[:, :, ::-1,...]
        lk    = lk[:, :, ::-1,...]

    # Save UNETR output
    
    result = study.new_child(SeriesDescription = 'BK')
    result.set_array(masks, header, pixels_first=True)
    # result[['WindowCenter','WindowWidth']] = [1.0, 2.0]
    
    rk_series = study.new_child(SeriesDescription = 'RK')
    rk_series .set_array(rk, header, pixels_first=True)
    # left[['WindowCenter','WindowWidth']] = [1.0, 2.0]
    
    lk_series = study.new_child(SeriesDescription = 'LK')
    lk_series.set_array(lk, header, pixels_first=True)
    # left[['WindowCenter','WindowWidth']] = [1.0, 2.0]

    database.save()



def compute_whole_kidney_canvas(database):
    series_desc = [
        'Dixon_post_contrast_fat',
        'Dixon_post_contrast_out_phase'
    ] 
    features, study = input_series(database, series_desc, export_study)
    if features is None:
        return
    clusters = sklearn.sequential_kmeans(features, n_clusters=2, multiple_series=True)
    for c in clusters:
        c.move_to(study)
    return clusters