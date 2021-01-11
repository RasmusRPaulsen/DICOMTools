# Alex Weston
# Digital Innovation Lab, Mayo Clinic

import os
import pydicom  # pydicom is using the gdcm package for decompression


def clean_text(string):
    # clean and standardize text descriptions, which makes searching files easier
    forbidden_symbols = ["*", ".", ",", "\"", "\\", "/", "|", "[", "]", ":", ";", " "]
    for symbol in forbidden_symbols:
        string = string.replace(symbol, "_")  # replace everything with an underscore
    return string.lower()


# user specified parameters
# src = "D:/Data/IMM/Kristine/RHTestJan2021/SE00001/"
# dst = "D:/Data/IMM/Kristine/RHTestJan2021/SE00001/out/"

#src = "D:/Data/IMM/Kristine/ODB_June2020/0305473111/Ct Hjerte Uden Og Med Kontrast/HALF 312ms 1.20s Cardiac 0.5 CTA-HALF CE - 6"
#dst = "D:/Data/IMM/Kristine/ODB_June2020/0305473111/Ct Hjerte Uden Og Med Kontrast/HALF 312ms 1.20s Cardiac 0.5 CTA-HALF CE - 6/out"

src = "D:/Data/IMM/Kristine/ODB_June2020/1902470553/1902470553/Ct Hjerte Med Kontrast/CCTA function + venøs smartphase - 303"
dst = "D:/Data/IMM/Kristine/ODB_June2020/1902470553/1902470553/Ct Hjerte Med Kontrast/CCTA function + venøs smartphase - 303/out2"


print('reading file list...')
unsortedList = []
for root, dirs, files in os.walk(src):
    for file in files:
        # if ".dcm" in file:  # exclude non-dicoms, good for messy folders
        unsortedList.append(os.path.join(root, file))

print('%s files found.' % len(unsortedList))

# study_UID_old = ""
# serie_UID_Old = ""

for dicom_loc in unsortedList:
    # read the file
    ds = pydicom.read_file(dicom_loc, force=True)

    # get patient, study, and series information
    patientID = clean_text(ds.get("PatientID", "NA"))
    patient_name = ds.get("PatientName", "NA")
    real_patient_name = clean_text(patient_name.family_name)
    studyDate = clean_text(ds.get("StudyDate", "NA"))
    studyDescription = clean_text(ds.get("StudyDescription", "NA"))
    seriesDescription = clean_text(ds.get("SeriesDescription", "NA"))

    # generate new, standardized file name
    modality = ds.get("Modality", "NA")
    studyInstanceUID = ds.get("StudyInstanceUID", "NA")
    seriesInstanceUID = ds.get("SeriesInstanceUID", "NA")
    instanceNumber = str(ds.get("InstanceNumber", "0"))
    acquisition_number = str(ds.get("AcquisitionNumber", "0"))
    acquisition_time = str(ds.get("AcquisitionTime", "0"))
    content_time = str(ds.get("ContentTime", "0"))
    proc_time = str(ds.get("PerformedProcedureStepStartTime", "0"))
    series_time = str(ds.get("SeriesTime", "0"))
    # delta_time = float(content_time) - float(proc_time)

    in_stack = str(ds.get("InStackPositionNumber", "0"))
    stack_id = str(ds.get("StackID", "0"))
    patient_birth = str(ds.get("PatientBirthDate", "0"))
    # fileName = modality + "." + seriesInstanceUID + "." + instanceNumber + ".dcm"
    #fileName = "acq." + acquisition_time + ".inst." + instanceNumber + ".inStack." + in_stack + ".stackID." + \
    #          stack_id + ".contTime." + content_time + ".procTime." + proc_time + \
    #          ".deltaTime."  + ".dcm"
    # im_number = int(instanceNumber)
    # fileName = f"IM{im_number:{5}}.dcm"

    # print("StudyDesc:", studyDescription, "SeriesDesc:", seriesDescription, "Instance#", instanceNumber,
    #      "Acq.#", acquisition_number, "acqTime", acquisition_time, "procTime", proc_time,
    #      "contTime", content_time)

    print("Instance#", instanceNumber,
          "Acq.#", acquisition_number, "acqTime", acquisition_time, "procTime", proc_time,
          "contTime", content_time, "seriesTime", series_time)

    fileName = "IM" + instanceNumber.zfill(5) + ".dcm"

    # if study_UID_old != studyInstanceUID:
    #     print("new study UID")
    # if serie_UID_Old != seriesInstanceUID:
    #    print("new study UID")
    # study_UID_old = studyInstanceUID
    # serie_UID_Old = seriesInstanceUID


    # uncompress files (using the gdcm package)
    try:
        ds.decompress()
    except:
        # print('an instance in file %s - %s - %s - %s" could not be decompressed. exiting.' % (
        # patientID, studyDate, studyDescription, seriesDescription))
        print('an instance in file %s" could not be decompressed. exiting.' % (fileName))

    print(fileName)

    # save files to a 4-tier nested folder structure
    #if not os.path.exists(os.path.join(dst, real_patient_name)):
    #    os.makedirs(os.path.join(dst, real_patient_name))

    #if not os.path.exists(os.path.join(dst, patientID, studyDate)):
    #    os.makedirs(os.path.join(dst, patientID, studyDate))

    # if not os.path.exists(os.path.join(dst, patientID, studyDate, studyDescription)):
    #    os.makedirs(os.path.join(dst, patientID, studyDate, studyDescription))

    # if not os.path.exists(os.path.join(dst, real_patient_name, studyDate, content_time)):
    #     os.makedirs(os.path.join(dst, real_patient_name, studyDate, content_time))
    # ds.save_as(os.path.join(dst, real_patient_name, studyDate, content_time, fileName))

    if not os.path.exists(os.path.join(dst, real_patient_name, studyDate, acquisition_time)):
        os.makedirs(os.path.join(dst, real_patient_name, studyDate, acquisition_time))
    ds.save_as(os.path.join(dst, real_patient_name, studyDate, acquisition_time, fileName))


    #   print('Saving out file: %s - %s - %s - %s.' % (patientID, studyDate, studyDescription, seriesDescription))

    # ds.save_as(os.path.join(dst, patientID, studyDate, studyDescription, seriesDescription, fileName))

print('done.')