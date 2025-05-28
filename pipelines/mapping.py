import numpy as np

from dbdicom.pipelines import input_series

export_study = '2: Parameter maps'

def calculate_dixon_fat_water(folder):

    # Find source DICOM data
    series_Dixon_water_dom, study_Dixon_water_dom, desc_Dixon_water_dom = _map_input   (folder, "Dixon_post_contrast_water_dominant")
    series_Dixon_in_phase, study_Dixon_in_phase, desc_Dixon_in_phase    = _map_input   (folder, "Dixon_post_contrast_in_phase")
    series_Dixon_out_phase, study_Dixon_out_phase, desc_Dixon_out_phase = _map_input   (folder, "Dixon_post_contrast_out_phase")

    # Load data
    array_Dixon_water_dom, header_Dixon_water_dom = series_Dixon_water_dom.array('InstanceNumber', pixels_first=True)
    array_Dixon_in_phase, header_Dixon_in_phase   = series_Dixon_in_phase.array('InstanceNumber', pixels_first=True)
    array_Dixon_out_phase, header_Dixon_out_phase = series_Dixon_out_phase.array('InstanceNumber', pixels_first=True)

    array_water_calculated = np.zeros_like(array_Dixon_in_phase)  # Ensure same shape
    array_water_calculated = np.where(array_Dixon_water_dom == 1, array_Dixon_in_phase + array_Dixon_out_phase, array_water_calculated)
    array_water_calculated = np.where(array_Dixon_water_dom == 0, array_Dixon_in_phase - array_Dixon_out_phase, array_water_calculated)

    array_fat_calculated = np.zeros_like(array_Dixon_in_phase)  # Ensure same shape
    array_fat_calculated = np.where(array_Dixon_water_dom == 0, array_Dixon_in_phase + array_Dixon_out_phase, array_fat_calculated)
    array_fat_calculated = np.where(array_Dixon_water_dom == 1, array_Dixon_in_phase - array_Dixon_out_phase, array_fat_calculated)


    series = study_Dixon_in_phase.new_series(SeriesDescription="Dixon_post_contrast_water")
    series.set_array(array_water_calculated, header_Dixon_in_phase, pixels_first=True)

    series = study_Dixon_in_phase.new_series(SeriesDescription="Dixon_post_contrast_fat")
    series.set_array(array_fat_calculated, header_Dixon_in_phase, pixels_first=True)

def Dixon_post_contrast_water_dominant(folder):

    # Find source DICOM data
    series_Dixon_fat, study_Dixon_fat, desc_Dixon_fat                   = _map_input   (folder, "Dixon_post_contrast_fat")
    series_Dixon_in_phase, study_Dixon_in_phase, desc_Dixon_in_phase    = _map_input   (folder, "Dixon_post_contrast_in_phase")
    series_Dixon_out_phase, study_Dixon_out_phase, desc_Dixon_out_phase = _map_input   (folder, "Dixon_post_contrast_out_phase")

    # Load data
    array_Dixon_fat, header_Dixon_fat             = series_Dixon_fat.array('SliceLocation', pixels_first=True)
    array_Dixon_in_phase, header_Dixon_in_phase   = series_Dixon_in_phase.array('SliceLocation', pixels_first=True)
    array_Dixon_out_phase, header_Dixon_out_phase = series_Dixon_out_phase.array('SliceLocation', pixels_first=True)


    array_water_dominant_map = np.zeros(array_Dixon_fat.shape)
    array_water_dominant_map[array_Dixon_fat<0.5*array_Dixon_in_phase] =1

    array_water_calculated = np.zeros_like(array_Dixon_fat)  # Ensure same shape
    array_water_calculated = np.where(array_water_dominant_map == 1, array_Dixon_in_phase + array_Dixon_out_phase, array_water_calculated)
    array_water_calculated = np.where(array_water_dominant_map == 0, array_Dixon_in_phase - array_Dixon_out_phase, array_water_calculated)

    array_fat_calculated = np.zeros_like(array_Dixon_fat)  # Ensure same shape
    array_fat_calculated = np.where(array_water_dominant_map == 0, array_Dixon_in_phase + array_Dixon_out_phase, array_fat_calculated)
    array_fat_calculated = np.where(array_water_dominant_map == 1, array_Dixon_in_phase - array_Dixon_out_phase, array_fat_calculated)

    series = study_Dixon_fat.new_series(SeriesDescription="Dixon_post_contrast_fat_dominant_map")
    series.set_array(array_water_dominant_map, header_Dixon_fat, pixels_first=True)

    series = study_Dixon_fat.new_series(SeriesDescription="Dixon_post_contrast_water_calculated")
    series.set_array(array_water_calculated, header_Dixon_fat, pixels_first=True)

    series = study_Dixon_fat.new_series(SeriesDescription="Dixon_post_contrast_fat_calculated")
    series.set_array(array_fat_calculated, header_Dixon_fat, pixels_first=True)

def Dixon_map_fat_dominant(folder):

    # Find source DICOM data
    series_Dixon_fat, study_Dixon_fat, desc_Dixon_fat                = _map_input   (folder, "Dixon_fat [coreg]")
    series_Dixon_in_phase, study_Dixon_in_phase, desc_Dixon_in_phase = _map_input   (folder, "Dixon_in_phase [coreg]")

    # Load data
    array_Dixon_fat, header_Dixon_fat           = series_Dixon_fat.array('SliceLocation', pixels_first=True)
    array_Dixon_in_phase, header_Dixon_in_phase = series_Dixon_in_phase.array('SliceLocation', pixels_first=True)

    array_water_dominant_map = np.zeros(array_Dixon_fat.shape)
    array_water_dominant_map[array_Dixon_fat<0.5*array_Dixon_in_phase] =1

    series = study_Dixon_fat.new_series(SeriesDescription="Dixon_post_contrast_fat_dominant_map")
    series.set_array(array_water_dominant_map, header_Dixon_fat, pixels_first=True)




def _map_input(folder, desc):
    series, study = input_series(folder, desc + '_mdr_moco', export_study)
    if series is not None:
        return series, study, desc + '_mdr_moco'
    series, study = input_series(folder, desc, export_study)
    if series is None:
        raise RuntimeError('Cannot perform mapping: series ' + desc + 'does not exist. ')
    return series, study, desc




