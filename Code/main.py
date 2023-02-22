from __future__ import print_function
import pygame as pg, random, setti
import os
from pygame.locals import *
import threading
import sys
from time import sleep
from math import cos, pi, ceil
from itertools import cycle




class Board:
    running = True
    def __init__(self, width, height, platforms, missles, charms, objects, flames, menu, boys=[]):
        self.is_menu = True
        self.width = width
        self.height = height
        if not hasattr(self, 'mark'):
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
        self.last_tremor = 0
        for missle in self.missles:
            missle.board = self
        for charm in self.charms:
            charm.board = self
        for platform in self.platforms:
            platform.board = self
        self.boys=boys
        self.menu = menu
        self.menu.board = self
     
    
    def draw(self):
        for x in self.platforms:
            x.draw()
        for boy in self.boys:
            boy.draw()
        for x in self.missles:
            x.draw()
        for x in self.charms:
            x.draw()
        for x in self.objects:
            x.draw()
        for x in self.flames:
            x.draw()

    def tremor(self, strength, step):
        dy = strength*cos(step/setti.tremorsteps*2*pi)
        if step==0:
            self.mark.startplatformsposys = [p.posy for p in self.platforms]
        for platform in self.platforms:
            platform.posy += dy
        if step > setti.tremorsteps/4:
            if self.mark.enemy.stands():
                self.mark.enemy.stunned = True
                self.mark.enemy.vely -= screen_size_factor * setti.tremorjump
            markplatform = self.mark.stands()
            if markplatform:    
                self.mark.posy = markplatform.posy - self.mark.height
        if step == setti.tremorsteps-1:
            for i, p in enumerate(self.platforms):
                p.posy = self.mark.startplatformsposys[i]

    def checktremor(self):
        while True:
            curr_time = pg.time.get_ticks()
            if curr_time - self.last_tremor < setti.tremor_cd:
                yield
            elif self.mark is not None and self.mark.prevvely>0 and self.mark.vely == 0:
                self.last_tremor = curr_time
                for step in range(setti.tremorsteps):
                    yield self.tremor(setti.maxtremor, step)
                for pause in range(setti.tremorpause):
                    yield
            else:
                yield

    def run(self, screen):
        ct = self.checktremor()
        soundObj = random.choice(list(map(lambda x: pg.mixer.Sound(x), setti.songs)))
        soundObj.play()
        myfont = pg.font.SysFont('monospace', 100)
        pg.display.set_caption(setti.title)
        backgroundPic = random.choice(setti.backgrounds)
        bg = pg.transform.scale(setti.get_image(backgroundPic).convert_alpha(), (self.width, self.height))
        pg.mouse.set_visible(False)
        while self.running:
                
            while(self.menu.is_running):
                self.menu.run()

            pg.time.delay(6)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
               

            keys = pg.key.get_pressed()
            if keys[pg.K_ESCAPE]:
                self.running = False
            
            else:
                if len(self.boys) >=2:
                    self.boys[0].update(keys[pg.K_w], keys[pg.K_a], keys[pg.K_d], keys[pg.K_c], keys[pg.K_v], keys[pg.K_b])
                    self.boys[1].update(keys[pg.K_UP], keys[pg.K_LEFT], keys[pg.K_RIGHT], keys[pg.K_i], keys[pg.K_o], keys[pg.K_p])
                for x in self.missles:
                    x.move()
                end = False
                for boy in self.boys:
                    if boy.hp <= 0:
                        end = True
                        screen.blit(myfont.render(boy.__class__.__name__ + " lost", 1, (255, 100, 255)), (self.width/3, self.height/2))
                        pg.display.flip()
                        sleep(3)
                if end:
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
        self.width = screen_size_factor * width
        self.height = screen_size_factor * height
        self.posx = posx
        self.posy = posy
        self.image = pg.transform.scale(image, (self.width, self.height)).convert_alpha()
        self.rightImage = self.image
        self.leftImage = pg.transform.flip(self.image, True, False)
        self.board = board

    def draw(self):
        screen.blit(self.image, (self.posx, self.posy))

    def checkhitcond(self, x):
        if (self.posx + self.width > x.posx) and (self.posx  < x.posx + x.width) and (self.posy + self.height > x.posy) and (self.posy < x.posy + x.height):
            return True
        return False

