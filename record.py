import pyaudio
import wave

# Audio recording parameters
audio_format = pyaudio.paInt16  # 16-bit resolution
num_channels = 1  # mono
sample_rate = 44100  # 44.1 kHz
chunk_size = 4096  # Larger buffer size
record_seconds = 5  # Duration of recording
output_filename = "output.wav"  # Output file

# Initialize PyAudio
p = pyaudio.PyAudio()

# Open stream
stream = p.open(format=audio_format,
                channels=num_channels,
                rate=sample_rate,
                input=True,
                frames_per_buffer=chunk_size)

print("Recording...")

frames = []

# Record for 5 seconds
for i in range(0, int(sample_rate / chunk_size * record_seconds)):
    data = stream.read(chunk_size)
    frames.append(data)

print("Finished recording.")

# Stop and close the stream
stream.stop_stream()
stream.close()
p.terminate()

# Save the recorded data as a WAV file
wf = wave.open(output_filename, 'wb')
wf.setnchannels(num_channels)
wf.setsampwidth(p.get_sample_size(audio_format))
wf.setframerate(sample_rate)
wf.writeframes(b''.join(frames))
wf.close()
