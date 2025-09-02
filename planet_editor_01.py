import pygame
import sys
from OpenGL.GL import *
from OpenGL.GLU import *
import random

# Define land cell types
LAND_TYPES = {
    'wuste': (1.0, 0.9, 0.5),  # Desert
    'steppe': (0.6, 0.8, 0.4),  # Steppe
    'wald': (0.0, 0.5, 0.0),    # Forest
    'tundra': (0.6, 0.6, 0.6),  # Tundra
    'fjord':  (0.4, 0.5, 0.8),    # Fjord
    'water': (0.0,0.0,1.0) #Water
}

# Define water cell color
WATER_COLOR = (0.0, 0.0, 1.0)  # Blue color for water

class World:
    def __init__(self, radius):
        self.radius = radius
        self.grid_size = 20  # Adjust grid size for larger simulation
        self.cells = [[Cell(self, i, j) for j in range(self.grid_size)] for i in range(self.grid_size)]
        self.humans = []

    def generate_resources(self):
        for row in self.cells:
            for cell in row:
                if random.random() < 0.1:
                    cell.add_resource()

    def generate_land_types(self):
        for row in self.cells:
            for cell in row:
                cell.type = random.choice(list(LAND_TYPES.keys()))

    def generate_water(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                cell = self.cells[i][j]
                if cell.type == 'fjord':
                    cell.type = 'water'
                    # Make neighboring cells water too
                    for dx in [-1, 0, 1]:
                        for dy in [-1, 0, 1]:
                            nx, ny = i + dx, j + dy
                            if 0 <= nx < self.grid_size and 0 <= ny < self.grid_size:
                                self.cells[nx][ny].type = 'water'

    def spawn_human(self, x, y, gender):
        if 0 <= x < self.grid_size and 0 <= y < self.grid_size:
            human = Human(self, x, y, gender)
            self.humans.append(human)

    def update(self):
        for human in self.humans:
            if not human.dead:
                human.move_and_collect()

    def fight(self, human1, human2):
        # Simple fight mechanism
        damage = random.randint(1, 10)
        if random.random() < 0.5:
            human1.hp -= damage
            if human1.hp <= 0:
                self.handle_death(human1, human2)
        else:
            human2.hp -= damage
            if human2.hp <= 0:
                self.handle_death(human2, human1)

    def handle_death(self, victim, killer):
        victim.dead = True
        killer.freibeute_timer = max(killer.freibeute_timer * 2, 60)  # Increase freibeute timer
        for human in self.humans:
            if human != killer and not human.dead:
                human.add_target(killer)

class Cell:
    def __init__(self, world, x, y):
        self.world = world
        self.x = x * 2  # Adjusting for OpenGL coordinates
        self.y = y * 2  # Adjusting for OpenGL coordinates
        self.type = random.choice(list(LAND_TYPES.keys()))  # Random land type
        self.resource = False

    def add_resource(self):
        self.resource = True

class Human:
    def __init__(self, world, x, y, gender):
        self.world = world
        self.x = x
        self.y = y
        self.gender = gender
        self.vision_range = 1  # Human can see adjacent cells
        self.resources = 0
        self.hp = 100  # Health points
        self.dead = False
        self.freibeute_timer = 0  # Time left as Freibeute
        self.group = None
        self.targets = []  # List of humans that can attack this human

    def move_and_collect(self):
        # Randomly move to a neighboring cell
        dx = random.choice([-1, 0, 1])
        dy = random.choice([-1, 0, 1])
        new_x = self.x + dx
        new_y = self.y + dy

        # Ensure the new position is within bounds and not water
        if 0 <= new_x < self.world.grid_size and 0 <= new_y < self.world.grid_size:
            if self.world.cells[new_x][new_y].type != 'water':
                self.x = new_x
                self.y = new_y
                cell = self.world.cells[self.x][self.y]
                if cell.resource:
                    if self.group:
                        if not any(human.x == self.x and human.y == self.y and human != self for human in self.group.members):
                            cell.resource = False  # Collect the resource
                            self.resources += 1
                    else:
                        cell.resource = False  # Collect the resource
                        self.resources += 1

    def see_surroundings(self):
        visible_cells = []
        for dx in range(-self.vision_range, self.vision_range + 1):
            for dy in range(-self.vision_range, self.vision_range + 1):
                nx, ny = self.x + dx, self.y + dy
                if 0 <= nx < self.world.grid_size and 0 <= ny < self.world.grid_size:
                    visible_cells.append(self.world.cells[nx][ny])
        return visible_cells

    def join_group(self, group):
        self.group = group
        group.add_member(self)

    def add_target(self, target):
        if target not in self.targets:
            self.targets.append(target)

class Group:
    def __init__(self):
        self.members = []
        self.guardians = 0

    def add_member(self, human):
        self.members.append(human)
        if len(self.members) >= 8:
            self.form_clan()

    def form_clan(self):
        # Clan bonuses
        self.guardians = 2  # Number of guardians for the clan

    def night_watch(self):
        if self.guardians > 0:
            # Implement guardians keeping watch
            pass
        
class Game:
    def __init__(self):
        self.screen_width = 800
        self.screen_height = 600
        self.world_radius = 10  # Adjusted to fit in the view
        self.world = World(self.world_radius)
        self.world.generate_resources()  # Generate resources in the world
        self.world.generate_land_types()  # Generate land types in the world
        self.cell_size = 2  # Adjusted for OpenGL coordinates
        self.resource_color = (1.0, 1.0, 0.0)  # OpenGL color range is 0.0 to 1.0
        self.male_color = (0.0, 0.0, 1.0)  # Blue color for males
        self.female_color = (1.0, 0.0, 1.0)  # Magenta color for females
        self.water_color = (0.0, 0.0, 1.0)   # Blue color for water
        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.OPENGL | pygame.DOUBLEBUF)
        pygame.display.set_caption("3D World")
        self.clock = pygame.time.Clock()

        glEnable(GL_DEPTH_TEST)  # Enable depth testing

        glMatrixMode(GL_PROJECTION)
        gluPerspective(45, (self.screen_width / self.screen_height), 0.1, 50.0)
        glMatrixMode(GL_MODELVIEW)
        glTranslatef(-self.world.grid_size, -self.world.grid_size, -30)  # Adjusted for a better view of the world

        # Spawn initial humans
        self.world.spawn_human(0, 0, 'male')
        self.world.spawn_human(5, 5, 'female')


