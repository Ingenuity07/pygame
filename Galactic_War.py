import pygame
import os
pygame.font.init()
pygame.mixer.init()

pygame.init()

HI,WI= 605,1080


WIN=pygame.display.set_mode((WI,HI))
pygame.display.set_caption("FIRST GAME")

BORDER =pygame.Rect(WI//2 - 5,0,10,HI)
  
BUL_H_S=pygame.mixer.Sound(os.path.join('ASSETS','Assets_Grenade+1.mp3'))
BUL_F_S=pygame.mixer.Sound(os.path.join('ASSETS','Assets_Gun+Silencer.mp3'))

FPS=60
WHITE=(255,255,255)
BLACK=(0,0,0)
RED=(255,0,0)
YELLOW=(0,255,0)
VEL=5
BULV=10
MAXB=3

HEALTH_FONT =pygame.font.SysFont('comicsans',40)
WINNER_FONT =pygame.font.SysFont('comicsans',100)

YEL_H= pygame.USEREVENT+1
RED_H= pygame.USEREVENT+2

YEL_SS = pygame.image.load(os.path.join('ASSETS','spaceship_yellow.png'))
YEL_SSD =pygame.transform.rotate( pygame.transform.scale(YEL_SS,(50,50)),(90))

RED_SS =pygame.image.load(os.path.join('ASSETS','spaceship_red.png'))
RED_SSD =pygame.transform.rotate(pygame.transform.scale(RED_SS,(50,50)),(270))

SPACE = pygame.image.load(os.path.join('ASSETS','space.png'))

def draw_win(red,yel,red_b,yel_b,RED_HE,YEL_HE):
    WIN.blit(SPACE,(0,0))
    pygame.draw.rect(WIN,BLACK,BORDER )

    RED_HE_T=HEALTH_FONT.render("Health: "+str(RED_HE),1,WHITE)
    YEL_HE_T=HEALTH_FONT.render("Health: "+str(YEL_HE),1,WHITE)

    WIN.blit(RED_HE_T,(WI-RED_HE_T.get_width()-10,10))
    WIN.blit(YEL_HE_T,(10,10))

    WIN.blit(YEL_SSD,(yel.x,yel.y))
    WIN.blit(RED_SSD,(red.x,red.y))



    for bul in red_b:
        pygame.draw.rect(WIN,RED,bul) 
    pygame.display.update()

    for bul in yel_b:
        pygame.draw.rect(WIN,YELLOW,bul) 
    pygame.display.update()

def yel_mov(key_presd,yel):

    if key_presd[pygame.K_a] and yel.x-VEL>0:#left
        yel.x-=VEL
    if key_presd[pygame.K_d] and yel.x+50+VEL< BORDER.x:#right
        yel.x+=VEL
    if key_presd[pygame.K_w] and yel.y-VEL>0:#up
        yel.y-=VEL
    if key_presd[pygame.K_s] and yel.y+VEL+50<HI:#down
        yel.y+=VEL 

def red_mov(key_presd,red):

    if key_presd[pygame.K_LEFT] and red.x-VEL>BORDER.x:#left
        red.x-=VEL
    if key_presd[pygame.K_RIGHT] and red.x+VEL+50< WI:#right
        red.x+=VEL
    if key_presd[pygame.K_UP] and red.y-VEL>0:#up
        red.y-=VEL
    if key_presd[pygame.K_DOWN] and red.y+VEL+50<HI:#down
        red.y+=VEL 

def bul_handle(yel_b,red_b,yell,redd):
    for bullet in yel_b:
        bullet.x+=BULV
        if(redd.colliderect(bullet)):
            pygame.event.post(pygame.event.Event(RED_H))
            yel_b.remove(bullet)
    
    for bullet in red_b:
        bullet.x-=BULV
        if(yell.colliderect(bullet)):
            pygame.event.post(pygame.event.Event(YEL_H))
            red_b.remove(bullet)

def draw_winn(text):
    draw_text=WINNER_FONT.render(text,1,WHITE)
    WIN.blit(draw_text,(WI/2 -draw_text.get_width()/2,HI/2-draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)



def main():
    YEL_HE=10
    RED_HE=10

    red =pygame.Rect(780,250,50,50)
    yel =pygame.Rect(200,250,50,50)

    yel_b =[]
    red_b =[]

    clock=pygame.time.Clock()
    run=True
    
    while(run):
        
        clock.tick(FPS)
       
               
        for event in pygame.event.get():
            if(event.type==pygame.QUIT):
                run = False
                pygame.quit()

            if(event.type==pygame.KEYDOWN):
                if event.key == pygame.K_LCTRL and len(yel_b)< MAXB:
                    bul=pygame.Rect(yel.x+yel.width,yel.y+yel.height//2-2,10,5)
                    yel_b.append(bul)
                    BUL_F_S.play()
                    
                if event.key == pygame.K_RCTRL and len(red_b)< MAXB:
                    bul=pygame.Rect(red.x,red.y+red.height//2-2,10,5)
                    red_b.append(bul)
                    BUL_F_S.play()
                
                

            if event.type==YEL_H:
                YEL_HE -=1
                BUL_H_S.play()
            if event.type==RED_H:
                RED_HE -=1
                BUL_H_S.play()
                
        wint=""
        if RED_HE<=0:
            wint="YELLOW WINS!"

        if YEL_HE<=0:
            wint="RED WINS!"

        if wint != "":
            draw_winn(wint)
            break


        print(yel_b,red_b)
        key_presd = pygame.key.get_pressed()
        yel_mov(key_presd,yel)
        red_mov(key_presd,red)

        bul_handle(yel_b,red_b,yel,red)
        draw_win(red,yel,red_b,yel_b,RED_HE,YEL_HE)
   
    
    main()

if __name__ == "__main__":
    main()
