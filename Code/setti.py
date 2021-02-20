import pygame as pg
import os
from pygame.locals import *
import threading
import sys
import numpy as np

_image_library = {}
def get_image(path):
        global _image_library
        image = _image_library.get(path)
        if image == None:
                canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
                image = pg.image.load(canonicalized_path)
                _image_library[path] = image
        return image



#Game options
title = "Hot Men Cool Boys"
missleImage = get_image("../Assets/Pics/dropp.png")
crushImage = pg.transform.scale(get_image("../Assets/Pics/splash.png"), (20, 20))
numberofplatforms = 20
platformimage = get_image("../Assets/Pics/platformimage.png")
hp_size = [5,7]
hp_space = 1
hp_height = -10
hp_image = pg.transform.scale(get_image("../Assets/Pics/hp.png"), np.array(hp_size))
width = 1700
height = 1100
splashtime = 200
misslewidth = 30
missleheight = 15
fallspeed = 0.4
accframes = 20
jumpvel = 12
jumpcatch = 15
shootheight = 0.6
misvel = 10
misslecatch = 20
colors = {"blue":(0, 0, 255)}
safeshot = -40
spreadfactor = 0.3
rightmissleImage = pg.transform.scale(pg.transform.rotate(missleImage, 90), (misslewidth, missleheight))
leftmissleImage = pg.transform.scale(pg.transform.rotate(missleImage, 270), (misslewidth, missleheight))
platform_dist = [550, 40]
platform_widths = [300, 250, 500, 450]
song_pump = '../Assets/Sounds/pump.wav'
song_sweetdreams = '../Assets/Sounds/sweetdreams.wav'
song_duhast = '../Assets/Sounds/duhast.wav'
song_intheend = '../Assets/Sounds/intheend.wav'
sound_billylose = '../Assets/Sounds/billylose.wav'
platform_height= 25
width_correction = 0
height_correction = 200
#VAN
vansize = [60, 120]
vanImage = pg.transform.scale(get_image("../Assets/Pics/van.png"), (vansize[0], vansize[1]))
#width, height, posx, posy, image, dmg, movespeed, shootpause, hp, 0
van = [vansize[0], vansize[1], 500, 720, vanImage, 1, 3, 600, 15, 0]
shootwidth = 2
showerwidth = 100
showerheight = 500
showervel = 10
shotguncd = 2000
showercd = 3000
showersize = 1




#MARK
fatshotfactor = 4
fatshotwidth = misslewidth * fatshotfactor
fatrightmissleImage = pg.transform.scale(pg.transform.rotate(missleImage, 90), (misslewidth * fatshotfactor, missleheight * fatshotfactor))
fatleftmissleImage = pg.transform.scale(pg.transform.rotate(missleImage, 270), (misslewidth * fatshotfactor, missleheight * fatshotfactor))
marksize = [140, 120]
markImage = pg.transform.scale(get_image("../Assets/Pics/mark.png"), (marksize[0], marksize[1]))
#width, height, posx, posy, image, dmg, movespeed, shootpause, hp, 0
mark = [marksize[0], marksize[1], 600, 400, markImage, 1, 2, 1000, 23, 0]
tremorsteps = 16
tremorpause = 120
tremorjump = 5
maxtremor = 2
fatshotcd = 2000
fatcrushImage = get_image('../Assets/Pics/fatsplachimage.png')
stunnedbonus = 2
maxstunnedframes = 140

#billy
billysize = [100, 120]
billyImage = pg.transform.scale(get_image("../Assets/Pics/billy.png"), (billysize[0], billysize[1]))
#width, height, posx, posy, image, dmg, movespeed, shootpause, hp, 0
billy = [billysize[0], billysize[1], 600, 720, billyImage, 1, 5, 1000, 15, 0]
charmwidth = 20
charmheight = 20
charmimage = pg.transform.scale(get_image("../Assets/Pics/charm.png"), (charmwidth, charmheight))
charmcrushimage = charmimage
charmtime = 2500
charmedvel = 3
charmvelx = 6
charmcd = 3500
maxcharmedframes = 140


#PIRO

pirosize = [140, 100]
piroImage = pg.transform.scale(get_image("../Assets/Pics/piro.png"), (pirosize[0], pirosize[1]))
#width, height, posx, posy, images, dmg, movespeed, shootpause, hp, 0
piro = [pirosize[0], pirosize[1], 600, 720, piroImage, 1, 5, 1000, 8, 0]
fire_size=[80,120]
fire_images = [pg.transform.scale(get_image("../Assets/Pics/fire/1.png"), (fire_size[0], fire_size[1])), pg.transform.scale(get_image("../Assets/Pics/fire/2.png"), (fire_size[0], fire_size[1])), pg.transform.scale(get_image("../Assets/Pics/fire/3.png"), (fire_size[0], fire_size[1])), pg.transform.scale(get_image("../Assets/Pics/fire/4.png"), (fire_size[0], fire_size[1])), pg.transform.scale(get_image("../Assets/Pics/fire/5.png"), (fire_size[0], fire_size[1])), pg.transform.scale(get_image("../Assets/Pics/fire/6.png"), (fire_size[0], fire_size[1]))]
fire_image_change_cd = 70
fire_dmg_cd = 500
fire_cd = 1000
fire_damage = 0.5