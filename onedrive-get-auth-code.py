#!/bin/python
#
#  Push files in a directory to onedrive folder. Session should have been saved.
#  The client-code.txt file will be written to a file. Move this file down to the watcher
#  (DO NOT CHECK IN)
import onedrivesdk
from onedrivesdk.helpers import GetAuthCodeServer
from PIL import Image
import os


def main():
	redirect_uri = "http://localhost:8080/"

	with open("client_secret.txt") as myfile:
		client_secret = myfile.readline().strip()
	with open("client_id.txt") as myfile:
		client_id = myfile.readline().strip()


	client = onedrivesdk.get_default_client(client_id = client_id,

											scopes=['wl.signin',

													'wl.offline_access',

													'onedrive.readwrite'])

	auth_url = client.auth_provider.get_auth_url(redirect_uri)



	# Block thread until we have the code

	code = GetAuthCodeServer.get_auth_code(auth_url, redirect_uri)
	client.auth_provider.authenticate(code, redirect_uri, client_secret)

	client.auth_provider.save_session(path="client_code.data")

if __name__ == '__main__':
	main()
