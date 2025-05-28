import time
from pipelines import (
    fetch_Drive_mask,
    mdr, 
    mapping, 
    harmonize,
    measure,
    segment,
    export, 
)


## HARMONIZATION

def harmonize_subject_name(database,dataset):
    start_time = time.time()
    database.log("Harmonizing subject name has started!")
    try:
        harmonize.subject_name_internal(database,dataset)
        database.log("Harmonizing subject name was completed --- %s seconds ---" % (int(time.time() - start_time)))
        database.save()
    except Exception as e:
        database.log("Harmonizing subject name was NOT completed; error: " + str(e)) 
        database.restore()

## SEGMENTATION

def fetch_kidney_masks(database):
    start_time = time.time()
    database.log("Fetching kidney masks has started")
    try:
        fetch_Drive_mask.kidney_masks(database)
        database.log("Fetching kidney masks was completed --- %s seconds ---" % (int(time.time() - start_time)))
        database.save()
    except Exception as e:
        database.log("Fetching kidney masks was NOT completed; error: "+str(e))
        database.restore()

def fetch_kidney_masks(database):
    start_time = time.time()
    database.log("Fetching kidney masks has started")
    try:
        fetch_Drive_mask.kidney_masks(database)
        database.log("Fetching kidney masks was completed --- %s seconds ---" % (int(time.time() - start_time)))
    except Exception as e:
        database.log("Fetching kidney masks was NOT completed; error: "+str(e))
        database.restore()

def compute_whole_kidney_canvas(database):
    start_time = time.time()
    database.log('Starting computing canvas')
    try:
        segment.compute_whole_kidney_canvas(database)
        database.log("Computing canvas was completed --- %s seconds ---" % (int(time.time() - start_time)))
        database.save()
    except Exception as e: 
        database.log("Computing canvas was NOT computed; error: "+str(e))
        database.restore()

def export_whole_kidney_only_segmentations_as_png(database):
    start_time = time.time()
    database.log("Export kidney segmentations has started")

    try:
        export.kidney_masks_as_png(database,backgroud_series = 'Dixon_post_contrast_out_phase',RK_mask = 'RK', LK_mask = 'LK',mask_name = 'Whole Kidney_masks')
    except Exception as e:
        database.log("Export kidney segmentations was NOT completed; error: "+str(e))

    database.log("Export kidney segmentations was completed --- %s seconds ---" % (int(time.time() - start_time)))

def export_project_pre_Dixon_whole_kidney_only_segmentations_as_png(database):
    start_time = time.time()
    database.log("Export kidney segmentations has started")

    try:
        export.kidney_masks_as_png(database,backgroud_series = 'Dixon_out_phase [coreg]',RK_mask = 'RK', LK_mask = 'LK',mask_name = 'Whole Kidney_masks')
    except Exception as e:
        database.log("Export kidney segmentations was NOT completed; error: "+str(e))

    database.log("Export kidney segmentations was completed --- %s seconds ---" % (int(time.time() - start_time)))

def export_project_post_Dixon_whole_kidney_only_segmentations_as_png(database):
    start_time = time.time()
    database.log("Export kidney segmentations has started")

    try:
        export.kidney_masks_as_png(database,backgroud_series = 'Dixon_post_contrast_out_phase',RK_mask = 'RK', LK_mask = 'LK',mask_name = 'Whole Kidney_masks')
    except Exception as e:
        database.log("Export kidney segmentations was NOT completed; error: "+str(e))

    database.log("Export kidney segmentations was completed --- %s seconds ---" % (int(time.time() - start_time)))

def export_segmentations_folder_volumetry_1(database):
    start_time = time.time()
    database.log("Export kidney segmentations has started")
    try:
        export.kidney_masks_as_dicom_folder_1(database)
        export.kidney_masks_as_png_folder_1(database)
        database.log("Export kidney segmentations was completed --- %s seconds ---" % (int(time.time() - start_time)))
    except Exception as e:
        database.log("Export kidney segmentations was NOT completed; error: "+str(e))



## MAPPING

