import time
import random
class GamePlay :
    play_duration = 0
    no_of_sjumps = 0
    score = 0
    level = 1
    seconds_paused=0
    def Inplay(self) :
        pass
    def Paused(self,s) :
        self.seconds_paused+=s
        time.sleep(s)
    def change_stage(self) :
        pass
    def quitgam(self) :
        self.score=0
class users :
    def __init__(self,nam,ide,age):
        self.name = nam
        self.Id = ide
        self.age = age
    highscore=0
    n_played=0
    game=GamePlay()
    def resetscore(self):
        self.highscore=0
    def play() :
        pass
    def resume() :
        pass
    def quitgame() :
        pass
class admin(users) :
    users_list=[]
    no_users=len(users_list)
    users_in_gam=0
    def avAbo(self) :
        pass
    def remu(self) :
        pass
    def add(self,us) :
        self.users_list.append(us)

class obstrucle() :
    def __init__(self,hei,wid) :
        self.height=hei
        self.width=wid
    position=0
    def incvel(self) :
        pass
    def veldir(self) :
        pass
    def gethit(self) :
        return self.height
    def getwidth(self) :
        return self.width
class bird :
    def __init__(self, typ, area) :
        self.birdtyp = typ
        self.birdarea = area
    birdspeed = 0
    xcor=0
    ycor=0
    def incspeed(self,speed) :
        self.birdspeed+=speed
    def decspeed(self,speed):
        self.birdspeed-=speed
    def jump(self) :
        self.ycor+=self.birdspeed
    def fall(self) :
        self.ycor -= self.birdspeed
master = admin("mass",'ma12',22)
b=bird("kiwi",5)
#obst=obstrucle(25,6)
#list_gameplay        
pos=0
for r in range(4) :
    query=input("Are u regestering for the first time 'yes' or 'no':")
    if query=='yes':
        master.add(users(input("name :",),input("Id : "),int(input("age : "))))
        pos = len(master.users_list)-1
    else :
        old=input("enter your name")
        for k in range(len(master.users_list)) :
            if master.users_list[k].name == old :
                pos=k
    play=input("if u want to play enter y else n : ")
    if play=='y' :
        initime=time.time()
        print("Game starting at ",time.strftime("%H:%M:%S",time.localtime()))
        print("Your previous high score : ",admin.users_list[pos].highscore)
        print("Let's begin the game ;)")
        #time.sleep(1)
        i=0
        jorf=''
        
        while i>=0 :
            if i%2==0 :
                if jorf!='p' :
                    obst=obstrucle(random.randrange(0,95,1),random.randrange(5,10,1))
                    obst.position+=5
                print("bird speed is ",b.birdspeed,"kmph and position is (",b.xcor,",",b.ycor,")")
                print("obstrucle passage is from height",obst.gethit(),"to",obst.gethit()+obst.getwidth())
                iord=input("if u incre or decre speed typ i or d or nothing only if u paused game")
                if iord=='i' :
                    b.incspeed(int(input("enter the kmph to increase : ")))
                elif iord=='d' :
                    b.decspeed(int(input("enter the kmph to decrease : ")))
                else :
                    pass
                jorf=input("if u want to jump  or fall or pause or exit enter the first alphabet :")
                if jorf=='j' :
                    b.jump()
                elif jorf=='f' :
                    b.fall()
                elif jorf=='p' :
                    delay=int(input("how many seconds do u want to stop"))
                    master.users_list[pos].game.Paused(delay)
                    continue
                else :
                    print("Game ended at ",time.strftime("%H:%M:%S",time.localtime()))
                    master.users_list[pos].game.play_duration+=int(time.time()-initime)-int(master.users_list[pos].game.seconds_paused)
                    print("score : ",master.users_list[pos].game.score,"level :",master.users_list[pos].game.level,"Game play duration",master.users_list[pos].game.play_duration)
                    break
                b.xcor+=5
            else :
                if b.ycor>=obst.height and b.ycor+b.birdarea<=obst.height+obst.width :
                    master.users_list[pos].game.score+=1
                    if master.users_list[pos].game.score>500 :
                        master.users_list[pos].game.level=1+int(master.users_list[0].game.score/500)
                    #print(master.users_list[0].game.no_of_sjumps)
                else :
                    if master.users_list[pos].highscore<master.users_list[pos].game.score :
                        master.users_list[pos].highscore=master.users_list[pos].game.score
                    print("Your highest score is ",master.users_list[pos].highscore)
                    print("Your score is",master.users_list[pos].game.score)
                    print("Game over at",time.strftime("%H:%M:%S",time.localtime()))
                    master.users_list[pos].game.score=0
                    master.users_list[pos].game.level=1
                    break
            i+=1
            master.users_list[pos].game.no_of_sjumps+=1