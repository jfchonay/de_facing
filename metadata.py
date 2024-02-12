import glob
import statistics
import pandas as pd
import os
from bids import BIDSLayout


def extract_data(path):
    layout = BIDSLayout(path)
    T1_images = layout.get(datatype='anat', extension='nii.gz', suffix='T1w')
    all_images = layout.get(extension='nii.gz')
    n_images = len(T1_images)
    n_subjects = len(layout.get_subjects())
    n_sessions = len(layout.get_sessions())
    name = layout.get_dataset_description()['Name']
    doi = layout.get_dataset_description()['DatasetDOI']
    magnetic_field = 3

    subjects = layout.get_subjects()
    count_im = []

    for subject in subjects:
        t1_images_subject = layout.get(subject=subject, suffix='T1w', extension='.nii.gz')
        count_im.append(len(t1_images_subject))

    for scan in all_images:
        for entities in scan.entities:
            if 'MagneticFieldStrength' in entities:
                magnetic_field = scan.entities['MagneticFieldStrength']
                break
        else:
            continue
        break

    data = [('Name of dataset', name), ('DOI', doi), ('Number of subjects', n_subjects), ('Number of sessions', n_sessions)
            ,('Number of anatomical images', n_images), ('Anatomical images per subject', statistics.median(count_im)),
            ('Strength of the magnetic field', magnetic_field)]

    return data


if __name__=='__main__':
    root = '/archive/opendata/open_neuro/'
    all_metadata = []
    for folders in glob.iglob(os.path.join(root, '*')):
        data_description = extract_data(folders)
        dictionary = {key: value for key, value in data_description}
        all_metadata.append(dictionary)

    meta_data_df = pd.DataFrame(all_metadata)

    # meta_data_df['Type of preprocessing'] = [input(f"Row {index + 1}: ") for index in range(len(meta_data_df))]
