import pygame, math, random, sys

#set up playing screen
pygame.init()
playing_area = pygame.display.set_mode((690,690))
pygame.display.set_caption('Conquest')
font = pygame.font.SysFont('arial', 14)
Clock = pygame.time.Clock()
Playing = True
timer = 0
random.seed()

class Game_Object():
    def __init__(self, population, size, team):
        self.population = population
        self.size = size
        self.team = team
        self.image = self.make_object_surface()
        self.rect = self.image.get_rect()

    def make_object_surface(self):
        surface = pygame.Surface((self.size, self.size))
        surface.fill(BLACK)
        self.colour = team_colours[self.team]
        pygame.draw.rect(surface, self.colour, (3, 3, self.size-6, self.size-6))
        return surface

    def draw(self):
        top_left_corner = self.x, self.y
        playing_area.blit(self.image, top_left_corner)
        text = font.render(str(self.population), True, BLACK)
        playing_area.blit(text,(top_left_corner[0] + 2, top_left_corner[1] + self.size/4))

class Building(Game_Object):
    def __init__(self, column, row, population, team, status):
        super().__init__(population, 30, team)
        self.column = column
        self.row = row
        self.x = (self.column * 40) + 10
        self.y = (self.row * 40) + 10
        self.capacity = 100
        self.neutral = status

    def get_adjacent_squares(self):
        adjacent_squares = []
        if self.column != 0:
            adjacent_squares.append([self.column-1, self.row])
        if self.column != 16:
            adjacent_squares.append([self.column+1, self.row])
        if self.row != 0:
            adjacent_squares.append([self.column, self.row-1])
        if self.row != 16:
            adjacent_squares.append([self.column, self.row+1])
        return adjacent_squares

    def spawn_new_bases(self, game_squares):
        if not self.neutral:
            adjacent_squares = self.get_adjacent_squares()
            for square in adjacent_squares:
                column = square[0]
                row = square[1]
                if not game_squares[column][row]:
                    game_squares[column][row] = Building(column, row, 20, 0, True)
        return game_squares

    def inc_population(self):
        if self.population < self.capacity:
            self.population += 1

    def ai_turn(self, armies, game_squares):
        if random.random() > 0.5 and self.population > random.randint(10, 30) and self.team != 1:
            possible_squares = self.get_adjacent_squares()
            target_square = random.choice(possible_squares)
            target_building = game_squares[target_square[0]][target_square[1]]
            host_building = game_squares[self.column][self.row]
            armies.append(Soldier(target_building, host_building))
        return armies

class Soldier(Game_Object):
    def __init__(self, target, host):
        population = int(host.population/2)
        host.population = int(host.population/2)
        team = host.team
        super().__init__(population, 20, team)
        self.x = host.x + 5
        self.y = host.y + 5
        self.target = target
        diff_x = (self.target.x + 5) - self.x
        diff_y = (self.target.y + 5) - self.y
        distance = (diff_x**2 + diff_y**2)**0.5
        self.dx = diff_x / distance
        self.dy = diff_y / distance
        self.dead = False

    def chase(self):
        self.x += self.dx
        self.y += self.dy
        column, row = square_coords((self.x, self.y))
        ##print('army', column, row)
        ##print('target', target, column, row)
        if column == self.target.column and row == self.target.row:
            if self.team == self.target.team:
                self.target.population += self.population
            else:
                self.target.population -= self.population
                if self.target.population < 0:
                    self.target.team = self.team
                    self.target.population *= -1
                    self.target.image = self.target.make_object_surface()
                    self.target.neutral = False
            self.dead = True
        self.draw()

def square_coords(coords):
    square_x = math.floor(coords[0]/40)
    square_y = math.floor(coords[1]/40)
    return[square_x,square_y]

def select_square(selected):
    mouse_pos = pygame.mouse.get_pos()
    check_square = square_coords(mouse_pos)
    square_column = check_square[0]
    square_row = check_square[1]
    if square_row < 17 and square_column < 17:
        if isinstance(game_squares[square_column][square_row], Building) and game_squares[square_column][square_row].team == 1:
            selected = check_square
    return selected

def dispatch_army():
    mouse_pos = pygame.mouse.get_pos()
    target_square = square_coords(mouse_pos)
    if isinstance(game_squares[target_square[0]][target_square[1]], Building) and game_squares[selected[0]][selected[1]].population > 2:
        target_building = game_squares[target_square[0]][target_square[1]]
        host_building = game_squares[selected[0]][selected[1]]
        # check we're not targetting our highlighted building
        if not target_building == host_building:
            armies.append(Soldier(target_building, host_building))

GREY, BLACK = (150,150, 150), (0, 0, 0)
RED, YELLOW = (225, 50, 50), (225, 225, 50)
GREEN, BLUE = (50, 50, 225), (50, 225, 50)
team_colours = [GREY, RED, YELLOW, GREEN, BLUE]

game_squares = []
selected = (8, 0)
armies = []

for column in range(0, 17):
    # create balnk lists for rows in columns
    game_squares.append([])
    for row in range(0, 17):
        if row == 0 and column == 8:
            game_squares[column].append(Building(column, row, 20, 1, False))
        elif row == 8 and column == 0:
            game_squares[column].append(Building(column, row, 20, 2, False))
        elif row == 8 and column == 16:
            game_squares[column].append(Building(column, row, 20, 3, False))
        elif row == 16 and column == 8:
            game_squares[column].append(Building(column, row, 20, 4, False))
        else:
            game_squares[column].append(False)

while Playing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            selected = select_square(selected)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                dispatch_army()

    playing_area.fill(GREY)
    ##playing = check_playing(game_squares)
    for row in game_squares:
        for piece in row:
            # check square has building on it
            if isinstance(piece, Building):
                if timer == 60 and not piece.neutral:
                    piece.inc_population()
                    game_squares = piece.spawn_new_bases(game_squares)
                    armies = piece.ai_turn(armies, game_squares)
                piece.draw()
    for army in armies:
        army.chase()
        if army.dead:
            armies.remove(army)
    pygame.draw.circle(playing_area, BLACK, (25 + (40 * selected[0]), 25 + (40 * selected[1])), 25, 1)
    pygame.display.update()
    Clock.tick(60)
    timer += 1
    if timer == 61:
        timer = 0