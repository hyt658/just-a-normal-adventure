import pgzrun

TITLE = 'Just a normal Adventure'
WIDTH = 800
HEIGHT = 450
G = 0.3

player = Actor('stand1',(140,325))
stage1 = Actor('stage1',(370,333))
pipe1 = Actor('pipe1',(140,58))
pipe2_top = Actor('pipe2_top',(496,256))
pipe2_bottom = Actor('pipe2_bottom',(495,318))
block = Actor('block',(370,255))
block1 = Actor('white',(420,255))
blockrest = Actor('blockrestwhite',(173,255))
music.play('bgm')

player.vx = 3.8
player.vy = 0
player_velocity = -10
player.direction = 'right'
player.walking = 'on'
player.jumping = 'off'
player.life = 'live'


def update():
    player_walking()
    player_jumping()
    colliderect()
    landing_test()
    if player.life == 'death':
        exit()


def draw():
    screen.fill((255, 255, 255))
    stage1.draw()
    blockrest.draw()
    block.draw()
    block1.draw()
    player.draw()
    pipe1.draw()
    pipe2_top.draw()
    pipe2_bottom.draw()


def player_walking():
    if player.walking == 'on':
        if keyboard.d:
            player.direction = 'right'
            player.x += player.vx
            player.image = 'walk1'
            player.image = 'walk2'
        elif keyboard.a:
            player.direction = 'left'
            player.x -= player.vx
            player.image = 'walk3'
            player.image = 'walk4'
        else:
            if player.direction == 'right':
                player.image = 'stand1'
            elif player.direction == 'left':
                player.image = 'stand2'
    

def player_jumping():
    if player.jumping == 'off':
        if keyboard.w: 
            player.vy = player_velocity
            player.jumping = 'on'
    elif player.jumping == 'on':
        falling()

    if player.y < 336:  
        if player.direction == 'right':
            player.image = 'jump1'
        elif player.direction == 'left':
            player.image = 'jump2'


def falling():
    player.vy += G
    player.y += player.vy
    player.jumping = 'on'


def landing_test():
    if player.y > 336: 
        if stage1.left < player.x < stage1.right:
            player.y = 336
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
    else:
        falling()

    if player.y > HEIGHT:
        player.life = 'death'

    if player.colliderect(block):
        if block.left < player.x < block.right and player.y < block.y:
            player.y = 210
            player.vy = 0
            player.jumping = 'off'
            if player.direction == 'right':
                player.image = 'stand1'
            elif player.direction == 'left':
                player.image = 'stand2'        

    if player.colliderect(pipe2_top):
        if pipe2_top.left < player.x < pipe2_top.right:
            if player.y < pipe2_top.y:
                if not 475 < player.x < 515:
                    player.vy = 0
                    player.y = 215
                    player.jumping = 'off'  
                if player.direction == 'right':
                    player.image = 'stand1'
                elif player.direction == 'left':
                    player.image = 'stand2'  
            elif player.y > pipe2_top.y:
                player.pos = (140,58)
            

def colliderect():
    if player.colliderect(pipe2_bottom):
        if player.x < pipe2_bottom.x:
            player.walking = 'off'
            player.x -= 1
        elif player.x > pipe2_bottom.x:
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


def blockmove():    
    block.y += 4

def block1move():
    block1.y += 4

def blockrestmove():
    blockrest.y += 4


pgzrun.go()