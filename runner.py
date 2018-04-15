#!/usr/bin/python3
import argparse, time, sys
import pygame
from extractor import parseSaveFile, dumpClass, writeSaveFile
from shutil import copyfile

selectedCellType = None
TYPE_WATER_DEEP = 1
TYPE_WATER_FRESH = 2
TYPE_WATER_SALT = 3
TYPE_FARM_BARREN = 4
TYPE_FARM_FERTILE = 5
TYPE_FARM_FERTILE_PLUS = 6
TYPE_RES_ROCK = 7
TYPE_RES_STONE = 8
TYPE_RES_IRON = 9
TYPE_TREE_NOTREE = 10
TYPE_TREE_TREE = 11

def drawmap(surface, mapObject, width, height):
	tilesize = 640.0/width
	for i in range(0, height):
		for j in range(0, width):
			color = (0, 0, 0)
			obj = mapObject[height * i + j]
			if obj["type"]["value__"].value == 0:
				#Land
				if obj["fertile"].value == 0:
					color = (193, 206, 100)
				elif obj["fertile"].value == 1:	
					color = (146, 190, 69)
				elif obj["fertile"].value == 2:
					color = (103, 154, 49)
					
			elif obj["type"]["value__"].value == 1:
				color = (255, 255, 255)
			elif obj["type"]["value__"].value == 2:
				#Stone
				color = (166, 166, 166)
			elif obj["type"]["value__"].value == 3:
				#Water
				if obj["deepWater"].value:
					color = (56, 137, 192)
				else:
					if obj["saltWater"].value:
						color = (167, 239, 254)
					else:
						color = (124, 199, 230)
			elif obj["type"]["value__"].value == 4:
				#Rock
				color = (64, 64, 64)
			elif obj["type"]["value__"].value == 5:
				#Iron
				color = (153, 102, 0)	

			#if additionalObjects[height * i + j] != None:
			#	color = (255, 0, 0)
			screen.fill(color, pygame.Rect((width - j - 1) * tilesize, i*tilesize, tilesize, tilesize))
			if obj["amount"].value > 0 and obj["type"]["value__"].value == 0:
				treesize = int(tilesize / 3.0)
				screen.fill((102, 51, 0), pygame.Rect((width - j - 1) * tilesize + treesize, i*tilesize + treesize, treesize, treesize))

		
def turnAllFarms(mapObject, dataFile):
	for i in mapObject:
		i["fertile"].update(dataFile, 2)

def clearMap(mapObject, dataFile):
	for i in mapObject:
		i["fertile"].update(dataFile, 0)
		i["deepWater"].update(dataFile, True)
		i["saltWater"].update(dataFile, False)
		i["type"]["value__"].update(dataFile, 3)
		
def processMouseEvent(event, screen, mapObject, width, height, dataFile):
	global selectedCellType
	if event[0] > 640:
	
		pos = event[0] - 640
		pos /= 66
		pos = int(pos)
	
		if event[1] >= 60 and event[1] <= 126:
			if pos == 0:
				selectedCellType = TYPE_WATER_SALT
			elif pos == 1:
				selectedCellType = TYPE_WATER_FRESH
			else:
				selectedCellType = TYPE_WATER_DEEP
			
		elif event[1] >= 172 and event[1] <= 238:
			if pos == 0:
				selectedCellType = TYPE_FARM_BARREN
			elif pos == 1:
				selectedCellType = TYPE_FARM_FERTILE
			elif pos == 2:
				selectedCellType = TYPE_FARM_FERTILE_PLUS
		elif event[1] >= 278 and event[1] <= 344:
			if pos == 0:
				selectedCellType = TYPE_RES_ROCK
			elif pos == 1:
				selectedCellType = TYPE_RES_STONE
			elif pos == 2:
				selectedCellType = TYPE_RES_IRON			
		elif event[1] >= 384 and event[1] <= 450:
			if pos == 0:
				selectedCellType = TYPE_TREE_TREE
			elif pos == 1:
				selectedCellType = TYPE_TREE_NOTREE
			
	else:
		tileX = width - int(event[0] * (width / 640.0)) - 1
		tileY = int(event[1] * (height / 640.0))
		selectedTile = mapObject[tileY * width + tileX]
		if selectedCellType == TYPE_WATER_DEEP:
			selectedTile["type"]["value__"].update(dataFile, 3)
			selectedTile["deepWater"].update(dataFile, True)
		elif selectedCellType == TYPE_WATER_FRESH:
			selectedTile["type"]["value__"].update(dataFile, 3)
			selectedTile["deepWater"].update(dataFile, False)
			selectedTile["saltWater"].update(dataFile, False)
		elif selectedCellType == TYPE_WATER_SALT:
			selectedTile["type"]["value__"].update(dataFile, 3)
			selectedTile["deepWater"].update(dataFile, False)
			selectedTile["saltWater"].update(dataFile, True)
		elif selectedCellType == TYPE_FARM_BARREN:
			selectedTile["type"]["value__"].update(dataFile, 0)
			selectedTile["fertile"].update(dataFile, 0)
		elif selectedCellType == TYPE_FARM_FERTILE:
			selectedTile["type"]["value__"].update(dataFile, 0)
			selectedTile["fertile"].update(dataFile, 1)
		elif selectedCellType == TYPE_FARM_FERTILE_PLUS:
			selectedTile["type"]["value__"].update(dataFile, 0)
			selectedTile["fertile"].update(dataFile, 2)
		elif selectedCellType == TYPE_RES_ROCK:
			selectedTile["type"]["value__"].update(dataFile, 4)
		elif selectedCellType == TYPE_RES_STONE:
			selectedTile["type"]["value__"].update(dataFile, 2)
		elif selectedCellType == TYPE_RES_IRON:
			selectedTile["type"]["value__"].update(dataFile, 5)
		elif selectedCellType == TYPE_TREE_TREE:
			selectedTile["amount"].update(dataFile, 3)
		elif selectedCellType == TYPE_TREE_NOTREE:
			selectedTile["amount"].update(dataFile, 0)
		
		
		drawmap(screen, mapObject, gridWidth, gridHeight)
		
