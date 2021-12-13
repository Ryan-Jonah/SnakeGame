#Classic Game #1: Snake
from pathlib import Path
import pygame
import time
import random

pygame.init()

#COLOURS
WHITE     = (255, 255, 255)
BLACK     = (0  , 0  , 0  )
RED       = (255, 0  , 0  )
GREEN     = (0  , 255, 0  )
BLUE      = (0  , 0  , 255)
DARKGREEN = (0  , 155, 0  )

#IMAGES
str(Path('Images/'))
img_SnakeHead = pygame.image.load(str(Path('Images/SnakeHead.png')))
img_Apple     = pygame.image.load(str(Path('Images/Apple.png')))
img_Icon      = pygame.image.load(str(Path('Images/Icon.png')))

#GAME WINDOW
display_width  = 800
display_height = 600
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Snake")
pygame.display.set_icon(img_Icon)

pygame.display.update()

clock = pygame.time.Clock()
fps = 30

#START SCREEN
def game_intro():

	intro = True

	while intro:
	
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
				
		if event.type == pygame.TEXTINPUT:
			if event.text == "c":
				intro = False
			if event.text == "q":
				pygame.quit()
				quit()
		
		gameDisplay.fill(WHITE)
		message_to_screen("Welcome to Snake!",
						  colour = GREEN,
						  y_displace = -100,
						  size = "large")
		message_to_screen("The objective of the game is to eat the red apples",
		                  colour = BLACK,
						  y_displace = -30)
		message_to_screen("the more apples you eat, the longer you become",
		                  colour = BLACK,
						  y_displace = 10)
		message_to_screen("but if your run into the edge or yourself, you die.",
		                  colour = BLACK,
						  y_displace = 50)
		message_to_screen("press C to play, P to pause or Q to quit",
		                  colour = BLACK,
						  y_displace = 180)
						  
		pygame.display.update()
		clock.tick(15)

#PAUSE FUNCTION
def pause():
	
	paused = True
	
	message_to_screen("Paused",
					  BLACK,
					  -100,
					  size = "large")
	
	message_to_screen("Press C to continue or Q to quit",
					  BLACK,
					  25)
					  
	pygame.display.update()
	
	while paused:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_c:
					paused = False
				elif event.key == pygame.K_q:
					pygame.quit()
					quit()
		
		clock.tick(15)
		
#SCORE FUNCTION
def score(score):		
	text = smallfont.render("Score: "+str(score), True, BLACK)
	gameDisplay.blit(text, [10,10])
	
#APPLE COORDINATES FUNCTION		
def randAppleGen(borderSize, objectSize):

	randAppleX = round(random.randrange(borderSize, display_width  - (objectSize + borderSize))) #/10.0)*10.0
	randAppleY = round(random.randrange(borderSize, display_height - (objectSize + borderSize))) #/10.0)*10.0
	
	return randAppleX, randAppleY
	
#SNAKE FUNCTION
direction = 'right'
def snake(lead_width, lead_height, snakeList):

	if direction == 'right':
		head = pygame.transform.rotate(img_SnakeHead, 270)
		
	if direction == 'left':
		head = pygame.transform.rotate(img_SnakeHead, 90)
		
	if direction == 'up':
		head = img_SnakeHead
		
	if direction == 'down':
		head = pygame.transform.rotate(img_SnakeHead, 180)
	
	gameDisplay.blit(head, (snakeList[-1][0], snakeList[-1][1]))

	for XnY in snakeList[:-1]:
		pygame.draw.rect(gameDisplay, DARKGREEN, [XnY[0],XnY[1], lead_width,lead_height])

#TEXT FUNCTIONS
smallfont = pygame.font.SysFont("arialms", 25)
medfont   = pygame.font.SysFont("arialms", 50)
largefont = pygame.font.SysFont("arialms", 80)

def text_objects(text, colour, size):
	if size == "small":
		textSurface = smallfont.render(text, True, colour)
	elif size == "medium":
		textSurface = medfont.render(text, True, colour)
	elif size == "large":
		textSurface = largefont.render(text, True, colour)
	return textSurface, textSurface.get_rect()

