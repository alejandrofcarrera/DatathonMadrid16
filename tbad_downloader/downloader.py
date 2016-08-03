
import requests
import hashlib
import os
import re

#############################################


def generate_sha(fpath):
    sha1 = hashlib.sha1()
    f = open(fpath, 'rb')
    try:
        clean = re.sub("[\n\r]+", "", f.read());
        sha1.update(clean)
    finally:
        f.close()
    return sha1.hexdigest()


def download_dataset(fpath, dataset_id, dataset_url):
    with open(fpath, 'wb') as handle:
        response = requests.get(dataset_url, stream=True)
        for block in response.iter_content(1024):
            handle.write(block)
    print "Downloaded Dataset: " + dataset_id


def detect_dataset(old_path, new_path):
    if os.path.exists(new_path):
        if generate_sha(old_path) != generate_sha(new_path):
            os.remove(old_path)
            os.rename(new_path, old_path)
            print " * Updating data for dataset ..."
        else:
            os.remove(new_path)
            print " * Old data detected. Clean and do nothing."
            return True
    else:
        print " * Previous version not found. Saved."
    return False


#############################################


datasets = {}

dataset_folder = '/tmp/datasets/'


#############################################


if not os.path.exists(dataset_folder):
    os.makedirs(dataset_folder)

print "\nDownloading datasets ...\n"
for i in datasets.keys():
    ext = os.path.split(datasets[i])[-1].split('.')[-1]
    name_path = dataset_folder + i + '.' + ext
    name_new_path = dataset_folder + 'new_' + i + '.' + ext
    file_path = name_path
    if os.path.exists(name_path):
        file_path = name_new_path
    download_dataset(file_path, i, datasets[i])
    if not detect_dataset(name_path, name_new_path):
        print " * Doing things to data"