def map_post_contrast_water_dominant(database):
    start_time = time.time()
    print('Starting fat dominant mapping')
    database.log("Fat dominant mapping has started")
    try:
        mapping.Dixon_post_contrast_water_dominant(database)
        database.log("Fat dominant was completed --- %s seconds ---" % (int(time.time() - start_time)))
        database.save()
    except Exception as e: 
        database.log("Fat dominant was NOT completed; error: "+str(e))
        database.restore()

def map_fat_dominant(database):
    start_time = time.time()
    print('Starting fat dominant mapping')
    database.log("Fat dominant mapping has started")
    try:
        mapping.Dixon_fat_dominant(database)
        database.log("Fat dominant was completed --- %s seconds ---" % (int(time.time() - start_time)))
        database.save()
    except Exception as e: 
        database.log("Fat dominant was NOT completed; error: "+str(e))
        database.restore()


def calculate_Dixon_fat_water(database):
    start_time = time.time()
    print('Starting Fat/Water Dixon mapping')
    database.log("Fat/Water Dixon mapping has started")
    try:
        mapping.calculate_dixon_fat_water(database)
        database.log("Fat/Water Dixon was calculated --- %s seconds ---" % (int(time.time() - start_time)))
        database.save()
    except Exception as e: 
        database.log("Fat/Water Dixon was NOT calculated; error: "+str(e))
        database.restore()



## MEASURE

def measure_kidney_volumetrics_paper_volumetry_skimage(database):
    start_time = time.time()
    database.log("Kidney volumetrics with skimage has started")
    try:
        measure.kidney_volumetrics_paper_volumetry_edited_skimage(database)
        database.log("Kidney volumetrics with skimage was completed --- %s seconds ---" % (int(time.time() - start_time)))
    except Exception as e:
        database.log("Kidney volumetrics with skimage was NOT completed; error: "+str(e))

def measure_kidney_volumetrics_paper_volumetry_pyradiomics(database):
    start_time = time.time()
    database.log("Kidney volumetrics with pyradiomics has started")
    try:
        measure.kidney_volumetrics_paper_volumetry_edited_pyradiomics(database)
        database.log("Kidney volumetrics with pyradiomics was completed --- %s seconds ---" % (int(time.time() - start_time)))
    except Exception as e:
        database.log("Kidney volumetrics with pyradiomics was NOT completed; error: "+str(e))

## ROI ANALYSIS

## DATA EXPORT


def export_project_pre_Dixon_to_AI(database,subject_ID):
    start_time = time.time()
    database.log("Export to AI has started")
    try:
        export.pre_Dixon_to_AI(database,subject_ID)
        database.log("Export to AI was completed --- %s seconds ---" % (int(time.time() - start_time)))
    except Exception as e:
        database.log("Export to AI was NOT completed; error: "+str(e))

def export_project_pre_Dixon_in_out_to_AI(database,subject_ID):
    start_time = time.time()
    database.log("Export to AI has started")
    try:
        export.pre_Dixon_in_out_to_AI(database,subject_ID)
        database.log("Export to AI was completed --- %s seconds ---" % (int(time.time() - start_time)))
    except Exception as e:
        database.log("Export to AI was NOT completed; error: "+str(e))

def export_project_post_contrast_Dixon_to_AI(database,subject_ID):
    start_time = time.time()
    database.log("Export to AI has started")
    try:
        export.post_contrast_Dixon_to_AI(database,subject_ID)
        database.log("Export to AI was completed --- %s seconds ---" % (int(time.time() - start_time)))
    except Exception as e:
        database.log("Export to AI was NOT completed; error: "+str(e))

def export_project_post_contrast_in_out_Dixon_to_AI(database,subject_ID):
    start_time = time.time()
    database.log("Export to AI has started")
    try:
        export.post_contrast_in_out_Dixon_to_AI(database,subject_ID)
        database.log("Export to AI was completed --- %s seconds ---" % (int(time.time() - start_time)))
    except Exception as e:
        database.log("Export to AI was NOT completed; error: "+str(e))
    