class Menu:
    def get_next_character_index(self, current_index):
        if(current_index == len(self.characters) - 1):
            return 0
        else:
            return current_index + 1

    def get_previous_character_index(self, current_index):
        if(current_index == 0):
            return len(self.characters) - 1
        else:
            return current_index - 1

    def user_1_left_arrow_click(self):
        self.user_1_character_index = self.get_previous_character_index(self.user_1_character_index)
        self.user_1_character = setti.character_images[self.characters[self.user_1_character_index]]
    def user_1_right_arrow_click(self):
        self.user_1_character_index = self.get_next_character_index(self.user_1_character_index)
        self.user_1_character = setti.character_images[self.characters[self.user_1_character_index]]
    def user_2_left_arrow_click(self):
        self.user_2_character_index = self.get_previous_character_index(self.user_2_character_index)
        self.user_2_character = setti.character_images[self.characters[self.user_2_character_index]]
    def user_2_right_arrow_click(self):
        self.user_2_character_index = self.get_next_character_index(self.user_2_character_index)
        self.user_2_character = setti.character_images[self.characters[self.user_2_character_index]]

    def start_game(self):
        boy_names = [self.characters[self.user_1_character_index], self.characters[self.user_2_character_index]]  # HERE CHANGE CHARACTERS
        boy1 = generate_boy(boy_names[0])
        boy2 = generate_boy(boy_names[1])
        boy1.enemy = boy2
        boy2.enemy = boy1
        self.board.boys = [boy1, boy2]
        self.is_running = False


    def __init__(self, board_width, board_height):
        self.board = None
        self.board_width = board_width
        self.board_height = board_height
        self.is_running = True
        self.image = setti.menupic
        self.width = setti.menu_width
        self.height = setti.menu_height
        self.characters = ['mark', 'van', 'billy', 'piro', 'billy_motor']

        self.user_1_character_index = 1
        self.user_2_character_index = 3
        self.user_1_character = setti.character_images[self.characters[self.user_1_character_index]]
        self.user_2_character = setti.character_images[self.characters[self.user_2_character_index]]
        self.x_offset = (self.board_width - self.width) /2
        self.y_offset = (self.board_height - self.height) /2
        self.user_1_left_arrow_button  = Button(setti.arrow_button_width, setti.arrow_button_height, self.x_offset + 0.15*self.width - setti.arrow_button_width/2, self.y_offset + 0.3*self.height, setti.left_arrow_button_image,  handle_click=self.user_1_left_arrow_click)
        self.user_1_right_arrow_button = Button(setti.arrow_button_width, setti.arrow_button_height, self.x_offset + 0.35*self.width - setti.arrow_button_width/2, self.y_offset + 0.3*self.height, setti.right_arrow_button_image, handle_click=self.user_1_right_arrow_click)
        self.user_2_left_arrow_button  = Button(setti.arrow_button_width, setti.arrow_button_height, self.x_offset + 0.65*self.width - setti.arrow_button_width/2, self.y_offset + 0.3*self.height, setti.left_arrow_button_image,  handle_click=self.user_2_left_arrow_click)
        self.user_2_right_arrow_button = Button(setti.arrow_button_width, setti.arrow_button_height, self.x_offset + 0.85*self.width - setti.arrow_button_width/2, self.y_offset + 0.3*self.height, setti.right_arrow_button_image, handle_click=self.user_2_right_arrow_click)
        self.start_button = Button(setti.start_button_width, setti.start_button_height, self.x_offset + self.width/2 - setti.start_button_width/2, self.y_offset + 0.8 * self.height, setti.start_button_image, handle_click=self.start_game)
        
        self.buttons = [self.user_1_left_arrow_button, self.user_1_right_arrow_button, self.user_2_left_arrow_button, self.user_2_right_arrow_button, self.start_button]
        self.user_1_button_start_position = [self.x_offset + 0.12*self.width, self.y_offset + 0.5*self.height]
        self.user_2_button_start_position = [self.x_offset + 0.62*self.width, self.y_offset + 0.5*self.height]

        self.keyboard_buttons = [Button(setti.keyboard_button_width, setti.keyboard_button_height, self.user_1_button_start_position[0] + setti.keyboard_button_width, self.user_1_button_start_position[1], setti.keyboard_button_image, text="W"),
                                 Button(setti.keyboard_button_width, setti.keyboard_button_height, self.user_1_button_start_position[0], self.user_1_button_start_position[1] + setti.keyboard_button_height + setti.keyboard_gap, setti.keyboard_button_image, text="A"),
                                 Button(setti.keyboard_button_width, setti.keyboard_button_height, self.user_1_button_start_position[0] + setti.keyboard_button_width + setti.keyboard_gap, self.user_1_button_start_position[1] + setti.keyboard_button_height + setti.keyboard_gap, setti.keyboard_button_image, text="S"),
                                 Button(setti.keyboard_button_width, setti.keyboard_button_height, self.user_1_button_start_position[0] + 2*setti.keyboard_button_width + 2*setti.keyboard_gap, self.user_1_button_start_position[1] + setti.keyboard_button_height + setti.keyboard_gap, setti.keyboard_button_image, text="D"),
                                 Button(setti.keyboard_button_width, setti.keyboard_button_height, self.user_1_button_start_position[0] + 4*setti.keyboard_button_width + 4*setti.keyboard_gap, self.user_1_button_start_position[1] + setti.keyboard_button_height + setti.keyboard_gap, setti.keyboard_button_image, text="C"),
                                 Button(setti.keyboard_button_width, setti.keyboard_button_height, self.user_1_button_start_position[0] + 5*setti.keyboard_button_width + 5*setti.keyboard_gap, self.user_1_button_start_position[1] + setti.keyboard_button_height + setti.keyboard_gap, setti.keyboard_button_image, text="V"),
                                 Button(setti.keyboard_button_width, setti.keyboard_button_height, self.user_1_button_start_position[0] + 6*setti.keyboard_button_width + 6*setti.keyboard_gap, self.user_1_button_start_position[1] + setti.keyboard_button_height + setti.keyboard_gap, setti.keyboard_button_image, text="B"),

                                 Button(setti.keyboard_button_width, setti.keyboard_button_height, self.user_2_button_start_position[0] + setti.keyboard_button_width, self.user_2_button_start_position[1], setti.keyboard_button_image, text="↑"),
                                 Button(setti.keyboard_button_width, setti.keyboard_button_height, self.user_2_button_start_position[0], self.user_2_button_start_position[1] + setti.keyboard_button_height + setti.keyboard_gap, setti.keyboard_button_image, text="←"),
                                 Button(setti.keyboard_button_width, setti.keyboard_button_height, self.user_2_button_start_position[0] + setti.keyboard_button_width + setti.keyboard_gap, self.user_2_button_start_position[1] + setti.keyboard_button_height + setti.keyboard_gap, setti.keyboard_button_image, text="↓"),
                                 Button(setti.keyboard_button_width, setti.keyboard_button_height, self.user_2_button_start_position[0] + 2*setti.keyboard_button_width + 2*setti.keyboard_gap, self.user_2_button_start_position[1] + setti.keyboard_button_height + setti.keyboard_gap, setti.keyboard_button_image, text="→"),
                                 Button(setti.keyboard_button_width, setti.keyboard_button_height, self.user_2_button_start_position[0] + 4*setti.keyboard_button_width + 4*setti.keyboard_gap, self.user_2_button_start_position[1] + setti.keyboard_button_height + setti.keyboard_gap, setti.keyboard_button_image, text="I"),
                                 Button(setti.keyboard_button_width, setti.keyboard_button_height, self.user_2_button_start_position[0] + 5*setti.keyboard_button_width + 5*setti.keyboard_gap, self.user_2_button_start_position[1] + setti.keyboard_button_height + setti.keyboard_gap, setti.keyboard_button_image, text="O"),
                                 Button(setti.keyboard_button_width, setti.keyboard_button_height, self.user_2_button_start_position[0] + 6*setti.keyboard_button_width + 6*setti.keyboard_gap, self.user_2_button_start_position[1] + setti.keyboard_button_height + setti.keyboard_gap, setti.keyboard_button_image, text="P")
                                 ]

   

    def draw(self):
        screen.fill([0,0,0])
        screen.blit(self.image, (self.board_width/2 - self.width/2, self.board_height/2 - self.height/2))
        for button in self.buttons:
            button.draw()
        for button in self.keyboard_buttons:
            button.draw()
        screen.blit(self.user_1_character['image'], (self.x_offset + 0.25*self.width - self.user_1_character['width']/2, self.y_offset + 0.3*self.height - self.user_1_character['height'] + setti.arrow_button_height))
        screen.blit(self.user_2_character['image'], (self.x_offset + 0.75*self.width - self.user_2_character['width']/2, self.y_offset + 0.3*self.height - self.user_2_character['height'] + setti.arrow_button_height))
        


    def run(self):
        default_cursor = setti.cursor_default_image
        pointer_cursor = setti.cursor_pointer_image
        while self.is_running:
            is_pointer_cursor = False
            mouse_pos = pg.mouse.get_pos()
            for event in pg.event.get():
                keys = pg.key.get_pressed()
                if keys[pg.K_ESCAPE]:
                    self.is_running = False

                for button in self.buttons:
                        if button.check_if_clicked(mouse_pos):  
                            if event.type == pg.MOUSEBUTTONDOWN:
                                button.handle_click()

            self.draw()

            
            
            
            cursor_posx = mouse_pos[0]
            cursor_posy = mouse_pos[1]

            if mouse_pos[0] < self.x_offset:
                pg.mouse.set_pos([self.x_offset, mouse_pos[1]])
                cursor_posx = self.x_offset
                cursor_posy = mouse_pos[1]
            
            elif  mouse_pos[0] > self.x_offset + self.width:
                pg.mouse.set_pos([self.x_offset + self.width, mouse_pos[1]])
                cursor_posx = self.x_offset + self.width
                cursor_posy =  mouse_pos[1]
            
            if mouse_pos[1] < self.y_offset:
                pg.mouse.set_pos([mouse_pos[0], self.y_offset])
                cursor_posx = mouse_pos[0]
                cursor_posy = self.y_offset
            elif mouse_pos[1] > self.y_offset + self.height:
                pg.mouse.set_pos([mouse_pos[0], self.y_offset + self.height])
                cursor_posx = mouse_pos[0]
                cursor_posy = self.y_offset + self.height

            for button in self.buttons:
                if button.check_if_clicked(mouse_pos):  
                    screen.blit(pointer_cursor, (cursor_posx - setti.cursor_pointer_width/2, cursor_posy - setti.cursor_pointer_height/2))

                    is_pointer_cursor = True
            if not is_pointer_cursor:
                screen.blit(default_cursor, (cursor_posx - setti.cursor_default_width/2, cursor_posy - setti.cursor_default_height/2))
            
            pg.display.flip()  
            


