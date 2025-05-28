import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


from dbdicom.extensions import vreg


import nibabel as nib


def kidney_masks_as_dicom(folder):

    folder.message('Exporting whole kidney masks as dicom..')
    results_path = os.path.join(folder.path() + '_output', 'masks')
    if not os.path.exists(results_path):
        os.mkdir(results_path)

    fat_desc = 'Dixon_post_contrast_fat_' 
    out_desc = 'Dixon_post_contrast_out_phase'
    in_desc = 'Dixon_post_contrast_in_phase'
    water_desc = 'Dixon_post_contrast_water'
    k_means1_desc = 'KMeans cluster 1'
    k_means2_desc = 'KMeans cluster 2'
    lk_mask = 'LK' 
    rk_mask = 'RK'

    fat = folder.series(SeriesDescription=fat_desc)
    out_ph = folder.series(SeriesDescription=out_desc)
    in_ph = folder.series(SeriesDescription=in_desc)
    water = folder.series(SeriesDescription=water_desc)
    k_means1 = folder.series(SeriesDescription=k_means1_desc)
    k_means2 = folder.series(SeriesDescription=k_means2_desc)
    LK = folder.series(SeriesDescription=lk_mask)
    RK = folder.series(SeriesDescription=rk_mask)

    export_to_folder = LK + RK + fat + out_ph + in_ph + water + k_means1 + k_means2
    
    for series in export_to_folder:
        series.export_as_dicom(results_path)

def kidney_masks_as_dicom_folder_1(folder):

    folder.message('Exporting whole kidney masks as dicom..')
    results_path = os.path.join(folder.path() + '_output',folder.PatientName)
    if not os.path.exists(results_path):
        os.mkdir(results_path)

    fat_desc = 'Dixon_post_contrast_fat' 
    out_desc = 'Dixon_post_contrast_out_phase'
    in_desc = 'Dixon_post_contrast_in_phase'
    water_desc = 'Dixon_post_contrast_water'
    k_means1_desc = 'KMeans cluster 1'
    k_means2_desc = 'KMeans cluster 2'
    lk_mask = 'LK' 
    rk_mask = 'RK'

    fat = folder.series(SeriesDescription=fat_desc)
    out_ph = folder.series(SeriesDescription=out_desc)
    in_ph = folder.series(SeriesDescription=in_desc)
    water = folder.series(SeriesDescription=water_desc)
    k_means1 = folder.series(SeriesDescription=k_means1_desc)
    k_means2 = folder.series(SeriesDescription=k_means2_desc)
    LK = folder.series(SeriesDescription=lk_mask)
    RK = folder.series(SeriesDescription=rk_mask)

    export_to_folder = LK + RK + fat + out_ph + in_ph + water + k_means1 + k_means2
    
    for series in export_to_folder:
        series.export_as_dicom(results_path)

