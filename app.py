from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

@app.route("/transcript")
def transcript():
    video_id = request.args.get("video_id")
    if not video_id:
        return jsonify({"error": "Missing video_id"}), 400

    url = f"https://www.youtube.com/watch?v={video_id}"
    output_dir = "/tmp"
    output_path = os.path.join(output_dir, f"{video_id}.en.vtt")

    try:
        subprocess.run([
            "yt-dlp",
            "--write-auto-sub",
            "--sub-lang", "en",
            "--skip-download",
            "-o", os.path.join(output_dir, f"{video_id}.%(ext)s"),
            url
        ], check=True)

        if not os.path.exists(output_path):
            return jsonify({"error": "Legenda não encontrada"}), 404

        # Converte .vtt em texto limpo
        lines = []
        with open(output_path, "r") as f:
            for line in f:
                if "-->" in line or line.strip() == "" or line.strip().isdigit():
                    continue
                lines.append(line.strip())

        transcript_text = " ".join(lines)
        return jsonify({"video_id": video_id, "transcript": transcript_text})

    except subprocess.CalledProcessError as e:
        return jsonify({"error": f"Erro ao rodar yt-dlp: {e}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
