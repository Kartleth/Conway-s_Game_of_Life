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

#Define las función que actualiza las células
def update(screen, cells, size, with_shadow=False):
    updated_cells = np.zeros((cells.shape[0], cells.shape[1]))
    # Recorre cada célula de la matriz de células
    for row, col in np.ndindex(cells.shape):
        # Cuenta el número de células vecinas vivas
        alive = np.sum(cells[row-1:row+2, col-1:col+2]) - cells[row, col]
        # Si la célula está muerta, el color es COLOR_BG, si está viva, el color es COLOR_ALIVE
        color = COLOR_BG if cells[row,col] == 0 else COLOR_ALIVE
        # Si la célula está viva
        if cells[row, col] == 1:
            # Si tiene menos de dos o más de tres células vecinas vivas, muere
            if alive < 2 or alive > 3:
                # Si se debe aplicar sombra, cambia el color a COLOR_DIE_NEXT
                if with_shadow:
                    color = COLOR_DIE_NEXT
            # Si tiene dos o tres células vecinas vivas, sigue viva
            elif 2 <= alive <= 3:
                updated_cells[row, col] = 1
                # Si se debe aplicar sombra, cambia el color a COLOR_NEON
                if with_shadow:
                    color = COLOR_NEON
        # Si la célula está muerta y tiene exactamente tres células vecinas vivas, revive
        else: 
            if alive == 3:
                updated_cells[row, col] = 1
                # Si se debe aplicar sombra, cambia el color a COLOR_NEON
                if with_shadow:
                    color = COLOR_NEON
        
        # Si la célula va a reproducirse, cambia su color a un color arcoiris
        if updated_cells[row, col] == 1 and with_shadow:
            # Calcula el valor del hue (color) en el rango 0-360
            h = (time.time() * 100) % 360 # calcula el valor del hue (color) en el rango 0-360
            # Crea un objeto Color de Pygame
            color = pygame.Color(0) 
            # Asigna los valores de hsv (matiz, saturación, brillo, alfa) al objeto Color
            color.hsva = (h, 100, 100, 100) 
            
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