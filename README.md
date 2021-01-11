# DICOMTools
Tools for diagnosing and sorting series of DICOM files.

This is mostly an internal diagnostic tool set that some might find useful.


## Requirements
- Python 3.6 (it does now work with Python 3.7 or higher due to GDCM)
- GDCM (https://anaconda.org/conda-forge/gdcm)
- pydicom

## dicom_sorter

The dicom_sorter.py script can sort DICOM files into a hiearchical sub-structure. It starts by (for each file) extracting relevant DICOM header information as patient id
, study dates and times. These values can then later be used to define the sub-structure of the output files. 

This script is mostly a copy of the code described by  Alex Weston (https://towardsdatascience.com/a-python-script-to-sort-dicom-files-f1623a7f40b8)

## dicom_dump_series_info

The dicom_dump_series_info.py parses the file headers of a set of DICOM files in a given directory structure. It extracts some relevant values and dumps
the values into a csv file. This can be used diagnose potential mixed series and other DICOM related issues.
