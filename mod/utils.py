# logging

import datetime

# print_log('text', 'INFO', 'DOCKER')
def print_log(msg, status, app):
	text = f'{datetime.datetime.now().strftime("%d-%m-%Y %H:%M")}: - {app}:[{status}] - {msg}\n'

	try:
		f = open(f'logs//LOG-{datetime.datetime.now().strftime("%d-%m-%Y")}.log', "a")
		f.write(text)
		f.close()
	except:
		f = open(f'logs//LOG-{datetime.datetime.now().strftime("%d-%m-%Y")}.log', "w")
		f.write(text)
		f.close()
	print(text+'\n')