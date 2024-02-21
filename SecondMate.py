from distutils.log import debug
from random import choice as random_choice
from time import time
from cmath import inf
from copy import deepcopy
from sys import stdout as STDOUT


class Logger(object):
	def __init__(self, stdout=False, logFile=False):
		self.stdout = stdout
		self.logFile = logFile
		if logFile:
			self.fd = open('PiratesCode.log', 'w+')
	def log(self, message, writeStdout=True, writeLogFile=True):
		if self.logFile and writeLogFile:
			self.fd.write(message)
		if self.stdout and writeStdout:
			STDOUT.write(message)

logger = Logger(stdout=True, logFile=True)
debugMode = False

class Coords:
	North = 8
	East = 4
	South = 2
	West = 1

class Tile:
	DeadEnd = 0
	Corner = 1
	Hallway = 2
	Triple = 3
	Quad = 4

	def ConvertToBitmask(tileType):
		if tileType == Tile.DeadEnd:
			return 1
		elif tileType == Tile.Corner:
			return 3
		elif tileType == Tile.Hallway:
			return 5
		elif tileType == Tile.Triple:
			return 7
		else:
			return 15

	def GetPossibleOrientations(tileBitmask):
		orientations = [tileBitmask]
		for _ in range(3):
			if tileBitmask >= 8:
				tileBitmask = ((tileBitmask - 8) << 1 ) + 1
			else:
				tileBitmask = tileBitmask << 1
			if tileBitmask not in orientations:
					orientations.append(tileBitmask)
		return orientations

class TileDeck:
	def __init__(self, debugMode = False) -> None:
		self.debugMode = debugMode
		self.tiles = []
		self.tiles.extend([Tile.DeadEnd for _ in range(3)])
		self.tiles.extend([Tile.Corner for _ in range(4)])
		self.tiles.extend([Tile.Hallway for _ in range(1)])
		self.tiles.extend([Tile.Triple for _ in range(8)])
		self.tiles.extend([Tile.Quad for _ in range(4)])

		# Return this if we're in debug mode
		# self.debugTiles = [Tile.DeadEnd, Tile.DeadEnd, Tile.DeadEnd, Tile.Quad]
		# self.debugTiles = [Tile.Corner, Tile.Corner, Tile.Corner, Tile.DeadEnd, Tile.DeadEnd]
		# self.debugTiles = [Tile.Corner, Tile.Corner, Tile.Corner, Tile.Corner, Tile.DeadEnd, Tile.DeadEnd, Tile.DeadEnd, Tile.Quad]
		# self.debugTiles = [Tile.Corner, Tile.Corner, Tile.Corner, Tile.Corner, Tile.DeadEnd, Tile.DeadEnd, Tile.DeadEnd, Tile.Quad]
		self.debugTiles = [1, 4, 1, 0, 1, 4, 4, 1, 3, 3, 3, 3, 3, 2, 0, 3, 0, 3, 3, 4] # = 11
		# self.debugTiles = [3, 3, 1, 3, 3, 3, 3, 0, 0, 3, 2, 4, 1, 0, 1, 1, 3, 4, 4, 4] # = 7 but spread out
		# self.debugTiles = [1, 1, 3, 3, 3, 0, 2, 3, 3, 0, 1, 3, 3, 0, 4, 4, 3, 4, 4, 1] # = 9
		# self.debugTiles = [3, 1, 2, 1, 3, 4, 1, 3, 4, 3, 3, 0, 4, 0, 4, 0, 3, 1, 3, 3] # = 6 (ok)
		# self.debugTiles = [1, 3, 4, 3, 4, 3, 3, 2, 1, 4, 1, 4, 3, 3, 0, 0, 3, 3, 0, 1] # = 7 but spread out
		# self.debugTiles = [3, 3, 1, 0, 0, 3, 3, 2, 3, 0, 1, 4, 3, 3, 4, 4, 1, 4, 1, 3] # = 9 pretty bad
		# self.debugTiles = [3, 3, 3, 3, 4, 3, 0, 0, 4, 1, 1, 4, 3, 2, 0, 4, 3, 1, 1, 3] # = 8 pretty bad

	def GetPossibleTilesTypes(self):
		types = []
		for type in [Tile.DeadEnd, Tile.Corner, Tile.Hallway, Tile.Triple, Tile.Quad]:
			if type in self.tiles:
				types.append(type)
		return types

	def PopTile(self, tileType):
		try:
			self.tiles.remove(tileType)
		except ValueError:
			logger.log(f"trying to pop tileType of {tileType}")
			raise

	def Empty(self):
		if self.debugMode:
			return len(self.debugTiles) == 0
		else:
			return len(self.tiles) == 0

	def GetRandomTile(self):
		if self.debugMode:
			return self.debugTiles.pop(0)
		else:
			return random_choice(self.tiles)

class Ship:

	def __init__(self) -> None:
		self.ship = [[7, 7, 7]]
		self.start = (0, 1)

	def Duplicate(self):
		newShip = Ship()
		newShip.ship = deepcopy(self.ship)
		return newShip

	def Print(self, stdout = False):
		yAxis = "     "
		for x in range(len(self.ship[0])):
			yAxis += f"    {x}    "
		logger.log(yAxis + "\n", stdout, stdout)
		for y in range(len(self.ship)):
			for tileHeight in range(5):
				if stdout:
					if tileHeight == 2:
						logger.log(f"  {y}  ", stdout, stdout)
					else:
						logger.log("     ", stdout, stdout)
				for x in range(len(self.ship[y])):
					for tileWidth in range(9):
						width = tileWidth % 9
						height = tileHeight % 5
						if width == 0 or width == 8:
							logger.log(" ", stdout, stdout)
						elif height == 0 or height == 4:
							logger.log("-", stdout, stdout)
						elif width == 1 or width == 7:
							logger.log("|", stdout, stdout)
						elif (width == 4 and height == 1) and self.ship[y][x] & Coords.North == Coords.North:
							logger.log("N", stdout, stdout)
						elif (width == 4 and height == 2) and self.ship[y][x] > 16:
							logger.log("X", stdout, stdout)
						elif (width == 4 and height == 3) and self.ship[y][x] & Coords.South == Coords.South:
							logger.log("S", stdout, stdout)
						elif (width == 3 and height == 2) and self.ship[y][x] & Coords.West == Coords.West:
							logger.log("W", stdout, stdout)
						elif (width == 5 and height == 2) and self.ship[y][x] & Coords.East == Coords.East:
							logger.log("E", stdout, stdout)
						else:
							logger.log(" ", stdout, stdout)
				logger.log("\n", stdout, stdout)

	def PlaceTile(self, tile, y, x):
		while len(self.ship) <= y:
			self.ship.append([0 for _ in range(len(self.ship[0]))])
		if x == -1:
			for row in range(len(self.ship)):
				self.ship[row].insert(0, 0)
			x = 0
			self.start = (self.start[0], self.start[1] + 1)
		elif x == len(self.ship[0]):
			for row in range(len(self.ship)):
				self.ship[row].append(0)
		self.ship[y][x] = tile

	def GetPlayableLocationsForTile(self, tileBitmask):
		playable = []
		for y, x in self.GetAvailableShipLocations():
			allowed = True
			for dy, dx, tileDir, oppositeDir in [(-1, 0, Coords.North, Coords.South), (0, 1, Coords.East, Coords.West), (1, 0, Coords.South, Coords.North), (0, -1, Coords.West, Coords.East)]:
				if tileBitmask & tileDir == tileDir:
					if y + dy >= 0 and y + dy < len(self.ship) and x + dx >= 0 and x + dx < len(self.ship[0]):
						if self.ship[y + dy][x + dx] != 0 and self.ship[y + dy][x + dx] & oppositeDir != oppositeDir:
							allowed = False
					elif y == 0 and tileDir & Coords.North == Coords.North:
						allowed = False
				else:
					if y + dy >= 0 and y + dy < len(self.ship) and x + dx >= 0 and x + dx < len(self.ship[0]):
						if self.ship[y + dy][x + dx] != 0 and self.ship[y + dy][x + dx] & oppositeDir != 0:
							allowed = False
			if allowed:
				playable.append((y, x))
		return playable

	def GetAvailableShipLocations(self):
		availableLocations = []
		for y in range(len(self.ship)):
			for x in range(len(self.ship[y])):
				for dy, dx, dir in [(-1, 0, Coords.North), (0, 1, Coords.East), (1, 0, Coords.South), (0, -1, Coords.West)]:
					if y + dy < 0:
						continue
					if self.ship[y][x] < 16 and self.ship[y][x] & dir == dir and (y + dy, x + dx) not in availableLocations:
						if 0 > x + dx or x + dx >= len(self.ship[0]) or y + dy >= len(self.ship):
							availableLocations.append((y + dy, x + dx))
						else:
							if self.ship[y + dy][x + dx] == 0:
								availableLocations.append((y + dy, x + dx))
		return availableLocations

	def GetMaxDistanceWavefront(self, startY, startX):
		y, x = startY, startX
		queue = [(y, x, 0)]
		visited = {(y, x): 0}
		while len(queue):
			y, x, distance = queue.pop()
			if visited[(y, x)] < distance:
				distance = visited[(y, x)]
			neighbors = []
			if y - 1 >= 0 and self.ship[y][x] & Coords.North == Coords.North and self.ship[y - 1][x] & Coords.South == Coords.South:
				neighbors.append((y - 1, x, distance + 1))
			if x + 1 < len(self.ship[0]) and self.ship[y][x] & Coords.East == Coords.East and self.ship[y][x + 1] & Coords.West == Coords.West:
				neighbors.append((y, x + 1, distance + 1))
			if y + 1 < len(self.ship) and self.ship[y][x] & Coords.South == Coords.South and self.ship[y + 1][x] & Coords.North == Coords.North:
				neighbors.append((y + 1, x, distance + 1))
			if x - 1 >= 0 and self.ship[y][x] & Coords.West == Coords.West and self.ship[y][x - 1] & Coords.East == Coords.East:
				neighbors.append((y, x - 1, distance + 1))
			for y, x, distance in neighbors:
				if (y, x) not in visited:
					visited[(y, x)] = distance
					queue.append((y, x, distance))
				else:
					if distance < visited[(y, x)]:
						visited[(y, x)] = distance
						queue.append((y, x, distance))
		maxDistance = -1
		for key in visited.keys():
			if visited[key] > maxDistance:
				maxDistance = visited[key]
		return maxDistance

class StateType:

	Node = 0
	Win = 1
	Loss = 2

class Move:

	def __init__(self, tile, y, x) -> None:
		self.tile = tile
		self.x = x
		self.y = y

class State:

	def __init__(self, ship, tileDeck, type, parent, move) -> None:
		self.ship = ship
		self.tileDeck = tileDeck
		self.children = []
		self.type = type
		self.parent = parent
		self.move = move

	def GetChildren(self, tileTypes = None):
		if self.type != StateType.Node:
			return []
		if tileTypes == None:
			tileTypes = self.tileDeck.GetPossibleTilesTypes()
		tileTypesString = ""
		for type in tileTypes:
			tileTypesString += str(type)
		self.ship.Print()
		for possibleTileType in tileTypes:
			placable = False
			for tile in Tile.GetPossibleOrientations(Tile.ConvertToBitmask(possibleTileType)):
				for location in self.ship.GetPlayableLocationsForTile(tile):
					placable = True
					newShip = self.ship.Duplicate()
					newShip.PlaceTile(tile, location[0], location[1])
					newShip.Print()
					newTileDeck = deepcopy(self.tileDeck)
					newTileDeck.PopTile(possibleTileType)
					newType = StateType.Win if newTileDeck.Empty() else StateType.Node
					self.children.append(State(newShip, newTileDeck, newType, self, Move(tile, location[0], location[1])))
			if not placable:
				newState = deepcopy(self)
				newState.type = StateType.Loss
				self.children.append(newState)
		return self.children

	def ComputeStateValue(self):
		if self.type == StateType.Loss:
			return -1000
		remainingTileTypes = self.tileDeck.GetPossibleTilesTypes()
		playableTilesScore = 100.0
		if len(remainingTileTypes):
			remainingPlacableTileTypes = 0
			for possibleTileType in remainingTileTypes:
				placable = False
				for tile in Tile.GetPossibleOrientations(Tile.ConvertToBitmask(possibleTileType)):
					for _ in self.ship.GetPlayableLocationsForTile(tile):
						placable = True
						break
					if placable:
						break
				if placable:
					remainingPlacableTileTypes += 1
				else:
					pass
			playableTilesScore = playableTilesScore * (float(remainingPlacableTileTypes) / float(len(remainingTileTypes)))
		return playableTilesScore - (max(self.ship.GetMaxDistanceWavefront(self.ship.start[0], self.ship.start[1]) - 2, 0)) ** 4

def AStar(state, maxDepth, depth=1):
	global debugCounter
	state.ship.Print()
	if depth < maxDepth:
		stateValue = 0
		childStates = state.GetChildren(None)
		for childState in childStates:
			stateValue += (1.0 / len(childStates)) * AStar(childState, maxDepth, depth + 1)
		return stateValue
	else:
		debugCounter += 1
		return state.ComputeStateValue()

if __name__ == "__main__":
	global debugCounter

	gameType = "automatic"
	# gameType = "manual"

	if debugMode:
		gameCount = 1
		printTurns = True
	else:
		gameCount = 100
		printTurns = False

	nTurns = -1
	turnCounter = 1

	wins = 0
	losses = 0
	wavefront_total = 0
	for game in range(gameCount):

		logger.log(f"Starting game {game + 1}\n")
		gameStart = time()
		ship = Ship()
		tileDeck = TileDeck(debugMode=debugMode)
		state = State(ship, tileDeck, StateType.Node, None, None)
		tileOrder = []

		while not tileDeck.Empty():
			if printTurns or gameType == "manual":
				state.ship.Print(stdout=True)
			if gameType == "automatic":
				tile = tileDeck.GetRandomTile()
			else:
				displayShip = Ship()
				displayShip.ship = [[]]
				possibleTileTypes = tileDeck.GetPossibleTilesTypes()
				selectionMap = {}
				for index, possibleTileType in enumerate(possibleTileTypes):
					tile = Tile.ConvertToBitmask(possibleTileType)
					selectionMap[index] = possibleTileType
					displayShip.ship[0].append(tile)
				logger.log("Tile Options\n")
				displayShip.Print(stdout=True)
				tileSelection = input(f"Enter your tile number (0 - {len(possibleTileTypes) - 1}) or -1 for manual edits: ")
				if tileSelection == "-1":
					y = input(f"Enter y (vertical): ")
					x = input(f"Enter x (horizontal): ")
					bitmask = input(f"Enter tile as bitmask: ")
					state.ship.ship[int(y)][int(x)] = int(bitmask)
					continue
				else:
					tile = selectionMap[int(tileSelection)]
			tileOrder.append(tile)

			if turnCounter == nTurns:
				logger.log(f"Ending game after {nTurns} turns\n")
				break

			if printTurns:
				logger.log(f"Remailing tiles: {tileDeck.tiles}\n")
				logger.log(f"Placing tile type {tile}\n")

			turnStart = time()
			bestMove = None
			bestMoveValue = -inf
			childStates = state.GetChildren([tile])
			debugCounter = 0
			for childState in childStates:
				value = AStar(childState, 2)
				if value > bestMoveValue:
					bestMove = childState.move
					bestMoveValue = value
			logger.log(f"Visited {debugCounter} states to decide on move\n")
			
			if bestMove is None:
				logger.log("I think we lost :(\n")
				logger.log(f"Tile we can't place {tile}\n")
				logger.log(f"Tile order was {tileOrder}\n")
				state.ship.Print(stdout=True)
				logger.log(f"Ship: {state.ship.ship}")
				losses += 1
				break
			if printTurns:
				logger.log(f"Best move {bestMove.tile} at ({bestMove.y}, {bestMove.x})\n")

			state.ship.PlaceTile(bestMove.tile, bestMove.y, bestMove.x)
			state.children = []
			state.tileDeck.PopTile(tile)
			if printTurns:
				logger.log(f"Turn duration: {time() - turnStart}\n")
			turnCounter += 1

			if tileDeck.Empty():
				state.ship.Print(stdout=True)
				logger.log(f"Victory! (time = {time() - gameStart}s)\n")
				logger.log(f"Start point is {state.ship.start}\n")
				wavefront_distance = state.ship.GetMaxDistanceWavefront(state.ship.start[0], state.ship.start[1])
				wavefront_total += wavefront_distance
				logger.log(f"Ship start point is {state.ship.start}\n")
				logger.log(f"Wavefront distance is {wavefront_distance}\n")
				logger.log(f"Ship: {state.ship.ship}")
				logger.log(f"Tile order: {tileOrder}\n")
				wins += 1
				break

	logger.log(f"Win Percentage: {(wins / gameCount) * 100.0}%\n")
	logger.log(f"Average size: {wavefront_total / gameCount}\n")
