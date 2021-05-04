import pyaudio
import struct
import pyautogui  # to press a button to play the game
import pvporcupine

key1 = r'snake_up_windows.ppn'
key2 = r'snake_down_windows.ppn'
key3 = r'snake_right_windows.ppn'
key4 = r'snake_left_windows.ppn'
keyword_file_paths = [key1, key2, key3, key4]

sensitivities = [1,1,1,1]
handle = pvporcupine.create(keyword_paths=keyword_file_paths, sensitivities=sensitivities )

def get_next_audio_frame():
    pa = pyaudio.PyAudio()
    audio_stream = pa.open(rate=handle.sample_rate, channels=1, format=pyaudio.paInt16, input=True,
                           frames_per_buffer=handle.frame_length, input_device_index=None)
    pcm = audio_stream.read(handle.frame_length)
    pcm = struct.unpack_from("h" * handle.frame_length, pcm)
    return pcm


while True:

    pcm = get_next_audio_frame()
    keyword_index = handle.process(pcm)
    if keyword_index == 0:
        print("Up")
        pyautogui.press('up')
    if keyword_index == 3:
        print("Left")
        pyautogui.press('left')
    if keyword_index == 2:
        print("Right")
        pyautogui.press('right')
    if keyword_index == 1:
        print("Down")
        pyautogui.press('down')