def message_to_screen(msg, colour, y_displace=0, size = "small"):
	textSurf, textRect = text_objects(msg, colour, size)
	textRect.center = (display_width/2), (display_height/2)+y_displace
	gameDisplay.blit(textSurf, textRect)

def gameLoop():

	#GAME CONDITIONS
	gameExit = False
	gameOver = False

	#SNAKE VARIABLES
	lead_x         = display_width/2
	lead_y         = display_height/2
	lead_width     = 20
	lead_height    = 20
	lead_x_change  = 1
	lead_y_change  = 0
	block_change   = 10
	border         = 10
	snakeList      = []
	snakeLength    = 1
	appleThickness = 20
	global direction
	
	#INITIAL APPLE VARIABLES
	randAppleX, randAppleY = randAppleGen(border, appleThickness)
	
	#MAIN LOOP
	while not gameExit:
	
		#GAMEOVER PROMPT
		if gameOver == True:
		
			message_to_screen("Game over", 
							  RED,
							  y_displace = -50,
							  size = "large")
			message_to_screen("press C to play again or Q to quit.", 
							  BLACK, 
							  y_displace = +50,
							  size = "medium")
			pygame.display.update()
		
		while gameOver == True:
				
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_q:
						gameExit = True
						gameOver = False
					elif event.key == pygame.K_c:
						direction = 'right'
						gameLoop()
				elif event.type == pygame.QUIT:
					gameOver = False
					gameExit = True
			
		#KEYPRESS EVENTS
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					if direction == 'right':
						continue
					lead_x_change = -block_change
					lead_y_change =  0
					direction = 'left'
				elif event.key == pygame.K_RIGHT:
					if direction == 'left':
						continue
					lead_x_change =  block_change
					lead_y_change =  0
					direction = 'right'
				elif event.key == pygame.K_UP:
					if direction == 'down':
						continue
					lead_y_change = -block_change
					lead_x_change =  0
					direction = 'up'
				elif event.key == pygame.K_DOWN:
					if direction == 'up':
						continue
					lead_y_change =  block_change
					lead_x_change =  0
					direction = 'down'
				elif event.key == pygame.K_p:
					pause()
					
			#QUIT EVENT
			if event.type == pygame.QUIT:
				gameOver = False
				gameExit = True
				
		#WALL COLLISION
		if lead_x >= display_width -lead_width or lead_x <= 0 or lead_y >= display_height -lead_height or lead_y <= 0:
			gameOver = True
			
		#SNAKE MOVEMENT
		lead_x += lead_x_change
		lead_y += lead_y_change
		
		#GAME WINDOW
		gameDisplay.fill(WHITE)
		pygame.draw.rect(gameDisplay, BLUE, [0,0, display_width,display_height], border)
		gameDisplay.blit(img_Apple, (randAppleX, randAppleY))
		
		#SNAKE LENGTH
		snakeHead = []
		snakeHead.append(lead_x)
		snakeHead.append(lead_y)
		snakeList.append(snakeHead)
		
		if len(snakeList) > snakeLength:
			del snakeList[0]
		
		#SELF COLLISION
		for eachSegment in snakeList[:-1]:
			if eachSegment == snakeHead:
				gameOver = True
		
		snake(lead_width, lead_height, snakeList)
		
		score(snakeLength-1)
		
		#APPLE COLLISION/RESET
		if lead_x >= randAppleX and lead_x <= randAppleX +appleThickness or lead_x +block_change >= randAppleX and lead_x +block_change <= randAppleX +appleThickness:
			if lead_y >= randAppleY and lead_y <= randAppleY +appleThickness:
				randAppleX, randAppleY = randAppleGen(border, appleThickness)
				snakeLength += 1
			elif lead_y +block_change >= randAppleY and lead_y +block_change <= randAppleY + appleThickness:
				randAppleX, randAppleY = randAppleGen(border, appleThickness)
				snakeLength += 1
			
		pygame.display.update()
		
		clock.tick(fps)

	#GAMEOVER MESSAGE
	pygame.display.update()

	pygame.quit()
	quit()

#GAME
game_intro()	
gameLoop()
