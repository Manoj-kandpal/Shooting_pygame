import pygame
pygame.init()
import random

win_width = 500
win_height = 500
win = pygame.display.set_mode((win_width,win_height))
pygame.display.set_caption("First game")

left = [pygame.image.load("Pics/L1.png"),pygame.image.load("Pics/L2.png"),pygame.image.load("Pics/L3.png"),pygame.image.load("Pics/L4.png"),pygame.image.load("Pics/L5.png"),pygame.image.load("Pics/L6.png"),pygame.image.load("Pics/L7.png"),pygame.image.load("Pics/L8.png"),pygame.image.load("Pics/L9.png")]
right = [pygame.image.load("Pics/R1.png"),pygame.image.load("Pics/R2.png"),pygame.image.load("Pics/R3.png"),pygame.image.load("Pics/R4.png"),pygame.image.load("Pics/R5.png"),pygame.image.load("Pics/R6.png"),pygame.image.load("Pics/R7.png"),pygame.image.load("Pics/R8.png"),pygame.image.load("Pics/R9.png")]
backGround = pygame.image.load("Pics/bg.jpg")
standingOnly = pygame.image.load("Pics/standing.png")
clock = pygame.time.Clock()
facing = 1
music = pygame.mixer.music.load("Pics/rise-and-shine.wav")
shoot = pygame.mixer.Sound("Pics/bullet.wav")
hit = pygame.mixer.Sound("Pics/hit.wav")
pygame.mixer.music.play(-1)

