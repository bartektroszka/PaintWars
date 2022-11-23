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
jumpvel = 50
jumpcatch = 15
shootheight = 0.6
misvel = 10
misslecatch = 20
colors = {"blue":(0, 0, 255)}
safeshot = -40
spreadfactor = 0.3 #how much characters velocity impacts missle velocity
rightmissleImage = pg.transform.scale(pg.transform.rotate(missleImage, 90), (misslewidth, missleheight))
topmissleImage = pg.transform.scale(pg.transform.rotate(missleImage, 180), (missleheight, misslewidth))
leftmissleImage = pg.transform.scale(pg.transform.rotate(missleImage, 270), (misslewidth, missleheight))
platform_dist = [550, 40]
platform_widths = [300, 250, 500, 450]
songs = ['../Assets/Sounds/pump.wav', '../Assets/Sounds/sweetdreams.wav', '../Assets/Sounds/duhast.wav', '../Assets/Sounds/intheend.wav', '../Assets/Sounds/♂RIGHT ♂INTRO ♂.wav', '../Assets/Sounds/dueloffate.wav']
backgrounds = ["../Assets/Pics/bg2.png", "../Assets/Pics/bg3.png", "../Assets/Pics/bg4.png", "../Assets/Pics/bg5.png"]
platform_height= 25
width_correction = 0
height_correction = 200
platform_height_correction = 200

#VAN
vansize = [80, 120]
vanImage = pg.transform.scale(get_image("../Assets/Pics/van.png"), (vansize[0], vansize[1]))
#width, height, posx, posy, image, dmg, movespeed, accframes, shootpause, hp
van = [vansize[0], vansize[1], 500, 200, vanImage, 1, 6, 20, 600, 15, 12]
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
#width, height, posx, posy, image, dmg, movespeed, accframes shootpause, hp, 0
mark = [marksize[0], marksize[1], 600, 400, markImage, 1, 4, 20, 1000, 23, 12]
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
#width, height, posx, posy, image, dmg, movespeed, accframes shootpause, hp
billy = [billysize[0], billysize[1], 600, 200, billyImage, 1, 10, 20, 500, 15, 12]
charmwidth = 20
charmheight = 20
charmimage = pg.transform.scale(get_image("../Assets/Pics/charm.png"), (charmwidth, charmheight))
charmcrushimage = charmimage
charmtime = 2500
charmedvel = 3
charmvelx = 10
charmcd = 3500
maxcharmedframes = 140


#PIRO

pirosize = [120, 100]
piroImage = pg.transform.scale(get_image("../Assets/Pics/piro.png"), (pirosize[0], pirosize[1]))
#width, height, posx, posy, images, dmg, movespeed,accframes shootpause, hp
size_factor = 2 #real width can be as big as picture width ;/
piro = [pirosize[0], pirosize[1], 600, 720, piroImage, 1, 8, 20, 1000, 8, 12]
fire_size=[40,100]
fire_images = [pg.transform.scale(get_image("../Assets/Pics/fire/1.png"), (fire_size[0], fire_size[1])), pg.transform.scale(get_image("../Assets/Pics/fire/2.png"), (fire_size[0], fire_size[1])), pg.transform.scale(get_image("../Assets/Pics/fire/3.png"), (fire_size[0], fire_size[1])), pg.transform.scale(get_image("../Assets/Pics/fire/4.png"), (fire_size[0], fire_size[1])), pg.transform.scale(get_image("../Assets/Pics/fire/5.png"), (fire_size[0], fire_size[1])), pg.transform.scale(get_image("../Assets/Pics/fire/6.png"), (fire_size[0], fire_size[1]))]
fire_image_change_cd = 70
fire_dmg_cd = 500
fire_cd = 1000
fire_damage = 0.5

#Billy_motor
billy_motorsize = [140, 100]
billy_motorImage = pg.transform.scale(get_image("../Assets/Pics/billy_motor.png"), (billy_motorsize[0], billy_motorsize[1]))


size_factor = 2 #real width can be as big as picture width ;/
billy_motor_misslevel=20
billy_jumpvel = 7
billy_motor_hit_velx = 1
billy_motor_hit_vely = 0.5
billy_mottor_missle_velx_spread_factor = 0.3
billy_motor_static_hit_vely = 5
billy_motor_hit_cd = 2000
#width, height, posx, posy, images, dmg, movespeed,accframes,  shootpause, hp, 0
billy_motor = [billy_motorsize[0], billy_motorsize[1], 600, 500, billy_motorImage, 1, 16, 50, 1000, 8, billy_jumpvel]
billy_motor_hit_dmg_multiplier = 0.3