def kidney_masks_as_png_folder_1(database,backgroud_series = 'Dixon_post_contrast_out_phase',RK_mask = 'RK', LK_mask = 'LK', mask_name = 'Masks' ):
#def kidney_masks_as_png(database,backgroud_series = 'Dixon_out_phase',RK_mask = 'RK', LK_mask = 'LK' ): #ONLY FOR REPEATABILITY STUDY

    database.message('Exporting masks as png..')
    results_path = os.path.join(database.path() + '_output')
    if not os.path.exists(results_path):
        os.mkdir(results_path)

    series_img = database.series(SeriesDescription=backgroud_series)
    series_mask_LK = database.series(SeriesDescription=LK_mask)
    series_mask_RK = database.series(SeriesDescription=RK_mask)

    overlay_mask_LK  = vreg.map_to(series_mask_LK[0],series_img[0])
    overlay_mask_RK  = vreg.map_to(series_mask_RK[0],series_img[0])

    array_series_img, _ = series_img[0].array(['SliceLocation','AcquisitionTime'], pixels_first=True)
    array_overlay_mask_LK , _  = overlay_mask_LK.array(['SliceLocation','AcquisitionTime'], pixels_first=True)
    array_overlay_mask_RK , _  = overlay_mask_RK.array(['SliceLocation','AcquisitionTime'], pixels_first=True)

    #overlay_mask_LK.remove()
    #overlay_mask_RK.remove()

    array_series_img = np.squeeze(array_series_img)
    array_overlay_mask_LK = np.squeeze(array_overlay_mask_LK)
    array_overlay_mask_RK = np.squeeze(array_overlay_mask_RK)

    array_series_img = array_series_img.transpose((1,0,2))
    array_overlay_mask_LK = array_overlay_mask_LK.transpose((1,0,2))
    array_overlay_mask_RK = array_overlay_mask_RK.transpose((1,0,2))

    #array_overlay_mask = array_overlay_mask_LK + array_overlay_mask_RK
    array_overlay_mask_LK[array_overlay_mask_LK >0.5] = 1
    array_overlay_mask_LK[array_overlay_mask_LK <0.5] = np.nan

    array_overlay_mask_RK[array_overlay_mask_RK >0.5] = 1
    array_overlay_mask_RK[array_overlay_mask_RK <0.5] = np.nan
    


    num_row_cols = int(np.ceil (np.sqrt(array_overlay_mask_LK.shape[2])))

    fig, ax = plt.subplots(nrows=num_row_cols, ncols=num_row_cols,gridspec_kw = {'wspace':0, 'hspace':0},figsize=(num_row_cols,num_row_cols))
    i=0
    for row in ax:
        for col in row:
            if i>=array_overlay_mask_LK.shape[2]:
                col.set_xticklabels([])
                col.set_yticklabels([])
                col.set_aspect('equal')
                col.axis("off")
            else:  
            
                # Display the background image
                col.imshow(array_series_img[:,:,i], cmap='gray', interpolation='none', vmin=0, vmax=np.mean(array_series_img) + 2 * np.std(array_series_img))
            
                # Overlay the mask with transparency
                col.imshow(array_overlay_mask_LK[:,:,i], cmap='autumn', interpolation='none', alpha=0.5)
                col.imshow(array_overlay_mask_RK[:,:,i], cmap='summer', interpolation='none', alpha=0.5)

                col.set_xticklabels([])
                col.set_yticklabels([])
                col.set_aspect('equal')
                col.axis("off")
            i = i +1 


    
    fig.suptitle(mask_name, fontsize=14)
    fig.savefig(os.path.join(results_path, database.PatientName +'.png'), dpi=600)

#def kidney_masks_as_png(database,backgroud_series = 'Dixon_post_contrast_out_phase',RK_mask = 'RK', LK_mask = 'LK', mask_name = 'Masks' ):
def kidney_masks_as_png(database,backgroud_series = 'Dixon_out_phase',RK_mask = 'RK', LK_mask = 'LK',mask_name = 'Masks' ): #ONLY FOR REPEATABILITY STUDY

    database.message('Exporting masks as png..')
    results_path = database.path() + '_output'
    if not os.path.exists(results_path):
        os.mkdir(results_path)

    series_img = database.series(SeriesDescription=backgroud_series)
    series_mask_LK = database.series(SeriesDescription=LK_mask)
    series_mask_RK = database.series(SeriesDescription=RK_mask)

    overlay_mask_LK  = vreg.map_to(series_mask_LK[0],series_img[0])
    overlay_mask_RK  = vreg.map_to(series_mask_RK[0],series_img[0])

    array_series_img, _ = series_img[0].array(['SliceLocation','AcquisitionTime'], pixels_first=True)
    array_overlay_mask_LK , _  = overlay_mask_LK.array(['SliceLocation','AcquisitionTime'], pixels_first=True)
    array_overlay_mask_RK , _  = overlay_mask_RK.array(['SliceLocation','AcquisitionTime'], pixels_first=True)

    #overlay_mask_LK.remove()
    #overlay_mask_RK.remove()

    array_series_img = np.squeeze(array_series_img)
    array_overlay_mask_LK = np.squeeze(array_overlay_mask_LK)
    array_overlay_mask_RK = np.squeeze(array_overlay_mask_RK)

    array_series_img = array_series_img.transpose((1,0,2))
    array_overlay_mask_LK = array_overlay_mask_LK.transpose((1,0,2))
    array_overlay_mask_RK = array_overlay_mask_RK.transpose((1,0,2))

    array_overlay_mask = array_overlay_mask_LK + array_overlay_mask_RK
    array_overlay_mask[array_overlay_mask >0.5] = 1
    array_overlay_mask[array_overlay_mask <0.5] = np.nan
    


    num_row_cols = int(np.ceil (np.sqrt(array_overlay_mask.shape[2])))

    fig, ax = plt.subplots(nrows=num_row_cols, ncols=num_row_cols,gridspec_kw = {'wspace':0, 'hspace':0},figsize=(num_row_cols,num_row_cols))
    i=0
    for row in ax:
        for col in row:
            if i>=array_overlay_mask.shape[2]:
                col.set_xticklabels([])
                col.set_yticklabels([])
                col.set_aspect('equal')
                col.axis("off")
            else:  
            
                # Display the background image
                col.imshow(array_series_img[:,:,i], cmap='gray', interpolation='none', vmin=0, vmax=np.mean(array_series_img) + 2 * np.std(array_series_img))
            
                # Overlay the mask with transparency
                col.imshow(array_overlay_mask[:,:,i], cmap='autumn', interpolation='none', alpha=0.5)

                col.set_xticklabels([])
                col.set_yticklabels([])
                col.set_aspect('equal')
                col.axis("off")
            i = i +1 


    
    fig.suptitle(mask_name, fontsize=14)
    fig.savefig(os.path.join(results_path, mask_name + '.png'), dpi=600)