class Button(Object):
    def __init__(self, width, height, posx, posy, image, handle_click=None, text=None, board=None):
        super().__init__(width, height, posx, posy, image)
        self.text = text
        self.handle_click = handle_click

    def check_if_clicked(self, mouse_pos):
        if (mouse_pos[0] >= self.posx) and (mouse_pos[0] <= self.posx + self.width) and (mouse_pos[1] >= self.posy) and (mouse_pos[1] <= self.posy + self.height):
            return True
    def draw(self):
        if not self.text:
            super().draw()
        else:
            button = pg.Surface((self.width, self.height), pg.SRCALPHA, 32).convert_alpha()
            font = pg.font.SysFont('firacode', 20, bold=True)
            buttonBG = self.image
            button.blit(buttonBG , (0, 0))
            text = font.render(self.text, 1, (36, 30, 100))
            text_rect = text.get_rect(center=(self.width/2, self.height/2 ))
            button.blit(text, text_rect)
            screen.blit(button, (self.posx, self.posy))


class Platform(Object):
    def __init__(self, width, height, posx, posy):
        super().__init__(width, height, posx, posy, setti.platformimage)
    def draw(self):
        super().draw()
    


class Charm(Object):
    def __init__(self, width, height, posx, posy, charmimage, velx, crushimage, owner, board=None):
        super().__init__(width, height, posx, posy, charmimage, board)
        self.velx = screen_size_factor * velx
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
        self.velx = screen_size_factor * velx
        self.vely = screen_size_factor * vely
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
        
        for x in self.board.boys:
            if (not self.crushed) and (self.checkhitcond(x)):
                self.crushed = True
                if x.stunned and self.width:
                    x.hp -= setti.stunnedbonus
                x.hp -= self.dmg
                self.crushtime = pg.time.get_ticks()
                self.velx = 0
                self.vely = 0
                self.image = self.crushimage
       



