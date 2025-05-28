"""
Pipelines for between-sequence alignment.
"""

from dbdicom.extensions import vreg as vreg_dicom
from dbdicom.extensions import elastix
from dbdicom.pipelines import input_series

export_study = "3: Alignment"



###########################################
# Alignment of pre- and post-contrast DIXON
###########################################


def dixon(database):
    # A freeform transformation is found by coregistering the precontrast 
    # DIXON fat map to the post-contrast DIXON fat map. The same 
    # transformation is then applied to the other precontrast DIXON images.

    # Get the approrpiate DICOM series
    desc = [   
        'Dixon_out_phase',
        'Dixon_in_phase',
        'Dixon_water',
        'Dixon_fat',
        'Dixon_post_contrast_fat',
    ]
    series, study = input_series(database, desc, export_study)
    if series is None:
        raise RuntimeError('Cannot perform DIXON alignment: not all required data exist.')

    # Perform the corgistration on the DICOM series
    coregistered, followers = elastix.coregister_3d_to_3d(
        series[3], series[4],
        transformation = "Freeform", 
        metric = "AdvancedMeanSquares",
        final_grid_spacing = 25.0,
        apply_to = series[:3],
    )

    # Move the results to the new study
    coregistered.move_to(study)
    for series in followers:
        series.move_to(study)
    return coregistered, followers
