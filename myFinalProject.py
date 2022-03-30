import pgzrun
import os
import sys
import random

TITLE = 'Just a normal Adventure'
WIDTH = 800
HEIGHT = 450
G = 0.3

failpic = ['fail1','fail2','fail3','fail4','fail5']
n = random.randint(0,4)

player = Actor('stand1',(140,325))
stage1 = Actor('stage1',(370,225))
stage2 = Actor('stage2',(1249,226))
stage3 = Actor('stage3',(1973,226))
pipe_top = Actor('pipe_top',(500,251))
pipe_bottom = Actor('pipe_bottom',(500,313))
block = Actor('block',(370,255))
block1 = Actor('white',(420,255))
block2 = Actor('white',(1940,235))
blockrest = Actor('blockrestwhite',(173,255))
enemy = Actor('enemy',(370,255))
stair1 = Actor('stair',(762,274))
stair2 = Actor('stair',(965,170))
stair3 = Actor('stair',(1168,274))
stair4 = Actor('stair',(1365,378))
door = Actor('door',(2023,326))
out = Actor('exit',(2020,228))
heavendoor = Actor('heavendoor',(2020,60))
fail = Actor(failpic[n],(400,225))
congratulations = Actor('congratulations',(176,225))
letter = Actor('letter',(575,225))
music.play('bgm')
music.set_volume(0.8)

player.vx = 4
player.vy = 0
player.velocity = -10
speed = 4
player.direction = 'right'
player.walking = 'on'
player.jumping = 'off'
player.situation = 'live'
enemy.attack = 'off'
stair1.moving = 'off'
stair4.moving = 'off'
player.knockoff = 'off'



def update():
    if player.situation == 'live':
        map_moving()
        player_walking()
        player_jumping()
        colliderect()
        enemy_flower()
        landing_test()
        stair_moving()
    elif player.situation == 'pass':
        passed()
    elif player.situation == 'death':
        if keyboard.space:
            restart()
    
def draw():
    screen.fill((255, 255, 255))
    stage1.draw()
    stage2.draw()
    stage3.draw() 
    enemy.draw()
    blockrest.draw()
    block.draw()
    block1.draw()
    block2.draw()
    door.draw()
    out.draw()
    player.draw()
    pipe_top.draw()
    pipe_bottom.draw()
    stair1.draw()
    stair2.draw()
    stair3.draw()
    stair4.draw()
    if player.situation == 'pass':
        heavendoor.draw()
        player.draw()
    elif player.situation == 'death':
        fail.draw()
    elif player.situation == 'passed':
        screen.clear()
        screen.fill((255, 255, 255))
        congratulations.draw()
        letter.draw()
    
def restart():
    python = sys.executable
    os.execl(python, python, * sys.argv)

def player_walking():
    if player.walking == 'on':
        if keyboard.d:
            player.direction = 'right'
            player.x += player.vx
            player.image = 'walk1'
        elif keyboard.a:
            player.direction = 'left'
            player.x -= player.vx
            player.image = 'walk2'
        else:
            if player.direction == 'right':
                player.image = 'stand1'
            elif player.direction == 'left':
                player.image = 'stand2'
    
def player_jumping():
    if player.jumping == 'off':
        if keyboard.w:
            player.vy = player.velocity
            player.jumping = 'on'
    elif player.jumping == 'on':
        falling()

    if player.y < 332:  
        if not player.colliderect(block) or not player.colliderect(stair1) or not player.colliderect(stair2) or not player.colliderect(stair3) or not player.colliderect(stair4) or not player.colliderect(block2):
            if player.direction == 'right':
                player.image = 'jump1'
            elif player.direction == 'left':
                player.image = 'jump2'

def falling():
    player.vy += G
    player.y += player.vy
    player.jumping = 'on'

def landing_test():
    if player.y > 332 and not player.colliderect(stair4):
        if stage1.left < player.x < stage1.right:
            player.y = 332
            player.vy = 0
            player.jumping = 'off'
        elif stage1.left > player.x:
            if player.colliderect(stage1):
                player.vx = 0
                player.x -= 1
        elif stage1.right < player.x:
            if player.colliderect(stage1):
                player.vx = 0
                player.x += 1
        if stage3.left < player.x < stage3.right:
            player.y = 332
            player.vy = 0
            player.jumping = 'off'
        elif stage3.left > player.x:
            if player.colliderect(stage3):
                player.vx = 0
                player.x -= 1
        elif stage3.right < player.x:
            if player.colliderect(stage3):
                player.vx = 0
                player.x += 1
    else:
        falling()

    if player.top > HEIGHT:
        player.situation = 'death'

    if player.colliderect(block):
        if block.left < player.x < block.right and player.y < block.y:
            player.y = 210
            player.vy = 0
            player.jumping = 'off'
            if player.direction == 'right':
                player.image = 'stand1'
            elif player.direction == 'left':
                player.image = 'stand2'

    if block2.image == 'blockblank':
        if player.colliderect(block2):
            if block2.left < player.x < block2.right and player.y < block.y:
                player.y = 190
                player.vy = 0
                player.jumping = 'off'
                if player.direction == 'right':
                    player.image = 'stand1'
                elif player.direction == 'left':
                    player.image = 'stand2'      

    if player.colliderect(pipe_top):
        if pipe_top.left < player.x < pipe_top.right:
            if player.y < pipe_top.y:
                if not 480 < player.x < 515:
                    player.vy = 0
                    player.y = 209
                    player.jumping = 'off'  
                if player.direction == 'right':
                    player.image = 'stand1'
                elif player.direction == 'left':
                    player.image = 'stand2'  
            elif player.y > pipe_top.y:
                player.pos = (140,58)

    if player.colliderect(stair1):
        if player.y < stair1.y:
            if stair1.left < player.x < stair1.right:
                player.vy = 0
                player.y = 240
                player.jumping = 'off'
            if player.direction == 'right':
                player.image = 'stand1'
            elif player.direction == 'left':
                player.image = 'stand2'   
    
    if player.colliderect(stair2):
        if player.y < stair2.y:
            if stair2.left < player.x < stair2.right:
                player.vy = 0
                player.y = 136
                player.jumping = 'off'
            if player.direction == 'right':
                player.image = 'stand1'
            elif player.direction == 'left':
                player.image = 'stand2'   

    if player.colliderect(stair3):
        if player.y < stair3.y:
            if stair3.left < player.x < stair3.right:
                player.vy = 0
                player.y = 240
                player.jumping = 'off'
                clock.schedule(stairfalling,1.2)
            if player.direction == 'right':
                player.image = 'stand1'
            elif player.direction == 'left':
                player.image = 'stand2'   

    if player.colliderect(stair4):
        if player.y < stair4.y:
            if stair4.left < player.x < stair4.right:
                player.vy = 0
                player.y = 344
                player.jumping = 'off'
            if player.direction == 'right':
                player.image = 'stand1'
            elif player.direction == 'left':
                player.image = 'stand2'

    if player.colliderect(out):
        if out.left < player.x < out.right and player.y < out.y:
            if player.vy > 0:
                player.situation = 'pass'

