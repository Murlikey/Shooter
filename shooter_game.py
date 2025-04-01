#Создай собственный Шутер!

from pygame import *
from random import randint
from time import time as timer
mw = display.set_mode((800,600))
display.set_caption('шутер')

bg = transform.scale(image.load('galaxy.jpg'), (800,600))

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

font.init()
font2 = font.SysFont('Arial', 35)
score = 0
lost = 0

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, w, h, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (w,h))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        mw.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_RIGHT] and self.rect.x < 735:
            self.rect.x += self.speed
        if keys[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, 15)
        bullets.add(bullet)
        
class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = randint(0,620)
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()


bullets = sprite.Group()

player = Player('rocket.png', 5, 420, 80, 100,4)

monsters = sprite.Group()
for i in range(5):
    monster = Enemy('ufo.png', randint(0,620), -40, 80, 50, randint(1,5))
    monsters.add(monster)

asteroids = sprite.Group()
for i in range(3):
    asteroid = Enemy('asteroid.png', randint(0,620), -40, 80, 50, randint(1,5))
    asteroids.add(asteroid)

run = True

font.init()
font = font.SysFont('Arial', 70)
win = font.render("YOU WIN", True, (0, 255, 0))
lose = font.render("YOU LOSE", True, (255, 0, 0))

num_fire = 0
rel_time = False

game = True
finish = False
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    fire_sound.play()
                    player.fire()
                    num_fire += 1
                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True
    if not finish:
        mw.blit(bg, (0,0))
        if rel_time:
            now_time = timer()
            if now_time - last_time < 3:
                reload = font.render("RELOAD", True, (0, 255, 0))
                mw.blit(reload, (250, 400))
            else:
                num_fire = 0
                rel_time = False
        player.reset()
        player.update()
        monsters.update()
        monsters.draw(mw)
        text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        mw.blit(text_lose, (10,50))
        text = font2.render("Счет" + str(score), True, (255,255,255))
        mw.blit(text, (10,20))
        bullets.update()
        bullets.draw(mw)
        asteroids.draw(mw)
        asteroids.update()
        if sprite.groupcollide(bullets,monsters,True,True):
            score += 1
            monster = Enemy('ufo.png', randint(0,620), -40, 80, 50, randint(1,5))
            monsters.add(monster)
        if score > 9:
            finish = True
            mw.blit(win, (300, 200))
        if sprite.spritecollide(player, monsters, False) or sprite.spritecollide(player, asteroids, False):
            finish = True
            mw.blit(lose, (300,200))
            

            
        
        
            



    display.update()
    time.delay(10)