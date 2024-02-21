from distutils.log import debug
from random import choice as random_choice
from time import time
from cmath import inf
from copy import deepcopy

debugPrint = True
debugCounter = 0
debugMode = True
logFile = None

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
		# self.debugTiles = [TileType.DeadEnd, TileType.DeadEnd, TileType.DeadEnd, TileType.Quad]
		# self.debugTiles = [TileType.Corner, TileType.Corner, TileType.Corner, TileType.DeadEnd, TileType.DeadEnd]
		# self.debugTiles = [TileType.Corner, TileType.Corner, TileType.Corner, TileType.Corner, TileType.DeadEnd, TileType.DeadEnd, TileType.DeadEnd, TileType.Quad]
		# self.debugTiles = [TileType.Corner, TileType.Corner, TileType.Corner, TileType.Corner, TileType.DeadEnd, TileType.DeadEnd, TileType.DeadEnd, TileType.Quad]
		self.debugTiles = [1, 4, 1, 0, 1, 4, 4, 1, 3, 3, 3, 3, 3, 2, 0, 3, 0, 3, 3, 4] # = 11
		# self.debugTiles = [3, 3, 1, 3, 3, 3, 3, 0, 0, 3, 2, 4, 1, 0, 1, 1, 3, 4, 4, 4] # = 7 but spread out
		# self.debugTiles = [1, 1, 3, 3, 3, 0, 2, 3, 3, 0, 1, 3, 3, 0, 4, 4, 3, 4, 4, 1] # = 9
		# self.debugTiles = [3, 1, 2, 1, 3, 4, 1, 3, 4, 3, 3, 0, 4, 0, 4, 0, 3, 1, 3, 3] # = 6 (ok)
		# self.debugTiles = [1, 3, 4, 3, 4, 3, 3, 2, 1, 4, 1, 4, 3, 3, 0, 0, 3, 3, 0, 1] # = 7 but spread out
		# self.debugTiles = [3, 3, 1, 0, 0, 3, 3, 2, 3, 0, 1, 4, 3, 3, 4, 4, 1, 4, 1, 3] # = 9 pretty bad
		# self.debugTiles = [3, 3, 3, 3, 4, 3, 0, 0, 4, 1, 1, 4, 3, 2, 0, 4, 3, 1, 1, 3] # = 8 pretty bad


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
		if stdout:
			print(self.ship)
			yAxis = "     "
			for x in range(len(self.ship[0])):
				yAxis += f"    {x}    "
			print(yAxis)
		for h in range(len(self.ship)):
			for tileHeight in range(5):
				if stdout:
					if tileHeight == 2:
						print(f"  {h}  ", end="")
					else:
						print("     ", end="")
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

	def GetMaxDistanceWavefront(self, startY, startX):
		y, x = startY, startX
		queue = [(y, x, 0)]
		visited = {(y, x): 0}
		while len(queue):
			y, x, distance = queue.pop()
			if visited[(y, x)] < distance:
				distance = visited[(y, x)]
			# print(f"Investigating location ({y}, {x}), distance = {distance}")
			neighbors = []
			if y - 1 >= 0 and self.ship[y][x] & self.North == self.North and self.ship[y - 1][x] & self.South == self.South:
				neighbors.append((y - 1, x, distance + 1))
			if x + 1 < len(self.ship[0]) and self.ship[y][x] & self.East == self.East and self.ship[y][x + 1] & self.West == self.West:
				neighbors.append((y, x + 1, distance + 1))
			if y + 1 < len(self.ship) and self.ship[y][x] & self.South == self.South and self.ship[y + 1][x] & self.North == self.North:
				neighbors.append((y + 1, x, distance + 1))
			if x - 1 >= 0 and self.ship[y][x] & self.West == self.West and self.ship[y][x - 1] & self.East == self.East:
				neighbors.append((y, x - 1, distance + 1))
			for y, x, distance in neighbors:
				if (y, x) not in visited:
					visited[(y, x)] = distance
					queue.append((y, x, distance))
					# print(f"Queueing neighbor ({y}, {x}) with distance = {distance}")
				else:
					if distance < visited[(y, x)]:
						# print(f"Found shorter path to ({y}, {x}) of distance = {distance}")
						visited[(y, x)] = distance
						queue.append((y, x, distance))
					# visited[(y, x)] = distance if distance < visited[(y, x)] else visited[(y, x)]
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
		# mode = "original"
		mode = "sockets"
		if mode == "original":
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
				playableTilesMultiplier = float(remainingPlacableTileTypes) / float(len(remainingTileTypes))
			else:
				playableTilesMultiplier = 1.0

			# Number of spaces available for tiles
			availableLocations = len(self.ship.GetAvailableShipLocations())

			# How walkable is the ship?
			maxWavefrontDistance = self.ship.GetMaxDistanceWavefront(self.ship.start[0], self.ship.start[1])

			# Number of tiles left
			tilesLeft = len(self.tileDeck.tiles)

			# Collective value
			# return ((20 - tilesLeft) * playableTilesMultiplier) - ((maxWavefrontDistance / 2))
			if self.type == StateType.Loss:
				return -1000
			return (1.0 - playableTilesMultiplier) * 100 - (maxWavefrontDistance)
			# return -maxWavefrontDistance
		if mode == "sockets":
			start = time()
			counter = 0
			ship = self.ship
			if self.type == StateType.Loss:
				return -1000
			# if self.type == StateType.Win:
			# 	return 100
			# for x in range(len(ship.ship[0])):
			# 	for y in range(len(ship.ship)):
			# 		if ship.ship[y][x] == 0:
			# 			if y - 1 >= 0 and ship.ship[y - 1][x] & ship.South == ship.South:
			# 				counter += 1
			# 				continue
			# 			if x + 1 < len(ship.ship[0]) and ship.ship[y][x + 1] & ship.West == ship.West:
			# 				counter += 1
			# 				continue
			# 			if y + 1 < len(ship.ship) and ship.ship[y + 1][x] & ship.North == ship.North:
			# 				counter += 1
			# 				continue
			# 			if x - 1 >= 0 and ship.ship[y][x - 1] & ship.East == ship.East:
			# 				counter += 1
			duration = time() - start
			# print(f"Method took {duration}s")
			return len(self.ship.GetAvailableShipLocations()) - (max(self.ship.GetMaxDistanceWavefront(self.ship.start[0], self.ship.start[1]) - 2, 0)) ** 3


