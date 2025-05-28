import time
from pipelines import (
    fetch_AI_model,
    fetch_nnunet_model,
    segment, 
    measure, 
    export, 
    rename, 
    mdr, 
    mapping, 
    harmonize, 
    align,
    roi_fit,
)



## HARMONIZATION

def rename_all_series(database):
    start_time = time.time()
    database.log("Renaming has started!")
    try:
        rename.all_series(database)
        rename.check(database)
        database.log("Renaming was completed --- %s seconds ---" % (int(time.time() - start_time)))
        database.save()
    except Exception as e:
        database.log("Renaming was NOT completed; error: " + str(e))  
        database.restore()
        raise RuntimeError('Critical step failed (renaming) - exiting pipeline.')



def harmonize_subject_name(database):
    start_time = time.time()
    database.log("Harmonizing subject name has started!")
    try:
        harmonize.subject_name(database)
        database.log("Harmonizing subject name was completed --- %s seconds ---" % (int(time.time() - start_time)))
        database.save()
    except Exception as e:
        database.log("Harmonizing subject name was NOT completed; error: " + str(e)) 
        database.restore()


## SEGMENTATION


def fetch_dl_models(database):
    start_time = time.time()
    database.log("Fetching deep-learning models has started")
    try:
        fetch_AI_model.dl_models(database)
        database.log("Fetching deep-learning models was completed --- %s seconds ---" % (int(time.time() - start_time)))
    except Exception as e:
        database.log("Fetching deep-learning models was NOT completed; error: "+str(e))
        database.restore()

def fetch_nnunet_models(database):
    start_time = time.time()
    database.log("Fetching deep-learning models has started")
    try:
        fetch_nnunet_model.nnunet_models(database)
        database.log("Fetching deep-learning models was completed --- %s seconds ---" % (int(time.time() - start_time)))
    except Exception as e:
        database.log("Fetching deep-learning models was NOT completed; error: "+str(e))
        database.restore()

def fetch_nnunet_models_water_dominant(database): 
    start_time = time.time()
    database.log("Fetching deep-learning models has started")
    try:
        fetch_nnunet_model.nnunet_models_water_dominant(database)
        database.log("Fetching deep-learning models was completed --- %s seconds ---" % (int(time.time() - start_time)))
    except Exception as e:
        database.log("Fetching deep-learning models was NOT completed; error: "+str(e))
        database.restore()

def segment_kidneys(database):
    start_time = time.time()
    database.log("Kidney segmentation has started")
    try:

        lk = database.series(SeriesDescription='LK')
        rk = database.series(SeriesDescription='RK')

        if len(lk) == 0 or len(rk) == 0:
            database.log("Starting AI kidney segmentation")
            segment.kidneys(database)
            database.log("AI Kidney segmentation was completed")
        else:
            database.log('Both masks were already present - no AI kidney segmentation was performed.')
        database.save()
        
    except Exception as e:
        database.log("AI Kidney segmentation was NOT completed; error: "+str(e))
        database.restore()
        raise RuntimeError('Critical step failed (kidney segmentation) - exiting pipeline.')

    database.log("Kidney segmentation was completed --- %s seconds ---" % (int(time.time() - start_time)))

def segment_kidneys_nnunet(database):
    start_time = time.time()
    database.log("Kidney segmentation has started")
    try:

        lk = database.series(SeriesDescription='LK')
        rk = database.series(SeriesDescription='RK')

        if len(lk) == 0 or len(rk) == 0:
            database.log("Starting nnunet kidney segmentation")
            segment.kidneys_nnunet(database)
            database.log("nnunet Kidney segmentation was completed")
        else:
            database.log('Both masks were already present - no nnunet kidney segmentation was performed.')
        database.save()
        
    except Exception as e:
        database.log("nnunet Kidney segmentation was NOT completed; error: "+str(e))
        database.restore()
        raise RuntimeError('Critical step failed (kidney segmentation) - exiting pipeline.')

    database.log("Kidney segmentation was completed --- %s seconds ---" % (int(time.time() - start_time)))

def segment_kidneys_nnunet_water_dominant(database):

    start_time = time.time()
    database.log("Kidneys water dominant segmentation has started")
    try:

        segment.kidneys_nnunet_water_dominant(database)
        database.log("Kidneys water dominant segmentation was completed")

        database.save()
        
    except Exception as e:
        database.log("Kidneys water dominant segmentation was NOT completed; error: "+str(e))
        database.restore()
        raise RuntimeError('Critical step failed (Kidneys water dominant segmentation) - exiting pipeline.')

    database.log("Kidneys water dominant segmentation was completed --- %s seconds ---" % (int(time.time() - start_time)))





# Set up exports as individual steps
def export_segmentations(database):
    start_time = time.time()
    database.log("Export kidney segmentations has started")
    try:
        export.kidney_masks_as_dicom(database)
        export.kidney_masks_as_png(database)
        database.log("Export kidney segmentations was completed --- %s seconds ---" % (int(time.time() - start_time)))
    except Exception as e:
        database.log("Export kidney segmentations was NOT completed; error: "+str(e))



        

def align_dixon(database):
    start_time = time.time()
    print('Starting DIXON alignment')
    database.log("DIXON alignment has started")
    try:
        align.dixon(database)
        database.log("DIXON alignment was completed --- %s seconds ---" % (int(time.time() - start_time)))
        database.save()
    except Exception as e: 
        database.log("DIXON alignment was NOT completed; error: "+str(e))
        database.restore()
        

## MEASURE
        
def measure_kidney_volumetrics(database):
    start_time = time.time()
    database.log("Kidney volumetrics has started")
    try:
        measure.kidney_volumetrics(database)
        database.log("Kidney volumetrics was completed --- %s seconds ---" % (int(time.time() - start_time)))
    except Exception as e:
        database.log("Kidney volumetrics was NOT completed; error: "+str(e))

def measure_kidney_volumetrics_pyradiomics(database):
    start_time = time.time()
    database.log("Kidney volumetrics has started")
    try:
        measure.kidney_volumetrics_paper_volumetry_edited_pyradiomics(database)
        database.log("Kidney volumetrics was completed --- %s seconds ---" % (int(time.time() - start_time)))
    except Exception as e:
        database.log("Kidney volumetrics was NOT completed; error: "+str(e))
    
