import requests
from time import sleep

url = 'https://api.telegram.org/bot739393314:AAHWAmhb3lYsP-j2xhlejFMbojqXhRZigMo/'

def get_updates_json(request):
	params = {'timeout': 30, 'offset': None}
	response = requests.get(request + 'getUpdates')
	return response.json()

def last_update(data):
	results = data['result']
	total_updates = len(results) - 1
	return results[total_updates]

def send_info(update):
	chat_id = update['message']['chat']['id']
	first_name = update['message']['from']['first_name']
	username = update['message']['from']['username']
	user_id = update['message']['from']['id']
	is_bot = update['message']['from']['is_bot']
	language = update['message']['from']['language_code']
	if is_bot:
		bot = '\nYou\'re bot'
	else:
		bot = '\nYou\'re not bot'
	text = 'Your name: ' + first_name + '\nUsername: ' + username + '\nID: ' + str(user_id) + bot + '\nYour language: ' + language
	params = {'chat_id': chat_id, 'text': text}
	response = requests.post(url + 'sendMessage', data = params)
	return response

def main():
	update_id = last_update(get_updates_json(url))['update_id']
	while True:
		if update_id == last_update(get_updates_json(url))['update_id']:
			send_info(last_update(get_updates_json(url)))
			update_id += 1
		sleep(1)

if __name__ == '__main__':
	main()