import datetime
from wezel.gui import Action, Menu
from wezel.displays import TableDisplay, MatplotLibDisplay
from wezel.plugins.pyvista import SurfaceDisplay


from pipelines import (
    fetch_AI_model,
    fetch_Drive_mask,
    rename,  
    fetch_AI_model,
    fetch_Drive_mask,
    segment, 
    measure, 
    export, 
    align,
)
import utilities.upload as upload


# Needs to be in a central location
#weights = 'C:\\Users\\steve\\Dropbox\\Data\\dl_models\\UNETR_kidneys_v1.pth'


def _never(app):
    return False

def _if_a_database_is_open(app): 
    return app.database() is not None



## HARMONIZATION



def rename_all_series(app):
    folder = app.database()
    rename.all_series(folder)
    rename.check(folder)
    app.refresh()


action_rename = Action("Rename series..", on_clicked=rename_all_series, is_clickable=_if_a_database_is_open)




## SEGMENTATION


def fetch_dl_models(app):
    folder = app.database()
    fetch_AI_model.dl_models(folder)
    app.refresh()

def fetch_kidney_masks(app):
    folder = app.database()
    fetch_Drive_mask.kidney_masks(folder)
    app.refresh()

def segment_kidneys(app):
    database = app.database()
    kidneys = segment.kidneys(database)
    for kidney in kidneys:
        app.addWidget(SurfaceDisplay(kidney), title=kidney.label())
    app.refresh()

def whole_kidney_canvas(app):
    folder = app.database()
    clusters = segment.compute_whole_kidney_canvas(folder)
    if clusters is not None:
        app.display(clusters)
    app.refresh()

def export_segmentations(app):
    database = app.database()
    export.kidney_masks_as_dicom(database)
    export.kidney_masks_as_png(database)
    app.refresh()

def all_segmentation_steps(app):
    answer = app.dialog.question('This is going to take a while. Do you want to continue?')
    if 'Yes' != answer:
        return
    fetch_dl_models(app)
    fetch_kidney_masks(app)
    segment_kidneys(app)
    whole_kidney_canvas(app)
    export_segmentations(app)


action_all_segmentation_steps = Action("All above segmentation steps..", on_clicked=all_segmentation_steps, is_clickable=_if_a_database_is_open)
action_fetch_dl_models = Action("Fetch deep learning models..", on_clicked=fetch_dl_models, is_clickable=_if_a_database_is_open)
action_fetch_kidney_masks = Action("Fetch kidney masks..", on_clicked=fetch_kidney_masks, is_clickable=_never)
action_segment_kidneys = Action("Auto-segment kidneys...", on_clicked=segment_kidneys, is_clickable=_if_a_database_is_open)

action_whole_kidney_canvas = Action("Calculate segmentation canvas..", on_clicked=whole_kidney_canvas, is_clickable=_if_a_database_is_open)
action_export_kidney_segmentations = Action("Export segmentations..", on_clicked=export_segmentations, is_clickable=_if_a_database_is_open)

menu_segment = Menu('Segment..')
menu_segment.add(action_fetch_dl_models)
menu_segment.add(action_fetch_kidney_masks)
menu_segment.add(action_segment_kidneys)
menu_segment.add_separator()
menu_segment.add(action_whole_kidney_canvas)
menu_segment.add_separator()
menu_segment.add(action_export_kidney_segmentations)
menu_segment.add_separator()
menu_segment.add(action_all_segmentation_steps)






## MAPPING



# ALIGNMENT


def align_dixon(app):
    database = app.database()
    results = align.dixon(database)
    for series in results:
        app.display(series)
    app.refresh()



def align_all(app):
    answer = app.dialog.question('This is going to take a while. Do you want to continue?')
    if 'Yes' != answer:
        return
    align_dixon(app)


action_align_all = Action("Align all sequences..", on_clicked=align_all, is_clickable=_if_a_database_is_open)
action_align_dixon = Action("Align DIXON..", on_clicked=align_dixon, is_clickable=_if_a_database_is_open)


menu_align = Menu('Align scans..')
menu_align.add(action_align_dixon)
menu_align.add(action_align_all)



# MEASURE



def measure_kidney_volumetrics(app):
    database = app.database()
    features = measure.kidney_volumetrics(database)
    app.addWidget(TableDisplay(features), 'Kidney - Volume features')
    app.refresh()


def measure_all(app):
    answer = app.dialog.question('This is going to take a while. Do you want to continue?')
    if 'Yes' != answer:
        return
    measure_kidney_volumetrics(app)


action_all_measurements = Action("All measurements..", on_clicked=measure_all, is_clickable=_if_a_database_is_open)
action_measure_kidney_volumetrics = Action("Measure kidney volumetrics..", on_clicked=measure_kidney_volumetrics, is_clickable=_if_a_database_is_open)


menu_measure = Menu('Pixel values..')
menu_measure.add(action_measure_kidney_volumetrics)
menu_measure.add(action_all_measurements)





# OTHER STEPS


def _upload(app):
    folder = app.database()
    path = folder.path()
    filename_log = path + datetime.datetime.now().strftime('%Y%m%d_%H%M_') + "log_segmentation.txt"
    upload.main(path, filename_log)
    app.refresh()


action_upload = Action("Upload to drive..", on_clicked=_upload, is_clickable=_if_a_database_is_open)