def stairfalling():
    stair3.vy = 0
    stair3.vy += 20
    stair3.y += stair3.vy

def colliderect():
    if player.colliderect(pipe_bottom):
        if player.x < pipe_bottom.x:
            player.walking = 'off'
            player.x -= 1
        elif player.x > pipe_bottom.x:
            player.walking = 'off'
            player.x += 1
    else:
        player.walking = 'on'  

    if block.left < player.x < block.right and player.y > block.y: 
        if player.colliderect(block):
            player.vy = 0
            block.y -= 4
            block.image = 'blockblank'
            clock.schedule(blockmove, 0.05)
            block1.image = 'blockblank' 
            blockrest.image = 'blockrest'
    elif player.x < block.left:
        if player.colliderect(block):
            player.walking = 'off'
            player.x -= 1
    
    if player.colliderect(block1) and player.y > block1.y:
        if player.vy < 0:
            player.vy = 0
            block1.y -= 4
            block1.image = 'blockblank'
            clock.schedule(block1move, 0.05)
        
    if block1.image == 'blockblank':
        if blockrest.left < player.x < blockrest.right and player.y > blockrest.y:
            if player.colliderect(blockrest):
                player.vy = 0
                blockrest.y -= 4
                blockrest.image = 'blockrest'
                clock.schedule(blockrestmove, 0.05)
    
    if player.colliderect(door):
        door.image = 'dooropen'
        player.walking = 'off'
        player.knockoff = 'on'
    if player.knockoff == 'on':
        player.image = 'knockdown'
        player.velocity = 0
        if player.colliderect(stage3):
            player.x -= 10

    if block2.left < player.x < block2.right and player.y > block2.y:
        if player.colliderect(block2):
            if player.vy < 0:
                block2.image = 'blockblank'
                player.vy = 0
                block2.y -= 4
                clock.schedule(block2move, 0.05)
    elif player.x < block2.left:
        if player.colliderect(block2):
            player.walking = 'off'
            player.x -= 1
    elif player.x > block2.right:
        if player.colliderect(block2):
            player.walking = 'off'
            player.x += 1

def blockmove():    
    block.y += 4

def block1move():
    block1.y += 4

def blockrestmove():
    blockrest.y += 4

def block2move():
    block2.y += 4

def enemy_flower():
    if enemy.attack == 'off':
        if 300 < player.x < block.right:
            if player.y < block.y:
                if enemy.y > 216:
                    enemy.y -= 3
                    clock.schedule(enemy_flowerOff,1.5)
        if not enemy.colliderect(block):
            if player.colliderect(enemy):
                player.situation = 'death'

def enemy_flowerOff():
    enemy.y += 3
    enemy.attack = 'on'

def map_moving():
    global speed
    if player.x > 562:
        player.x -= speed
        stage1.x -= speed
        stage2.x -= speed
        stage3.x -= speed
        pipe_top.x -= speed
        pipe_bottom.x -= speed
        block.x -= speed
        block1.x -= speed
        block2.x -= speed
        blockrest.x -= speed
        enemy.x -= speed
        stair1.x -= speed
        stair2.x -= speed
        stair3.x -= speed
        stair4.x -= speed
        door.x -= speed
        out.x -= speed
        heavendoor.x -= speed
        if stage3.right < WIDTH:
            speed = 0
    if stair4.moving == 'on':
        stair4.x += 2.5

def stair_moving():
    if stair1.moving == 'off':
        if player.y < stair1.top:
            if stair1.right < 700:
                stair1.x += 60
                stair1.moving = 'on'

    if stair4.moving == 'off' and stage3.left > 685:
        if player.colliderect(stair4):
            stair4.moving = 'on'
    if stage3.left < 685:
        stair4.moving = 'off'
        stair4.x -= 4

def passed():
    player.image = 'stand1'
    player.vy = 0
    player.vy += 1
    player.y -= player.vy
    if player.y < heavendoor.y:
        player.situation = 'passed'

pgzrun.go()