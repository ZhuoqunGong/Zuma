import eventBasedAnimation
import random
from math import *
import copy

#####################  basic settings  ####################################
menu=True
gameOver=False
screenWidth=1000
screenHeight=650
colorPool=["red","yellow","blue","green","black","grey","purple","cyan"]

ballRadius=20
enemyAmount=40
ballColor=colorPool[random.randint(0,len(colorPool)-1)]
frogBallColor=ballColor
frogLocation=(500,300)
frogX,frogY=frogLocation
bulletGroup=[]

enemyGate=[0,30]
enemyGroup=[]
enemySpeed=2.0
bulletSpeed=25.0
turnSpeed=pi/10


####################  classes  ###################################
class Frog(object):
    def __init__(self,frogBallColor,frogLocation,radian):
        self.x,self.y=frogLocation
        self.color=ballColor

class Enemy(object):
    def __init__(self,color,location):
        self.location=location
        self.x,self.y=self.location
        self.color=color

    def move(self):
        if self.y==enemyGate[1] and self.x<screenWidth-30:
            self.x+=enemySpeed
        elif enemyGate[1] <= self.y<=screenHeight-60 and self.x>=screenWidth-30:
            self.y+=enemySpeed
        elif 30<=self.x<=screenWidth-30 and self.y>=screenHeight-60 :
            self.x-=enemySpeed
        elif self.x<=30 and self.y>=100:
            self.y-=enemySpeed
        
class Bullet(object):
    def __init__(self,color,location,radian):
        self.color=color
        self.x,self.y=frogLocation
        self.radian=radian
    def move(self):
        self.x+=bulletSpeed*cos(self.radian)
        self.y-=bulletSpeed*sin(self.radian)


###################  helper functions #############################

def distance(x1,y1,x2,y2):
    return sqrt((x1-x2)**2+(y1-y2)**2)
def collide(x1,y1,x2,y2,distance):
    if( x1-x2)**2+(y1-y2)**2<distance**2:

        return True
    else:
        return False

  ###########   animation functions  ##############################  



def zumaInitFn(data):
    data.menu=True
    data.bulletSpeed=bulletSpeed
    data.bulletGroup=bulletGroup
    data.enemyGroup=enemyGroup
    data.frogLocation=frogLocation
    data.frogX,data.frogY=data.frogLocation
    data.currentColor=ballColor
    data.radian=0
    data.score=0
    data.goal=1000000
    data.endGate=(28.0,98.0)
    data.gameOver=False
def zumaKeyFn(event, data):
    pass


def zumaMouseFn(event, data):
    (data.x, data.y) = (event.x, event.y)
    data.radian=asin((data.x-frogX)/(sqrt((data.x-frogX)**2+(data.y-frogY)**2)))
    if data.y<frogY:
        data.radian=pi-data.radian
    data.radian-=pi/2.0
def zumaMouseReleaseFn(event,data):
    (data.x, data.y) = (event.x, event.y)
    if not data.menu and not data.gameOver:
        data.bulletGroup.append(Bullet(data.currentColor,frogLocation,data.radian))
        data.currentColor=colorPool[random.randint(0,len(colorPool)-1)]
    elif data.gameOver:
        data.enemyGroup=[]
        data.bulletGroup=[]
        data.gameOver=False
    else:    
        if screenWidth/2.0-50<data.x<screenWidth/2.0+50 and  screenHeight*2.0/3<data.y<screenHeight*2.0/3+50:
            data.menu=False

def zumaDrawFn(canvas,data):
    # draw the game over version
    if data.gameOver==True:
        canvas.create_rectangle(0,0,screenWidth,screenHeight, fill="blue")
        canvas.create_text(screenWidth/2.0,screenHeight/2.0,text="GAME OVER", font="bold 100",fill="brown")
        canvas.create_text(screenWidth*2/3.0,screenHeight*2/3.0,text="Click anywhere to restart",fill="black",font="bold 20")
        # draw the main menu
    elif data.menu:
        canvas.create_rectangle(0,0,screenWidth,screenHeight,fill="cyan")
        canvas.create_text(screenWidth/2.0,screenHeight/2.0,text="ZUMA" ,font=" bold 100 " ,fill="blue"  ) 
        canvas.create_rectangle(screenWidth/2.0-50,screenHeight*2.0/3,screenWidth/2.0+50,screenHeight*2.0/3+50, fill="blue")
        canvas.create_text(screenWidth/2.0,screenHeight*2.0/3+25,text="start",font="bold 20", fill="cyan")
         # draw the game   
    else:
        (w,z)=data.endGate
        canvas.create_oval(w-25,z-25,w+25,z+25,fill="brown")
        canvas.create_oval(data.frogX-ballRadius,data.frogY-ballRadius,
            data.frogX+ballRadius,data.frogY+ballRadius,fill=data.currentColor)
        for bullet in data.bulletGroup:
            canvas.create_oval(bullet.x-ballRadius,bullet.y-ballRadius,
                bullet.x+ballRadius,bullet.y+ballRadius, fill=bullet.color)
        for enemy in data.enemyGroup:
            canvas.create_oval(enemy.x-ballRadius,enemy.y-ballRadius,
                enemy.x+ballRadius,enemy.y+ballRadius,fill=enemy.color)
        # draw the score board
        canvas.create_rectangle(0,screenHeight-30,200,screenHeight,fill= "cyan")
        canvas.create_text(100,screenHeight-15,text="SCORE:"+str(data.score)+"/"+str(data.goal),
         font= " bold  20 ", fill="red")
