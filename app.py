
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import uuid
import whisper
import librosa
import numpy as np
from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip, ColorClip
from pydub import AudioSegment
from werkzeug.utils import secure_filename
import subprocess
import shutil

import soundfile as sf
print(sf.available_formats())



app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'
ALLOWED_EXTENSIONS = {'mp3', 'wav', 'mp4', 'm4a', 'ogg'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

whisper_model = whisper.load_model("medium")

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def isolate_vocals_demucs(input_path, output_folder):
    command = [
        'demucs',
        '--two-stems', 'vocals',
        '--out', output_folder,
        input_path
    ]

    result = subprocess.run(command, capture_output=True, text=True)

    if result.returncode != 0:
        raise Exception(f"Demucs error: {result.stderr}")

    file_stem = os.path.splitext(os.path.basename(input_path))[0]
    vocal_path = os.path.join(output_folder, 'htdemucs', file_stem, 'vocals.wav')

    if not os.path.exists(vocal_path):
        raise FileNotFoundError(f'Vocal file not found at {vocal_path}')

    return vocal_path

@app.route('/')
def index():
    return "LyricSync Backend Server with Demucs"

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_id = str(uuid.uuid4())
        file_extension = filename.rsplit('.', 1)[1].lower()
        new_filename = f"{file_id}.{file_extension}"
        file_path = os.path.join(UPLOAD_FOLDER, new_filename)
        
        file.save(file_path)
        
        try:
            if file_extension in ['mp3', 'wav', 'm4a', 'ogg']:
                audio = AudioSegment.from_file(file_path)
                duration = len(audio) / 1000.0
            else:
                video = VideoFileClip(file_path)
                duration = video.duration
                video.close()
        except Exception as e:
            return jsonify({'error': f'Error processing file: {str(e)}'}), 500
        
        return jsonify({
            'file_id': file_id,
            'filename': filename,
            'duration': duration,
            'message': 'File uploaded successfully'
        })
    
    return jsonify({'error': 'File type not allowed'}), 400

@app.route('/audio/<file_id>')
def serve_audio(file_id):
    for ext in ALLOWED_EXTENSIONS:
        file_path = os.path.join(UPLOAD_FOLDER, f"{file_id}.{ext}")
        if os.path.exists(file_path):
            return send_file(file_path)
    return jsonify({'error': 'File not found'}), 404

@app.route('/waveform/<file_id>', methods=['GET'])
def get_waveform(file_id):
    try:
        file_path = None
        for ext in ALLOWED_EXTENSIONS:
            potential_path = os.path.join(UPLOAD_FOLDER, f"{file_id}.{ext}")
            if os.path.exists(potential_path):
                file_path = potential_path
                break
        
        if not file_path:
            return jsonify({'error': 'File not found'}), 404
        
        y, sr = librosa.load(file_path, sr=22050)
        downsample_factor = len(y) // 1000
        y_downsampled = y[::downsample_factor] if downsample_factor > 1 else y
        waveform_data = (y_downsampled / np.max(np.abs(y_downsampled))).tolist()
        
        return jsonify({
            'waveform': waveform_data,
            'duration': len(y) / sr,
            'sample_rate': sr
        })
    
    except Exception as e:
        return jsonify({'error': f'Waveform generation failed: {str(e)}'}), 500

@app.route('/transcribe/<file_id>', methods=['POST'])
def transcribe_audio(file_id):
    try:
        print(f"[INFO] Iniciando transcrição para file_id: {file_id}")

        # Verificar se o arquivo existe
        file_path = None
        for ext in ALLOWED_EXTENSIONS:
            potential_path = os.path.join(UPLOAD_FOLDER, f"{file_id}.{ext}")
            if os.path.exists(potential_path):
                file_path = potential_path
                break
        
        if not file_path:
            print("[ERROR] Arquivo não encontrado.")
            return jsonify({'error': 'File not found'}), 404

        print(f"[INFO] Arquivo encontrado em: {file_path}")

        # Isolar voz
        print("[INFO] Iniciando Demucs...")
        vocal_path = isolate_vocals_demucs(file_path, OUTPUT_FOLDER)
        print(f"[INFO] Vocal isolado em: {vocal_path}")

        # Whisper transcrição
        print("[INFO] Rodando Whisper...")
        result = whisper_model.transcribe(vocal_path, word_timestamps=True)

        # Limpeza dos arquivos temporários
        folder = os.path.dirname(vocal_path)
        if os.path.exists(vocal_path):
            os.remove(vocal_path)
        if os.path.exists(folder):
            shutil.rmtree(folder)

        lyrics = []
        for segment in result['segments']:
            lyrics.append({
                'text': segment['text'].strip(),
                'start': segment['start'],
                'end': segment['end']
            })

        print("[INFO] Transcrição finalizada com sucesso.")

        return jsonify({
            'lyrics': lyrics,
            'language': result.get('language', 'unknown'),
            'message': 'Transcription completed successfully'
        })

    except Exception as e:
        print(f"[FATAL ERROR] {e}")
        return jsonify({'error': f'Transcription failed: {str(e)}'}), 500

@app.route('/export/srt', methods=['POST'])
def export_srt():
    try:
        data = request.json
        file_id = data.get('file_id')
        lyrics = data.get('lyrics', [])
        
        srt_content = ""
        for i, lyric in enumerate(lyrics, 1):
            start_time = format_srt_time(lyric['start'])
            end_time = format_srt_time(lyric['end'])
            srt_content += f"{i}\n{start_time} --> {end_time}\n{lyric['text']}\n\n"
        
        srt_filename = f"{file_id}_lyrics.srt"
        srt_path = os.path.join(OUTPUT_FOLDER, srt_filename)
        
        with open(srt_path, 'w', encoding='utf-8') as f:
            f.write(srt_content)
        
        return jsonify({
            'srt_url': f'/download/srt/{srt_filename}',
            'message': 'SRT file exported successfully'
        })
    
    except Exception as e:
        return jsonify({'error': f'SRT export failed: {str(e)}'}), 500

def format_srt_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millisecs = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millisecs:03d}"

@app.route('/download/video/<filename>')
def download_video(filename):
    try:
        file_path = os.path.join(OUTPUT_FOLDER, filename)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download/srt/<filename>')
def download_srt(filename):
    try:
        file_path = os.path.join(OUTPUT_FOLDER, filename)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
