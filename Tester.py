# from FirstMate import Ship
from SecondMate import Ship, Tile, Coords


def Test(name, f):
    if not f():
        raise RuntimeError(name)

def TestShip():
    ship = Ship()
    ship.ship = [[7, 7, 7]]
    if ship.GetMaxDistanceWavefront(0, 1) != 1:
        print("Wavefront test 1 failed")
        return False

    ship.ship = [[0, 4, 7, 7, 7, 7, 7, 3, 0], [0, 0, 14, 0, 10, 12, 0, 14, 1], [0, 0, 14, 7, 15, 1, 6, 15, 3], [7, 7, 15, 15, 0, 0, 0, 0, 0]]
    ship.Print(stdout=True)
    if ship.GetMaxDistanceWavefront(0, 6) != 6:
        print("Wavefront test 2 failed")
        return False

    ship.ship = [[4, 5, 7, 7, 7, 7, 7, 7, 1, 0], [0, 0, 14, 15, 0, 14, 0, 14, 7, 3], [0, 6, 15, 15, 3, 8, 6, 15, 0, 14]]
    ship.Print(stdout=True)
    if ship.GetMaxDistanceWavefront(0, 6) != 7:
        print("Wavefront test 3 failed")
        return False

    return True

if __name__ == "__main__":
    # Test("Test basic ship", TestShip)

    ship = Ship()
    # ship.ship = [[0, 4, 7, 7, 7, 7, 7, 3, 0], [0, 0, 14, 0, 10, 12, 0, 14, 1], [0, 0, 14, 7, 15, 1, 6, 15, 3], [7, 7, 15, 15, 0, 0, 0, 0, 0]]
    # ship.Print(stdout=True)
    # dist = ship.GetMaxDistanceWavefront(0, 5)
    # print("Dist =", dist)

    ship.ship = [[0, 5, 7, 7, 7, 7, 7, 7, 1, 0], [0, 0, 14, 15, 0, 14, 0, 14, 7, 3], [0, 6, 15, 15, 3, 8, 6, 15, 0, 14]]
    # ship.ship = [[0, 4, 7, 7, 7, 7, 7, 3, 0], [0, 0, 14, 0, 10, 12, 0, 14, 1], [0, 0, 14, 7, 15, 1, 6, 15, 3], [7, 7, 15, 15, 0, 0, 0, 0, 0]]
    ship.Print(stdout=True)
    dist = ship.GetMaxDistanceWavefront(0, 6)
    print("Wavefront Distance =", dist)

    locations = ship.GetAvailableShipLocations()
    print("Available locations:", locations)
    if locations != [(1, 4), (1, 6), (2, 8), (3, 1), (3, 2), (3, 3), (3, 4), (3, 6), (3, 7), (2, 10), (3, 9)]:
        print("Locations were incorrect")

    tileOrientations = {
        1: [1, 2, 4, 8],
        3: [3, 6, 12, 9],
        5: [5, 10],
        7: [7, 14, 13, 11],
        15: [15]
    }

    for tileOrientation in tileOrientations.keys():
        possibleOrientations = Tile.GetPossibleOrientations(tileOrientation)
        correctPossibilities = tileOrientations[tileOrientation]
        print(f"Checking possible orientations for tile {tileOrientation}: {possibleOrientations}")
        if possibleOrientations != correctPossibilities:
            print(f"Possible orientations {possibleOrientations} for tile {tileOrientation} are incorrect. Should be {correctPossibilities}")

    for name, type in [("DeadEnd", Tile.DeadEnd), ("Corner", Tile.Corner), ("Hallway", Tile.Hallway), ("Triple", Tile.Triple), ("Quad", Tile.Quad)]:
        for orientedTile in Tile.GetPossibleOrientations(Tile.ConvertToBitmask(type)):
            facing = ""
            for dirName, dir in [("North ", Coords.North), ("East ", Coords.East), ("West ", Coords.West), ("South ", Coords.South)]:
                if orientedTile & dir == dir:
                    facing += dirName
            if len(facing):
                facing = facing[:-1]
            print(f"Playable locations for {name} with orientation {orientedTile} (facing {facing}): {ship.GetPlayableLocationsForTile(orientedTile)}")

    print("\n\nChecking ship tile placement")
    ship.ship = [[7, 7, 7]]
    for tile, y, x in [(6, 0, -1), (1, 0, 4), (15, 1, 2)]:
        print(f"Placing tile {tile} at ({y}, {x})")
        ship.PlaceTile(tile, y, x)
        ship.Print(stdout=True)

    print("\n\nChecking negative tiles")
    ship.ship = [[23, 7, 7]]
    ship.Print(stdout=True)
    locations = ship.GetAvailableShipLocations()
    print("Available locations:", locations)