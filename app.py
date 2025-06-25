from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

@app.route("/transcript")
def transcript():
    video_id = request.args.get("video_id")
    lang = request.args.get("lang", "en")  # idioma opcional (default: inglês)

    if not video_id:
        return jsonify({"error": "Missing video_id"}), 400

    url = f"https://www.youtube.com/watch?v={video_id}"
    output_dir = "/tmp"
    output_path = os.path.join(output_dir, f"{video_id}.{lang}.vtt")
    output_template = os.path.join(output_dir, f"{video_id}.%(ext)s")

    try:
        # Executa yt-dlp para baixar legenda automática
        result = subprocess.run(
            [
                "yt-dlp",
                "--write-auto-sub",
                "--sub-lang", lang,
                "--skip-download",
                "-o", output_template,
                url
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False
        )

        if result.returncode != 0:
            return jsonify({
                "error": "Erro ao rodar yt-dlp",
                "details": result.stderr.strip()
            }), 500

        if not os.path.exists(output_path):
            return jsonify({"error": f"Legenda '{lang}' não encontrada para este vídeo."}), 404

        # Converte o arquivo .vtt para texto limpo
        lines = []
        with open(output_path, "r") as f:
            for line in f:
