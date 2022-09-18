from distutils.log import debug
from random import choice as random_choice
from time import time
from cmath import inf
from copy import deepcopy

debugPrint = False
debugCounter = 0
debugMode = False

class TileType:

	DeadEnd = 0
	Corner = 1
	Hallway = 2
	Triple = 3
	Quad = 4

class TileDeck:

	def __init__(self, debugMode = False) -> None:
		self.debugMode = debugMode
		self.tiles = []
		self.tiles.extend([TileType.DeadEnd for _ in range(3)])
		self.tiles.extend([TileType.Corner for _ in range(4)])
		self.tiles.extend([TileType.Hallway for _ in range(1)])
		self.tiles.extend([TileType.Triple for _ in range(8)])
		self.tiles.extend([TileType.Quad for _ in range(4)])

		# Return this if we're in debug mode
		self.debugTiles = [TileType.DeadEnd, TileType.DeadEnd, TileType.DeadEnd, TileType.Quad]

	def GetPossibleTilesTypes(self):
		types = []
		for type in [TileType.DeadEnd, TileType.Corner, TileType.Hallway, TileType.Triple, TileType.Quad]:
			if type in self.tiles:
				types.append(type)
		return types

	def PopTile(self, tileType):
		try:
			self.tiles.remove(tileType)
		except ValueError:
			print("trying to pop tileType of", tileType)
			print(self.tiles)
			raise

	def Empty(self):
		if self.debugMode:
			return len(self.debugTiles)
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
		self.North = 8
		self.East = 4
		self.South = 2
		self.West = 1
		self.start = (0, 1)

	def Duplicate(self):
		newShip = Ship()
		newShip.ship = deepcopy(self.ship)
		return newShip

	def Print(self, stdout = False):
		for h in range(len(self.ship)):
			for tileHeight in range(5):
				for w in range(len(self.ship[h])):
					for tileWidth in range(9):
						width = tileWidth % 9
						height = tileHeight % 5

						if width == 0 or width == 8:
							if stdout:
								print(" ", end="")
							if debugPrint:
								logFile.write(" ")
						elif height == 0 or height == 4:
							if stdout:
								print("-", end="")
							if debugPrint:
								logFile.write("-")
						elif width == 1 or width == 7:
							if stdout:
								print("|", end="")
							if debugPrint:
								logFile.write("|")
						elif (width == 4 and height == 1) and self.ship[h][w] & self.North == self.North:
							if stdout:
								print("N", end="")
							if debugPrint:
								logFile.write("N")
						elif (width == 4 and height == 3) and self.ship[h][w] & self.South == self.South:
							if stdout:
								print("S", end="")
							if debugPrint:
								logFile.write("S")
						elif (width == 3 and height == 2) and self.ship[h][w] & self.West == self.West:
							if stdout:
								print("W", end="")
							if debugPrint:
								logFile.write("W")
						elif (width == 5 and height == 2) and self.ship[h][w] & self.East == self.East:
							if stdout:
								print("E", end="")
							if debugPrint:
								logFile.write("E")
						else:
							if stdout:
								print(" ", end="")
							if debugPrint:
								logFile.write(" ")
				if stdout:
					print()
				if debugPrint:
					logFile.write("\n")

	def ConvertTileTypeToTile(self, tileType):
		if tileType == TileType.DeadEnd:
			return 1
		elif tileType == TileType.Corner:
			return 3
		elif tileType == TileType.Hallway:
			return 5
		elif tileType == TileType.Triple:
			return 7
		else:
			return 15

	def GetPossibleTileOrientations(self, tile):
		orientations = [tile]
		for _ in range(3):
			if tile > 8:
				tile = ((tile - 8) << 1 ) + 1
				if tile not in orientations:
					orientations.append(tile)
			else:
				tile = tile << 1
				if tile not in orientations:
					orientations.append(tile)
		return orientations

	def PlaceTile(self, tile, y, x):
		while len(self.ship) < y:
			self.ship.append([])
		if x == 0:
			for h in range(len(self.ship)):
				if h == y - 1:
					self.ship[h].insert(0, tile)
				else:
					self.ship[h].insert(0, 0)
			startY, startX = self.start
			self.start = (startY, startX + 1)
		else:
			while len(self.ship[y - 1]) < x:
				self.ship[y - 1].append(0)
			self.ship[y - 1][x - 1] = tile
		sizes = [len(h) for h in self.ship]
		for h in self.ship:
			if len(h) < max(sizes):
				padding = [0 for p in range(max(sizes) - len(h))]
				h.extend(padding)

	def GetPlayableLocationsForTile(self, tile):
		available = self.GetAvailableShipLocations()
		availableLocationsString = ""
		for location in available:
			availableLocationsString += (str(location) + " ")
		if debugPrint:
			logFile.write("Available locations are " + availableLocationsString + "\n")
		playable = self.GetPlayableFromAvailableLocations(available, tile)
		playableLocationsString = ""
		for location in playable:
			playableLocationsString += (str(location) + " ")
		if debugPrint:logFile.write("Playable locations are " + playableLocationsString + "\n")
		return playable

	def GetAvailableShipLocations(self):
		availableLocations = []
		for h in range(len(self.ship)):
			for w in range(len(self.ship[h])):
				if debugPrint:
					logFile.write(f"Checking location ({h}, {w})\n")
				if self.ship[h][w] & self.North == self.North:
					if h - 1 >= 0 and self.ship[h - 1][w] == 0:
						if debugPrint:
							logFile.write(f"  Adding location N {(h, w + 1)}\n")
						if (h, w + 1) not in availableLocations:
							availableLocations.append((h, w + 1))
				if self.ship[h][w] & self.East == self.East:
					if w + 1 == len(self.ship[h]):
						if (h + 1, w + 2) not in availableLocations:
							availableLocations.append((h + 1, w + 2))
							if debugPrint:
								logFile.write(f"  Adding location Ei {(h + 1, w + 2)}\n")
					elif self.ship[h][w + 1] == 0:
						if (h + 1, w + 2) not in availableLocations:
							availableLocations.append((h + 1, w + 2))
							if debugPrint:
								logFile.write(f"  Adding location Ee {(h + 1, w + 2)}\n")
				if self.ship[h][w] & self.South == self.South:
					if h + 1 == len(self.ship):
						if (h + 2, w + 1) not in availableLocations:
							availableLocations.append((h + 2, w + 1))
							if debugPrint:
								logFile.write(f"  Adding location Si {(h + 2, w + 1)}\n")
					elif self.ship[h + 1][w] == 0:
						if (h + 2, w + 1) not in availableLocations:
							availableLocations.append((h + 2, w + 1))
							if debugPrint:
								logFile.write(f"  Adding location Se {(h + 2, w + 1)}\n")
				if self.ship[h][w] & self.West == self.West:
					if w - 1 == -1:
						if (h + 1, 0) not in availableLocations:
							availableLocations.append((h + 1, 0))
							if debugPrint:
								logFile.write(f"  Adding location Wi {(h + 1, 0)}\n")
					elif self.ship[h][w - 1] == 0:
						if (h + 1, w) not in availableLocations:
							availableLocations.append((h + 1, w))
							if debugPrint:
								logFile.write(f"  Adding location We {(h + 1, w)}\n")
		return availableLocations

	def GetPlayableFromAvailableLocations(self, availableLocations, tile):
		allowedLocations = []
		for location in availableLocations:
			allowed = True
			y = location[0] - 2
			x = location[1] - 1
			if y == -1 and tile & self.North == self.North:
				allowed = False
			if y in range(len(self.ship)) and x in range(len(self.ship[y])) and self.ship[y][x] != 0 and ((self.ship[y][x] & self.South == self.South) != (tile & self.North == self.North)):
				allowed = False
			y = location[0] - 1
			x = location[1]
			if y in range(len(self.ship)) and x in range(len(self.ship[y])) and self.ship[y][x] != 0 and ((self.ship[y][x] & self.West == self.West) != (tile & self.East == self.East)):
				allowed = False
			y = location[0]
			x = location[1] - 1
			if y in range(len(self.ship)) and x in range(len(self.ship[y])) and self.ship[y][x] != 0 and ((self.ship[y][x] & self.North == self.North) != (tile & self.South == self.South)):
				allowed = False
			y = location[0] - 1
			x = location[1] - 2
			if y in range(len(self.ship)) and x in range(len(self.ship[y])) and self.ship[y][x] != 0 and ((self.ship[y][x] & self.East == self.East) != (tile & self.West == self.West)):
				allowed = False
			if allowed:
				allowedLocations.append(location)
		return allowedLocations

	def GetMaxDistanceWavefront(self):
		y, x = self.start
		queue = [(y, x, 0)]
		visited = []
		maxDistance = -1
		while len(queue):
			y, x, distance = queue.pop(-1)
			if distance > maxDistance:
				maxDistance = distance
			visited.append((y, x))
			if y - 1 >= 0 and self.ship[y][x] & self.North == self.North and self.ship[y - 1][x] & self.South == self.South:
				if (y - 1, x) not in visited:
					queue.append((y - 1, x, distance + 1))
			if x + 1 < len(self.ship[0]) and self.ship[y][x] & self.East == self.East and self.ship[y][x + 1] & self.West == self.West:
				if (y, x + 1) not in visited:
					queue.append((y, x + 1, distance + 1))
			if y + 1 < len(self.ship) and self.ship[y][x] & self.South == self.South and self.ship[y + 1][x] & self.North == self.North:
				if (y + 1, x) not in visited:
					queue.append((y + 1, x, distance + 1))
			if x - 1 >= 0 and self.ship[y][x] & self.West == self.West and self.ship[y][x - 1] & self.East == self.East:
				if (y, x - 1) not in visited:
					queue.append((y, x - 1, distance + 1))
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
		if debugPrint:
			logFile.write("Getting children of tileType " + tileTypesString + "\n")
		if debugPrint:
			logFile.write(f"Existing children: {len(self.children)}\n")
		self.ship.Print()
		for possibleTileType in tileTypes:
			placable = False
			for tile in self.ship.GetPossibleTileOrientations(self.ship.ConvertTileTypeToTile(possibleTileType)):
				for location in self.ship.GetPlayableLocationsForTile(tile):
					placable = True
					if debugPrint:
						logFile.write("Adding location " + str(location) + "\n")
					newShip = self.ship.Duplicate()
					newShip.PlaceTile(tile, location[0], location[1])
					if debugPrint:
						logFile.write("Creating new ship that looks like\n")
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
		remainingTileTypes = self.tileDeck.GetPossibleTilesTypes()
		if len(remainingTileTypes):
			remainingPlacableTileTypes = 0
			for possibleTileType in remainingTileTypes:
				placable = False
				for tile in self.ship.GetPossibleTileOrientations(self.ship.ConvertTileTypeToTile(possibleTileType)):
					for _ in self.ship.GetPlayableLocationsForTile(tile):
						placable = True
						break
					if placable:
						break
				if placable:
					remainingPlacableTileTypes += 1
				else:
					pass
					# print(f"  Cannot place tileType {possibleTileType}")
			playableTilesMultiplier = (float(remainingPlacableTileTypes) / float(len(remainingTileTypes))) ** 3
		else:
			playableTilesMultiplier = 1.0

		# Number of spaces available for tiles
		availableLocations = len(self.ship.GetAvailableShipLocations())

		# How walkable is the ship?
		wavefrontDistance = self.ship.GetMaxDistanceWavefront()
		
		# Empty tiles
		emptyTiles = 0
		for h in self.ship.ship:
			for w in h:
				if w == 0:
					emptyTiles += 1

		# Number of tiles left
		tilesLeft = len(self.tileDeck.tiles)

		# Collective value
		return ((20 - tilesLeft) * availableLocations * playableTilesMultiplier) - ((wavefrontDistance + emptyTiles / 4) ** 2)
		
		# value = ((1000 - tilesLeft) * playableTilesMultiplier) # - ((wavefrontDistance + (emptyTiles)) * 2)
		
		# print(f"State Value Calculation: (1000 - {tilesLeft}) * {playableTilesMultiplier}", end="")
		return value

