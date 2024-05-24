import pygame
import random
import sys

fps = 30
score = 0
pygame.font.init()
font = pygame.font.Font('./assets/monogram.ttf', 72)
font_two = pygame.font.Font('./assets/monogram.ttf', 64)

prompts = ['Musician/Band','Fruit', 'TV Show', 'Movie', 'Celebrity', 'TV Show Host', 'Country', 
           'Sea Creature', 'Animal', 'Flower', 'Holiday', 'Song', 'Occupation', 'Hobby', 'Snack',
           'City', 'State', 'Body Part', 'Video Game', 'Artist\'s Name', 'Sport', 'Name',
           'Month', 'Baked Goods', 'Historical Figure', 'Color', 'Gemstone', 'Dog Breed', 'Fictional Character',
           'Book Title', 'Board Game', 'Insect', 'Clothing', 'Accessories', 'Villain', 'Type of Shoe', 'Onomatopoeia',
           'Restaurant', 'Household Item', 'Kitchen Appliance', 'Condiment',
           'Instrument']

letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
           'N', 'O', 'P', 'R', 'S', 'T', 'U', 'V', 'W', 'Y',]

# Bird class code inspired by https://stackoverflow.com/questions/73942168/pygame-mouse-hover 
class Bird(pygame.sprite.Sprite):
    """A bird sprite"""
    def __init__(self, alt, pos=(0, 0)):
        pygame.sprite.Sprite.__init__(self)
        
        # if you're loading an image, make sure to use .convert()
        self.base = pygame.image.load('./assets/icon.png')
        self.base.convert()
        
        self.alt_image = pygame.image.load(alt)
        self.alt_image.convert()
        
        self.image = self.base
        self.rect = self.image.get_rect(center=pos)

    def update(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.image = self.alt_image
        else:
            self.image = self.base

class RandomChoice():
    def __init__(self, text_list, x, y, prompt_text):
        self.rect = pygame.Rect(x, y, 0, 0)
        self.text_list = text_list
        self.backup_list = text_list
        self.prompt_text = prompt_text
        self.updateText()
        self.clicked = False
        

    def updateText(self):
        if len(self.text_list) == 0:
            self.text_list = self.backup_list # refresh the list
            self.text = random.choice(self.text_list)
            self.render = font.render(f'{self.prompt_text}{self.text}', True, 'black')
            self.text_list.remove(str(self.text)) # make sure the prompt doesn't pop up again this round
            self.text_width = self.render.get_width()
            self.text_height = self.render.get_height()
            self.box = pygame.Surface((150, 45))
            self.rect = self.render.get_rect()
            
        else:
            self.text = random.choice(self.text_list)
            self.render = font.render(f'{self.prompt_text}{self.text}', True, 'black')
            self.text_list.remove(str(self.text)) # make sure the prompt doesn't pop up again this round
            self.text_width = self.render.get_width()
            self.text_height = self.render.get_height()
            self.box = pygame.Surface((150, 45))
            self.rect = self.render.get_rect()

    def draw(self):       
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            self.box.set_alpha(100) 
            self.box.fill((255, 255, 255))
            
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
        
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
        else:
            self.box.set_alpha(0) 

        rect = self.render.get_rect()
        box_width, box_height = font.size(self.text)
        #screen.blit(self.box, (self.rect.x, self.rect.y))
        if self.prompt_text == 'Starts With: ':
            screen.blit(self.render, (((850 + 36)/2), 225) )  
        else:
            screen.blit(self.render, (((850 + 36)/2), ((360 - box_height)/2)) )  
            
        return self.clicked



        

pygame.init()
print('Now Playing: Starts with J!')

screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption('Starts with J!')
icon = pygame.image.load('./assets/icon.png')
pygame.display.set_icon(icon)
clock = pygame.time.Clock()

skip = Bird(alt='./assets/skip.png', pos=(250, 350))
point = Bird(alt='./assets/point.png', pos=(1025, 350))

birds = pygame.sprite.Group()
birds.add(skip)
birds.add(point)

prompt_button = RandomChoice(prompts, 640, 175, 'Prompt: ') # position
letter_prompt = RandomChoice(letters, 640, 250, 'Starts With: ')






running = True

while running:
    # poll for events

    #TODO: add in letter generator, add in reset button (resets letter, promptlist, score), fix positioning, add in scoreboard
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONUP and point.rect.collidepoint(pygame.mouse.get_pos()):
            score += 1
            score_text = font_two.render(f'Score: {score}', True, 'black')
            screen.blit(score_text, (1000,20))
            prompt_button.updateText()
        elif event.type == pygame.MOUSEBUTTONUP and skip.rect.collidepoint(pygame.mouse.get_pos()):
            prompt_button.updateText()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                prompt_button.text_list = []
                prompt_button.updateText()
                letter_prompt.updateText()
                score = 0
                score_text = font_two.render(f'Score: {score}', True, 'black')
                screen.blit(score_text, (1000,20))
    
    birds.update()
    screen.fill("pink")
    score_text = font_two.render(f'Score: {score}', True, 'black')
    reset_text = font_two.render('Reset!', True, "black")

    
    screen.blit(score_text, (1000,20))
    screen.blit(reset_text, (((1090 + 36)/2), 625))
    birds.draw(screen)
    prompt_button.draw()
    letter_prompt.draw()
    pygame.display.update()
    clock.tick(fps)

pygame.quit()
sys.exit()