def pre_Dixon_to_AI(folder, subject_ID):

    folder.message('Exporting kidney masks as nifti')
    #results_path = os.path.join(folder.path() + '_output', 'to_AI')
    results_path = "//mnt//fastdata//md1jdsp//nnUNet_training_data//Pre_Dixon_to_AI"
    if not os.path.exists(results_path):
        os.mkdir(results_path)

    fat_desc = 'Dixon_fat [coreg]' 
    out_desc = 'Dixon_out_phase [coreg]'
    in_desc = 'Dixon_in_phase [coreg]'
    water_desc = 'Dixon_water [coreg]'
 
    lk_mask = 'LK' 
    rk_mask = 'RK'

    fat = folder.series(SeriesDescription=fat_desc)
    out_ph = folder.series(SeriesDescription=out_desc)
    in_ph = folder.series(SeriesDescription=in_desc)
    water = folder.series(SeriesDescription=water_desc)
    LK = folder.series(SeriesDescription=lk_mask)
    RK = folder.series(SeriesDescription=rk_mask)

    overlay_mask_LK  = vreg.map_to(LK[0],out_ph[0])
    overlay_mask_RK  = vreg.map_to(RK[0],out_ph[0])

    array_fat, _    = fat[0].array(['SliceLocation'], pixels_first=True, first_volume=True)
    array_out_ph, _ = out_ph[0].array(['SliceLocation'], pixels_first=True, first_volume=True)
    array_in_ph, _  = in_ph[0].array(['SliceLocation'], pixels_first=True, first_volume=True)
    array_water, _  = water[0].array(['SliceLocation'], pixels_first=True, first_volume=True)
    array_RK, _  = overlay_mask_RK.array(['SliceLocation'], pixels_first=True, first_volume=True)
    array_LK, _  = overlay_mask_LK.array(['SliceLocation'], pixels_first=True, first_volume=True)

    array_RK[array_RK >0.5] = 1
    array_RK[array_RK <0.5] = 0
    array_LK[array_LK >0.5] = 1
    array_LK[array_LK <0.5] = 0

    array_LK = array_LK * 2
    final_mask = array_RK + array_LK

    affine = np.eye(4)
    nii_final_mask = nib.Nifti1Image(final_mask, affine)
    nib.save(nii_final_mask, os.path.join(results_path, 'Dixon_'+ subject_ID + '.nii.gz'))

    nii_out_ph = nib.Nifti1Image(array_out_ph, affine)
    nib.save(nii_out_ph, os.path.join(results_path, 'Dixon_'+ subject_ID + '_0000.nii.gz'))

    nii_in_ph = nib.Nifti1Image(array_in_ph, affine)
    nib.save(nii_in_ph, os.path.join(results_path, 'Dixon_'+ subject_ID + '_0001.nii.gz'))

    nii_water = nib.Nifti1Image(array_water, affine)
    nib.save(nii_water, os.path.join(results_path, 'Dixon_'+ subject_ID + '_0002.nii.gz'))

    nii_fat = nib.Nifti1Image(array_fat, affine)
    nib.save(nii_fat, os.path.join(results_path, 'Dixon_'+ subject_ID + '_0003.nii.gz'))


