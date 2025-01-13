
import os

def get_newest_file_time(folder):
    newest_time = None
    for root, _, files in os.walk(folder):
        for file in files:
            file_path = os.path.join(root, file)
            if(os.path.islink(file_path)): # Symlinks
                file_time = os.lstat(file_path).st_mtime
            else: # Other files
                file_time = os.path.getmtime(file_path)
            if newest_time is None or file_time > newest_time:
                newest_time = file_time
    return newest_time

def is_newer(target_folder, reference_folder):
    """
    Check if the newest file in target_folder is newer than the newest file in reference_folder.

    :param target_folder: Path to the target folder.
    :param reference_folder: Path to the reference folder.
    :return: True if the newest file in target_folder is newer than the newest in reference_folder, False otherwise.
    """

    newest_time_tgt = get_newest_file_time(target_folder)
    newest_time_ref = get_newest_file_time(reference_folder)

    if newest_time_tgt is None or newest_time_ref is None:
        raise ValueError("One of the folders does not contain any files.")

    return newest_time_tgt > newest_time_ref