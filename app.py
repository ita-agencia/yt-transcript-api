from flask import Flask, request, send_file, jsonify
import subprocess
import os

app = Flask(__name__)

@app.route("/audio")
def download_audio():
    video_id = request.args.get("video_id")
    if not video_id:
        return jsonify({"error": "Missing video_id"}), 400

    url = f"https://www.youtube.com/watch?v={video_id}"
    output_path = f"/tmp/{video_id}.mp3"

    # Se o arquivo já existe, não baixa novamente
    if not os.path.exists(output_path):
        try:
            # Baixa apenas o áudio em MP3
           result = subprocess.run(
    [
        "yt-dlp",
        "-f", "bestaudio",
        "--extract-audio",
        "--audio-format", "mp3",
        "-o", output_path,
        url
    ],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

if result.returncode != 0:
    return jsonify({
        "error": "Erro ao baixar áudio",
        "details": result.stderr.strip()
    }), 500

        except subprocess.CalledProcessError as e:
            return jsonify({"error": f"Erro ao baixar áudio: {str(e)}"}), 500

    # Retorna o arquivo de áudio como resposta
    try:
        return send_file(output_path, mimetype="audio/mpeg")
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
