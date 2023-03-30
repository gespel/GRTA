import numpy as np
import pygame
from grta import GRTA

pygame.init()
pygame.display.set_caption('Realtime Spectrum Analyzer')
WINDOW_WIDTH, WINDOW_HEIGHT = 1200, 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

FREQUENCY_BANDS = 1200

MIN_FREQUENCY = 20
MAX_FREQUENCY = 20000


color_palette = [(i*0.4, 0, 255-i*0.8) for i in range(256)]

g = GRTA()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break

    spectrum_data = g.calculate_spectrum()

    screen.fill((0, 0, 0))
    font = pygame.font.SysFont(None, 20)

    label_x = font.render("Frequency (Hz)", True, (255, 255, 255))
    label_y = font.render("Amplitude", True, (255, 255, 255))

    freq_lines = [5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000]
    for freq in freq_lines:
        freq_pos = int(np.log10(freq) * WINDOW_WIDTH / np.log10(MAX_FREQUENCY))
        pygame.draw.line(screen, (100, 100, 100), (freq_pos, 0), (freq_pos, WINDOW_HEIGHT), 1)
        freq_label = font.render(str(freq), True, (255, 255, 255))
        screen.blit(freq_label, (freq_pos + 10, 20))

    for i in range(FREQUENCY_BANDS):
        bar_height = int(np.log10(spectrum_data[i] + 1) * WINDOW_HEIGHT / np.log10(MAX_FREQUENCY))
        color = color_palette[min(bar_height, 255)]
        pygame.draw.rect(screen, color,
                         (i * (WINDOW_WIDTH // FREQUENCY_BANDS), WINDOW_HEIGHT - bar_height / 2,
                          WINDOW_WIDTH // FREQUENCY_BANDS, bar_height))
    screen.blit(label_x, (WINDOW_WIDTH // 2, WINDOW_HEIGHT - 20))
    screen.blit(label_y, (20, WINDOW_HEIGHT // 2))
    pygame.display.update()

pygame.quit()