def pre_Dixon_in_out_to_AI(folder, subject_ID):

    folder.message('Exporting kidney masks as nifti')
    results_path = os.path.join(folder.path() + '_output', 'to_AI')
    #results_path = "//mnt//fastdata//md1jdsp//nnUNet_training_data//Pre_Dixon_in_out_to_AI"
    if not os.path.exists(results_path):
        os.mkdir(results_path)

    out_desc = 'Dixon_out_phase [coreg]'
    in_desc = 'Dixon_in_phase [coreg]'
 
    lk_mask = 'LK' 
    rk_mask = 'RK'

    out_ph = folder.series(SeriesDescription=out_desc)
    in_ph = folder.series(SeriesDescription=in_desc)
    water_dominant = 'Dixon_water_dominant_map'

    out_ph = folder.series(SeriesDescription=out_desc)
    in_ph = folder.series(SeriesDescription=in_desc)
    fat_dom = folder.series(SeriesDescription=water_dominant)

    array_out_ph, _ = out_ph[0].array(['SliceLocation'], pixels_first=True, first_volume=True)
    array_in_ph, _  = in_ph[0].array(['SliceLocation'], pixels_first=True, first_volume=True)
    array_fat_dom, _  = fat_dom[0].array(['SliceLocation'], pixels_first=True, first_volume=True)


    array_fat_dom[array_fat_dom >0.5] = 1
    array_fat_dom[array_fat_dom <0.5] = 0

    affine = np.eye(4)
    nii_final_mask = nib.Nifti1Image(array_fat_dom, affine)
    nib.save(nii_final_mask, os.path.join(results_path, 'Dixon_'+ subject_ID + '.nii.gz'))

    nii_out_ph = nib.Nifti1Image(array_out_ph, affine)
    nib.save(nii_out_ph, os.path.join(results_path, 'Dixon_'+ subject_ID + '_0000.nii.gz'))

    nii_in_ph = nib.Nifti1Image(array_in_ph, affine)
    nib.save(nii_in_ph, os.path.join(results_path, 'Dixon_'+ subject_ID + '_0001.nii.gz'))

def post_contrast_Dixon_to_AI(folder, subject_ID):

    folder.message('Exporting kidney masks as nifti')
    results_path = os.path.join(folder.path() + '_output', 'to_AI')
    #results_path = "//mnt//fastdata//md1jdsp//nnUNet_training_data//Post_Dixon_to_AI"
    if not os.path.exists(results_path):
        os.mkdir(results_path)

    fat_desc = 'Dixon_post_contrast_fat' 
    out_desc = 'Dixon_post_contrast_out_phase'
    in_desc = 'Dixon_post_contrast_in_phase'
    water_desc = 'Dixon_post_contrast_water'
 
    lk_mask = 'LK' 
    rk_mask = 'RK'

    fat = folder.series(SeriesDescription=fat_desc)
    out_ph = folder.series(SeriesDescription=out_desc)
    in_ph = folder.series(SeriesDescription=in_desc)
    water = folder.series(SeriesDescription=water_desc)
    LK = folder.series(SeriesDescription=lk_mask)
    RK = folder.series(SeriesDescription=rk_mask)

    overlay_mask_LK  = vreg.map_to(LK[0],out_ph[0])
    overlay_mask_RK  = vreg.map_to(RK[0],out_ph[0])

    array_fat, _    = fat[0].array(['SliceLocation'], pixels_first=True, first_volume=True)
    array_out_ph, _ = out_ph[0].array(['SliceLocation'], pixels_first=True, first_volume=True)
    array_in_ph, _  = in_ph[0].array(['SliceLocation'], pixels_first=True, first_volume=True)
    array_water, _  = water[0].array(['SliceLocation'], pixels_first=True, first_volume=True)
    array_RK, _  = overlay_mask_RK.array(['SliceLocation'], pixels_first=True, first_volume=True)
    array_LK, _  = overlay_mask_LK.array(['SliceLocation'], pixels_first=True, first_volume=True)

    array_RK[array_RK >0.5] = 1
    array_RK[array_RK <0.5] = 0
    array_LK[array_LK >0.5] = 1
    array_LK[array_LK <0.5] = 0

    array_LK = array_LK * 2
    final_mask = array_RK + array_LK

    affine = np.eye(4)
    nii_final_mask = nib.Nifti1Image(final_mask, affine)
    nib.save(nii_final_mask, os.path.join(results_path, 'Dixon_'+ subject_ID + '.nii.gz'))

    nii_out_ph = nib.Nifti1Image(array_out_ph, affine)
    nib.save(nii_out_ph, os.path.join(results_path, 'Dixon_'+ subject_ID + '_0000.nii.gz'))

    nii_in_ph = nib.Nifti1Image(array_in_ph, affine)
    nib.save(nii_in_ph, os.path.join(results_path, 'Dixon_'+ subject_ID + '_0001.nii.gz'))

    nii_water = nib.Nifti1Image(array_water, affine)
    nib.save(nii_water, os.path.join(results_path, 'Dixon_'+ subject_ID + '_0002.nii.gz'))

    nii_fat = nib.Nifti1Image(array_fat, affine)
    nib.save(nii_fat, os.path.join(results_path, 'Dixon_'+ subject_ID + '_0003.nii.gz'))