class Character(Object):
    def __init__(self, width, height, posx, posy, image, dmg, movespeed, accframes, shootpause, hp, jumpvel, board=None):
        super().__init__(width, height, posx, posy, image, board)
        self.velx = 0
        self.vely = 0
        self.prevvely = 0
        self.dmg = dmg
        self.movespeed = screen_size_factor * movespeed
        self.accframes = accframes
        self.shootpause = shootpause
        self.hp = hp
        self.jumpvel = screen_size_factor * jumpvel
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
        if self.posy < 0:
            self.posy = 0
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
            elif self.__class__.__name__ == 'Billy_motor':
                self.shoot()
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
            if self.velx > -self.movespeed:
                self.velx -= self.movespeed/self.accframes
            self.image = self.leftImage
        if p_right:
            if self.velx < self.movespeed:
                self.velx += self.movespeed/self.accframes
            self.image = self.rightImage
        if not (p_left or p_right):
            if abs(self.velx) < self.movespeed/self.accframes:
                self.velx = 0
            else:
                if self.velx > 0:
                    self.velx -= self.movespeed/self.accframes
                elif  self.velx <0:
                    self.velx += self.movespeed/self.accframes

        if self.stands() and self.vely>0:
            self.posy = self.stands().posy - self.height
            self.vely = 0
        elif self.stands() and self.vely==0:
            pass
        else:
            self.vely += screen_size_factor * setti.fallspeed
        if self.stands() and self.vely == 0 and p_up:
            self.vely -= self.jumpvel
        if self.charmed:
            if self.enemy.posx > self.posx:
                self.velx = screen_size_factor * setti.charmedvel
            else:
                self.velx = - screen_size_factor * setti.charmedvel
        self.posx += self.velx
        if(self.posx + self.velx > (self.board.width - self.width) and self.velx > 0):
            self.velx = 0
            self.posx = self.board.width - self.width
        if(self.posx + self.velx < 0 and self.velx < 0):
            self.velx = 0
            self.posx = 0

        
        self.posy += self.vely
        if(self.__class__.__name__ == 'Billy_motor'):
            if(self.checkhitcond(self.enemy)):
                curr_time = pg.time.get_ticks()
                if (curr_time-self.last_hit > setti.billy_motor_hit_cd):
                    self.last_hit = curr_time
                    self.enemy.hp -= (abs(self.velx) * setti.billy_motor_hit_dmg_multiplier) // 1
                    self.enemy.velx += setti.billy_motor_hit_velx*self.velx
                    if self.enemy.vely > setti.billy_motor_hit_vely*self.vely - setti.billy_motor_static_hit_vely:
                        self.enemy.vely += setti.billy_motor_hit_vely*self.vely - setti.billy_motor_static_hit_vely






    def stands(self):
        for x in self.board.platforms:
            if ((((self.posy + self.height) > x.posy - screen_size_factor * setti.jumpcatch) and ((self.posy + self.height) < x.posy + screen_size_factor * setti.jumpcatch)) 
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
    def __init__(self, width, height, posx, posy, image, dmg, movespeed, accframes, shootpause, hp, jumpvel, board=None):
        super().__init__(width, height, posx, posy, image, dmg, movespeed, accframes, shootpause, hp, jumpvel, board)
        self.shotguncd = 0
        self.showercd = 0

    def shotgun(self, dir):
        if (pg.time.get_ticks() - self.shotguncd) > setti.shotguncd:
            self.shotguncd = pg.time.get_ticks()
            if dir == "right":
                self.board.missles.append(Missle(setti.misslewidth, setti.missleheight, self.posx + self.width, 
                self.posy + self.height * setti.shootheight, setti.rightmissleImage, screen_size_factor * setti.misvel + self.velx, screen_size_factor * (self.vely*setti.spreadfactor + setti.shootwidth), self.dmg,  setti.splashtime, setti.crushImage, self.board))
                self.board.missles.append(Missle(setti.misslewidth, setti.missleheight, self.posx + self.width, 
                self.posy + self.height * setti.shootheight, setti.rightmissleImage, screen_size_factor * setti.misvel + self.velx, screen_size_factor * (self.vely*setti.spreadfactor), self.dmg,  setti.splashtime, setti.crushImage, self.board))
                self.board.missles.append(Missle(setti.misslewidth, setti.missleheight, self.posx + self.width, 
                self.posy + self.height * setti.shootheight, setti.rightmissleImage, screen_size_factor * setti.misvel + self.velx, screen_size_factor * (self.vely*setti.spreadfactor - setti.shootwidth), self.dmg,  setti.splashtime, setti.crushImage, self.board))

            else:
                self.board.missles.append(Missle(setti.misslewidth, setti.missleheight, self.posx + setti.safeshot, 
                self.posy + self.height * setti.shootheight, setti.leftmissleImage, screen_size_factor * -setti.misvel + self.velx, screen_size_factor *(self.vely*setti.spreadfactor + setti.shootwidth), self.dmg,  setti.splashtime, setti.crushImage, self.board))
                self.board.missles.append(Missle(setti.misslewidth, setti.missleheight, self.posx + setti.safeshot, 
                self.posy + self.height * setti.shootheight, setti.leftmissleImage, screen_size_factor *  -setti.misvel + self.velx, screen_size_factor * self.vely*setti.spreadfactor, self.dmg,  setti.splashtime, setti.crushImage, self.board))
                self.board.missles.append(Missle(setti.misslewidth, setti.missleheight, self.posx + setti.safeshot, 
                self.posy + self.height * setti.shootheight, setti.leftmissleImage, screen_size_factor * -setti.misvel + self.velx, screen_size_factor * (self.vely*setti.spreadfactor - setti.shootwidth), self.dmg,  setti.splashtime, setti.crushImage, self.board))


    def shower(self):
        if(pg.time.get_ticks() - self.showercd > setti.showercd):
            self.showercd = pg.time.get_ticks()
            self.board.missles.append(Missle(setti.missleheight * setti.showersize, setti.misslewidth * setti.showersize, self.enemy.posx - setti.showerwidth, 
            0, pg.transform.rotate(setti.rightmissleImage, -90), 0, screen_size_factor * setti.showervel, self.dmg,  setti.splashtime, setti.crushImage, self.board))
            self.board.missles.append(Missle(setti.missleheight * setti.showersize, setti.misslewidth * setti.showersize, self.enemy.posx, 
            0, pg.transform.rotate(setti.rightmissleImage, -90), 0, screen_size_factor * setti.showervel, self.dmg,  setti.splashtime, setti.crushImage, self.board))
            self.board.missles.append(Missle(setti.missleheight * setti.showersize, setti.misslewidth * setti.showersize, self.enemy.posx + setti.showerwidth, 
            0, pg.transform.rotate(setti.rightmissleImage, -90), 0, screen_size_factor * setti.showervel, self.dmg,  setti.splashtime, setti.crushImage, self.board))

    
class Mark(Character):
    def __init__(self, width, height, posx, posy, image, dmg, movespeed, accframes, shootpause, hp, jumpvel, board=None):
        super().__init__(width, height, posx, posy, image, dmg, movespeed, accframes, shootpause, hp, jumpvel, board)
        self.fatshotcd = 0

    def fatshot(self, dir):
        if(pg.time.get_ticks() - self.fatshotcd > setti.fatshotcd):
            self.fatshotcd = pg.time.get_ticks()
            if dir == "right":
                self.board.missles.append(Missle(setti.misslewidth * setti.fatshotfactor , setti.missleheight * setti.fatshotfactor, self.posx + self.width, 
                self.posy + self.height * setti.shootheight, setti.fatrightmissleImage, screen_size_factor * setti.misvel + self.velx, screen_size_factor * self.vely*setti.spreadfactor, self.dmg, setti.splashtime, pg.transform.scale(setti.fatcrushImage, (setti.misslewidth*setti.fatshotfactor, setti.missleheight*setti.fatshotfactor)), self.board))
            else:
                self.board.missles.append(Missle(setti.misslewidth * setti.fatshotfactor , setti.missleheight * setti.fatshotfactor, self.posx - setti.fatshotwidth, 
                self.posy + self.height * setti.shootheight, setti.fatleftmissleImage, screen_size_factor * -setti.misvel + self.velx, screen_size_factor * self.vely*setti.spreadfactor, self.dmg, setti.splashtime, pg.transform.scale(setti.fatcrushImage, (setti.misslewidth*setti.fatshotfactor, setti.missleheight*setti.fatshotfactor)), self.board))


class Billy(Character):
    def __init__(self, width, height, posx, posy, image, dmg, movespeed, accframes, shootpause, hp, jumpvel, board=None):
        super().__init__(width, height, posx, posy, image, dmg, movespeed, accframes, shootpause, hp, jumpvel, board)
        self.charmcd = 0


    def charm(self):
        if(pg.time.get_ticks() - self.charmcd > setti.charmcd):
            self.charmcd = pg.time.get_ticks()
            self.board.charms.append(Charm(setti.charmwidth, setti.charmheight, self.posx + self.width/2, self.posy + self.height/2, setti.charmimage, screen_size_factor * setti.charmvelx, setti.charmcrushimage, self, self.board))
            self.board.charms.append(Charm(setti.charmwidth, setti.charmheight, self.posx + self.width/2, self.posy + self.height/2, setti.charmimage, screen_size_factor * -setti.charmvelx, setti.charmcrushimage, self, self.board))

    def shoot(self, dir):
        if (pg.time.get_ticks() - self.lastshot) > self.shootpause:
            self.lastshot = pg.time.get_ticks()
            if dir == "right":
                self.board.missles.append(Missle(setti.misslewidth, setti.missleheight, self.posx + self.width, 
                self.posy + self.height * setti.shootheight, setti.rightmissleImage, screen_size_factor * setti.misvel + self.velx, screen_size_factor * self.vely*setti.spreadfactor, self.dmg,  setti.splashtime, setti.crushImage, self.board))
            else:
                self.board.missles.append(Missle(setti.misslewidth, setti.missleheight, self.posx + setti.safeshot, 
                self.posy + self.height * setti.shootheight, setti.leftmissleImage, screen_size_factor * -setti.misvel + self.velx, screen_size_factor * self.vely*setti.spreadfactor, self.dmg,  setti.splashtime, setti.crushImage, self.board))

class Billy_motor(Character):
    def __init__(self, width, height, posx, posy, image, dmg, movespeed, accframes, shootpause, hp, jumpvel, board=None):
        super().__init__(width, height, posx, posy, image, dmg, movespeed, accframes, shootpause, hp, jumpvel, board)
        self.last_hit = 0


    def shoot(self):
        if (pg.time.get_ticks() - self.lastshot) > self.shootpause:
            self.lastshot = pg.time.get_ticks()
            self.board.missles.append(Missle(setti.missleheight, setti.misslewidth, self.posx + self.width/2, 
            self.posy - self.height, setti.topmissleImage, self.velx * setti.billy_mottor_missle_velx_spread_factor, -setti.billy_motor_misslevel, self.dmg, setti.splashtime, setti.crushImage, self.board))

    
            

class Piro(Character):
    def __init__(self, width, height, posx, posy, image, dmg, movespeed, accframes, shootpause, hp, jumpvel, board=None):
        super().__init__(width, height, posx, posy, image, dmg, movespeed, accframes, shootpause, hp, jumpvel, board)
        self.last_fire = 0

    def fire(self):#self, width, height, posx, posy, images, owner, board=None)
        curr_time = pg.time.get_ticks()
        if (curr_time-self.last_fire > setti.fire_cd):
            self.board.flames.append(Flame(setti.fire_size[0], setti.fire_size[1], self.enemy.posx + (self.enemy.width/2 - setti.fire_size[0]/2), self.enemy.posy+ (self.enemy.height - setti.fire_size[1]), setti.fire_images, self, self.board))
            self.last_fire = curr_time
    

    
pg.init()
infoObject = pg.display.Info()
width = infoObject.current_w
height = infoObject.current_h
screen = pg.display.set_mode((width, height), pg.FULLSCREEN)
plats = []
screen_size_factor = width/setti.width

#generate platforms randomly
def draw_platforms():
    for i in range(setti.numberofplatforms):
        stopper = True
        platform_x, platform_y = 0, 0
        plat_width = random.choice(setti.platform_widths)
        while stopper:
            platform_x = random.randint(0, width)
            platform_y = random.randint(setti.platform_height_correction, height - setti.platform_height)
            found = True
            for platform in plats:
                if abs(platform.posx - platform_x) < screen_size_factor * setti.platform_dist[0] and abs(platform.posy - platform_y) < screen_size_factor * setti.platform_dist[1] or platform_x + plat_width > width:
                    found = False
            stopper = not found

        plats.append(Platform(plat_width, setti.platform_height, platform_x, platform_y))
        
draw_platforms()

board = Board(width, height, [Platform(2*width, setti.platform_height, -500, height - setti.platform_height/2), *plats], [], [], [], [], Menu(width, height), boys=[])



def generate_boy(name):
    if name == 'mark':
        mark = Mark(*setti.mark, board)
        board.mark = mark
        return mark
    elif name == 'van':
        return Van(*setti.van, board)
    elif name == 'billy':
        return Billy(*setti.billy, board)
    elif name == 'piro':
        return Piro(*setti.piro, board)
    elif name == 'billy_motor':
        return Billy_motor(*setti.billy_motor, board)



board.run(screen)














