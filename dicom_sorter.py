# Rasmus R. Paulsen, DTU Compute
# Code examples from Alex Weston, Digital Innovation Lab, Mayo Clinic

import os
import pydicom  # pydicom is using the gdcm package for decompression


def clean_text(string):
    # clean and standardize text descriptions, which makes searching files easier
    forbidden_symbols = ["*", ".", ",", "\"", "\\", "/", "|", "[", "]", ":", ";", " "]
    for symbol in forbidden_symbols:
        string = string.replace(symbol, "_")  # replace everything with an underscore
    return string.lower()


# source DICOM directory
src = "D:/Data/IMM/Kristine/RHTestJan2021/SE00001/"

# where to put the results
dst = "D:/Data/IMM/Kristine/RHTestJan2021/SE00001_sorted/"

print('reading file list...')
unsortedList = []
for root, dirs, files in os.walk(src):
    for file in files:
        # the next line can be used if you need to filter files
        # if ".dcm" in file:  # exclude non-dicoms, good for messy folders
        unsortedList.append(os.path.join(root, file))

print('%s files found.' % len(unsortedList))

for dicom_loc in unsortedList:
    ds = pydicom.read_file(dicom_loc, force=True)

    # get information from DICOM header
    patientID = clean_text(ds.get("PatientID", "NA"))
    patient_name = ds.get("PatientName", "NA")
    real_patient_name = clean_text(patient_name.family_name)
    studyDate = clean_text(ds.get("StudyDate", "NA"))
    studyDescription = clean_text(ds.get("StudyDescription", "NA"))
    seriesDescription = clean_text(ds.get("SeriesDescription", "NA"))
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

    # some debug printing
    print("Instance#", instanceNumber,
          "Acq.#", acquisition_number, "acqTime", acquisition_time, "procTime", proc_time,
          "contTime", content_time, "seriesTime", series_time)

    # Create a simple file name that is just "IM" + the number of the DICOM file
    fileName = "IM" + instanceNumber.zfill(5) + ".dcm"
    print(fileName)

    # uncompress files (using the gdcm package)
    try:
        ds.decompress()
    except:
        # print('an instance in file %s - %s - %s - %s" could not be decompressed. exiting.' % (
        # patientID, studyDate, studyDescription, seriesDescription))
        print('an instance in file %s" could not be decompressed. exiting.' % (fileName))

    # Here you can define the path structure of the output - it should depend on the information in
    # your DICOM series

    #if not os.path.exists(os.path.join(dst, real_patient_name)):
    #    os.makedirs(os.path.join(dst, real_patient_name))

    #if not os.path.exists(os.path.join(dst, patientID, studyDate)):
    #    os.makedirs(os.path.join(dst, patientID, studyDate))

    # if not os.path.exists(os.path.join(dst, patientID, studyDate, studyDescription)):
    #    os.makedirs(os.path.join(dst, patientID, studyDate, studyDescription))

    # real_patient_name - study date - content time
    # works for some series and not for others
    if not os.path.exists(os.path.join(dst, real_patient_name, studyDate, content_time)):
         os.makedirs(os.path.join(dst, real_patient_name, studyDate, content_time))
    ds.save_as(os.path.join(dst, real_patient_name, studyDate, content_time, fileName))

    # if not os.path.exists(os.path.join(dst, real_patient_name, studyDate, acquisition_time)):
    #    os.makedirs(os.path.join(dst, real_patient_name, studyDate, acquisition_time))
    # ds.save_as(os.path.join(dst, real_patient_name, studyDate, acquisition_time, fileName))

print('done.')