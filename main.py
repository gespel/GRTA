import time

import numpy as np
import pygame
import pyaudio

# Pygame initialisieren
pygame.init()
pygame.display.set_caption('Realtime Spectrum Analyzer')
WINDOW_WIDTH, WINDOW_HEIGHT = 1200, 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# PyAudio initialisieren
p = pyaudio.PyAudio()
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 48000
CHUNK_SIZE = 2048

# Anzahl der Frequenzbänder festlegen
FREQUENCY_BANDS = 1200

# Minimal- und Maximalfrequenzen festlegen (in Hz)
MIN_FREQUENCY = 20
MAX_FREQUENCY = 20000

# Logarithmische Skala der Frequenzen erzeugen
freqs = np.logspace(np.log10(MIN_FREQUENCY), np.log10(MAX_FREQUENCY), num=FREQUENCY_BANDS + 1)

# Bandbreite jedes Frequenzbands berechnen
band_widths = np.diff(freqs)

stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True,
                frames_per_buffer=CHUNK_SIZE)


def calculate_spectrum():

    audio_data = np.frombuffer(stream.read(CHUNK_SIZE), dtype=np.int16)

    fft_data = np.fft.fft(audio_data) / CHUNK_SIZE

    mag_data = np.abs(fft_data[:CHUNK_SIZE // 2]) ** 2
    data2 = np.abs(fft_data / 1024)
    freqs_data = np.fft.fftfreq(CHUNK_SIZE, 1 / RATE)[:CHUNK_SIZE // 2]

    spectrum_data = np.zeros(FREQUENCY_BANDS)
    for i in range(FREQUENCY_BANDS):
        start_idx = np.searchsorted(freqs_data, freqs[i], 'left')
        end_idx = np.searchsorted(freqs_data, freqs[i + 1], 'right')

        spectrum_data[i] = np.sum(mag_data[start_idx:end_idx] * band_widths[i])
    for i in range(FREQUENCY_BANDS):
        print(str(i * FREQUENCY_BANDS) + ":" + str(spectrum_data[i]))
    return spectrum_data

color_palette = [(i * 0.5, 0, 255 - 255 / (i + 1)) for i in range(256)]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break

    spectrum_data = calculate_spectrum()

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

stream.stop_stream()
stream.close()
p.terminate()

pygame.quit()
