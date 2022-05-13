import time
import numpy as np
from threading import Thread


class WaveSource:

    def __init__(self, queue, wave_id=None, amplitude=1, sampling_rate=300, frame_rate=30,
                 offset=0, wave_frequency_hz=4, delay_rate=0):
        """
        Gera um sinal senoidal em tempo de execução. Cada amostra é composta por um valor de
        tempo e um valor de amplitude. A cada intervalo de tempo (dado pelo frame rate) é
        'publicado' um frame (pacote, não confundir com a taxa de atualização dos gráficos) de
        amostras.

        :param wave_id: Identificador único para este sinal.
        :param amplitude: Amplitude da senoide.
        :param sampling_rate: Total de amostras geradas por segundo.
        :param frame_rate: Número de pacotes de amostras gradas por segundo.
        :param offset: Deslocamento vertical da senoide em relação a origem.
        :param wave_frequency_hz: Frequência da senoide em Hertz.
        :param delay_rate: Taxa de atraso. Simula uma fonte de dados com atrazo temporal contínuo.
        """
        self.queue = queue
        self.wave_id = wave_id or id(self)
        self.amplitude = amplitude
        self.sampling_rate = sampling_rate
        self.frame_rate = frame_rate
        self.delay_rate = delay_rate
        self.wave_frequency_rad = 2 * np.pi * wave_frequency_hz

        self.t0 = 0
        self.points_per_frame = round(self.sampling_rate / self.frame_rate)
        self.frame_time_interval = 1 / self.frame_rate
        self.offset = offset
        self.time_samples = []
        self.value_samples = []
        self.thread = Thread(target=self._run)
        self.thread.daemon = True
        self.thread.start()

    def get_id(self):
        return self.wave_id

    def _run(self):
        while True:
            # Make new points
            t0_old, self.t0 = self.t0, self.t0 + self.frame_time_interval * (1 - self.delay_rate)
            new_time_samples = np.linspace(t0_old, self.t0, self.points_per_frame)
            new_value_samples = np.sin(self.wave_frequency_rad * new_time_samples) + self.offset
            self.queue.put((self.wave_id, new_time_samples, new_value_samples))
            time.sleep(self.frame_time_interval)