def AStarDepth2(state, tileType):
	global debugCounter

	if debugPrint:
		logFile.write(f"Running A*3 on tileType {tileType}\n")
	state.ship.Print()

	bestChildValue = -inf
	bestMove = None
	childStates  = state.GetChildren([tileType])
	for childState in childStates:

		grandchildrenValue = 0
		grandchildrenStates = childState.GetChildren(None)
		if childState.type == StateType.Win or childState.type == StateType.Loss:
			childValue = childState.ComputeStateValue()
		# 	childValue = 1000
		# if childState.type == StateType.Loss:
		# 	childValue = -1000
		else:
			for grandchildState in grandchildrenStates:

				# if grandchildState.type == StateType.Win:
				# 	greatGrandchildValue = 100
				# if grandchildState.type == StateType.Loss:
				# 	greatGrandchildValue = -1000
				# else:
				greatGrandchildValue = (1.0 / len(grandchildrenStates)) * grandchildState.ComputeStateValue()
				grandchildrenValue += greatGrandchildValue

			childValue = (1.0 / len(childStates)) * grandchildrenValue
		if childValue > bestChildValue:
			bestChildValue = childValue
			bestMove = childState.move

	return (bestMove, bestChildValue)

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


def AutomaticMode():
	global debugCounter
	global logFile
	with open("PiratesCode.log", 'w+') as logFile:


		if debugMode:
			gameCount = 1
			printTurns = True
		else:
			gameCount = 10
			printTurns = False

		wins = 0
		losses = 0
		wavefront_total = 0
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
				# bestMove, value = AStarDepth2(state, tile)
				bestMove = None
				bestMoveValue = -inf
				childStates = state.GetChildren([tile])
				debugCounter = 0
				for childState in childStates:
					value = AStar(childState, 2)
					if value > bestMoveValue:
						bestMove = childState.move
						bestMoveValue = value
				# print(f"Visited {debugCounter} states to determine move")

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
					wavefront_distance = state.ship.GetMaxDistanceWavefront(state.ship.start[0], state.ship.start[1])
					wavefront_total += wavefront_distance
					print("Wavefront distance is", wavefront_distance)
					print("Tile order:", tileOrder)
					wins += 1
					break

		print(f"Win Percentage: {(wins / gameCount) * 100.0}%")
		print(f"Average size: {wavefront_total / gameCount}")

def ManualMode():
	ship = Ship()
	tileDeck = TileDeck(debugMode=False)
	state = State(ship, tileDeck, StateType.Node, None, None)
	tileOrder = []

	while not tileDeck.Empty():

		displayShip = Ship()
		displayShip.ship = [[]]
		possibleTileTypes = tileDeck.GetPossibleTilesTypes()
		selectionMap = {}
		for index, possibleTileType in enumerate(possibleTileTypes):
			tile = displayShip.ConvertTileTypeToTile(possibleTileType)
			displayShip.PlaceTile(tile, 1, len(displayShip.ship[0]) + 1)
			selectionMap[index + 1] = possibleTileType
		print("Tile Options")
		displayShip.Print(stdout=True)
		tileSelection = input(f"Enter your tile number (1 - {len(possibleTileTypes)}): ")
		tileType = selectionMap[int(tileSelection)]
		tileOrder.append(tileType)
		bestMove, value = AStarDepth2(state, tileType)

		if bestMove is None:
			print("I think we lost :(")
			print("Tile we can't place", tileType)
			print("Tile order was", tileOrder)
			state.ship.Print(stdout=True)
			break
		print(f"Best move at ({bestMove.y}, {bestMove.x})")

		state.ship.PlaceTile(bestMove.tile, bestMove.y, bestMove.x)
		state.children = []
		state.ship.Print(stdout=True)
		state.tileDeck.PopTile(tileType)

		if tileDeck.Empty():
			state.ship.Print(stdout=True)
			print(f"Victory!")
			break


if __name__ == "__main__":
	AutomaticMode()
	# ManualMode()
