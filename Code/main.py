from __future__ import print_function
import pygame as pg, random, setti, characters
import os
from pygame.locals import *
import threading
import sys
from time import sleep
from math import cos, pi, ceil
from itertools import cycle



class Board:
    running = True
    def __init__(self, width, height, boy, boy2, platforms, missles, charms, objects, flames):
        self.width = width
        self.height = height
        self.boy = boy
        self.boy2 = boy2
        if type(boy) == Mark:
            self.mark = boy
        elif type(boy2) == Mark:
            self.mark = boy2
        else:
            self.mark = None
        self.platforms = platforms
        self.objects = objects
        self.flames = flames
        self.missles = missles
        self.charms= charms
        self.shakeon = False
        self.remembered = False
        self.tremorcounter = 0
        self.tremoron = False
        for missle in self.missles:
            missle.board = self
        for charm in self.charms:
            charm.board = self
        for platform in self.platforms:
            platform.board = self
        self.boy.board = self
        self.boy2.board = self
     
    
    def draw(self):
        for x in self.platforms:
            x.draw()
        self.boy.draw()
        self.boy2.draw()
        for x in self.missles:
            x.draw()
        for x in self.charms:
            x.draw()
        for x in self.objects:
            x.draw()
        for x in self.flames:
            x.draw()
    def enemies(self):
        self.boy.enemy = self.boy2
        self.boy2.enemy = self.boy

    def tremor(self, strength, step):
        dy = strength*cos(step/setti.tremorsteps*2*pi)
        if step==0:
            self.mark.startplatformsposys = [p.posy for p in self.platforms]
        for platform in self.platforms:
            platform.posy += dy
        if step > setti.tremorsteps/4:
            if self.mark.enemy.stands():
                self.mark.enemy.stunned = True
                self.mark.enemy.vely -= setti.tremorjump
            markplatform = self.mark.stands()
            if markplatform:    
                self.mark.posy = markplatform.posy - self.mark.height
        if step == setti.tremorsteps-1:
            for i, p in enumerate(self.platforms):
                p.posy = self.mark.startplatformsposys[i]

    def checktremor(self):
        while True:
            if self.mark is not None and self.mark.prevvely>0 and self.mark.vely == 0:
                for step in range(setti.tremorsteps):
                    yield self.tremor(setti.maxtremor, step)
                for pause in range(setti.tremorpause):
                    yield
            else:
                yield

    def run(self):
        ct = self.checktremor()
        songs = [pg.mixer.Sound(setti.song_pump), pg.mixer.Sound(setti.song_sweetdreams), pg.mixer.Sound(setti.song_duhast), pg.mixer.Sound(setti.song_intheend)]
        soundObj = random.choice(songs)
        soundObj.play()
        myfont = pg.font.SysFont('monospace', 100)
        pg.display.set_caption(setti.title)
        bg = pg.transform.scale(setti.get_image("../Assets/Pics/bg2.png").convert_alpha(), (self.width, self.height))
        while self.running:
            pg.time.delay(6)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
            keys = pg.key.get_pressed()
            self.boy.update(keys[pg.K_w], keys[pg.K_a], keys[pg.K_d], keys[pg.K_f], keys[pg.K_g], keys[pg.K_h])
            self.boy2.update(keys[pg.K_UP], keys[pg.K_LEFT], keys[pg.K_RIGHT], keys[pg.K_KP_DIVIDE], keys[pg.K_KP_MULTIPLY], keys[pg.K_KP_MINUS])
            for x in self.missles:
                x.move()
            if self.boy.hp <= 0:
                screen.blit(myfont.render(self.boy.__class__.__name__ + " lost", 1, (255, 100, 255)), (self.width/3, self.height/2))
                self.boy = 0
                pg.display.flip()
                sleep(3)
                break
            if self.boy2.hp <= 0:
                screen.blit(myfont.render(self.boy2.__class__.__name__ + " lost", 1, (255, 100, 255)), (self.width/3, self.height/2))
                self.boy2 = 0
                pg.display.flip()
                sleep(3)
                break
            for x in self.charms:
                x.move()
            for flame in self.flames:
                flame.update()
            next(ct)
            
            screen.fill([255, 255, 255])
            screen.blit(bg, bg.get_rect())  
            self.draw()
            pg.display.flip()   


