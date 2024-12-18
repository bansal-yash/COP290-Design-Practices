# The github link for the project is :-

#     https://github.com/bansal-yash/COP290_Assignment_2

# The one drive link for the assets is :-

#     https://csciitd-my.sharepoint.com/:f:/g/personal/cs5221133_iitd_ac_in/EigAA05xbVpHj_Uw9-eYgF4BlvJWggp2bBmnxjmVGug24Q?e=pUF1Z0

import pygame
import pytmx
import sys
import random
import time
import math

info = [
    "Creating wildlife corridors can help reduce animal-vehicle collisions and allow animals to safely migrate between different parts of their habitat.",
    "Removing invasive species from an ecosystem can help native plants and animals thrive by reducing competition for resources.",
    "Installing bird boxes and bat boxes can provide safe nesting sites and help boost local populations.",
    "Water conservation measures, such as rainwater harvesting, are vital for maintaining water bodies within reserves, supporting both aquatic life and terrestrial animals.",
    "Planting native vegetation enhances the natural habitat, supports local wildlife, and promotes biodiversity.",
    "Regular patrols and the use of motion-sensitive cameras can help monitor wildlife populations and deter poaching.",
    "Engaging local communities in reserve activities and benefits can promote conservation and reduce human-wildlife conflicts.",
    "Restoring wetlands is crucial for maintaining biodiversity, purifying water, and providing habitat for numerous species.",
    "Providing wildlife with supplementary feeding during extreme weather can help prevent starvation and reduce mortality rates.",
    "Conducting regular wildlife censuses helps track population trends and assess the effectiveness of conservation strategies.",
    "Using eco-friendly materials and renewable energy sources in the construction of reserve facilities can minimize environmental impact.",
    "Educating visitors about the importance of not feeding wild animals helps maintain natural behaviors and diet.",
    "Implementing fire management practices can help prevent catastrophic wildfires and maintain ecological balance.",
    "Recycling and proper waste management practices reduce pollution and its harmful impacts on wildlife.",
    "Promoting ecotourism and responsible wildlife viewing practices can generate income for conservation while minimizing disturbance to animals."
    "Fencing critical areas helps protect endangered species from poachers and prevent human-wildlife conflict, especially near village borders.",
    "Reforestation projects can restore degraded areas, improve climate resilience, and reconnect fragmented habitats, supporting larger, more viable wildlife populations.",
    "Anti-poaching technology, such as drones and AI-powered surveillance systems, can enhance the monitoring of vast and hard-to-reach areas within the reserve.",
    "Wildlife health monitoring programs ensure early detection of diseases that can affect animal populations, with veterinary units prepared to intervene when necessary.",
    "Educational outreach programs in schools and communities raise awareness about the importance of biodiversity and conservation practices.",
    "Artificial reefs can be created to enhance marine biodiversity, providing additional habitats and attracting a variety of marine life to degraded areas.",
    "Eco-sensitive waste management in and around the reserve includes composting organic waste and ensuring that all plastics and non-biodegradable materials are removed or recycled.",
    "Sustainable tourism guidelines ensure that the influx of visitors does not disrupt wildlife or degrade the natural environment, maintaining the reserve's integrity and appeal.",
]

pygame.init()
pygame.mixer.init()

pygame.mixer.music.load('background.mp3')
pygame.mixer.music.play(-1)

# Constants for the screen size
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 800
LION_SIZE = (100, 32)
GIRAFFE_SIZE = (100, 100)
POACHER_SIZE = (100,32)
RANGER_SIZE = (150,32)
VEHICLE_SIZE = (300,150)
MAP_WIDTH = 4800
MAP_HEIGHT = 4800

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

Game_over = [False]
spacebar = [False]
playscreen = [True]
Play_mode = [False]
selected_character = None
play_char = [False]
Player_dead = [False]

button_width = 200
button_height = 50
button_spacing = 20
button_x = (SCREEN_WIDTH - button_width) // 2
button_y = SCREEN_HEIGHT - 100  # Placing the button 100 pixels from the bottom of the screen
total_button_width = button_width * 5 + button_spacing * 4
button_start_x = (SCREEN_WIDTH - total_button_width) // 2  # Center buttons horizontally
button_start_y = SCREEN_HEIGHT - 200
# pygame.display.set_caption("Flashing Game Over")



# Font settings
font = pygame.font.Font(None, 48)
game_over_text = font.render("Game Over", True, GRAY)



# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Load the game map using pytmx
tmx_data = pytmx.load_pygame("game/tmx/game_mao.tmx", pixelalpha=True)

def render_map(surface, tmx_data, camera):
    """Render the map with the camera offset."""
    tw = tmx_data.tilewidth
    th = tmx_data.tileheight

    for layer in tmx_data.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, gid in layer:
                tile = tmx_data.get_tile_image_by_gid(gid)
                if tile:
                    surface.blit(tile, camera.apply(pygame.Rect(x * tw, y * th, tw, th)))

