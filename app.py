from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({'status': 'ok', 'message': 'API funcionando'})

@app.route('/transcript')
def transcript():
    video_id = request.args.get('video_id')

    if not video_id:
        return jsonify({'error': 'Parâmetro video_id é obrigatório'}), 400

    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['pt', 'en'])
        texto = ' '.join([item['text'] for item in transcript])
        return jsonify({'video_id': video_id, 'transcript': texto})
    
    except TranscriptsDisabled:
        return jsonify({'error': 'Transcrição desativada no vídeo'}), 403
    except NoTranscriptFound:
        return jsonify({'error': 'Nenhuma transcrição disponível'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