class Object:
    def __init__(self, width, height, posx, posy, image, board=None):
        self.width = width
        self.height = height
        self.posx = posx
        self.posy = posy
        self.image = pg.transform.scale(image, (self.width, self.height)).convert_alpha()
        self.board = board

    def draw(self):
        screen.blit(self.image, (self.posx, self.posy))

    def checkhitcond(self, x):
        if (self.posx + self.width > x.posx) and (self.posx  < x.posx + x.width) and (self.posy + self.height > x.posy) and (self.posy < x.posy + x.height):
            return True
        return False

class Platform(Object):
    def __init__(self, width, height, posx, posy):
        super().__init__(width, height, posx, posy, setti.platformimage)
    def draw(self):
        super(Platform, self).draw()
    


class Charm(Object):
    def __init__(self, width, height, posx, posy, charmimage, velx, crushimage, owner, board=None):
        super().__init__(width, height, posx, posy, charmimage, board)
        self.velx = velx
        self.crushimage = crushimage.convert_alpha()
        self.crushed = False
        self.crushtime = 0
        self.owner = owner

    def move(self):
        if(self.posx < 0 or self.posx > self.board.width) or (self.posy < 0) or (self.posy > self.board.height):
            self.board.charms.remove(self)
        if(self.crushed):
            if((pg.time.get_ticks() - self.crushtime) > setti.charmtime):
                self.owner.enemy.velx = 0
                self.owner.enemy.stunned = False
                self.board.charms.remove(self)
        self.posx += self.velx
        if (not self.crushed) and (self.checkhitcond(self.owner.enemy)):
            self.crushed = True
            self.crushtime = pg.time.get_ticks()
            self.image = self.crushimage
            self.owner.enemy.stunned = True
            self.owner.enemy.charmed = True

class Flame(Object):
    def __init__(self, width, height, posx, posy, images, owner, board=None):
        super().__init__(width, height, posx, posy, setti.fire_images[0].convert_alpha(), board)
        self.owner = owner
        self.last_burn = pg.time.get_ticks()
        self.images_cycle = cycle(images)
        self.image = next(self.images_cycle).convert_alpha()
        self.last_image_change_time = pg.time.get_ticks()

    def update(self):
        if self.checkhitcond(self.owner.enemy):
            curr_time = pg.time.get_ticks()
            if(curr_time-self.last_burn > setti.fire_dmg_cd):
                self.owner.enemy.hp -= setti.fire_damage
                self.last_burn = curr_time
    
    def draw(self):
        if pg.time.get_ticks() - self.last_image_change_time >= setti.fire_image_change_cd:
            self.last_image_change_time = pg.time.get_ticks()
            self.image = next(self.images_cycle).convert_alpha()
        screen.blit(self.image, (self.posx, self.posy))

            





class Missle(Object):
    def __init__(self, width, height, posx, posy, image, velx, vely, dmg, splashtime, crushimage, board=None):
        super().__init__(width, height, posx, posy, image, board)
        self.velx = velx
        self.vely = vely
        self.dmg = dmg
        self.splashtime = splashtime
        self.crushimage = crushimage.convert_alpha()
        self.crushed = False
        self.crushtime = 0
        

    def move(self):
        if(self.posx < 0 or self.posx > self.board.width) or (self.posy < 0) or (self.posy > self.board.height):
            self.board.missles.remove(self)
        if(self.crushed):
            if((pg.time.get_ticks() - self.crushtime) > self.splashtime):
                self.board.missles.remove(self)
        self.posx += self.velx 
        self.posy += self.vely
        
        for x in [self.board.boy, self.board.boy2]:
            if (not self.crushed) and (self.checkhitcond(x)):
                self.crushed = True
                if x.stunned and self.width > setti.fatshotfactor * setti.misslewidth * 0.9:
                    x.hp -= setti.stunnedbonus
                x.hp -= self.dmg
                self.crushtime = pg.time.get_ticks()
                self.velx = 0
                self.vely = 0
                self.image = self.crushimage
       



