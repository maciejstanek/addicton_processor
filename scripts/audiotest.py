#!/usr/bin/env python

import pyaudio
import math
import numpy as np

audio_queue = []
audio_queue_len = 10

def toarray(string):
    x = np.sum(np.array([ord(i) for i in string], dtype=int).reshape(-1, 2), axis=1)
    print(x)


def callback(in_data, frame_count, time_info, status):
    audio_queue.append(in_data)
    queue_front = audio_queue[0]
    if len(audio_queue) > audio_queue_len:
        audio_queue.pop(0)

    x = toarray(in_data)
    y = toarray(queue_front)
    z = np.column_stack((x, y))
    n = ''.join([chr(int(i)) for i in np.floor(np.mean(z, axis=1)).tolist()])
    # print(n)

    ostream.write(n)
    # x = [ord(i) for i in in_data]
    # print(type(in_data))
    # print(x)
    return (None, pyaudio.paContinue)

audio = pyaudio.PyAudio()
istream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=4096, stream_callback=callback)
ostream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, output=True, frames_per_buffer=4096)

try:
    while True:
        pass
except KeyboardInterrupt:
    pass

print('Shutting down')
istream.stop_stream()
istream.close()
ostream.close()
audio.terminate()
