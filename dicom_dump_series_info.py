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
dst = "D:/Data/IMM/Kristine/RHTestJan2021/SE00001_info.csv"

print('reading file list...')
unsortedList = []
for root, dirs, files in os.walk(src):
    for file in files:
        # the next line can be used if you need to filter files
        # if ".dcm" in file:  # exclude non-dicoms, good for messy folders
        unsortedList.append(os.path.join(root, file))

print('%s files found.' % len(unsortedList))
if len(unsortedList) == 0:
    print("No files found")
    exit(0)

out_file = open(dst,"w")
out_file.write("FileName, PatientID, PatientName, PatientBirthDate, StudyDate, StudyDescription, SeriesDescription"
               ", Modality, "
               "StudyInstanceUID,"
               "SeriesInstanceUID, InstanceNumber, ImageNumber, AcquisitionNumber, AcquisitionTime, ContentTime,"
               "PerformedProcedureStepStartTime, SeriesTime,InStackPositionNumber, StackID, CanDecompress\n")


im_count = 0
for dicom_loc in unsortedList:
    ds = pydicom.read_file(dicom_loc, force=True)

    # get information from DICOM header
    patientID = clean_text(ds.get("PatientID", "NA"))
    patient_name = ds.get("PatientName", "NA")
    real_patient_name = clean_text(patient_name.family_name)
    patient_birth = str(ds.get("PatientBirthDate", "0"))
    studyDate = clean_text(ds.get("StudyDate", "NA"))
    studyDescription = clean_text(ds.get("StudyDescription", "NA"))
    seriesDescription = clean_text(ds.get("SeriesDescription", "NA"))
    modality = ds.get("Modality", "NA")
    studyInstanceUID = ds.get("StudyInstanceUID", "NA")
    seriesInstanceUID = ds.get("SeriesInstanceUID", "NA")
    instanceNumber = str(ds.get("InstanceNumber", "0"))
    imageNumber = str(ds.get("ImageNumber", "0"))
    acquisition_number = str(ds.get("AcquisitionNumber", "0"))
    acquisition_time = str(ds.get("AcquisitionTime", "0"))
    content_time = str(ds.get("ContentTime", "0"))
    proc_time = str(ds.get("PerformedProcedureStepStartTime", "0"))
    series_time = str(ds.get("SeriesTime", "0"))
    # delta_time = float(content_time) - float(proc_time)

    in_stack = str(ds.get("InStackPositionNumber", "0"))
    stack_id = str(ds.get("StackID", "0"))
    # Create a simple file name that is just "IM" + the number of the DICOM file
    status_out = "Count " + str(im_count) + "/" + str(len(unsortedList)) + " instanceNumber" + instanceNumber
    print(status_out)

    can_decompress = True
    # try to uncompress files (using the gdcm package)
    try:
        ds.decompress()
    except:
        can_decompress = False

    # Horrible clumsy way of writing csv files :)
    out_file.write(str(dicom_loc) + "," +  patientID + "," + real_patient_name+ "," +  patient_birth + "," +
                   studyDate + "," + studyDescription + "," +
                   seriesDescription+ "," +  modality+ "," +  studyInstanceUID+ "," +  seriesInstanceUID+ "," +
                   instanceNumber +
                   "," +  imageNumber + "," + acquisition_number + "," + acquisition_time+ "," + content_time + "," +
                   proc_time + "," + series_time + "," + in_stack + "," + stack_id + "," + str(can_decompress) + "\n")

    im_count = im_count + 1
print('done.')
