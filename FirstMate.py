from random import choice as random_choice
from time import time
# 

# def drawCard(north, east, south, west):

# 	top = [' ', ' ', ' ', ' ', ' ', ' ', ' ']
# 	middle = [' ', ' ', ' ', ' ', ' ', ' ', ' ']
# 	bottom = [' ', ' ', ' ', ' ', ' ', ' ', ' ']

# 	if north:
# 		top[3] = u'\u25b2'
# 	if east:
# 		middle[5] = u'\u25b6'
# 	if south:
# 		bottom[3] = u'\u25bc'
# 	if west:
# 		middle[0] = u'\u25c0'

# 	print(u'\u250f' + u'\u2501' + u'\u2501' + u'\u2501' + u'\u2501' + u'\u2501' + u'\u2501' + u'\u2501' + u'\u2513')
# 	print(u'\u2503' + "".join(top) + u'\u2503')
# 	print(u'\u2503' + "".join(middle) + u'\u2503')
# 	print(u'\u2503' + "".join(bottom) + u'\u2503')
# 	print(u'\u2517' + u'\u2501' + u'\u2501' + u'\u2501' + u'\u2501' + u'\u2501' + u'\u2501' + u'\u2501' + u'\u251b')


# # Single
# single_1 = u'\u2515'

# # Triple
# triple_1 = u'\u253b'

# # Quad
# quad = u'\u254b'

# drawCard(north=True, east=True, south=True, west=True)
# print(single_1)
# print(quad)
# print(triple_1)
from cmath import inf
from copy import deepcopy

debugPrint = False

class TileType:

	DeadEnd = 0
	Corner = 1
	Hallway = 2
	Triple = 3
	Quad = 4

class TileDeck:

	def __init__(self) -> None:
		self.tiles = []
		self.tiles.extend([TileType.DeadEnd for _ in range(3)])
		self.tiles.extend([TileType.Corner for _ in range(4)])
		self.tiles.extend([TileType.Hallway for _ in range(1)])
		self.tiles.extend([TileType.Triple for _ in range(8)])
		self.tiles.extend([TileType.Quad for _ in range(4)])

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
		return len(self.tiles) == 0

	def GetRandomTile(self):
		return random_choice(self.tiles)
		# tile = random_choice(self.tiles)
		# self.PopTile(tile)
		# return tile

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
		# return self.GetPlayableFromAvailableLocations(self.GetAvailableShipLocations(), tile)

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
		# print("Available:", availableLocations)
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
			if y - 1 > 0 and self.ship[y][x] & self.North == self.North and self.ship[y - 1][x] & self.South == self.South:
				if (y - 1, x) not in visited:
					queue.append((y - 1, x, distance + 1))
			if x + 1 < len(self.ship[0]) and self.ship[y][x] & self.East == self.East and self.ship[y][x + 1] & self.West == self.West:
				if (y, x + 1) not in visited:
					queue.append((y, x + 1, distance + 1))
			if y + 1 < len(self.ship) and self.ship[y][x] & self.South == self.South and self.ship[y + 1][x] & self.North == self.North:
				if (y + 1, x) not in visited:
					queue.append((y + 1, x, distance + 1))
			if x - 1 > 0 and self.ship[y][x] & self.West == self.West and self.ship[y][x - 1] & self.East == self.East:
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
		# self.value = None
		self.move = move
		# self.hash = hash(self.ship)

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
			for tile in self.ship.GetPossibleTileOrientations(self.ship.ConvertTileTypeToTile(possibleTileType)):
				for location in self.ship.GetPlayableLocationsForTile(tile):
					if debugPrint:
						logFile.write("Adding location " + str(location) + "\n")
					newShip = self.ship.Duplicate()
					# newShip = deepcopy(self.ship)
					newShip.PlaceTile(tile, location[0], location[1])
					if debugPrint:
						logFile.write("Creating new ship that looks like\n")
					newShip.Print()
					newTileDeck = deepcopy(self.tileDeck)
					newTileDeck.PopTile(possibleTileType)
					newType = StateType.Win if newTileDeck.Empty() else StateType.Node
					self.children.append(State(newShip, newTileDeck, newType, self, Move(tile, location[0], location[1])))
		return self.children

	def ComputeStateValue(self):

		# Number of tile types that can be played
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
			playableTilesMultiplier = float(remainingPlacableTileTypes) / float(len(remainingTileTypes))
		else:
			playableTilesMultiplier = 1.0
		# print("Playable tile type multiplier", playableTilesMultiplier)

		# Number of spaces available for tiles
		availableLocations = len(self.ship.GetAvailableShipLocations())
		# print("Available locations", availableLocations)

		# Average tile distance from the rowboat
		totalDistance = 0
		tileCount = 0
		for h in range(len(self.ship.ship)):
			for w in range(len(self.ship.ship[h])):
				if self.ship.ship[h][w] != 0:
					tileCount += 1
					totalDistance += (abs(h - 0) + abs(w - 1))
		averageRowboatDistance = (float(totalDistance) / (float(tileCount) - 1)) + 1.0
		# print("Average distance to rowboat", averageRowboatDistance)

		# Bottlenecks?

		# Number of tiles left
		tilesLeft = len(self.tileDeck.tiles)
		# print("Tiles left", tilesLeft)

		# 
		return ((20 - tilesLeft) * availableLocations * playableTilesMultiplier) - averageRowboatDistance * 2.0

	def ComputeStateValue2(self):
		# Vastly increase prio of this
		# Number of tile types that can be played
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
			playableTilesMultiplier = (float(remainingPlacableTileTypes) / float(len(remainingTileTypes))) ** 3
		else:
			playableTilesMultiplier = 1.0
		# print("Playable tile type multiplier", playableTilesMultiplier)

		# Number of spaces available for tiles
		availableLocations = len(self.ship.GetAvailableShipLocations())
		# print("Available locations", availableLocations)

		# Average tile distance from the rowboat
		# Increase value
		# totalDistance = 0
		# tileCount = 0
		# for h in range(len(self.ship.ship)):
		# 	for w in range(len(self.ship.ship[h])):
		# 		if self.ship.ship[h][w] != 0:
		# 			tileCount += 1
		# 			totalDistance += (abs(h - 0) + abs(w - 1))
		# averageRowboatDistance = (float(totalDistance) / (float(tileCount) - 1)) + 1.0
		# shipArea = len(self.ship.ship) * len(self.ship.ship[0])
		wavefrontDistance = self.ship.GetMaxDistanceWavefront()
		# print("Average distance to rowboat", averageRowboatDistance)
		
		# Empty tiles
		emptyTiles = 0
		for h in self.ship.ship:
			for w in h:
				if w == 0:
					emptyTiles += 1

		# Bottlenecks?

		# Number of tiles left
		tilesLeft = len(self.tileDeck.tiles)
		# print("Tiles left", tilesLeft)

		# 
		return ((20 - tilesLeft) * availableLocations * playableTilesMultiplier) - ((wavefrontDistance + emptyTiles) ** 2)

	# def EstimateStateValue(self, depth):

	def GetPath(self):
		path = [deepcopy(self.move)]
		parent = self.parent
		while parent is not None:
			if parent.move is None:
				break
			path.append(deepcopy(parent.move))
			parent = parent.parent
		return path