def process_object_layer(game_over,surface, tmx_data, camera):
    """Process and render objects from the object layer for visualization, including image objects."""
    if(not(game_over)):
        for obj in tmx_data.objects:
            if hasattr(obj, 'image') and obj.image:
                image = pygame.transform.scale(obj.image, (int(obj.width) * camera.zoom_level , int(obj.height) * camera.zoom_level ))
                rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                surface.blit(image, camera.apply(rect))

            elif hasattr(obj, 'points'):
                pygame.draw.polygon(surface, (255, 0, 0), [(camera.apply_point((p[0], p[1]))) for p in obj.points], 3)
            elif hasattr(obj, 'ellipse') and obj.ellipse:
                ellipse_rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                pygame.draw.ellipse(surface, (255, 0, 0), camera.apply(ellipse_rect), 3)
            else:
                rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                pygame.draw.rect(surface, (0, 255, 0), camera.apply(rect), 3)
    else:
        screen.fill(BLACK)
        screen.blit(game_over_text, (MAP_WIDTH // 2 - game_over_text.get_width() // 2, MAP_HEIGHT // 2 - game_over_text.get_height() // 2))
        
def game_over():
    pygame.draw.rect(screen, GRAY, (button_x, button_y, button_width, button_height))
    text = font.render("Game Over", True, BLACK)
    text_rect = text.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
    screen.blit(text, text_rect)

def choose_character_screen():
    text = font.render("Choose Your Character", True, BLACK)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text, text_rect)

def draw_character_buttons():
    characters = ["lion", "giraffe", "poacher", "ranger","game-ai"]
    for idx, character in enumerate(characters):
        button_rect = pygame.Rect(button_start_x + idx * (button_width + button_spacing), button_start_y, button_width, button_height)
        if selected_character == character:
            pygame.draw.rect(screen, BLACK, button_rect)
        else:
            pygame.draw.rect(screen, GRAY, button_rect)
        text = font.render(character.capitalize(), True, WHITE)
        text_rect = text.get_rect(center=button_rect.center)
        screen.blit(text, text_rect)

def play_screen():
    pygame.draw.rect(screen, GRAY, (button_x, button_y, button_width, button_height))
    text = font.render("Play", True, BLACK)
    text_rect = text.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
    screen.blit(text, text_rect)



def custom_message(message, y_block = button_y + button_height // 2 ):
    # pygame.draw.rect(screen, GRAY, (button_x, button_y, button_width, button_height))
    text = font.render(message, True, BLACK)
    text_rect = text.get_rect(center=(button_x + button_width // 2, y_block))
    screen.blit(text, text_rect)
    
def info_message(message, y_block=button_y + button_height // 2):
    max_font_size = 48  # Maximum font size to start with
    max_width = SCREEN_WIDTH - button_width  # Maximum width for the message

    font_size = max_font_size
    font = pygame.font.Font(None, font_size)
    text_width, text_height = font.size(message)
    while text_width > max_width and font_size > 0:
        font_size -= 1
        font = pygame.font.Font(None, font_size)
        text_width, text_height = font.size(message)
    text = font.render(message, True, BLACK)
    text_rect = text.get_rect(center=(button_x + button_width // 2, y_block))
    screen.blit(text, text_rect)

class Camera:
    def __init__(self, width, height):
        self.camera_rect = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.width = width
        self.height = height
        self.zoom_level = 1.0

    def apply(self, rect):
        rect = rect.copy()
        rect.x -= self.camera_rect.x
        rect.y -= self.camera_rect.y
        rect.x = int(rect.x * self.zoom_level)
        rect.y = int(rect.y * self.zoom_level)
        rect.width = int(rect.width * self.zoom_level)
        rect.height = int(rect.height * self.zoom_level)
        return rect

    def update(self, target):
        # Center the camera on the target
        x = -target.rect.centerx + SCREEN_WIDTH // 2
        y = -target.rect.centery + SCREEN_HEIGHT // 2
        # Adjust the camera rectangle
        self.camera_rect = pygame.Rect(x, y, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.camera_rect.clamp_ip(pygame.Rect(0, 0, self.width, self.height))
        
    def zoom(self, increment):
        self.zoom_level = max(self.zoom_level + increment,1/3)
        
        center_x = self.camera_rect.x + (SCREEN_WIDTH / 2 / self.zoom_level)
        center_y = self.camera_rect.y + (SCREEN_HEIGHT / 2 / self.zoom_level)
        self.camera_rect.x = int(center_x - (SCREEN_WIDTH / 2 / self.zoom_level))
        self.camera_rect.y = int(center_y - (SCREEN_HEIGHT / 2 / self.zoom_level))
        self.camera_rect.clamp_ip(pygame.Rect(0, 0, self.width, self.height))
        
    def scroll(self, x, y):
        self.camera_rect.x = min(
            max(0, self.camera_rect.x + x),
            self.width - int(SCREEN_WIDTH / self.zoom_level),
        )
        self.camera_rect.y = min(
            max(0, self.camera_rect.y + y),
            self.height - int(SCREEN_HEIGHT / self.zoom_level),
        )
        
    def apply_point(self, point):
        """Adjust a point based on camera settings."""
        x, y = point
        x -= self.camera_rect.x
        y -= self.camera_rect.y
        return int(x * self.zoom_level), int(y * self.zoom_level)

def load_image(filename, size):
    image = pygame.image.load(filename).convert_alpha()
    return pygame.transform.scale(image, size)

lion_images = {
    "sitting": load_image("animal_images/lion/sitting.png", LION_SIZE),
    "moving": [
        load_image("animal_images/lion/moving_1.png", LION_SIZE),
        load_image("animal_images/lion/moving_2.png", LION_SIZE),
        load_image("animal_images/lion/moving_3.png", LION_SIZE)
        # load_image("animal_images/lion/lion_moving4.png", LION_SIZE),
        # load_image("animal_images/lion/lion_moving5.png", LION_SIZE),
        # load_image("animal_images/lion/lion_moving6.png", LION_SIZE),
        
    ],
    "standing": load_image("animal_images/lion/standing.png", LION_SIZE),
    "sleeping": load_image("animal_images/lion/sleeping.png", LION_SIZE),
    "dead": load_image("animal_images/lion/dead.png", LION_SIZE),
    "croco": load_image("animal_images/crocodile/croco_1.png",LION_SIZE)
}

giraffe_images = {
    "moving": [
        load_image("animal_images/giraffe/moving_1.png", GIRAFFE_SIZE),
        load_image("animal_images/giraffe/moving_2.png", GIRAFFE_SIZE),
        load_image("animal_images/giraffe/moving_3.png", GIRAFFE_SIZE),
    ],
    "standing": load_image("animal_images/giraffe/standing.png", GIRAFFE_SIZE),
    "sitting": load_image("animal_images/giraffe/standing.png", GIRAFFE_SIZE),
    "dead": load_image("animal_images/giraffe/dead.png", GIRAFFE_SIZE),
    "croco": load_image("animal_images/crocodile/croco_1.png",LION_SIZE)
    
}

poacher_images = {
    "moving": [
        load_image("animal_images/poacher/moving_1.png", POACHER_SIZE),
        load_image("animal_images/poacher/moving_2.png", POACHER_SIZE),
        load_image("animal_images/poacher/moving_3.png", POACHER_SIZE),
    ],
    "standing": load_image("animal_images/poacher/standing.png", POACHER_SIZE),
    "sitting": load_image("animal_images/poacher/standing.png", POACHER_SIZE),
    "dead": load_image("animal_images/poacher/dead.png", POACHER_SIZE),
    "shoot": load_image("animal_images/poacher/shoot.png", POACHER_SIZE),
    "croco": load_image("animal_images/crocodile/croco_1.png",LION_SIZE)
}

ranger_images = {
    "moving": [
        load_image("animal_images/ranger/moving_1.png", RANGER_SIZE),
        load_image("animal_images/ranger/moving_2.png", RANGER_SIZE),
        load_image("animal_images/ranger/moving_3.png", RANGER_SIZE),
        load_image("animal_images/ranger/moving_4.png", RANGER_SIZE),
    ],
    "standing": load_image("animal_images/ranger/standing.png", RANGER_SIZE),
    "sitting": load_image("animal_images/ranger/standing.png", RANGER_SIZE),
    "searching": load_image("animal_images/ranger/searching_moving.png", RANGER_SIZE),
    "dead": load_image("animal_images/ranger/dead.png", RANGER_SIZE),
    "shoot": load_image("animal_images/ranger/shoot.png", RANGER_SIZE),
    "croco": load_image("animal_images/crocodile/croco_1.png",LION_SIZE)
}

vehicle_images = {
    "standing": load_image("animal_images/vehicle/car_side.png", VEHICLE_SIZE),
    "sitting": load_image("animal_images/vehicle/car_side.png", VEHICLE_SIZE),
    "horizontal" :load_image("animal_images/vehicle/car_side.png", VEHICLE_SIZE),
    "vertical" :load_image("animal_images/vehicle/car_top.png", VEHICLE_SIZE)
}

Poacher_action = ["to_kill"]
Giraffe_action = ["to_drink","to_rest"]
Giraffe_location_map = {
    "to_drink": (340,950),
    "to_rest" : (1500,900)
    # "to_rest" : (2000,2500)
    
}
# Lion_action = ["to_drink","to_kill","to_rest"]
Lion_action = ["to_kill"]


Lion_location_map = {
    "to_drink": (360,2752),
    "to_rest": (2200,2752)
}

Poacher_action = ["to_kill"]
Poacher_location_map = {
    "to_rest" : (1500,50)
}

Vehicle_action = ["to_stand"]
Vehicle_location_map = {
    "to_rest" : (4500,1900)
}

Ranger_action = []
Ranger_location_map = {
    "to_rest" : (4500,1600),
    "to_inspect_jungle" : (4000,3400)
}


Animal_action = {
    "lion": Lion_action,
    "giraffe" : Giraffe_action,
    "poacher": Poacher_action
}


Animal_location_map = {
    "lion": Lion_location_map,
    "giraffe" : Giraffe_location_map,
    "poacher": Poacher_location_map,
    "vehicle": Vehicle_location_map,
    "ranger" : Ranger_location_map
}

def Animal_start(animal_type):
    x,y = Animal_location_map[animal_type]["to_rest"]
    if(animal_type == "lion"):
        return (random.randint(x-50,x+50),random.randint(y-20,y+20))
    elif(animal_type == "giraffe"):
        x,y = random.randint(x-200,x+200),random.randint(y-100,y+100)
        a,b = x,4800-y
        return random.choice([(a,b),(x,y)])
    elif (animal_type == "poacher"):
        return (random.randint(x-50,x+50),random.randint(y-20,y+20))
    elif (animal_type == "vehicle"):
        return (4500,1900)
    elif (animal_type == "ranger"):
        return (4500,1600)

def Animal_drink(animal_type):
    x,y = Animal_location_map[animal_type]["to_drink"]
    if(animal_type == "lion"):
        return (random.randint(x-40,x+40),random.randint(y-20,y+20))
    elif(animal_type == "giraffe"):
        return (random.randint(x-20,x+20),random.randint(y-200,y+200))


Animals = []
Preys = []
Predators = []
Poacher = []
Ranger = []
Vehicle = []
Player = []
Mark = []
    

class Animal:
    
    def __init__(self, images, start_x, start_y,speed,animal_type,time,play_char):
        self.animal = animal_type
        self.images = images
        self.image = images["sitting"]
        self.rect = self.image.get_rect()
        self.rect.x,self.rect.y = start_x,start_y
        self.frame_counter = 0
        self.frame_delay = 5
        self.moving_index = 0
        self.speed = speed
        self.map_width = MAP_WIDTH
        self.map_height = MAP_HEIGHT
        self.dir = "stop"
        self.current_action = "none"
        self.loc_x = 0 #self.loc_x and self.loc_y are the target location
        self.loc_y = 0
        self.alive = True
        self.predator = None
        self.prey = None
        self.poach_targ = None
        self.pred_near = True
        self.wait = time
        self.kill = 0
        self.alert = False
        self.player = play_char
        
        self.chase = False
        self.allow_chase = False
        self.allow_kill = False
        self.kill_prey_player = False
        self.shot = 0
        
    def near_prey(self):
        for prey in Preys:
            x,y = prey.get_location()
            if(abs(self.rect.x - x) < 200 and abs(self.rect.y - y) < 200):
                self.allow_chase = True
                Mark.append(prey)
                custom_message("Press C to start the chase")
                # print(prey.get_location())
                return prey
            
    def near_animal_poach(self):
        for animal in Animals:
            x,y = animal.get_location()
            if(abs(self.rect.x - x) < 150 and abs(self.rect.y - y) < 150):
                Mark.append(animal)
                custom_message("Press T to shoot")
                
    def kill_prey(self):
        prey = self.prey
        x,y = prey.get_location()
        if(abs(self.rect.x - x) < 60 and abs(self.rect.y - y) < 60):
            self.allow_kill = True
            custom_message("Press K to kill the prey")
            return
        
    def move_to_this_tile(self,x,y):
        if self.rect.x < x:
            return "right"
        elif self.rect.x > x:
            return "left"
        
        if self.rect.y < y:
            return "up"
        elif self.rect.y > y:
            return "down"
        return "stop"

    def update(self,direction):
        if (self.alive):
            zoom_adjusted_speed = self.speed * camera.zoom_level
            zoom_adjusted_delay = self.frame_delay / camera.zoom_level
            
            # There can be two cases either the player is playing or the game ai is playing
            if(self.player):
                self.dir = direction
                move_dir = direction
                if(self.animal == "lion"):
                    if (self.alive):
                        if(not self.chase):
                            self.near_prey()
                        else:
                            global Mark
                            self.prey = Mark[-1]
                            self.prey.predator = self
                            self.kill_prey()
                            if(self.kill_prey_player):
                                self.prey.killed()
                                if(self.prey.alive == False):
                                    self.prey.wait = 0
                                    self.prey = None
                                    Mark = []
                                    self.chase = False
                elif(self.animal == "giraffe"):
                    if(self.predator != None):
                        if(abs(self.predator.rect.x - self.rect.x) < 200 and abs(self.predator.rect.y - self.rect.y) < 200):
                            custom_message("predator_set")
                        
                elif(self.animal == "poacher"):
                    
                    self.near_animal_poach()
                    if(len(Mark) != 0):
                        self.poach_targ = Mark[-1] 
                        if(self.poach_targ.shot == 3):
                            self.poach_targ.killed()
                            self.poach_targ.wait = 100   
                            self.poach_targ = None
                            Vehicle[0].alert = True   
                        
            else:
                
                if(self.animal == "poacher"):
                    if(not self.alert):
                        if self.kill < 2:
                            self.nearest_animal()
                            self.loc_x,self.loc_y = self.poach_targ.get_location()
                            self.dir = self.move_to_this_tile(self.loc_x,self.loc_y)
                            if(abs(self.loc_x-self.rect.x) < 80 and abs(self.loc_y-self.rect.y) < 80):
                                if(self.wait >= 0):
                                    self.wait -= 1
                                    if(self.wait > 200):
                                        move_dir = "shot"
                                    elif(self.wait == 200 ):
                                        self.poach_targ.killed()
                                        move_dir = "stop"
                                        Vehicle[0].alert = True                                 
                                    elif(self.wait < 200 and self.wait > 0):
                                        move_dir = "stop"
                                    elif(self.wait == 0):
                                        self.remove_dead()
                                        self.wait = 290
                                        move_dir = "stop"
                                        self.kill += 1
                                        self.current_action = "none"
                            else:
                                move_dir = self.dir
                        else:
                            if(self.current_action == "none" ):
                                self.loc_x , self.loc_y = Animal_start(self.animal)
                                self.current_action = "Return_poacher"
                            self.dir = self.move_to_this_tile(self.loc_x,self.loc_y)
                            move_dir = self.dir
                    else:
                        self.loc_y = 15
                        self.dir = self.move_to_this_tile(self.loc_x,self.loc_y)
                        if(abs(self.rect.x - Ranger[0].rect.x) < 64 and abs(self.rect.y - Ranger[0].rect.y) < 64 and self.current_action != 'fight'):
                            self.current_action = 'fight'
                            Ranger[0].current_action = 'fight'
                            self.wait = 90
                            Ranger[0].wait = 95
                            move_dir = "shot"
                        elif(self.current_action == "fight"):
                            
                            if(self.wait > 0):
                                self.wait -= 1
                                move_dir = "shoot"
                            elif(self.wait == 0):
                                a = random.randint(0,2)
                                print(a)
                                if(a <= 1):
                                    Poacher[0].killed()
                                    Poacher[0].wait = 200
                                    move_dir = "stop"
                                else:
                                    self.kill = 2
                                    self.alert= False
                                    self.current_action = "none"
                                    move_dir = "stop"
                        elif(self.current_action == "Return_poacher"):
                            self.dir = self.move_to_this_tile(self.loc_x,self.loc_y)
                            move_dir = self.dir
                          
                        else:
                            move_dir = self.dir
                        
                elif(self.animal == "ranger"):
                    if(self.alert):
                        self.loc_x,self.loc_y = Poacher[0].get_location()
                        self.dir = self.move_to_this_tile(self.loc_x,self.loc_y)
                        move_dir = self.dir
                        if(Poacher[0].player):
                            if self.loc_y < 100:
                                print("here")
                                self.alert = False
                                move_dir = self.move_to_this_tile(Animal_start("ranger"))
                            elif (abs(self.rect.x - self.loc_x) < 40 and abs(self.rect.y - self.loc_y) < 40):
                                print("here")
                                Player[0].alive = False
                                self.alert = False
                        else:
                            if(self.current_action == "fight"):
                                if(self.wait >= 0):
                                    self.wait -= 1
                                    move_dir = "shoot"
                                if(self.wait == 0):
                                    if(Poacher[0].alive == True):
                                        Ranger[0].killed()
                                        move_dir = "stop"
                                    else:
                                        move_dir = "stop"
                                        self.alert = False
                    else:
                        self.loc_x, self.loc_y = Animal_start(self.animal)
                        self.dir = self.move_to_this_tile(self.loc_x,self.loc_y)
                        move_dir = self.dir
                        
                elif(self.animal == "vehicle"):
                    if(self.alert):
                        self.loc_x,self.loc_y = Poacher[0].get_location()
                        self.dir = self.move_to_this_tile(self.loc_x,self.loc_y)
                        move_dir = self.dir
                        if(abs(self.loc_x - self.rect.x) < 200 and abs(self.loc_y - self.rect.y) < 200):
                            self.alert = False
                            Ranger[0].alert = True
                            Ranger[0].rect.x = self.rect.x
                            Ranger[0].rect.y = self.rect.y
                            Poacher[0].alert = True
                    else:
                        self.loc_x, self.loc_y = Animal_start(self.animal)
                        self.dir = self.move_to_this_tile(self.loc_x,self.loc_y)
                        move_dir = self.dir
                else:
                    if(self.predator != None):
                        x,y = self.predator.get_location()
                        if abs(self.rect.x - x) < 160 and abs(self.rect.y - y) < 160 :
                            if(self.pred_near):
                                self.pred_near = False
                                self.speed = 3 * self.speed
                                self.predator.set_speed(self.speed+3)
                            dir = self.predator.get_dir()
                            if(dir == "up"):
                                self.dir = "up"
                            elif(dir == "down"):
                                self.dir = "down"
                            elif(dir == "right"):
                                self.dir = "right"
                            elif(dir == "left"):
                                self.dir = "left"
                            else:
                                self.dir = self.dir
                                self.predator = None
                        else:
                            if(self.current_action == "none"):
                                self.current_action = random.choice(Animal_action[self.animal])
                                if(self.current_action == "to_drink"):
                                    self.loc_x, self.loc_y = Animal_drink(self.animal)  
                                else:
                                    self.loc_x ,self.loc_y = Animal_location_map[self.animal][self.current_action]
                            self.dir = self.move_to_this_tile(self.loc_x,self.loc_y)
                        
                    elif(self.current_action == "none"):
                        if(self.wait != 0):
                            self.wait -= 1
                            return
                        else:
                            self.wait = 120
                        
                        self.current_action = random.choice(Animal_action[self.animal])
                        if(self.current_action == "to_kill"):
                            if(len(Preys) == 0):
                                screen.fill(BLACK)
                                Game_over[0] = True
                            else:
                                self.nearest_prey()
                                
                                self.prey.predator = self
                                self.loc_x,self.loc_y = self.prey.get_location()
                                if abs(self.rect.x - self.loc_x) < 40 and abs(self.rect.y - self.loc_y) < 40:
                                    a = random.randint(0,1)
                                    if(a == 1):
                                        self.prey.killed()
                                        self.remove_dead()
                                        self.wait = 200
                                        self.current_action = "none"
                                    else:
                                        self.current_action = "none"
                                        self.wait = 120
                                        self.prey.predator = None
                                        self.prey = None
                                        
                        elif(self.current_action == "to_drink"):
                            self.loc_x, self.loc_y = Animal_drink(self.animal)  
                        else:
                            self.loc_x ,self.loc_y = Animal_location_map[self.animal][self.current_action]
                    
                            
                    elif(self.current_action == "to_kill"):
                        if(len(Preys) != 0):
                            self.nearest_prey()
                            self.prey.predator = self
                            self.loc_x,self.loc_y = self.prey.get_location()
                            if abs(self.rect.x - self.loc_x) < 20 and abs(self.rect.y - self.loc_y) < 20:
                                a = random.randint(0,1)
                                if(a == 1):
                                    self.prey.killed()
                                    self.remove_dead()
                                    self.wait = 200
                                    self.current_action = "none"
                                else:
                                    self.current_action = "none"
                                    self.wait = 120
                                    self.prey.predator = None
                                    self.prey = None
                        else:
                            screen.fill(BLACK)
                            Game_over[0] = True
                            
                    if(self.predator == None): 
                        self.dir = self.move_to_this_tile(self.loc_x,self.loc_y)

                    move_dir = self.dir
                
            #Now that we have got the direction of the animal, we should move it  
            if move_dir != "stop":
                
                if(not(self.player)):
                    if(abs(self.rect.x - self.loc_x) < zoom_adjusted_speed):
                            self.rect.x = self.loc_x
                            if(self.current_action == "fight"):
                                if(move_dir == "shoot"):
                                    move_dir = "shoot"
                                else:  
                                    move_dir = move_dir
                            elif(abs(self.rect.y - self.loc_y ) < zoom_adjusted_speed and self.animal != "poacher"):
                                self.rect.y = self.loc_y
                                move_dir = "stop"
                            elif(abs(self.rect.y - self.loc_y) < zoom_adjusted_speed and self.current_action == "Return_poacher"):
                                self.rect.y = self.loc_y
                                move_dir = "ret_poacher"
                            elif(abs(self.loc_x-self.rect.x) < 80 and abs(self.loc_y-self.rect.y) < 80 and self.animal == "poacher" and self.current_action != "Return_poacher"):
                                move_dir = "shoot"
                            else:
                                if(self.rect.y < self.loc_y):
                                    move_dir = "down"
                                    self.dir = "down"
                                else:
                                    move_dir = "up"
                                    self.dir = "up"
                    new_speed = zoom_adjusted_speed
                else:
                    if(spacebar[0]):
                        new_speed = zoom_adjusted_speed + 5 * camera.zoom_level
                        spacebar[0] = False
                    else:
                        new_speed = zoom_adjusted_speed
                       
                
                if move_dir == "left":
                    self.rect.x -= new_speed
                    if(self.animal == "vehicle"):
                        self.image = self.images["horizontal"]
                    else:
                        self.image = pygame.transform.flip(
                            self.images["moving"][self.moving_index], True, False
                        )
                elif move_dir == "right":
                    self.rect.x += new_speed
                    if(self.animal == "vehicle"):
                        self.image = pygame.transform.flip(
                            self.images["horizontal"], True, False
                        )
                    else:
                        self.image = self.images["moving"][self.moving_index]

                elif move_dir == "up":
                    self.rect.y -= new_speed
                    if(self.animal == "vehicle"):
                        self.image = self.images["vertical"]
                    else:
                        self.image = pygame.transform.rotate(
                            self.images["moving"][self.moving_index], 90
                        )

                elif move_dir == "down":
                    self.rect.y += new_speed
                    if(self.animal == "vehicle"):
                        self.image = pygame.transform.rotate(
                            self.images["vertical"], 180
                        )
                    else:
                        self.image = pygame.transform.rotate(
                            self.images["moving"][self.moving_index], -90
                        )
                elif move_dir == "shoot":
                    self.image = self.images["shoot"]
                    
                elif move_dir == "ret_poacher":
                    Poacher.pop()
                    return
                

                self.frame_counter += 1
                if(self.animal != "vehicle"): 
                    if self.frame_counter >= zoom_adjusted_delay:
                        self.moving_index = (self.moving_index + 1) % len(self.images["moving"])
                        self.frame_counter = 0
            else:
                if(not self.player):
                    if(self.animal == "vehicle"):
                        self.image = self.images["horizontal"]
                    else:
                        self.image = self.images["sitting"]
                        self.moving_index = 0
                        self.current_action = "none"
                    if(self.animal != "poacher"):
                        self.wait = 120

            self.rect.x = max(0, min(self.map_width - LION_SIZE[0], self.rect.x))
            self.rect.y = max(0, min(self.map_height - LION_SIZE[1], self.rect.y))
            if(self.rect.x < 320):
                self.killed()
                self.wait = 30
                print("died")
        else:
            if(self.wait != 0):
                if(self.rect.x < 320):
                    self.image = self.images["croco"]
                else:
                    self.image = pygame.transform.rotate(self.images["dead"], 90)
                self.wait -= 1
            else:
                self.image = None
            
    def remove_dead(self):
        for i in range(len(Animals)):
            if (not Animals[i].is_alive()):
                if(Animals[i].wait == 0):
                    Animals.pop(i)
                    break
        for i in range(len(Preys)):
            if (not Preys[i].is_alive()):
                if(Preys[i].wait == 0):
                    Preys.pop(i)
                    break
        for i in range(len(Predators)):
            if (not Predators[i].is_alive()):
                if(Predators[i].wait == 0):
                    Predators.pop(i)
                    break
        for i in range(len(Poacher)):
            if (not Poacher[i].is_alive()):
                if(Poacher[i].wait == 0):
                    Poacher.pop(i)
                    break
                
        for i in range(len(Player)):
            if (not Player[i].is_alive()):
                if(Player[i].wait == 0):
                    Player.pop(i)
                    Player_dead[0] = True
                    play_char[0] = True
                    break
                # else:
                #     self.image = 
        
            
    def set_predator(self,pred):
        self.predator = pred
    
    def draw(self, surface, camera):
        if(self.image == None):
            return
        scaled_rect = camera.apply(self.rect)
        scaled_image = pygame.transform.scale(
            self.image, (scaled_rect.width, scaled_rect.height)
        )
        surface.blit(scaled_image, scaled_rect.topleft)
    
    def get_location(self):
        return self.rect.x , self.rect.y
    
    def killed(self):
        self.alive = False
        self.wait = 200
        self.image = pygame.transform.rotate(self.images["dead"], 90)
        
    def get_dir(self):
        return self.dir
    
    def set_speed(self,speed_new):
        self.speed = speed_new

    def nearest_animal(self):
        dist = 1000000000
        for i in range(len(Animals)):
            x,y = Animals[i].get_location()
            calc = math.sqrt((self.rect.x - x)**2 + (self.rect.y - y)**2)
            if(calc < dist):
                self.poach_targ = Animals[i]
                dist = calc
                
    def animal_type(self):
        return self.animal
    
    def is_alive(self):
        return self.alive
    
    def nearest_prey(self):
        dist = 1000000000
        for i in range(len(Preys)):
            x,y = Preys[i].get_location()
            calc = math.sqrt((self.rect.x - x)**2 + (self.rect.y - y)**2)
            if(calc < dist):
                self.prey = Preys[i]
                dist = calc
       
    
            
num_lions = 1
num_giraffe = 2

for i in range(num_lions):
    x,y = Animal_start("lion")
    ani = Animal(lion_images, x, y,10,"lion",0, False)
    Animals.append(ani)
    Predators.append(ani)
    
for i in range(num_giraffe):
    x,y = Animal_start("giraffe")
    ani = Animal(giraffe_images, x, y,3,"giraffe",0, False)
    Animals.append(ani)
    Preys.append(ani)
    
x,y = Animal_start("poacher")
poach = Animal(poacher_images,x,y,6,"poacher",290, False)
Poacher.append(poach)

x,y = Animal_start("ranger")

ranger = Animal(ranger_images,x,y,8,"ranger",0, False)
Ranger.append(ranger)
camera = Camera(tmx_data.width * tmx_data.tilewidth, tmx_data.height * tmx_data.tileheight)

x,y = Animal_start("vehicle")

vehicle = Animal(vehicle_images,x,y,30,"vehicle",0, False)
Vehicle.append(vehicle)


animal_time = time.time()
start_time = time.time()
info_time = time.time()
running = True

inf = ""
while running:
    
    if(not playscreen[0] and Play_mode[0]):
        
        keys = pygame.key.get_pressed()
        if(play_char[0]):
            if keys[pygame.K_w] :
                Player[0].update("up")
            if keys[pygame.K_s]:
                Player[0].update("down")
            if keys[pygame.K_a]:
                Player[0].update("left")
            if keys[pygame.K_d]:
                Player[0].update("right")
            if keys[pygame.K_SPACE]:
                spacebar[0] = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEWHEEL:
                camera.zoom(event.y * 0.1)
            elif event.type == pygame.MOUSEMOTION:
                if event.buttons[0]:
                    camera.scroll(-event.rel[0], -event.rel[1])
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_MINUS and pygame.key.get_mods() & pygame.KMOD_META and not pygame.key.get_mods() & pygame.KMOD_ALT:
                    camera.zoom(-0.1)
                elif event.key == pygame.K_EQUALS and pygame.key.get_mods() & pygame.KMOD_META and pygame.key.get_mods() & pygame.KMOD_SHIFT and not pygame.key.get_mods() & pygame.KMOD_ALT:
                    camera.zoom(0.1)
                    
                elif event.key == pygame.K_c:
                    print("pressed c")
                    if(Player[0].allow_chase == True):
                        Player[0].chase = True
                        Player[0].allow_chase = False
                        Player[0].prey = Mark[-1]
                elif event.key == pygame.K_k:
                    print("pressed k")
                    if(Player[0].allow_kill == True):
                        Player[0].kill_prey_player = True
                        Player[0].allow_kill = False
                elif event.key == pygame.K_t:
                    print("pressed t")
                    if(Player[0].poach_targ != None):
                        Player[0].poach_targ.shot += 1
        screen.fill(WHITE)
        if (len(Preys) != 0) and (len(Predators)!= 0 and not (Player_dead[0])):
            screen.fill((0, 100, 0)) 
            render_map(screen, tmx_data, camera)
            
            # Update and render animals
            Animals[0].remove_dead()
            
            for i in range(len(Animals)):
                if(not Animals[i].player):
                    Animals[i].update( "stop")
                    Animals[i].draw(screen, camera)
            for i in range(len(Poacher)):
                if(not Poacher[i].player):
                    Poacher[i].update("stop")
                    if(len(Poacher) != 0):
                        Poacher[i].draw(screen,camera)
            for i in range(len(Ranger)):
                if(not Ranger[i].player):
                    Ranger[i].update("stop")
                    if(len(Ranger) != 0):
                        Ranger[i].draw(screen,camera)
            for i in range(len(Player)):
                Player[i].update("stop")
                Player[i].draw(screen,camera)
                
                    
                    
                        
            vehicle.update("stop")
            vehicle.draw(screen,camera)
            process_object_layer(Game_over[0],screen,tmx_data,camera)
            
            if(time.time() - animal_time > 10.0):
                animal_time = time.time()
                
            
            if(time.time() - info_time > 10.0):
                inf = random.choice(info)
                info_time = time.time()
                if(len(Preys) < 4):
                    c = 4 - len(Preys)
                    for i in range(c):
                        x,y = Animal_start("giraffe")
                        ani = Animal(giraffe_images, x, y,3,"giraffe",0, False)
                        Animals.append(ani)
                        Preys.append(ani)
                if(len(Predators) < 2):
                    c = 2 - len(Predators)
                    for i in range(c):
                        x,y = Animal_start("lion")
                        ani = Animal(lion_images, x, y,3,"lion",0, False)
                        Animals.append(ani)
                        Predators.append(ani)
                
                
            info_message(inf,100)
            if(time.time() - start_time > 120.0 and len(Poacher) == 0):
                start_time = time.time()
                poach = Animal(poacher_images,MAP_WIDTH,MAP_HEIGHT,6,"poacher",290)
                Poacher.append(poach)
                
            # Render UI or game over screen if needed
            if Game_over[0]:
                screen.fill(GRAY)
                game_over()
        else:
            # Game over condition
            screen.fill(GRAY)
            game_over()
            
    elif(playscreen[0] and not(Play_mode[0])):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the mouse click is within the button
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_height:
                    print("yay")
                    playscreen[0] = False
                
        screen.fill(WHITE)
        play_screen()
        
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the mouse click is within the button
                mouse_x, mouse_y = pygame.mouse.get_pos()
                characters = ["lion", "giraffe", "poacher", "ranger","game-ai"]
                for idx, _ in enumerate(characters):
                    button_rect = pygame.Rect(button_start_x + idx * (button_width + button_spacing), button_start_y, button_width, button_height)
                    if button_rect.collidepoint(mouse_x, mouse_y):
                        
                        print("Selected character:", characters[idx])
                        Play_mode[0] = True
                        if(characters[idx] == "lion"):
                            play_char[0] = True
                            x,y = Animal_start("lion")
                            lion = Animal(lion_images, x, y,10,"lion",0, True)
                            Animals.append(lion)
                            Predators.append(lion)
                            Player.append(lion)
                        elif(characters[idx] == "giraffe"):
                            play_char[0] = True
                            x,y = Animal_start("giraffe")
                            giraffe = Animal(giraffe_images, x, y,10,"giraffe",0, True)
                            Animals.append(giraffe)
                            Preys.append(giraffe)
                            Player.append(giraffe)
                            
                        elif(characters[idx] == "poacher"):
                            play_char[0] = True
                            x,y = Animal_start("poacher")
                            poach = Animal(poacher_images, x, y,10,"poacher",0, True)
                            Poacher = []
                            Poacher.append(poach)
                            Player.append(poach)
                            
                        
        screen.fill(WHITE)
        choose_character_screen()
        draw_character_buttons()

    pygame.display.flip()
    clock.tick(60)  # Maintain 60 FPS