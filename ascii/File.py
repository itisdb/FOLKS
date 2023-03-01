import os, shutil

def filecount(dir):
    initial_count = 0
    for path in os.listdir(dir):
        if os.path.isfile(os.path.join(dir, path)):
            initial_count += 1
    return initial_count


def clear_files(dir):
    folder = dir
    try:
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))
    except Exception as error:
        os.mkdir(dir)


# print(filecount('./inputs'))
# print(clear_files('./inputs'))
# print(filecount('./inputs'))
# print(filecount('./inputs'))
# print(clear_files('./outputs'))
# print(filecount('./outputs'))