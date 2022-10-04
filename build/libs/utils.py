import os, shutil

def clear_dir(directory):
    '''
    Empties a directory according to : https://stackoverflow.com/a/185941
    '''
    if not os.path.isdir(directory):
        return None

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))