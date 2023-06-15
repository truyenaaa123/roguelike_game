SCREEN_WIDTH, SCREEN_HEIGHT = (1280, 720)
FPS = 60
TILE_SIZE = 64

# path
PLAYER_PATH = "texture/knight_player.png"
BULLET_PATH = "texture/bullet_energy.png"
EXP_PATH = 'texture/bluegem.png'
HEALTH_PATH = 'texture/heart.png'
MAGNET_PATH = 'texture/magnet.png'
BOOM_PATH = 'texture/boom.png'
FLOOR_PATH = 'texture/bg2.png'
FIREBALL_PATH = 'texture/fireball.png'
BOOMERANG_PATH = 'texture/boomerang.png'

# UI
BAR_HEIGHT = 15
HEALTH_BAR_WIDTH = 200
EXP_BAR_WIDTH = SCREEN_WIDTH - 20
ITEM_BOX_SIZE = 80
UI_FONT = 'font/DragonHunter.ttf'
UI_FONT_SIZE = 18

# COLOR
WATER_COLOR = '#71ddee'
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR = '#EEEEEE'

# UI COLOR
HEALTH_COLOR = 'red'
EXP_COLOR = '#4876FF'
UI_BORDER_COLOR_ACTIVE = 'gold'

# upgrade menu
TEXT_COLOR_SELECTED = '#111111'
BAR_COLOR = '#EEEEEE'
BAR_COLOR_SELECTED = '#111111'
UPGRADE_BG_COOR_SELECTED = '#EEEEEE'

# enemy
monster_data = {
    'zombie': {'health': 100, 'damage':100, 'speed': 1},
    'snake': {'health': 50, 'damage':50, 'speed': 3},
    'dragon': {'health': 1000, 'damage':500, 'speed': 2},
    'bat': {'health': 20, 'damage':20, 'speed': 2}
}

# player
player_data = {'health': 1000, 'exp': 50, 'speed': 3, 'damage':10}


# skill
skill_data = {
    'fireball': 1, 'boomerang': 1, 'vaccum': 50, 'damage': 5, 'health': 200, 'speed':0.5, 'attack_speed': 2
}