def AStarDepth2(state, tileType):
	global debugCounter

	if debugPrint:
		logFile.write(f"Running A*3 on tileType {tileType}\n")
	state.ship.Print()

	bestChildValue = -inf
	bestMove = None
	childStates  = state.GetChildren([tileType])
	for childState in childStates:

		# print("Checking child state")
		# childState.ship.Print(stdout=True)
		grandchildrenValue = 0
		grandchildrenStates = childState.GetChildren(None)
		if childState.type == StateType.Win:
			childValue = 1000
		if childState.type == StateType.Loss:
			childValue = -1000
		else:
			for grandchildState in grandchildrenStates:

				# print("Checking grandchild state")
				# grandchildState.ship.Print(stdout=True)
				if grandchildState.type == StateType.Win:
					greatGrandchildValue = 1000
				if grandchildState.type == StateType.Loss:
					greatGrandchildValue = -1000
				else:
					greatGrandchildValue = (1.0 / len(grandchildrenStates)) * grandchildState.ComputeStateValue()
				grandchildrenValue += greatGrandchildValue # (1.0 / len(grandchildrenStates)) * grandchildState.ComputeStateValue()
				# print(f" * 1 / {len(grandchildrenStates)} = {greatGrandchildValue}")

			childValue = (1.0 / len(childStates)) * grandchildrenValue
		# print(f"Child Value = 1 / {len(childStates)} * {grandchildrenValue} = {childValue}")
		if childValue > bestChildValue:
			bestChildValue = childValue
			bestMove = childState.move

	return (bestMove, bestChildValue)