debugCounter = 0
def AStar2(state, tileType, currentBestValue, currentBestMove, depth, maxDepth = 3):
	global debugCounter

	# print(f"Running A*2 on tileType {tileType} with depth =", depth)
	if debugPrint:
		logFile.write(f"Running A*2 on tileType {tileType} with depth = {depth}\n")
	state.ship.Print()
	tileTypes = [tileType] if depth == 0 else None
	if depth == maxDepth or len(state.tileDeck.tiles) == 0:
		# print("Max depth search")
		if debugPrint:
			logFile.write("Max depth search\n")
		pathString = ""
		for entry in state.GetPath():
			pathString += f"--> {entry.tile} ({entry.y}, {entry.x}) "
		# print(f"Path: {pathString} Value: {state.ComputeStateValue()}")
		if debugPrint:
			logFile.write(f"Path: {pathString} Value: {state.ComputeStateValue()}\n")
		debugCounter += 1
		return (state.move, state.ComputeStateValue())
	else:
		# print("Non-max depth search")
		if debugPrint:
			logFile.write("Non-max depth search\n")
		childStates = []
		childStates = state.GetChildren(tileTypes)
		logFile.flush()
		logFile.flush()
		for childState in childStates:
			# print("Child")
			if debugPrint:
				logFile.write(f"Child ({childState.move.y}, {childState.move.x})\n")
			childState.ship.Print()
			path, value = AStar2(childState, None, currentBestValue, currentBestMove, depth + 1, maxDepth)
			value = (1.0 / len(childStates)) * value
			if value > currentBestValue:
				currentBestValue = value
				currentBestMove = childState.move
		return (currentBestMove, currentBestValue)