class Player():
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.walkLeft = False
        self.walkRight = False
        self.walkCount = 0
        self.isJump = False
        self.jumpCount = 10
        self.standing = True
        self.hitbox = (self.x + 19,self.y + 10,25,55)
    
    def updater(self,win):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0
        if not(self.standing):
            if self.walkLeft:
                picShown = left[self.walkCount//3]
                self.walkCount += 1
                win.blit(picShown,(self.x,self.y))
            elif self.walkRight:
                picShown = right[self.walkCount//3]
                self.walkCount += 1
                win.blit(picShown,(self.x,self.y))
        else:
            if self.walkRight:
                win.blit(right[0],(self.x,self.y))
            else:
                win.blit(left[0],(self.x,self.y))
        self.hitbox = (self.x + 19,self.y + 10,25,55)
        #pygame.draw.rect(win,(250,0,0),self.hitbox,2)
        
    def hit(self):
        self.x = 60
        font = pygame.font.SysFont("Calibre",100)
        self.walkCount = 0
        text = font.render("-5",1,(255,0,0))
        win.blit(text,(250-(text.get_width()/2),200))
        pygame.display.update()
        pygame.time.delay(1000)
        
class Projectile():
    def __init__(self,x,y,radius,color,facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.vel = 8 * facing
        self.facing = facing
        
    def draw(self,win):
        pygame.draw.circle(win,self.color,(self.x,self.y),self.radius)
        
    def hit(self):
        hit.play()
        
        
class Enemy():
    walkLeft = [pygame.image.load("Pics/E/L1E.png"),pygame.image.load("Pics/E/L2E.png"),pygame.image.load("Pics/E/L3E.png"),pygame.image.load("Pics/E/L4E.png"),pygame.image.load("Pics/E/L5E.png"),pygame.image.load("Pics/E/L6E.png"),pygame.image.load("Pics/E/L7E.png"),pygame.image.load("Pics/E/L8E.png"),pygame.image.load("Pics/E/L9E.png"),pygame.image.load("Pics/E/L10E.png"),pygame.image.load("Pics/E/L11E.png")]
    walkRight = [pygame.image.load("Pics/E/R1E.png"),pygame.image.load("Pics/E/R2E.png"),pygame.image.load("Pics/E/R3E.png"),pygame.image.load("Pics/E/R4E.png"),pygame.image.load("Pics/E/R5E.png"),pygame.image.load("Pics/E/R6E.png"),pygame.image.load("Pics/E/R7E.png"),pygame.image.load("Pics/E/R8E.png"),pygame.image.load("Pics/E/R9E.png"),pygame.image.load("Pics/E/R10E.png"),pygame.image.load("Pics/E/R11E.png")]
    
    def __init__(self,x,y,width,height,end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x,self.end]
        self.vel = 5
        self.walkCount = 0
        self.hitbox = (self.x + 11,self.y,35,60)
        self.health = 10
        self.visible = True
        
    
    def draw(self,win):
        self.move()
        if self.health > 0:
            if self.vel > 0:
                win.blit(self.walkRight[self.walkCount//3],(self.x,self.y))
            else:
                win.blit(self.walkLeft[self.walkCount//3],(self.x,self.y))
            self.hitbox = (self.x + 11,self.y,45,60)
            #pygame.draw.rect(win,(250,0,0),self.hitbox,2)
            pygame.draw.rect(win,(250,0,0),(self.hitbox[0],self.hitbox[1]-10,50,7))
            pygame.draw.rect(win,(0,167,0),(self.hitbox[0],self.hitbox[1]-10,50 - (5 *(10 - self.health)),7))
        
    def move(self):
        if self.walkCount + 1 >= 33:
            self.walkCount = 0
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
                self.walkCount += 1
            else:
                self.vel *= -1
                self.walkCount = 0
        else:
            if self.x + self.vel > self.path[0]:
                self.x += self.vel
                self.walkCount += 1
            else:
                self.vel *= -1
                self.walkCount = 0

def window_updater():
    win.blit(backGround,(0,10))
    man.updater(win)
    goblin.draw(win)
    text = font.render("Score: " + str(score),1,(0,0,0))
    win.blit(text,(325,10))
    text2 = font.render("Lives Left: " + str(hitTimes),1,(255,0,0))
    win.blit(text2,(10,10))
    for bullet in bullets:
        bullet.draw(win)
    pygame.display.update()

font = pygame.font.SysFont("Calibre",50,True)
man = Player(250,400,64,64)
goblin = Enemy(0,405,64,64,450)
run = True
score = 0
hitTimes = 3
spaceLoop = 0
bullets = []
while run:
    if goblin.visible:
        if man.hitbox[1] > goblin.hitbox[1] and man.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3]:
            if man.hitbox[0] > goblin.x + goblin.hitbox[2]//2 and man.hitbox[0] < goblin.x + goblin.hitbox[2]:
                man.hit()
                goblin.x = 400
                score -= 5
                hitTimes -= 1
                if 0 < goblin.health <= 7:
                    goblin.health += 3
    if not(goblin.visible):
        #pygame.display.update()
        #pygame.time.delay(1000)
        goblin.visible = True
        goblin.health = 10
        if goblin.vel > 0:
            goblin.vel += 1
        else:
            goblin.vel -= 1
        goblin.x = 400
        man.x = 20
    if spaceLoop > 0:
        spaceLoop += 1
    if spaceLoop == 4:
        spaceLoop = 0
    clock.tick(27)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    keys = pygame.key.get_pressed()
    if goblin.health <= 0:
        goblin.visible = False
    
    for bullet in bullets:
        if goblin.visible:
            if bullet.y + bullet.radius > goblin.hitbox[1] and bullet.y + bullet.radius < goblin.hitbox[1] + goblin.hitbox[3]:
                if bullet.x + bullet.radius > goblin.x + goblin.hitbox[2]//2 and bullet.x + bullet.radius < goblin.x + goblin.hitbox[2]:
                    #bullet.hit()
                    hit.play()
                    score += random.randint(1,5)
                    goblin.health -= 1
                    bullets.pop(bullets.index(bullet))
        if bullet.x < win_width and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))
            
    if keys[pygame.K_RETURN] or score < -25:
        run = False
            
    if keys[pygame.K_SPACE] and spaceLoop == 0:
        if man.walkRight:
            facing = 1
        else:
            facing = -1
        if len(bullets) < 5:
            shoot.play()
            bullets.append(Projectile(round(man.x + man.width//2 ),round((man.y + man.height//2 )),5,(230,0,0),facing))
        spaceLoop = 1
    
    if keys[pygame.K_LEFT] and man.x > man.vel:
        man.x -= man.vel
        man.walkLeft = True
        man.walkRight = False
        man.standing = False
    elif keys[pygame.K_RIGHT] and man.x < win_width - man.width - man.vel:
        man.x += man.vel
        man.walkLeft = False
        man.walkRight = True
        man.standing = False
    else:
        man.standing = True
        man.walkCount = 0
    if not(man.isJump):
    
        """if keys[pygame.K_UP] and y > vel:
            y -= vel
        if keys[pygame.K_DOWN] and y < win_height - height - vel:
            y += vel"""
        if keys[pygame.K_UP]:
            man.isJump = True          
    else:
        if man.jumpCount >= -10:
            neg = 1
            if man.jumpCount < 0:
                neg = -1
            man.y -= (man.jumpCount ** 2) * 0.5 * neg
            man.jumpCount -= 1
            
        else:
            man.isJump = False
            man.jumpCount = 10
    if goblin.hitbox[0] == man.hitbox[0] or goblin.hitbox[1] == man.hitbox[1]:
        score -= 5
    window_updater()
    
    if hitTimes == 0:
        warningFont = pygame.font.SysFont("Calibre",50)
        warning = warningFont.render("Game Over, Your score is {}".format(score),1,(255,0,0))
        win.blit(warning,(250-(warning.get_width()/2),200))
        pygame.display.update()
        pygame.time.delay(3000)
        run = False
        


pygame.quit()