class Character(Object):
    def __init__(self, width, height, posx, posy, image, dmg, movespeed, shootpause, hp, enemy, board=None):
        super().__init__(width, height, posx, posy, image, board)
        self.velx = 0
        self.vely = 0
        self.prevvely = 0
        self.dmg = dmg
        self.movespeed = movespeed
        self.shootpause = shootpause
        self.hp = hp
        self.enemy = enemy
        self.lastshot = 0
        self.stunned = False
        self.charmed = False
        self.stunnedframes = 0
        self.charmedframes = 0
        self.blitfac = 0

    def update(self, p_up, p_left, p_right, p_sleft, p_sright, superab):
        if self.posy > self.board.height:
            self.posy = self.board.height - self.height
            self.vely = 0
        self.prevvely = self.vely
        if self.stunned:
            self.stunnedframes += 1
            p_up = False
            p_left = False
            p_right = False
            p_sleft = False
            p_sright = False
            superab = False
        if self.stunnedframes == 1:
            self.image = pg.transform.rotate(self.image, 90)
            self.blitfac = (self.height - self.width)
        if self.stunnedframes > setti.maxstunnedframes:
            self.stunned = False
            self.image = pg.transform.rotate(self.image, 270)
            self.stunnedframes = 0
            self.blitfac = 0
        if self.charmed:
            self.charmedframes += 1
            p_up = False
            p_left = False
            p_right = False
            p_sleft = False
            p_sright = False
            superab = False
        if self.charmedframes > setti.maxcharmedframes:
            self.charmed = False
            self.charmedframes = 0
        if p_sleft:
            if self.__class__.__name__ == 'Billy':
                self.shoot('left')
            elif self.__class__.__name__ == 'Van':
                self.shotgun('left')
            elif self.__class__.__name__ == 'Mark':
                self.fatshot('left')
        elif p_sright:
            if self.__class__.__name__ == 'Billy':
                self.shoot('right')
            elif self.__class__.__name__ == 'Van':
                self.shotgun('right')
            elif self.__class__.__name__ == 'Mark':
                self.fatshot('right')
        if superab:
            if self.__class__.__name__ == 'Billy':
                self.charm()
            elif self.__class__.__name__ == 'Van':
                self.shower()
            elif self.__class__.__name__ == 'Piro':
                self.fire()
        if p_left:
            self.velx -= self.movespeed/setti.accframes
        elif self.velx < 0:
            self.velx += self.movespeed/setti.accframes
        if p_right:
            self.velx += self.movespeed/setti.accframes
        elif self.velx>0:
            self.velx -= self.movespeed/setti.accframes
        if abs(self.velx) < self.movespeed/setti.accframes:
            self.velx = 0
        if self.velx < -self.movespeed:
            self.velx = -self.movespeed
        if self.velx > self.movespeed:
            self.velx = self.movespeed
        if self.stands() and self.vely>0:
            self.posy = self.stands().posy - self.height
            self.vely = 0
        elif self.stands() and self.vely==0:
            pass
        else:
            self.vely += setti.fallspeed
        if self.stands() and self.vely == 0 and p_up:
            self.vely -= setti.jumpvel
        if self.charmed:
            if self.enemy.posx > self.posx:
                self.velx = setti.charmedvel
            else:
                self.velx = - setti.charmedvel
        if (self.posx + self.velx <= (self.board.width - self.width)) and (self.posx + self.velx >= 0):
            self.posx += self.velx
        self.posy += self.vely

    def stands(self):
        for x in self.board.platforms:
            if ((((self.posy + self.height) > x.posy - setti.jumpcatch) and ((self.posy + self.height) < x.posy + setti.jumpcatch)) 
            and (((self.posx + (self.width / 2)) > x.posx) and ((self.posx + (self.width / 2)) < (x.posx + x.width)))):
                return x
        return False
   
    def draw(self):
        def draw_hp(pos_x, pos_y, length):
            px_length = length * (setti.hp_size[0] + setti.hp_space)
            x_left = px_length/2 - self.width/2
            for i in range(length):
                x = pos_x + i*(setti.hp_size[0] + setti.hp_space) - x_left
                y = pos_y + setti.hp_height
                screen.blit(setti.hp_image, (x, y + self.blitfac))


        screen.blit(self.image, (self.posx, self.posy + self.blitfac))
        draw_hp(self.posx, self.posy, ceil(self.hp))
        