# ship = Ship()
# ship.PlaceTile(4, 1, 0)
# ship.PlaceTile(1, 1, 5)
# ship.Print(stdout=True)
# tileDeck = TileDeck(debugMode=False)
# state = State(ship, tileDeck, StateType.Node, None, None)
# move, cost = AStarDepth2(state, tileType=TileType.DeadEnd)
# print(f"Best move {move.tile} at ({move.y}, {move.x})")
# state.ship.PlaceTile(move.tile, move.y, move.x)
# state.ship.Print(stdout=True)
# exit(0)


with open("C:\\Users\\jonny\\OneDrive\\Documents\\PiratesCode.log", 'w+') as logFile:


	if debugMode:
		gameCount = 1
		printTurns = True
	else:
		gameCount = 10
		printTurns = False

	wins = 0
	losses = 0
	for game in range(gameCount):

		print("Starting game", game + 1)
		gameStart = time()
		ship = Ship()
		tileDeck = TileDeck(debugMode=debugMode)
		state = State(ship, tileDeck, StateType.Node, None, None)
		tileOrder = []

		# for tile in debugTileOrder:
		while not tileDeck.Empty():
			tile = tileDeck.GetRandomTile()
			tileOrder.append(tile)

			if printTurns:
				print("Remaining tiles", tileDeck.tiles)

			if printTurns:
				print("Placing tile type", tile)
			if debugPrint:
				logFile.write(f"Placing tile type {tile}\n")

			turnStart = time()
			bestMove, value = AStarDepth2(state, tile)
			if printTurns:
				print(f"Visited {debugCounter} states")
			if debugPrint:
				logFile.write(f"Visited {debugCounter} states\n")
			debugCounter = 0

			if debugPrint:
				logFile.write(f"Best move: {bestMove}\n")
			if bestMove is None:
				print("I think we lost :(")
				print("Tile we can't place", tile)
				print("Tile order was", tileOrder)
				state.ship.Print(stdout=True)
				losses += 1
				break
			if printTurns:
				print(f"Best move {bestMove.tile} at ({bestMove.y}, {bestMove.x})")

			state.ship.PlaceTile(bestMove.tile, bestMove.y, bestMove.x)
			state.children = []
			if printTurns:
				state.ship.Print(stdout=True)
			state.tileDeck.PopTile(tile)
			if printTurns:
				print("Turn duration:", time() - turnStart)
			if debugPrint:
				logFile.write(f"Turn duration: {time() - turnStart}\n")

			if tileDeck.Empty():
				state.ship.Print(stdout=True)
				print(f"Victory! (time = {time() - gameStart}s)")
				print("Start point is ", state.ship.start)
				print("Wavefront distance is", state.ship.GetMaxDistanceWavefront())
				wins += 1
				break

	print(f"Win Percentage: {(wins / gameCount) * 100.0}%")
