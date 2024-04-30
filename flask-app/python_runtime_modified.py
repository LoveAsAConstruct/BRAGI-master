from flask import Flask, jsonify, render_template, redirect, url_for, session
import cv2
import torch
import numpy as np
from threading import Thread, Lock
from functions.detection_module import read_frame, load_yolov5_model, detect_objects, apply_homography, format_detections
import pyaudio
import wave
from google.cloud import speech
from werkzeug.security import generate_password_hash, check_password_hash


# Setup Google Cloud Speech client
client = speech.SpeechClient()
app = Flask(__name__,
            static_folder='frontend/static',
            template_folder='frontend/templates')

# Load the model and homography matrix
model = load_yolov5_model()
H_matrix = np.load(r'flask-app\config\homography_matrix.npy')

# Global frame for threading
frame_global = None
detections_global = []
lock = Lock()

def update_display():
    #print("updating display")
    cv2.namedWindow("Detections", cv2.WINDOW_NORMAL)
    while True:
        if frame_global is not None:
            lock.acquire()
            frame = frame_global.copy()
            frame = cv2.warpPerspective(frame, H_matrix, frame.shape[:2],flags=cv2.INTER_LINEAR)
            for det in detections_global:
                cv2.rectangle(frame, (det['x1'], det['y1']), (det['x2'], det['y2']), (0, 255, 0), 2)
                cv2.putText(frame, f"{det['objectName']} {det['confidence']:.2f}", (det['x1'], det['y1'] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                center = tuple(int(c) for c in det['center'])  # Convert to tuple of integers if not already
                cv2.circle(frame, center, 5, (0, 0, 255), -1)
            lock.release()
            #print("showframe")
            #print(frame.shape[:2])
            cv2.imshow("Detections", frame)
        if cv2.waitKey(1) == 27:  # Exit on ESC
            break
    cv2.destroyAllWindows()

@app.route('/detect', methods=['GET'])
def handle_detection_request(): 
    global frame_global, detections_global
    ret, frame = read_frame()
    if not ret:
        return jsonify({"error": "Failed to capture frame"}), 400
    print("Framecaptured")
    # Continue with detection if frame capture was successful
    detections = detect_objects(model, frame)
    formatted_detections = format_detections(detections)
    _, transformed_detections = apply_homography(H_matrix, detections=formatted_detections)
    
    lock.acquire()
    frame_global = frame.copy()
    detections_global = transformed_detections.copy()
    lock.release()

    return jsonify(transformed_detections)


@app.route('/listen', methods=['POST', 'GET'])
def handle_listen():
    print("Recording audio")
    audio_format = pyaudio.paInt16  # 16-bit resolution
    num_channels = 1  # mono
    sample_rate = 44100  # 44.1 kHz
    chunk_size = 220500  # Larger buffer size
    record_seconds = 5  # Duration of recording

    audio = pyaudio.PyAudio()
    stream = audio.open(format=audio_format, channels=num_channels, rate=sample_rate, input=True, frames_per_buffer=chunk_size)
    frames = []

    try:
        for i in range(0, int(sample_rate / chunk_size * record_seconds)):
            data = stream.read(chunk_size)
            frames.append(data)
    except IOError as e:
        print("Error recording audio: ", e)
    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()
    
    print("Audio recorded")
    # Save the recorded audio to a WAV file
    temp_audio_file = 'data\\temp_audio.wav'
    wf = wave.open(temp_audio_file, 'wb')
    wf.setnchannels(num_channels)
    wf.setsampwidth(audio.get_sample_size(audio_format))
    wf.setframerate(sample_rate)
    wf.writeframes(b''.join(frames))
    wf.close()

    # Send audio to Google Speech-to-Text
    with open(temp_audio_file, 'rb') as audio_file:
        audio_content = audio_file.read()
    
    audio = speech.RecognitionAudio(content=audio_content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=44100,
        language_code="es-ES"
    )

    response = client.recognize(config=config, audio=audio)

    # Extract transcript
    transcript = [result.alternatives[0].transcript for result in response.results]
    print(f"transcribed {transcript}")
    return jsonify({"Transcript": transcript})
import sqlite3
from flask import Flask, request, jsonify


@app.route('/log', methods=['POST'])
def log_interaction():
    if not request.is_json:
        print("Error: The request content type is not JSON")
        return jsonify({'error': 'Request must be JSON'}), 400

    data = request.get_json()
    user_id = data.get('userid')
    english_word = data.get('word')
    correct = data.get('correct')

    if user_id is None or english_word is None or correct is None:
        print(f"Error: Missing data - User ID: {user_id}, Word: {english_word}, Correct: {correct}")
        return jsonify({'error': 'Missing data'}), 400

    try:
        conn = sqlite3.connect('flask-app\data\data.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Interactions (user_id, english_word, correct)
            VALUES (?, ?, ?)
        ''', (user_id, english_word, correct))
        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        conn.close()
        print(f"SQLite Error: {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        if conn:
            conn.close()

    print("Interaction logged successfully")
    return jsonify({'message': 'Interaction logged successfully'}), 200

# FRONTEND SEPERATION
app.secret_key = 'isaslowkeybadatthis'

@app.route('/')
def home():
    return render_template('homepage.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

def get_db_connection():
    conn = sqlite3.connect('flask-app\data\data.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM Users WHERE username = ?', (username,)).fetchone()
        conn.close()
        if user is not None and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            return redirect(url_for('dashboard'))
        return render_template('login.html', error='Invalid username or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        conn = get_db_connection()
        conn.execute('INSERT INTO Users (username, password) VALUES (?, ?)', (username, hashed_password))
        conn.commit()
        conn.close()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    display_thread = Thread(target=update_display)
    display_thread.start()
    print("started display thread")
    app.run(debug=True, use_reloader=False)
