import time
import pygame
import numpy as np

# Define los colores
COLOR_BG = (10,10,10) # negro
COLOR_GRID = (40,40,40) # gris (40,40,40) (165,224,247)
COLOR_DIE_NEXT = (220,239,247) #(170,170,170)
COLOR_ALIVE = (255,255,255) # blanco (255,255,255)
COLOR_NEON = (87, 203, 248) # azul neon
current_color = COLOR_ALIVE

def update(screen, cells, size, with_shadow=False):
    updated_cells = np.zeros((cells.shape[0], cells.shape[1]))

    for row, col in np.ndindex(cells.shape):
        alive = np.sum(cells[row-1:row+2, col-1:col+2]) - cells[row, col]
        color = COLOR_BG if cells[row,col] == 0 else COLOR_ALIVE

        if cells[row, col] == 1:
            if alive < 2 or alive > 3:
                if with_shadow:
                    color = COLOR_DIE_NEXT
            elif 2 <= alive <= 3:
                updated_cells[row, col] = 1
                if with_shadow:
                    color = COLOR_NEON
        else: 
            if alive == 3:
                updated_cells[row, col] = 1
                if with_shadow:
                    color = COLOR_NEON
        
        # Si la célula va a reproducirse, cambia su color a un color arcoiris
        if updated_cells[row, col] == 1 and with_shadow:
            h = (time.time() * 100) % 360 # calcula el valor del hue (color) en el rango 0-360
            color = pygame.Color(0) # Crea un objeto Color de Pygame
            color.hsva = (h, 100, 100, 100) # Asigna los valores de hsv (matiz, saturación, brillo, alfa) al objeto Color
            
        # Dibuja la célula con el color correspondiente
        pygame.draw.rect(screen, color, (col * size, row * size, size - 1, size - 1))
    
    return updated_cells

def main():
    pygame.init()
    screen = pygame.display.set_mode((800,600))

    cells = np.zeros((60,80))
    screen.fill(COLOR_GRID)
    update(screen, cells, 10)

    pygame.display.flip()
    pygame.display.update()

    running = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = not running
                    update(screen, cells, 10)
                    pygame.display.update()
                elif event.key == pygame.K_r:
                    cells = np.zeros((60,80))
                    screen.fill(COLOR_GRID)
                    update(screen, cells, 10)
                    pygame.display.update()
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                cells[pos[1] // 10, pos[0] // 10] = 1
                update(screen,cells,10)
                pygame.display.update()
            
        
        screen.fill(COLOR_GRID)

        if running:
            cells = update(screen, cells, 10, with_shadow=True)
            pygame.display.update()
        
        time.sleep(0.001)


if __name__ == '__main__':
    main()