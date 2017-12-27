#!/bin/python
#
#  Push files in a directory to onedrive folder. Session should have been saved.
#
import onedrivesdk
import os
import sys

def main(onedrive_location, local_location):

	# Setup OneDrive
	with open("client_id.txt") as myfile:
		client_id = myfile.readline().strip()
	client = onedrivesdk.get_default_client(client_id=client_id,
											scopes=['wl.signin',
											'wl.offline_access',
											'onedrive.readwrite'])

	client.auth_provider.load_session(path="client_code.data")

	folder_id = get_folder_id(client, onedrive_location)

	# Upload any files that are ready for it.
	for fpath in get_new_files (local_location):
		onedrive_upload(client, folder_id, fpath)

def onedrive_upload(client, loc_id, fpath):
	fname = os.path.basename(fpath)
	client.item(id=loc_id).children[fname].content.request().upload(fpath)
	marker_filepath = marker_file(fpath)
	with open(marker_filepath, "w") as myfile:
		myfile.write("done!\n")

def get_new_files (location):
	'''Look for new files that don't have an "uploaded" marker.'''
	full_list = ["{0}/{1}".format(location,f) for f in os.listdir(location)]
	return [f for f in full_list if file_has_been_updated(f)]

def file_has_been_updated(fpath):
	'''Is this file ready for upload?'''
	# Is if a directory!?
	if not os.path.isfile(fpath):
		return False
	#Is it an upload marker file?
	if fpath.endswith(".uploaded"):
		return False
	# See if there is an uploaded version.
	marker_file_path = marker_file(fpath)
	if file_accessible(marker_file_path, "r"):
		marker_time = os.path.getmtime(marker_file_path)
		file_time = os.path.getmtime(fpath)
		return file_time > marker_time
	return True

def marker_file(fpath):
	return fpath + ".uploaded"

def file_accessible(filepath, mode):
    ''' Check if a file exists and is accessible. '''
    try:
        f = open(filepath, mode)
        f.close()
    except IOError as e:
        return False
 
    return True

def get_folder_id (client, location):
	'''Get the id for a folder'''

	folders = location.split('/')
	fid = folders[0]
	for f in folders[1:]:
		ls = client.item(id=fid).children.get()
		fid = next(i.id for i in ls if i.name == f)
	return fid

if __name__ == "__main__":
	main(sys.argv[1], sys.argv[2])
