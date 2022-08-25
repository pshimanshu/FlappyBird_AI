import pygame
import random
import neat
import os
pygame.init()
pygame.font.init()
bg = pygame.image.load('bg.png')


width = bg.get_width()
height = bg.get_height()
s = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()
FONT = pygame.font.Font(pygame.font.get_default_font(),25)
gen=0
class Bird :
    image = pygame.image.load('bird1.png')
    velocity = 0
    distance = 0
    acceleration = 0.9
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.move_along_x = 0
        self.score = 0
        self.entered = False
    def jump(self):
        #self.move_along_x =0
        self.velocity=-10

    def move(self):
        #self.move_along_x+=0.5
        #self.distance = self.velocity*self.move_along_x*(0.5) + (1/8)*self.acceleration*self.move_along_x**2 
        #if self.distance>10 :
        #    self.distance=10
        self.velocity+=self.acceleration
        self.y+=self.velocity
    def display(self,screen):
        #self.text_surface = FONT.render("Score : "+str(self.score),1,(255,255,255))
        screen.blit(self.image,(self.x,self.y))
    def get_mask(self):
        return pygame.mask.from_surface(self.image)
    


class Pipe :
    pipe1 = pygame.image.load('pipe.png')
    pipe2 = pygame.transform.rotate(pipe1,180)
    gap = 90
    def __init__(self,x):
        self.x = x
        self.y = random.randrange(200,375)
        self.width = self.pipe1.get_width()
        self.height = self.pipe1.get_height()
        self.is_crossed=False

    def display(self,screen):
        screen.blit(self.pipe1,(self.x,self.y))
        screen.blit(self.pipe2,(self.x,self.y-self.gap-self.height))
    def passed(self,bird):
        if bird.x > self.x+self.width :
            bird.entered=False
            bird.score+=1
            return  True
        else :
            return False
    def colloid(self,bird) :
        bird_mask= bird.get_mask()
        top_mask = pygame.mask.from_surface(self.pipe2)
        bottom_mask = pygame.mask.from_surface(self.pipe1)
        off_set_top = (bird.x-self.x,round(bird.y)-self.y+self.gap+self.height)
        off_set_bottom = (bird.x-self.x,round(bird.y)-self.y)
        check_top = top_mask.overlap(bird_mask,off_set_top)
        check_bottom= bottom_mask.overlap(bird_mask,off_set_bottom)
        if check_bottom==None and check_top==None :
            return False
        return True

class Ground :
    ground = pygame.image.load('base.png')
    def __init__(self,x):
        self.x = x
        self.y=height-self.ground.get_height()
    def display(self,screen) :
        screen.blit(self.ground,(self.x,self.y))

def eval_genome(genomes,config) :
    global gen
    game = True
    #bird = Bird(42, 200)
    birds = []
    nets=[]
    ge =[]
    for _,genome in genomes :
        genome.fitness =0
        net = neat.nn.FeedForwardNetwork.create(genome,config)
        nets.append(net)
        birds.append(Bird(42,200))
        ge.append(genome)
    pipe_list = [Pipe(288),Pipe(490)]
    ground1 = Ground(0)
    ground2 = Ground(336)
    max_score=0

    while game  and len(birds)>0 and max_score<150:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            """if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_SPACE :
                    bird.jump()"""
        pip_index=0
        if len(birds) > 0 :
            if len(pipe_list)>1 and birds[0].x > pipe_list[0].x +pipe_list[0].width :
                pip_index=1
        for x ,bird in enumerate(birds):
            ge[x].fitness+=0.1
            bird.move()
            output = nets[birds.index(bird)].activate((bird.y,abs(bird.y-pipe_list[pip_index].y),abs(bird.y-pipe_list[pip_index].y+pipe_list[pip_index].gap)))
            if output[0] >0 :
                bird.jump()
        for bird in birds :
            #if bird.entered==False :
            if pipe_list[pip_index].colloid(bird) :
                ge[birds.index(bird)].fitness-=0.5
                nets.pop(birds.index(bird))
                ge.pop(birds.index(bird))
                birds.pop(birds.index(bird))
                continue
            #if bird.x +bird.image.get_width()/2 >pipe_list[pip_index].x :
            #    bird.entered=True
        s.blit(bg,(0,0))
        for i in range(2):
            pipe_list[i].display(s)
            pipe_list[i].x-=2
        ground1.display(s)
        ground2.display(s)
        ground1.x-=2
        ground2.x-=2
        if ground1.x<-336 :
            ground1.x = ground2.x + ground2.ground.get_width()
        if ground2.x<-336 :
            ground2.x = ground1.x + ground1.ground.get_width()
        if pipe_list[0].x<=-52 :
            pipe_list.pop(0)
            pipe_list.append(Pipe(352))
        for bird in birds :
            if bird.y+bird.image.get_height() > ground1.y :
                bird.y=ground1.y-bird.image.get_height()
            if bird.y<0 :
                bird.y=0
            #if bird.entered==True:
            #    if bird.y+bird.image.get_height() > pipe_list[0].y :
            #        bird.y = pipe_list[0].y-bird.image.get_height()
            #    elif bird.y < pipe_list[0].y-pipe_list[0].gap :
            #        bird.y += pipe_list[0].y-pipe_list[0].gap - bird.y
            if pipe_list[pip_index].passed(bird) :
                ge[birds.index(bird)].fitness+=0.5
                
        max_score =0
        for bird in birds :
            if bird.score>max_score :
                max_score=bird.score
            bird.display(s)
        s.blit(FONT.render(str(max_score),1,(255,255,255)),(230,0))
        s.blit(FONT.render("gen : "+str(gen),1,(255,255,255)),(0,0))
        s.blit(FONT.render("Alive : "+str(len(birds)),1,(255,255,255)),(0,30))
        pygame.display.update()
        clock.tick(60)
    gen+=1



def run(config_path) :
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,neat.DefaultSpeciesSet, neat.DefaultStagnation,config_path)
    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    #p.add_reporter(neat.Checkpointer(5))
    winner = p.run(eval_genome,50)

    print('\nBest genome:\n{!s}'.format(winner))


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir,"config-feedforward.txt")
    run(config_path)
