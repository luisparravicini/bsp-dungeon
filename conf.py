
WIN_SIZE = [320, 200]
SCALE = 3
TILE_SIZE = 16 * SCALE
SCREEN_SIZE = [WIN_SIZE[0] * SCALE, WIN_SIZE[1] * SCALE]
ROOM_SIZE = [int(v / TILE_SIZE) for v in SCREEN_SIZE]
NO_TILE_POS = (-1, -1)
