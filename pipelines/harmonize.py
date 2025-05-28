
import utilities.standardize_subject_name as standardize_subject_name

# Note from older code:
# For T1-mapping, Siemens uses the field 'InversionTime' 
# but Philips uses (0x2005, 0x1572). Need to include a 
# harmonization step for Philips.



def subject_name_internal(database,dataset):

    series_list = database.series()

    if dataset[0] == 7:
        subject_name = database.PatientName
        if len(subject_name) != 7:
            correct_name = database.PatientName[3:7]+ "_" + database.PatientName[7:]
            database.PatientName = correct_name
            database.save()
            return


    subject_name = series_list[0]['PatientID']
    if len(subject_name) != 7 or subject_name[4] != "_":

        correct_name = standardize_subject_name.subject_hifen(subject_name)
        #print(correct_name)
        if correct_name != 0:
            if dataset[0] == 3 and dataset [1] == 3:
                correct_name = correct_name + "_followup"
            elif dataset[0] == 2 and dataset [1] == 0:
                correct_name = correct_name + "_followup"
            database.PatientName = correct_name
            database.save()
            return

        correct_name = standardize_subject_name.subject_underscore(subject_name)
        print(correct_name)
        if correct_name != 0:
            if dataset[0] == 3 and dataset [1] == 3:
                correct_name = correct_name + "_followup"
            elif dataset[0] == 2 and dataset [1] == 0:
                correct_name = correct_name + "_followup"
            database.PatientName = correct_name
            database.save()
            return
        
        correct_name = standardize_subject_name.subject_seven_digitd(subject_name)
        print(correct_name)
        if correct_name != 0:
            if dataset[0] == 3 and dataset [1] == 3:
                correct_name = correct_name + "_followup"
            elif dataset[0] == 2 and dataset [1] == 0:
                correct_name = correct_name + "_followup"
            database.PatientName = correct_name
            database.save()
            return

def subject_name(database):

    series_list = database.series()
    subject_name = series_list[0]['PatientID']
    if len(subject_name) != 7 or subject_name[4] != "_":

        correct_name = standardize_subject_name.subject_hifen(subject_name)
        #print(correct_name)
        if correct_name != 0:
            database.PatientName = correct_name
            database.save()
            return

        correct_name = standardize_subject_name.subject_underscore(subject_name)
        print(correct_name)
        if correct_name != 0:
            database.PatientName = correct_name
            database.save()
            return
        
        correct_name = standardize_subject_name.subject_seven_digitd(subject_name)
        print(correct_name)
        if correct_name != 0:
            database.PatientName = correct_name
            database.save()
            return

# def all_series(database):

#     pc_left(database)
#     pc_right(database)
#     t2(database)
#     mt(database)
#     dti(database)
#     ivim(database)
#     dce(database)
    