def zumaStepFn(data):
    if data.menu:
        pass
    elif data.gameOver:
        pass
    else:
    # random the color
        ballColor=colorPool[random.randint(0,len(colorPool)-1)]
        if data.enemyGroup==[]:
            data.enemyGroup.append(Enemy(ballColor,enemyGate))
        for bullet in data.bulletGroup:
            bullet.move()
        for n in xrange(len(data.enemyGroup)):
            
            data.enemyGroup[n].move()
        # add new enemy    
        lastEnemy=data.enemyGroup[len(data.enemyGroup)-1]
        if distance(lastEnemy.x,lastEnemy.y,enemyGate[0],enemyGate[1])>=ballRadius*2.0:
            data.enemyGroup.append(Enemy(ballColor,enemyGate))
            # if there is already a combo when new enemy is created
            # change the color to avoid it
            while data.enemyGroup[len(enemyGroup)-1].color==data.enemyGroup[len(enemyGroup)-2].color==data.enemyGroup[len(enemyGroup)-3].color:
                data.enemyGroup[len(enemyGroup)-1].color=colorPool[random.randint(0,len(colorPool)-1)]
        # when bullet move out of the screen
        # delete it
        for bullet in data.bulletGroup:
            if bullet.x-ballRadius> screenWidth:
                data.bulletGroup.remove(bullet)
            elif bullet.y-ballRadius> screenHeight:
                data.bulletGroup.remove(bullet)
            elif bullet.x+ballRadius<0:
                data.bulletGroup.remove(bullet)
            elif bullet.y+ballRadius<0:
                data.bulletGroup.remove(bullet)
        # make a collision
        coll=False
        for bullet in data.bulletGroup:
            for enemy in data.enemyGroup:
                if coll==False:
                    if collide(bullet.x,bullet.y,enemy.x,enemy.y,ballRadius*2):
                        coll=True
                        i = data.enemyGroup.index(enemy)
                        data.enemyGroup.insert(i,Enemy(bullet.color,(enemy.x,enemy.y)))
                        data.bulletGroup.remove(bullet)
                        for j in xrange(i+1,len(data.enemyGroup)-1):
                            data.enemyGroup[j].x=data.enemyGroup[j+1].x
                            
                            data.enemyGroup[j].y=data.enemyGroup[j+1].y
                            
                        data.enemyGroup.pop()

            # check combo
            comboList=[]
            for e in xrange(len(data.enemyGroup)):
                if e==0:
                    if data.enemyGroup[e].color==data.enemyGroup[e+1].color==data.enemyGroup[e+2].color:
                        comboList.append(e)
                elif e==len(data.enemyGroup)-1:
                    if data.enemyGroup[e].color==data.enemyGroup[e-1].color==data.enemyGroup[e-2].color:
                        comboList.append(e)
                elif e==1:
                    if data.enemyGroup[e].color==data.enemyGroup[e+1].color==data.enemyGroup[e+2].color:
                        comboList.append(e)
                    elif data.enemyGroup[e].color==data.enemyGroup[e+1].color==data.enemyGroup[e-1].color:
                        comboList.append(e)
                elif e==len(data.enemyGroup)-2:
                    if data.enemyGroup[e].color==data.enemyGroup[e-1].color==data.enemyGroup[e-2].color:
                        comboList.append(e)
                    elif data.enemyGroup[e].color==data.enemyGroup[e+1].color==data.enemyGroup[e-1].color:
                        comboList.append(e)
                else:
                    if data.enemyGroup[e].color==data.enemyGroup[e-1].color==data.enemyGroup[e-2].color:
                        comboList.append(e)
                    elif data.enemyGroup[e].color==data.enemyGroup[e+1].color==data.enemyGroup[e-1].color:
                        comboList.append(e)
                    elif data.enemyGroup[e].color==data.enemyGroup[e+1].color==data.enemyGroup[e+2].color:
                        comboList.append(e)
            
            if len(comboList)>=3:
                # add score
                data.score+=10**len(comboList)
                # pull back the balls
                mi=min(comboList)
                l=len(comboList)
                for ll in xrange(mi):
                    data.enemyGroup[ll].x=data.enemyGroup[ll+l].x
                    data.enemyGroup[ll].y=data.enemyGroup[ll+l].y
                # delete the combo balls    
                while len(comboList)>0:
                    m=max(comboList)
                    data.enemyGroup.remove(data.enemyGroup[m])
                    comboList.remove(m)
    if data.enemyGroup!=[] and (data.enemyGroup[0].x,data.enemyGroup[0].y)==data.endGate:
        data.gameOver=True




                   


    

    




##########################  run the whole game  ##################################


eventBasedAnimation.run(
    initFn=zumaInitFn ,
    stepFn=zumaStepFn ,
    mouseFn=zumaMouseFn ,
    mouseReleaseFn=zumaMouseReleaseFn ,
    keyFn=zumaKeyFn,
    drawFn=zumaDrawFn ,
    timerDelay=20,
    width=screenWidth,
    height=screenHeight
    )
