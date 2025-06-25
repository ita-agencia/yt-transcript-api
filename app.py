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
                if "-->" in line or line.strip() == "" or line.strip().isdigit():
                    continue
                lines.append(line.strip())

        transcript_text = " ".join(lines)
        return jsonify({
            "video_id": video_id,
            "lang": lang,
            "transcript": transcript_text
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