parser = argparse.ArgumentParser(description="Kingdoms and Castles save editor.")
parser.add_argument("--input", "-i", help="the path to your save file", required=True)
parser.add_argument("--gui", "-g", help="launches the GUI", action="store_true")
args = parser.parse_args()

savefile = args.input
savefile_backup = args.input + "-" + time.strftime("%Y%m%d%H%M%S")
print("Making a backup copy of", savefile, "to", savefile_backup)
try:
	copyfile(savefile, savefile_backup)
except FileNotFoundError:
	print("The savefile does not exists !")
	sys.exit(1)
	
mainObjects, dataFile = parseSaveFile(savefile_backup)
print("Loaded save for town", mainObjects["TownNameUI+TownNameSaveData"]["townName"].value)
gridWidth = mainObjects["World+WorldSaveData"]["gridWidth"].value
gridHeight = mainObjects["World+WorldSaveData"]["gridHeight"].value
print("The map is", gridWidth, "by", gridHeight)
mapObject = mainObjects["Cell+CellSaveData"].classBase.instances
additionalObjects = [None] * len(mapObject)

if "Building+BuildingSaveData" in mainObjects:
	for i in range(0, len(mainObjects["Building+BuildingSaveData"].classBase.instances)):
		posX = int(mainObjects["Building+BuildingSaveData"].classBase.instances[i]["globalPosition"]["x"][0])
		posY = int(mainObjects["Building+BuildingSaveData"].classBase.instances[i]["globalPosition"]["z"][0])
		additionalObjects[posX + posY * gridWidth] = mainObjects["Building+BuildingSaveData"].classBase.instances[i]["uniqueName"].value


if args.gui != None:
	print("Loading GUI...")
	screen = pygame.display.set_mode((840, 640))
	pygame.font.init()
	mainfont = pygame.font.SysFont("Arial", 20)
	smallfont = pygame.font.SysFont("Arial", 14)
	
	pygame.draw.line(screen, (255, 255, 255), (640, 0), (640, 640))
	screen.blit(mainfont.render('Water', False, (255, 255, 255)), (700, 30))
	pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(641, 60, 66, 66), 1)
	screen.blit(mainfont.render('Salt', False, (255, 255, 255)), (660, 66))
	pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(707, 60, 66, 66), 1)
	screen.blit(mainfont.render('Fresh', False, (255, 255, 255)), (716, 66))
	pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(773, 60, 66, 66), 1)
	screen.blit(mainfont.render('Deep', False, (255, 255, 255)), (783, 66))

	screen.blit(mainfont.render('Farm', False, (255, 255, 255)), (700, 136))
	pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(641, 166, 66, 66), 1)
	screen.blit(mainfont.render('Barren', False, (255, 255, 255)), (645, 172))
	pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(707, 166, 66, 66), 1)
	screen.blit(mainfont.render('Fertile', False, (255, 255, 255)), (716, 172))
	pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(773, 166, 66, 66), 1)
	screen.blit(mainfont.render('Fertile+', False, (255, 255, 255)), (773, 172))
	
	screen.blit(mainfont.render('Ressources', False, (255, 255, 255)), (700, 242))
	pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(641, 272, 66, 66), 1)
	screen.blit(mainfont.render('Rock', False, (255, 255, 255)), (645, 278))
	pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(707, 272, 66, 66), 1)
	screen.blit(mainfont.render('Stone', False, (255, 255, 255)), (716, 278))
	pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(773, 272, 66, 66), 1)
	screen.blit(mainfont.render('Iron', False, (255, 255, 255)), (773, 278))

	screen.blit(mainfont.render('Trees', False, (255, 255, 255)), (700, 348))
	pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(641, 378, 66, 66), 1)
	screen.blit(mainfont.render('Trees', False, (255, 255, 255)), (645, 384))
	pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(707, 378, 66, 66), 1)
	screen.blit(mainfont.render('Notree', False, (255, 255, 255)), (716, 384))

	
	screen.blit(smallfont.render('Press F to turn all farms fertile+', False, (255, 255, 255)), (640, 490))
	screen.blit(smallfont.render('Press C to clear the map', False, (255, 255, 255)), (640, 510))

	
	drawmap(screen, mapObject, gridWidth, gridHeight)
	pygame.display.flip()
	
	
	
	running = True
	isMouseDown = False
	while running:
		event = pygame.event.wait()
		if event.type == pygame.QUIT:
			running = False
			writeSaveFile(savefile, dataFile)
		elif event.type == pygame.MOUSEBUTTONDOWN:
			processMouseEvent(event.pos, screen, mapObject, gridWidth, gridHeight, dataFile)
			isMouseDown = True
			pygame.display.flip()
		elif event.type == pygame.MOUSEBUTTONUP:
			isMouseDown = False
		elif event.type == pygame.MOUSEMOTION:
			if isMouseDown:
				processMouseEvent(event.pos, screen, mapObject, gridWidth, gridHeight, dataFile)
				pygame.display.flip()		
		elif event.type == pygame.KEYDOWN:
			if event.unicode == "f" or event.unicode == "F":
				turnAllFarms(mapObject, dataFile)
				drawmap(screen, mapObject, gridWidth, gridHeight)
				pygame.display.flip()
			elif event.unicode == "c" or event.unicode == "C":
				clearMap(mapObject, dataFile)
				drawmap(screen, mapObject, gridWidth, gridHeight)
				pygame.display.flip()
