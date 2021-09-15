import pyautogui, time, pyperclip, os, math


def wait_for_image(image, num_tries=None):
	loc = None
	num_tries = num_tries or math.inf
	i = 0
	while loc == None:
		loc = pyautogui.locateOnScreen(image, grayscale=True, confidence=.5)
		time.sleep(0.1)
		i += 1
		if i > num_tries:
			return False
	time.sleep(1)
	return True

screenWidth, screenHeight = pyautogui.size()

currentMouseX, currentMouseY = pyautogui.position()



def paste_text(text):
	pyperclip.copy(text)
	time.sleep(0.1)
	pyautogui.keyDown('command')
	pyautogui.press('v')
	pyautogui.keyUp('command')

def list_nft(name, file_name, description, collection_link):
	print(f'adding file {filename}')
	wait_for_image(os.path.join('images', 'add.png'))
	time.sleep(0.05)
	print('add..')
	# add item
	pyautogui.click(1594, 239)
	time.sleep(0.2)

	if not wait_for_image(os.path.join('images', 'create.png'), num_tries=2):
		# click again
		time.sleep(0.5)
		pyautogui.click(1594, 239)

	wait_for_image(os.path.join('images', 'create.png'))
	print('create..')
	# choose image
	pyautogui.click(637, 587)

	time.sleep(0.5)

	if not wait_for_image(os.path.join('images', 'collection.png'), num_tries=2):
		# click again
		time.sleep(0.5)
		pyautogui.click(637, 587)

	wait_for_image(os.path.join('images', 'collection.png'))

	# search field
	pyautogui.click(1292, 115)

	time.sleep(0.5)

	paste_text(file_name)
	time.sleep(0.5)
	pyautogui.press('enter')


	time.sleep(0.5)
	# not macOS
	pyautogui.click(522, 156)

	time.sleep(1)
	#chose image
	pyautogui.click(362, 206)

	time.sleep(0.5)
	# open
	pyautogui.click(1515, 608)

	print('selected file')
	wait_for_image(os.path.join('images', 'change.png'))

	time.sleep(0.5)
	pyautogui.click(595, 873)
	time.sleep(0.5)
	paste_text(name)
	time.sleep(0.2)

	# description
	pyautogui.scroll(-20)
	time.sleep(0.05)
	pyautogui.click(705, 452)
	time.sleep(0.5)

	paste_text(description)
	time.sleep(0.05)

	pyautogui.scroll(-17)
	time.sleep(0.05)

	# create
	pyautogui.click(500, 903)
	time.sleep(0.05)


	wait_for_image(os.path.join('images', 'woot.png'))
	print('ADDED')
	#close popup
	pyautogui.click(1078, 263)
	time.sleep(0.05)


	# sell
	pyautogui.click(1375, 232)
	time.sleep(0.05)
	print('sell..')

	# price
	wait_for_image(os.path.join('images', 'amount.png'))
	pyautogui.click(923, 529)
	time.sleep(0.5)
	paste_text('0.01')

	time.sleep(0.3)

	# post listing
	pyautogui.click(1199, 568)
	time.sleep(0.05)

	#sign
	wait_for_image(os.path.join('images', 'signature.png'), num_tries=6)
	print('sign..')

	pyautogui.click(1579, 588)
	time.sleep(0.05)

	time.sleep(1)
	# handle when wallet crashes
	if wait_for_image(os.path.join('images', 'amount.png'), num_tries=1):
		# post listing
		pyautogui.click(1163,613)
		time.sleep(0.05)

		#sign
		print('sign..')
		wait_for_image(os.path.join('images', 'signature.png'))
		pyautogui.click(1579, 588)
		time.sleep(0.05)
		
	#view
	print('LISTED')
	wait_for_image(os.path.join('images', 'listed.png'))
	print('copy url and return...')


	# copy url to clipboard
	pyautogui.click(696, 641)

	time.sleep(.5)
	url = pyperclip.paste()

	if not url.startswith('https'):
		raise Exception('BAD URL.')

	#close
	pyautogui.click(1155, 266)
	time.sleep(0.5)
	#back
	pyautogui.click(407, 84)
	time.sleep(0.1)
	paste_text(collection_link)
	time.sleep(0.1)
	pyautogui.press('enter')
	time.sleep(0.5)

	return url

i = 0
# change window
pyautogui.click(1594, 239)

def nft_name_fun_csc(filename):
	name_parts = filename.split('.')[0].split('_')
	name_parts[-1] = str(int(name_parts[-1]) + 1)
	name_parts = [s.capitalize() for s in name_parts]
	name = ' '.join(name_parts)
	return name

def nft_name_fun_cfd(filename):
	nft_number = filename.split('.')[0]
	return f'Colorful Distortion #{nft_number}'

filename_list = os.listdir('/Users/pigu/Dropbox/DATA/Documents/projekte/nft/drue/vier/collection')
series_name = 'csc'
nft_name_fun = nft_name_fun_csc
description = """Each piece features a sample of the official source code of Ethereum.
Generative Art by pifragile.
"""
collection_link = 'https://opensea.io/collection/crypto-source'

filename_list = [f'{i:04d}.gif' for i in range(16, 128)]
series_name = 'cfd'
description = "Generative Art by pifragile."
nft_name_fun = nft_name_fun_cfd
collection_link = 'https://opensea.io/collection/colorful-distortion'

for filename in filename_list:

	if not filename.split('.')[-1] == 'gif':
		continue

	with open(f'processed_files_{series_name}.txt', 'r') as processed_files:
		if filename in processed_files.read().splitlines():
			print(f'Skipping file {filename}')
			continue	

	name = nft_name_fun(filename)

	nft_url = list_nft(name, filename, description, collection_link)

	with open(os.path.join('nft_data', f'nfts_{series_name}.csv'), 'a') as nft_file:
		nft_file.write(f'{filename},{name},{nft_url}\n')

	with open(f'processed_files_{series_name}.txt', 'a') as processed_files:
		processed_files.write(f'{filename}\n')
	i+=1
	if i > 100:
		break
