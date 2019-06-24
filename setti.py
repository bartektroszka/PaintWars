import pygame as pg
import os
from pygame.locals import *
import threading
import sys

_image_library = {}
def get_image(path):
        global _image_library
        image = _image_library.get(path)
        if image == None:
                canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
                image = pg.image.load(canonicalized_path)
                _image_library[path] = image
        return image

#######################################################
#CHARACTERS FIGHTING!: (pick "Mario", "Van" or "Mark")#
characters =['Mark', 'Mario']                         #
#######################################################



#Game options
title = "Paint Wars"
missleImage = get_image("dropp.png")
crushImage = pg.transform.scale(get_image("splash.png"), (20, 20))
numberofplatforms = 20
platformimage = get_image("platformimage.png")
width = 1500
height = 800
splashtime = 200
misslewidth = 30
missleheight = 15
fallspeed = 0.4
accframes = 20
jumpvel = 12
jumpcatch = 10
shootheight = 0.6
misvel = 10
misslecatch = 20
colors = {"blue":(0, 0, 255)}
safeshot = -40
spreadfactor = 0.3
rightmissleImage = pg.transform.scale(pg.transform.rotate(missleImage, 90), (misslewidth, missleheight))
leftmissleImage = pg.transform.scale(pg.transform.rotate(missleImage, 270), (misslewidth, missleheight))



#VAN
vansize = [40, 80]
vanImage = pg.transform.scale(get_image("van.png"), (vansize[0], vansize[1]))
#width, height, posx, posy, image, dmg, movespeed, shootpause, hp, 0
van = [vansize[0], vansize[1], 500, 720, vanImage, 1, 3, 1000, 20, 0]
shootwidth = 2
showerwidth = 100
showerheight = 500
showervel = 12
shotguncd = 1500
showercd = 1000
showersize = 1




#MARK
fatshotfactor = 4
fatrightmissleImage = pg.transform.scale(pg.transform.rotate(missleImage, 90), (misslewidth * fatshotfactor, missleheight * fatshotfactor))
fatleftmissleImage = pg.transform.scale(pg.transform.rotate(missleImage, 270), (misslewidth * fatshotfactor, missleheight * fatshotfactor))
marksize = [40, 80]
markImage = pg.transform.scale(get_image("mark.png"), (marksize[0], marksize[1]))
#width, height, posx, posy, image, dmg, movespeed, shootpause, hp, 0
mark = [marksize[0], marksize[1], 600, 400, markImage, 1, 2, 1000, 25, 0]
tremorsteps = 16
tremorpause = 120
tremorjump = 5
maxtremor = 2
fatshotcd = 1000
fatcrushImage = get_image('fatsplachimage.png')
stunnedbonus = 2
maxstunnedframes = 140

#MARIO
mariosize = [40, 80]
marioImage = pg.transform.scale(get_image("mario.png"), (mariosize[0], mariosize[1]))
#width, height, posx, posy, image, dmg, movespeed, shootpause, hp, 0
mario = [mariosize[0], mariosize[1], 600, 720, marioImage, 1, 5, 400, 15, 0]
charmwidth = 20
charmheight = 20
charmimage = pg.transform.scale(get_image("charm.png"), (charmwidth, charmheight))
charmcrushimage = charmimage
charmtime = 2500
charmedvel = 3
charmvelx = 6
charmcd = 1000
maxcharmedframes = 140

