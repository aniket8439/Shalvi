import os
from flask import Flask, request, jsonify, send_file, render_template
from flask_cors import CORS
from dotenv import load_dotenv
from shalvi_engine import ShalviEngine

load_dotenv()

app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = os.getenv('SECRET_KEY', 'shalvi-secret-key')
CORS(app)

shalvi = ShalviEngine()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/deepgram-key')
def deepgram_key():
    key = os.getenv('DEEPGRAM_API_KEY', '')
    if not key:
        return jsonify({'error': 'Deepgram API key not configured'}), 409
    return jsonify({'key': key})


@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message', '').strip()
    if not user_message:
        return jsonify({'error': 'Empty message'}), 400

    reply = shalvi.chat(user_message)

    # Generate audio
    try:
        audio_path = shalvi.tts_sync(reply)
    except Exception:
        audio_path = None

    return jsonify({
        'reply': reply,
        'has_audio': audio_path is not None,
        'audio_url': f'/api/audio?path={audio_path}' if audio_path else None,
    })


@app.route('/api/audio')
def serve_audio():
    path = request.args.get('path')
    if path and os.path.exists(path):
        return send_file(path, mimetype='audio/mpeg')
    return jsonify({'error': 'Audio not found'}), 404


@app.route('/api/clear', methods=['POST'])
def clear():
    shalvi.clear_history()
    return jsonify({'status': 'ok'})


if __name__ == "__main__":
    print('\n✨ SHALVI is online. Open http://localhost:5001\n')
    app.run(debug=True, host='127.0.0.1', port=5001)
