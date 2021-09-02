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

description = """Each piece features a sample of the official source code of Ethereum.
Generative Art by pifragile.
"""

def list_nft(name, file_name):
	print(f'adding file {filename}')
	wait_for_image('add.png')
	print('add..')
	# add item

	# change window
	pyautogui.click(1594, 239)

	pyautogui.click(1594, 239)
	time.sleep(0.05)

	wait_for_image('create.png')
	print('create..')
	# choose image
	pyautogui.click(637, 587)

	time.sleep(0.5)

	if not wait_for_image('collection.png', num_tries=2):
		# click again
		time.sleep(0.5)
		pyautogui.click(637, 587)

	wait_for_image('collection.png')

	# search field
	pyautogui.click(1292, 115)

	time.sleep(0.5)
	for c in file_name:
		pyautogui.write(c)

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
	wait_for_image('change.png')

	# name
	time.sleep(0.5)
	pyautogui.click(595, 873)
	time.sleep(0.5)

	pyautogui.write(name)
	time.sleep(0.05)

	# description
	pyautogui.scroll(-20)
	time.sleep(0.05)
	pyautogui.click(705, 452)
	time.sleep(0.5)

	pyautogui.write(description)
	time.sleep(0.05)

	pyautogui.scroll(-17)
	time.sleep(0.05)

	# create
	pyautogui.click(500, 903)
	time.sleep(0.05)


	wait_for_image('woot.png')
	print('ADDED')
	#close popup
	pyautogui.click(1078, 263)
	time.sleep(0.05)


	# sell
	pyautogui.click(1375, 232)
	time.sleep(0.05)
	print('sell..')

	# price
	wait_for_image('amount.png')
	pyautogui.click(923, 529)
	time.sleep(0.5)
	pyautogui.write('0.01')

	time.sleep(0.3)

	# post listing
	pyautogui.click(1199, 568)
	time.sleep(0.05)

	#sign
	wait_for_image('signature.png', num_tries=6)
	print('sign..')

	pyautogui.click(1579, 588)
	time.sleep(0.05)

	time.sleep(1)
	# handle when wallet crashes
	if wait_for_image('amount.png', num_tries=1):
		# post listing
		pyautogui.click(1163,613)
		time.sleep(0.05)

		#sign
		print('sign..')
		wait_for_image('signature.png')
		pyautogui.click(1579, 588)
		time.sleep(0.05)
		
	#view
	print('LISTED')
	wait_for_image('listed.png')
	print('copy url and return...')


	# copy url to clipboard
	pyautogui.click(696, 641)

	time.sleep(.5)
	url = pyperclip.paste()


	#close
	pyautogui.click(1155, 266)
	time.sleep(0.5)
	#back
	pyautogui.click(407, 84)
	time.sleep(0.05)
	pyautogui.write('https://opensea.io/collection/crypto-source')
	time.sleep(0.05)
	pyautogui.press('enter')
	time.sleep(0.05)

	return url

i = 0
for filename in os.listdir('/Users/pigu/Dropbox/DATA/Documents/projekte/nft/drue/vier/collection'):

	if not filename.split('.')[-1] == 'gif':
		continue

	with open('processed_files.txt', 'r') as processed_files:
		if filename in processed_files.read().splitlines():
			print(f'Skipping file {filename}')
			continue	

	name_parts = filename.split('.')[0].split('_')
	name_parts[-1] = str(int(name_parts[-1]) + 1)
	name_parts = [s.capitalize() for s in name_parts]
	name = ' '.join(name_parts)

	nft_url = list_nft(name, filename)

	with open('nfts.csv', 'a') as nft_file:
		nft_file.write(f'{filename},{name},{nft_url}\n')

	with open('processed_files.txt', 'a') as processed_files:
		processed_files.write(f'{filename}\n')
	i+=1
	if i > 100:
		break
