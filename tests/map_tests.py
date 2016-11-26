from nose.tools import *
from gothonweb.map import *


def test_room():
    gold = Room("GoldRoom",
                """This room has gold in it you can grab. There's a
                door to the north.""")
    assert_equal(gold.name, "GoldRoom")
    assert_equal(gold.paths, {})
    
def test_room_central_corridor():
	cc = Room("Central Corridor", "*")
	assert_equal(cc.name, "Central Corridor")
	assert_equal(cc.paths, {})

def test_room_armory():
	lwa = Room("Laser Weapon Armory", "*")
	assert_equal(lwa.name, "Laser Weapon Armory")
	assert_equal(lwa.paths, {})

def test_room_bridge():
	tb = Room("The Bridge", "*")
	assert_equal(tb.name, "The Bridge")
	assert_equal(tb.paths, {})

def test_room_pod():
	ep = Room("Escape Pod", "*")
	assert_equal(ep.name, "Escape Pod")
	assert_equal(ep.paths, {})

def test_room_end_win():
	ew = Room("The End",
		"""
		You jump into pod 2 and hit the eject button.
		The pod easily slides out into space heading to
		the planet below.  As it flies to the planet, you look
		back and see your ship implode then explode like a
		bright star, taking out the Gothon ship at the same
		time.  You won!
		""")
	assert_equal(ew.name, "The End")
	assert_equal(ew.paths, {})

def test_room_end_lose():
	el = Room("The End",
		"""
		You jump into a random pod and hit the eject button.
		The pod escapes out into the void of space, then
		implodes as the hull ruptures, crushing your body
		into jam jelly.
		""")
	assert_equal(el.name, "The End")
	assert_equal(el.paths, {})

def test_death():
	gd = Room("Death", "*")
	assert_equal(gd.name, "Death")
	assert_equal(gd.paths, {})


def test_room_paths():
    center = Room("Center", "Test room in the center.")
    north = Room("North", "Test room in the north.")
    south = Room("South", "Test room in the south.")

    center.add_paths({'north': north, 'south': south})
    assert_equal(center.go('north'), north)
    assert_equal(center.go('south'), south)

def test_cc_paths():
    cc = Room("Central Corridor", "*")

    cc.add_paths({
		'shoot!': generic_death,
		'dodge!': generic_death,
		'tell a joke': laser_weapon_armory
	})
    assert_equal(cc.go('shoot!'), generic_death)
    assert_equal(cc.go('dodge!'), generic_death)
    assert_equal(cc.go('tell a joke'), laser_weapon_armory)

def test_armory_paths():
    lwa = Room("Laser Weapon Armory", "*")

    lwa.add_paths({
		'0132': the_bridge,
		'*': generic_death
	})
    assert_equal(lwa.go('0132'), the_bridge)
    assert_equal(lwa.go('*'), generic_death)

def test_bridge_paths():
    tb = Room("The Bridge", "*")

    tb.add_paths({
		'throw the bomb': generic_death,
		'slowly place the bomb': escape_pod
	})
    assert_equal(tb.go('throw the bomb'), generic_death)
    assert_equal(tb.go('slowly place the bomb'), escape_pod)

def test_pod_paths():
    ep = Room("Escape Pod", "*")

    ep.add_paths({
		'2': the_end_winner,
		'*': the_end_loser
	})
    assert_equal(ep.go('2'), the_end_winner)
    assert_equal(ep.go('*'), the_end_loser)

def test_map():
    start = Room("Start", "You can go west and down a hole.")
    west = Room("Trees", "There are trees here, you can go east.")
    down = Room("Dungeon", "It's dark down here, you can go up.")

    start.add_paths({'west': west, 'down': down})
    west.add_paths({'east': start})
    down.add_paths({'up': start})

    assert_equal(start.go('west'), west)
    assert_equal(start.go('west').go('east'), start)
    assert_equal(start.go('down').go('up'), start)
    
def test_gothon_game_map():
	assert_equal(START.go('shoot!'), generic_death)
	assert_equal(START.go('dodge!'), generic_death)
	
	room = START.go('tell a joke')
	assert_equal(room, laser_weapon_armory)
	assert_equal(room.go('0132'), the_bridge)
	assert_equal(room.go('0132').go('slowly place the bomb'), escape_pod)
	assert_equal(room.go('0132').go('slowly place the bomb').go('2'), the_end_winner)
	assert_equal(room.go('*'), generic_death)
	assert_equal(room.go('0132').go('throw the bomb'), generic_death)
	assert_equal(room.go('0132').go('slowly place the bomb').go('*'), the_end_loser)
