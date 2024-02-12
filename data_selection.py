import os
import subprocess
import pandas as pd


def clone_repositories(root, list_repo):
    for repo_id in list_repo:
        # Create a new directory for the dataset
        dataset_dir = os.path.join(root, f'{repo_id}')

        os.makedirs(dataset_dir, exist_ok=True)

        # Change into the dataset directory
        os.chdir(dataset_dir)

        # Use DataLad to clone the repository
        cmd = f'datalad clone https://github.com/OpenNeuroDatasets/{repo_id}.git'

        # Execute the command in the shell
        subprocess.run(cmd, shell=True)

        # Use DataLad to get the "anat" folder from the cloned repository
        get_cmd = f'datalad get /sub-*/ses-*/anat/*'
        subprocess.run(get_cmd, shell=True)


if __name__ == "__main__":
    root = os.path.dirname(os.path.realpath(__file__))
    # Get repository ID
    repo_ids = pd.read_csv((root + '/repo_id.csv'), header=0)
    list_repo = repo_ids['dataset'].tolist()

    # Call the function to clone repositories
    clone_repositories(root, list_repo)
