import numpy as np
import pygame
from grta import GRTA
import matplotlib.pyplot as plt

pygame.init()
pygame.display.set_caption('Realtime Spectrum Analyzer')
WINDOW_WIDTH, WINDOW_HEIGHT = 1200, 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

FREQUENCY_BANDS = 1200

MIN_FREQUENCY = 20
MAX_FREQUENCY = 20000


color_palette = [(i*0.4, 0, 255-i*0.8) for i in range(256)]

g = GRTA()
print(g.do_measurements(10))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            spectrum_data = g.measure_spectrum()
            plt.plot(spectrum_data)
            plt.xlabel('Frequenz (Hz)')
            plt.ylabel('Amplitude')
            plt.show()
        if event.type == pygame.QUIT:
            running = False
            break

    spectrum_data = g.measure_spectrum()

    screen.fill((0, 0, 0))
    font = pygame.font.SysFont(None, 20)

    label_x = font.render("Frequency (Hz)", True, (255, 255, 255))
    label_y = font.render("Amplitude", True, (255, 255, 255))

    frequency_seq = np.logspace(np.log10(MIN_FREQUENCY), np.log10(MAX_FREQUENCY), FREQUENCY_BANDS)

    for i in range(FREQUENCY_BANDS):
        bar_height = int(np.log10(spectrum_data[i] + 1) * WINDOW_HEIGHT / np.log10(MAX_FREQUENCY))
        color = color_palette[min(bar_height, 255)]
        pygame.draw.rect(screen, color,
                         (i * (WINDOW_WIDTH // FREQUENCY_BANDS), WINDOW_HEIGHT - bar_height / 2,
                          WINDOW_WIDTH // FREQUENCY_BANDS, bar_height))
        if i % 100 == 0:
            freq_value = int(frequency_seq[i])
            freq_label = font.render(str(freq_value) + " Hz", True, (255, 255, 255))

            pygame.draw.line(screen, (255, 255, 255), (i * (WINDOW_WIDTH // FREQUENCY_BANDS), 0),
                             (i * (WINDOW_WIDTH // FREQUENCY_BANDS), WINDOW_HEIGHT), 1)
            screen.blit(freq_label, (i * (WINDOW_WIDTH // FREQUENCY_BANDS), WINDOW_HEIGHT - 40))
    screen.blit(label_x, (WINDOW_WIDTH // 2, WINDOW_HEIGHT - 20))
    screen.blit(label_y, (20, WINDOW_HEIGHT // 2))

    pygame.display.update()

pygame.quit()
