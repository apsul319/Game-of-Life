import sys, pygame, random, tkinter

backgroundColor = 0, 0, 0
aliveColor = 255, 255, 255
deadColor = backgroundColor
square_side = 10
FPS = 20
root = tkinter.Tk()
root.withdraw()
screen_width = root.winfo_screenwidth()-20
screen_height = root.winfo_screenheight()-80
clock = pygame.time.Clock()

class Game_of_Life:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Game of Life")
        pygame.display.set_icon(pygame.image.load('Seal.png'))
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.oldGrid = []
        for i in range(int(screen_height/square_side)):
            c = []
            for j in range(int(screen_width/square_side)):
                if random.randint(1, 3) == 1: c.append(1)
                else: c.append(0)
            self.oldGrid.append(c)
    
    def generation(self):
        newGrid = []
        for col in range(len(self.oldGrid)):
            c = []
            for row in range(len(self.oldGrid[0])):
                neighbor_count = 0
                if self.oldGrid[(col-1) % len(self.oldGrid)][row] == 1: neighbor_count += 1
                if self.oldGrid[(col+1) % len(self.oldGrid)][row] == 1: neighbor_count += 1
                if self.oldGrid[col][(row-1) % len(self.oldGrid[0])] == 1: neighbor_count += 1
                if self.oldGrid[col][(row+1) % len(self.oldGrid[0])] == 1: neighbor_count += 1
                if self.oldGrid[(col-1) % len(self.oldGrid)][(row-1) % len(self.oldGrid[0])] == 1: neighbor_count += 1
                if self.oldGrid[(col+1) % len(self.oldGrid)][(row-1) % len(self.oldGrid[0])] == 1: neighbor_count += 1
                if self.oldGrid[(col-1) % len(self.oldGrid)][(row+1) % len(self.oldGrid[0])] == 1: neighbor_count += 1
                if self.oldGrid[(col+1) % len(self.oldGrid)][(row+1) % len(self.oldGrid[0])] == 1: neighbor_count += 1

                if neighbor_count < 2 or neighbor_count > 3: c.append(0) # Overpopulation / Underpopulation (Rules 1 and 2)
                elif self.oldGrid[col][row] == 0 and neighbor_count == 3: c.append(1) # Reproduction (Rule 4: Any dead cell with exactly three live neighbours will come to life)
                else: c.append(self.oldGrid[col][row])
            newGrid.append(c)
        self.oldGrid = newGrid
    
    def randomize(self):
        for col in range(len(self.oldGrid)):
            for row in range(len(self.oldGrid[0])):
                if random.randint(1, 3) == 1: self.oldGrid[col][row] = 1
                else: self.oldGrid[col][row] = 0
    
    def update(self):
        pos_height = 0
        for col in range(len(self.oldGrid)):
            pos_col = 0
            for row in range(len(self.oldGrid[0])):
                if self.oldGrid[col][row] == 1: pygame.draw.rect(self.screen, aliveColor, pygame.Rect(pos_col, pos_height, square_side, square_side))
                else: pygame.draw.rect(self.screen, deadColor, pygame.Rect(pos_col, pos_height, square_side, square_side))
                pos_col += square_side
            pos_height += square_side

    def manipGrid(self, mouseX, mouseY, mode):
        self.oldGrid[mouseY][mouseX] = mode
        self.update()
        if mode == 1:
            pygame.draw.rect(self.screen, aliveColor, pygame.Rect(mouseX*10, mouseY*10, square_side, square_side))
        else:
            pygame.draw.rect(self.screen, deadColor, pygame.Rect(mouseX*10, mouseY*10, square_side, square_side))

    def clearGrid(self):
        for col in range(len(self.oldGrid)):
            for row in range(len(self.oldGrid[0])):
                self.oldGrid[col][row] = 0
        pygame.display.flip()
      
    def run(self):
        paused = False
        pressed_right = False
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT: pressed_right = True # Pressing the right arrow key will allow you to individually pass each generation while the game is paused
                    if event.key == pygame.K_r: self.randomize() # The r key virtually resets the board by creating another randomized grid of alive and dead cells
                    if event.key == pygame.K_SPACE and paused == False: paused = True # Space pauses the passing of generations until space is pressed again
                    elif event.key == pygame.K_SPACE and paused == True: paused = False
                    if event.key == pygame.K_n: self.clearGrid()
                if pygame.mouse.get_pressed()[0]: # Left mouse click initiates manipGrid method on ADD Mode
                    pos = pygame.mouse.get_pos()
                    self.manipGrid(int(pos[0]/10), int(pos[1]/10), 1)
                elif pygame.mouse.get_pressed()[2]: # Right mouse click initiates manipGrid method on DELETE Mode
                    pos = pygame.mouse.get_pos()
                    self.manipGrid(int(pos[0]/10), int(pos[1]/10), 0)
            self.screen.fill(deadColor)

            if not paused or (paused and pressed_right):
                pressed_right = False
                self.generation()
                
            self.update()
            pygame.display.flip()
            clock.tick(FPS)
                

if __name__ == "__main__":
    game = Game_of_Life()
    game.run()