class Van(Character):
    def __init__(self, width, height, posx, posy, image, dmg, movespeed, shootpause, hp, enemy, board=None):
        super().__init__(width, height, posx, posy, image, dmg, movespeed, shootpause, hp, enemy, board)
        self.shotguncd = 0
        self.showercd = 0

    def shotgun(self, dir):
        if (pg.time.get_ticks() - self.shotguncd) > setti.shotguncd:
            self.shotguncd = pg.time.get_ticks()
            if dir == "right":
                self.board.missles.append(Missle(setti.misslewidth, setti.missleheight, self.posx + self.width, 
                self.posy + self.height * setti.shootheight, setti.rightmissleImage, setti.misvel + self.velx, self.vely*setti.spreadfactor + setti.shootwidth, self.dmg,  setti.splashtime, setti.crushImage, self.board))
                self.board.missles.append(Missle(setti.misslewidth, setti.missleheight, self.posx + self.width, 
                self.posy + self.height * setti.shootheight, setti.rightmissleImage, setti.misvel + self.velx, self.vely*setti.spreadfactor, self.dmg,  setti.splashtime, setti.crushImage, self.board))
                self.board.missles.append(Missle(setti.misslewidth, setti.missleheight, self.posx + self.width, 
                self.posy + self.height * setti.shootheight, setti.rightmissleImage, setti.misvel + self.velx, self.vely*setti.spreadfactor - setti.shootwidth, self.dmg,  setti.splashtime, setti.crushImage, self.board))

            else:
                self.board.missles.append(Missle(setti.misslewidth, setti.missleheight, self.posx + setti.safeshot, 
                self.posy + self.height * setti.shootheight, setti.leftmissleImage, -setti.misvel + self.velx, self.vely*setti.spreadfactor + setti.shootwidth, self.dmg,  setti.splashtime, setti.crushImage, self.board))
                self.board.missles.append(Missle(setti.misslewidth, setti.missleheight, self.posx + setti.safeshot, 
                self.posy + self.height * setti.shootheight, setti.leftmissleImage, -setti.misvel + self.velx, self.vely*setti.spreadfactor, self.dmg,  setti.splashtime, setti.crushImage, self.board))
                self.board.missles.append(Missle(setti.misslewidth, setti.missleheight, self.posx + setti.safeshot, 
                self.posy + self.height * setti.shootheight, setti.leftmissleImage, -setti.misvel + self.velx, self.vely*setti.spreadfactor - setti.shootwidth, self.dmg,  setti.splashtime, setti.crushImage, self.board))


    def shower(self):
        if(pg.time.get_ticks() - self.showercd > setti.showercd):
            self.showercd = pg.time.get_ticks()
            self.board.missles.append(Missle(setti.missleheight * setti.showersize, setti.misslewidth * setti.showersize, self.enemy.posx - setti.showerwidth, 
            0, pg.transform.rotate(setti.rightmissleImage, -90), 0, setti.showervel, self.dmg,  setti.splashtime, setti.crushImage, self.board))
            self.board.missles.append(Missle(setti.missleheight * setti.showersize, setti.misslewidth * setti.showersize, self.enemy.posx, 
            0, pg.transform.rotate(setti.rightmissleImage, -90), 0, setti.showervel, self.dmg,  setti.splashtime, setti.crushImage, self.board))
            self.board.missles.append(Missle(setti.missleheight * setti.showersize, setti.misslewidth * setti.showersize, self.enemy.posx + setti.showerwidth, 
            0, pg.transform.rotate(setti.rightmissleImage, -90), 0, setti.showervel, self.dmg,  setti.splashtime, setti.crushImage, self.board))

    
class Mark(Character):
    def __init__(self, width, height, posx, posy, image, dmg, movespeed, shootpause, hp, enemy, board=None):
        super().__init__(width, height, posx, posy, image, dmg, movespeed, shootpause, hp, enemy, board)
        self.fatshotcd = 0
        self.tremorcd = 0

    def fatshot(self, dir):
        if(pg.time.get_ticks() - self.fatshotcd > setti.fatshotcd):
            self.fatshotcd = pg.time.get_ticks()
            if dir == "right":
                self.board.missles.append(Missle(setti.misslewidth * setti.fatshotfactor , setti.missleheight * setti.fatshotfactor, self.posx + self.width, 
                self.posy + self.height * setti.shootheight, setti.fatrightmissleImage, setti.misvel + self.velx, self.vely*setti.spreadfactor, self.dmg, setti.splashtime, pg.transform.scale(setti.fatcrushImage, (setti.misslewidth*setti.fatshotfactor, setti.missleheight*setti.fatshotfactor)), self.board))
            else:
                self.board.missles.append(Missle(setti.misslewidth * setti.fatshotfactor , setti.missleheight * setti.fatshotfactor, self.posx - setti.fatshotwidth, 
                self.posy + self.height * setti.shootheight, setti.fatleftmissleImage, -setti.misvel + self.velx, self.vely*setti.spreadfactor, self.dmg, setti.splashtime, pg.transform.scale(setti.fatcrushImage, (setti.misslewidth*setti.fatshotfactor, setti.missleheight*setti.fatshotfactor)), self.board))