def handle_events(self):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

def draw_world(self):
    glBegin(GL_QUADS)
    for i in range(self.world.grid_size):
          for j in range(self.world.grid_size):
                cell = self.world.cells[i][j]
                x0 = i * self.cell_size
                y0 = j * self.cell_size
                x1 = x0 + self.cell_size
                y1 = y0
                x2 = x0 + self.cell_size
                y2 = y0 + self.cell_size
                x3 = x0
                y3 = y0 + self.cell_size

                if cell.type == 'water':
                    glColor3f(*self.water_color)
                else:
                    glColor3f(*LAND_TYPES[cell.type])

                glVertex3f(x0, y0, 0)
                glVertex3f(x1, y1, 0)
                glVertex3f(x2, y2, 0)
                glVertex3f(x3, y3, 0)
        glEnd()

def draw_resources(self):
    for row in self.world.cells:
        for cell in row:
            if cell.resource:
                glPushMatrix()
                glTranslatef(cell.x, cell.y, 0)
                glColor3f(*self.resource_color)
                self.draw_sphere(0.5, 10, 10)  # Adjusted sphere size
                glPopMatrix()

def draw_humans(self):
    for human in self.world.humans:
        if not human.dead:
            glPushMatrix()
            glTranslatef(human.x * self.cell_size, human.y * self.cell_size, 0)
            glColor3f(*self.male_color if human.gender == 'male' else self.female_color)
            self.draw_sphere(0.5, 10, 10)  # Adjusted sphere size
            self.draw_hp(human)  # Draw HP
            glPopMatrix()

def draw_sphere(self, radius, slices, stacks):
    quad = gluNewQuadric()
    gluSphere(quad, radius, slices, stacks)

def draw_hp(self, human):
    glPushMatrix()
    glTranslatef(human.x * self.cell_size, human.y * self.cell_size, 0.5)
    glColor3f(1.0, 0.0, 0.0)
    glBegin(GL_QUADS)
    hp_ratio = human.hp / 100.0
    glVertex3f(-0.5, -0.1, 0)
    glVertex3f(-0.5 + hp_ratio, -0.1, 0)
    glVertex3f(-0.5 + hp_ratio, 0.1, 0)
    glVertex3f(-0.5, 0.1, 0)
    glEnd()
    glPopMatrix()

def run(self):
    while True:
        self.handle_events()
        self.world.update()  # Update world state
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.draw_world()
        self.draw_resources()
        self.draw_humans()
        pygame.display.flip()
        self.clock.tick(60)