def AStar3(state, tileType):
	global debugCounter

	# print(f"Running A*2 on tileType {tileType} with depth =", depth)
	if debugPrint:
		logFile.write(f"Running A*3 on tileType {tileType}\n")
	state.ship.Print()

	bestChildValue = -inf
	bestMove = None
	childStates  = state.GetChildren([tileType])
	for childState in childStates:

		grandchildrenValue = 0
		grandchildrenStates = childState.GetChildren(None)
		for grandchildState in grandchildrenStates:

			greatGrandchildrenValue = 0
			greatGrandchildStates = grandchildState.GetChildren(None)
			for greatGrandchildState in greatGrandchildStates:

				greatGrandchildrenValue += (1.0 / len(greatGrandchildStates)) * greatGrandchildState.ComputeStateValue()
			
			grandchildrenValue += (1.0 / len(grandchildrenStates)) * greatGrandchildrenValue

		childValue = (1.0 / len(childStates)) * grandchildrenValue
		if childValue > bestChildValue:
			bestChildValue = childValue
			bestMove = childState.move

	return (bestMove, bestChildValue)

def AStar4(state, tileType):
	global debugCounter

	# print(f"Running A*2 on tileType {tileType} with depth =", depth)
	if debugPrint:
		logFile.write(f"Running A*3 on tileType {tileType}\n")
	state.ship.Print()

	bestChildValue = -inf
	bestMove = None
	childStates  = state.GetChildren([tileType])
	for childState in childStates:

		grandchildrenValue = 0
		grandchildrenStates = childState.GetChildren(None)
		for grandchildState in grandchildrenStates:

			grandchildrenValue += (1.0 / len(grandchildrenStates)) * grandchildState.ComputeStateValue2()

		childValue = (1.0 / len(childStates)) * grandchildrenValue
		if childValue > bestChildValue:
			bestChildValue = childValue
			bestMove = childState.move

	return (bestMove, bestChildValue)


# ship = Ship()

# ship.PlaceTile(15, 2, 2)
# ship.PlaceTile(15, 2, 1)
# ship.PlaceTile(15, 2, 3)
# ship.Print(stdout=True)
# print(ship.GetMaxDistanceWavefront())

# ship.PlaceTile(15, 3, 2)
# ship.Print(stdout=True)
# print(ship.GetMaxDistanceWavefront())

# ship.PlaceTile(15, 4, 2)
# ship.Print(stdout=True)
# print(ship.GetMaxDistanceWavefront())

# ship.PlaceTile(15, 5, 2)
# ship.PlaceTile(15, 4, 3)
# ship.Print(stdout=True)
# print(ship.GetMaxDistanceWavefront())
# exit(0)


with open("C:\\Users\\jonny\\OneDrive\\Documents\\PiratesCode.log", 'w+') as logFile:

	# debugTileOrder = [TileType.Quad, TileType.Corner]
	# debugTileOrder = [TileType.Quad, TileType.Quad]
	# debugTileOrder = [TileType.Quad]
	# debugTileOrder = [TileType.Corner]
	# debugTileOrder = [TileType.DeadEnd, TileType.Quad]

	if 'debugTileOrder' in locals():
		gameCount = 1
		printTurns = True
		debugMode = True
	else:
		gameCount = 1
		printTurns = False
		debugMode = False

	wins = 0
	losses = 0
	for game in range(gameCount):

		print("Starting game", game + 1)
		gameStart = time()
		ship = Ship()
		tileDeck = TileDeck()
		state = State(ship, tileDeck, StateType.Node, None, None)

		# for tile in debugTileOrder:
		while not tileDeck.Empty():
			tile = tileDeck.GetRandomTile()

			if printTurns:
				print("Remaining tiles", tileDeck.tiles)

			if printTurns:
				print("Placing tile type", tile)
			if debugPrint:
				logFile.write(f"Placing tile type {tile}\n")

			turnStart = time()
			# bestMove, value = AStar2(state, tile, currentBestValue=-inf, currentBestMove=None, depth=0, maxDepth=2)
			# bestMove, value = AStar3(state, tile)
			bestMove, value = AStar4(state, tile)
			if printTurns:
				print(f"Visited {debugCounter} states")
			if debugPrint:
				logFile.write(f"Visited {debugCounter} states\n")
			debugCounter = 0

			if printTurns:
				print(f"Best move {bestMove.tile} at ({bestMove.y}, {bestMove.x})")
			if debugPrint:
				logFile.write(f"Best move: {bestMove}\n")
			if bestMove is None:
				print("I think we lost :(")
				print("Tile we can't place", tile)
				state.ship.Print(stdout=True)
				losses += 1
				break

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
	winPercentage = 100 if losses == 0 else wins / losses
	print(f"Win Percentage: {winPercentage}%")