class Billy(Character):
    def __init__(self, width, height, posx, posy, image, dmg, movespeed, shootpause, hp, enemy, board=None):
        super().__init__(width, height, posx, posy, image, dmg, movespeed, shootpause, hp, enemy, board)
        self.charmcd = 0


    def charm(self):
        if(pg.time.get_ticks() - self.charmcd > setti.charmcd):
            self.charmcd = pg.time.get_ticks()
            self.board.charms.append(Charm(setti.charmwidth, setti.charmheight, self.posx + self.width/2, self.posy + self.height/2, setti.charmimage, setti.charmvelx, setti.charmcrushimage, self, self.board))
            self.board.charms.append(Charm(setti.charmwidth, setti.charmheight, self.posx + self.width/2, self.posy + self.height/2, setti.charmimage, -setti.charmvelx, setti.charmcrushimage, self, self.board))

    def shoot(self, dir):
        if (pg.time.get_ticks() - self.lastshot) > self.shootpause:
            self.lastshot = pg.time.get_ticks()
            if dir == "right":
                self.board.missles.append(Missle(setti.misslewidth, setti.missleheight, self.posx + self.width, 
                self.posy + self.height * setti.shootheight, setti.rightmissleImage, setti.misvel + self.velx, self.vely*setti.spreadfactor, self.dmg,  setti.splashtime, setti.crushImage, self.board))
            else:
                self.board.missles.append(Missle(setti.misslewidth, setti.missleheight, self.posx + setti.safeshot, 
                self.posy + self.height * setti.shootheight, setti.leftmissleImage, -setti.misvel + self.velx, self.vely*setti.spreadfactor, self.dmg,  setti.splashtime, setti.crushImage, self.board))

class Piro(Character):
    def __init__(self, width, height, posx, posy, image, dmg, movespeed, shootpause, hp, enemy, board=None):
        super().__init__(width, height, posx, posy, image, dmg, movespeed, shootpause, hp, enemy, board)
        self.last_fire = 0

    def fire(self):#self, width, height, posx, posy, images, owner, board=None)
        curr_time = pg.time.get_ticks()
        if (curr_time-self.last_fire > setti.fire_cd):
            self.board.flames.append(Flame(setti.fire_size[0], setti.fire_size[1], self.enemy.posx, self.enemy.posy, setti.fire_images, self, self.board))
            self.last_fire = curr_time
    
pg.init()
info = pg.display.Info() 
screen_width,screen_height = info.current_w - setti.width_correction,info.current_h - setti.height_correction
screen = pg.display.set_mode((screen_width,screen_height))
plats = []
#generate platforms randomly
for i in range(setti.numberofplatforms):
    stopper = True
    platform_x, platform_y = 0, 0
    plat_width = random.choice(setti.platform_widths)
    while stopper:
        platform_x = random.randint(0, screen_width)
        platform_y = random.randint(0, screen_height)
        found = True
        for platform in plats:
            if abs(platform.posx - platform_x) < setti.platform_dist[0] and abs(platform.posy - platform_y) < setti.platform_dist[1] or platform_x + plat_width > screen_width:
                found = False
        stopper = not found


    plats.append(Platform(plat_width, setti.platform_height, platform_x, platform_y))
        
    
    firstchar = Mark(*setti.mark)
    secondchar = Piro(*setti.piro)
        

board = Board(screen_width,screen_height,  secondchar, firstchar, [Platform(2*screen_width, setti.platform_height, -500, screen_height - setti.platform_height), *plats], [], [], [], [])
board.enemies()


board.run()











