import numpy as np
import pyaudio


class GRTA:
    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 48000
        self.CHUNK_SIZE = 2048

        # Anzahl der Frequenzbänder festlegen
        self.FREQUENCY_BANDS = 1200

        # Minimal- und Maximalfrequenzen festlegen (in Hz)
        self.MIN_FREQUENCY = 20
        self.MAX_FREQUENCY = 20000

        # Logarithmische Skala der Frequenzen erzeugen
        self.freqs = np.logspace(np.log10(self.MIN_FREQUENCY), np.log10(self.MAX_FREQUENCY),
                                 num=self.FREQUENCY_BANDS + 1)

        # Bandbreite jedes Frequenzbands berechnen
        self.band_widths = np.diff(self.freqs)

        self.stream = self.p.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE, input=True,
                                  frames_per_buffer=self.CHUNK_SIZE)

    def calculate_spectrum(self):

        audio_data = np.frombuffer(self.stream.read(self.CHUNK_SIZE), dtype=np.int16)

        fft_data = np.fft.fft(audio_data) / self.CHUNK_SIZE

        mag_data = np.abs(fft_data[:self.CHUNK_SIZE // 2]) ** 2
        data2 = np.abs(fft_data / 1024)
        freqs_data = np.fft.fftfreq(self.CHUNK_SIZE, 1 / self.RATE)[:self.CHUNK_SIZE // 2]

        spectrum_data = np.zeros(self.FREQUENCY_BANDS)
        for i in range(self.FREQUENCY_BANDS):
            start_idx = np.searchsorted(freqs_data, self.freqs[i], 'left')
            end_idx = np.searchsorted(freqs_data, self.freqs[i + 1], 'right')

            spectrum_data[i] = np.sum(mag_data[start_idx:end_idx] * self.band_widths[i])
        print(len(spectrum_data))
        return spectrum_data
