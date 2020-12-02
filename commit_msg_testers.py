#!/usr/bin/python

import sys
import json
import requests
import os
from pprint import pprint

def is_int(value):
	try:
		int(value)
	except ValurError:
		return False

	return True

def check_issue_in_dev(labels):
	label = 'EM_DEV'

	for i in range(len(labels)):
		print labels[i]['name']

	for i in range(len(labels)):
		if labels[i]['name'] == label:
			return True

	return False

def validate_issue(issues, commit_msg):
	cerc_pos = commit_msg.find('#')

	if cerc_pos == -1:
		print 'NAO FOI ENCONTRADO O CARACTERE # NA MENSAGEM, O COMMIT NAO SE REFERE A NENHUMA ISSUE'
		return False
	if cerc_pos == len(commit_msg)-2:
		print 'O CARACTERE # ESTA AO FINAL DA MENSAGEM, O COMMIT NAO SE REFERE A NENHUMA ISSUE'
		return False

	if not is_int(commit_msg[cerc_pos+1]):
		print 'O COMMIT NAO SE REFERE A NENHUMA ISSUE'
		return False

	print commit_msg[cerc_pos+1]
	for i in range(len(issues)):
		if int(issues[i]['number']) == int(commit_msg[cerc_pos+1]):
			if check_issue_in_dev(issues[i]['labels']):
				return True
			else:
				print 'SEU COMMIT NAO SE REFERE A UMA ISSUE EM_DEV'
				return False

	return False;


def usando_api():
	token = os.getenv('GITHUB_TOKEN', 'ee8e599c9c6ebd2311b05e6eaf1e035f20dfa171')
	#params = { 'state' : 'open', }
	headers = { 'Autorization' : 'token {token}' }
	result = requests.get('https://api.github.com/repos/OdailtonMarinho/ci-tester/issues', headers=headers)

	if result.status_code == 200:
		return result.json()
	else:
		print "Mim apareci que o traqui faio. CODE: ", result.status_code
		return result.status_code

def main():
	print "Number of Args: ", len(sys.argv)
	print "Argument List: ", str(sys.argv)

	file = open(sys.argv[1], "r")
	commit_msg = file.read()

	issues = usando_api()

	print os.system('git diff --name-only --cached')
	print os.system('date -I')
	print os.system('date +"%H:%M"')
	print os.system('git config user.name')
	print os.system('git config user.email')

	if validate_issue(issues, commit_msg):
		print "DEU CERTISSIMO!! MAS COMO EH SO UM TESTE, COMMIT BARRADO!!"
		sys.exit(1)
	else:
		print "VAI APRENDER A COMMITAR, AEO."
		sys.exit(1)

	print "MIM APARECE QUE ESTAH TUDO NUS CONFORMIS..."
	sys.exit(0)

if __name__ == "__main__":
	main()