def post_contrast_in_out_Dixon_to_AI(folder, subject_ID='000'):

    folder.message('Exporting kidney masks as nifti')
    results_path = folder.path()
    #results_path = "//mnt//fastdata//md1jdsp//nnUNet_training_data//Post_Dixon_in_out_to_AI"
    subject_ID='000'
    if not os.path.exists(results_path):
        os.mkdir(results_path)

    out_desc = 'Dixon_post_contrast_out_phase'
    in_desc = 'Dixon_post_contrast_in_phase'
    fat_dominant = 'Dixon_post_contrast_fat_dominant_map'

    fat_calculated = 'Dixon_post_contrast_fat_calculated'
    water_calculated = 'Dixon_post_contrast_water_calculated'

    out_ph = folder.series(SeriesDescription=out_desc)
    in_ph = folder.series(SeriesDescription=in_desc)
    fat_dom = folder.series(SeriesDescription=fat_dominant)

    water_cal = folder.series(SeriesDescription=water_calculated)
    fat_calc = folder.series(SeriesDescription=fat_calculated)


    array_out_ph, _ = out_ph[0].array(['SliceLocation'], pixels_first=True, first_volume=True)
    array_in_ph, _  = in_ph[0].array(['SliceLocation'], pixels_first=True, first_volume=True)
    array_fat_dom, _  = fat_dom[0].array(['SliceLocation'], pixels_first=True, first_volume=True)

    array_water, _  = water_cal[0].array(['SliceLocation'], pixels_first=True, first_volume=True)
    array_fat, _   = fat_calc[0].array(['SliceLocation'], pixels_first=True, first_volume=True)


    array_fat_dom[array_fat_dom >0.5] = 1
    array_fat_dom[array_fat_dom <0.5] = 0

    affine = np.eye(4)
    nii_final_mask = nib.Nifti1Image(array_fat_dom, affine)
    nib.save(nii_final_mask, os.path.join(results_path, 'Dixon_'+ subject_ID + '.nii.gz'))

    nii_out_ph = nib.Nifti1Image(array_out_ph, affine)
    nib.save(nii_out_ph, os.path.join(results_path, 'Dixon_'+ subject_ID + '_0000.nii.gz'))

    nii_in_ph = nib.Nifti1Image(array_in_ph, affine)
    nib.save(nii_in_ph, os.path.join(results_path, 'Dixon_'+ subject_ID + '_0001.nii.gz'))

    nii_fat = nib.Nifti1Image(array_fat, affine)
    nib.save(nii_fat, os.path.join(results_path, 'Dixon_'+ subject_ID + '_fat.nii.gz'))

    nii_water = nib.Nifti1Image(array_water, affine)
    nib.save(nii_water, os.path.join(results_path, 'Dixon_'+ subject_ID + '_water.nii.gz'))
