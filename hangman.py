########################################################################
## File Name: hangman.py                                              ##
## Description: Hangman game using words from Wordnik (eventually)    ##
########################################################################

from wordnik import swagger, WordsApi
from secrets import API_KEY, API_URL
import pygame
import math

pygame.init()
winHeight = 500
winWidth = 900
win=pygame.display.set_mode((winWidth,winHeight))

client = swagger.ApiClient(API_KEY, API_URL)

# initialize global variables/constants #
btn_font = pygame.font.SysFont("chalkduster", 20)
guess_font = pygame.font.SysFont("chalkduster", 24)
end_font = pygame.font.SysFont('sertomalankara', 40)
hangman_font = pygame.font.SysFont("chalkduster", 50)

hangmanPics = [pygame.image.load('images/hangman%s.png' % i) for i in range(7)]
background = pygame.image.load('images/background.png')

# Redraws window #
def redraw_game_window(word, buttons, guessed, limbs):
	WHITE = (255, 255, 255)
	win.blit(background, (0,0))
	
	# Draws buttons to select from
	for btn in buttons:
		if btn[4]:
			pygame.draw.circle(win, WHITE, (btn[1], btn[2]), btn[3])
			pygame.draw.circle(win, btn[0], (btn[1], btn[2]), btn[3] - 2)
			letter = btn_font.render(chr(btn[5]), 1, WHITE)
			win.blit(letter, (int(btn[1] - letter.get_width() / 2), int(btn[2] - letter.get_height() / 2)))

	spaced = spacedOut(word, guessed)
	label = guess_font.render(spaced, 1, WHITE)
	length = label.get_width()
	pic = hangmanPics[limbs]
	hangman = hangman_font.render("HANGMAN", 1, WHITE)

	win.blit(hangman, (5, winHeight - (hangman.get_height() + 10)))
	win.blit(label,(int(winWidth/2 - length/2), 400))
	win.blit(pic, (int(winWidth/2 - pic.get_width()/2 + 20), 150))
	pygame.display.update()

# Pulls a random word from an api #
def randomWord():
	wordapi = WordsApi.WordsApi(client)
	word = wordapi.getRandomWord()

	return word.word

# Determines what letters have already been identified #
def spacedOut(word, guessed):
	spacedWord = ''
	for char in word:
		if char.isalpha():
			if char.upper() in guessed:
				spacedWord += char + " " 
			else:
				spacedWord += '_ '
		else:
			spacedWord += char + ' '
	return spacedWord
			
def buttonHit(x, y, buttons):
	for btn in buttons:
		if math.sqrt(math.pow(btn[1] - x, 2) + math.pow(btn[2] - y, 2)) <= btn[3]:
			return btn[5]
	return None

def end(winner, word):
	WHITE = (255, 255, 255)
	pygame.time.delay(250)
	win.blit(background, (0,0))
	again = True

	text = 'WINNER!, press any key to play again...' if winner else 'You lost, press any key to play again...'
	
	label = end_font.render(text, 1, WHITE)
	wordTxt = end_font.render(word.upper(), 1, WHITE)
	wordWas = end_font.render('The phrase was: ', 1, WHITE)
	hangman = hangman_font.render("HANGMAN", 1, WHITE)

	win.blit(hangman, (5, winHeight - (hangman.get_height() + 10)))
	win.blit(label, (int(winWidth / 2 - label.get_width() / 2), 140))
	win.blit(wordWas, (int(winWidth/2 - wordWas.get_width()/2), 245))
	win.blit(wordTxt, (int(winWidth/2 - wordTxt.get_width()/2), 295))
	
	pygame.display.update()

	while again:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
			if event.type == pygame.KEYDOWN:
				again = False


def reset(buttons):
	for btn in buttons:
		btn[4] = True
	return (0, [], buttons, randomWord())

def main():
	limbs = 0
	guessed = []
	buttons = []
	word = ''

	# Setup buttons
	increase = round(winWidth / 13)
	for i in range(26):
		if i < 13:
			y = 40
			x = 25 + (increase * i)
		else:
			x = 25 + (increase * (i - 13))
			y = 85
		buttons.append([(115,115,115), x, y, 20, True, 65 + i])
		# buttons.append([color, x_pos, y_pos, radius, visible, char])

	word = randomWord()
	inPlay = True
	print(word)

	while inPlay:
		redraw_game_window(word, buttons, guessed, limbs)
		pygame.time.delay(10)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				inPlay = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					inPlay = False
			if event.type == pygame.MOUSEBUTTONDOWN:
				clickPos = pygame.mouse.get_pos()
				letter = buttonHit(clickPos[0], clickPos[1], buttons)
				if letter != None:
					guessed.append(chr(letter))
					buttons[letter - 65][4] = False
					if chr(letter).lower() not in word.lower():
						if limbs != 5:
							limbs += 1
						else:
							end(False, word)
							(limbs, guessed, buttons, word) = reset(buttons)
					else:
						# print(spacedOut(word, guessed))
						if spacedOut(word, guessed).count('_') == 0:
							end(True, word)
							(limbs, guessed, buttons, word) = reset(buttons)
	pygame.quit()

if __name__ == "__main__":
	main()