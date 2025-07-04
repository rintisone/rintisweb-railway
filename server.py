from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from openai import OpenAI
import os

app = Flask(__name__)
CORS(app)

# Gunakan environment variable untuk API key agar lebih aman di production
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENAI_API_KEY
)

@app.route("/")
def homepage():
    return render_template("main.html")

@app.route("/ai-assistant")
def ai_assistant():
    return render_template("ai-assistant.html")

INSTRUCTIONS = """
nama kamu rintis,Kamu adalah asisten virtual yang ramah, responsif, dan solutif, siap membantu pelanggan RintisOne dalam memahami layanan, menyelesaikan kendala teknis, menjawab pertanyaan umum, 
serta memberikan panduan penggunaan platform.

RintisOne adalah inisiatif kolaboratif mahasiswa dari berbagai universitas di Pulau Jawa yang bertujuan menjembatani perusahaan dengan ekosistem kampus. Kami memadukan riset lapangan, edukasi komunitas, dan teknologi seperti AI & Blockchain untuk menghasilkan strategi ekspansi yang akurat, transparan, dan berkelanjutan.
Dengan tim yang tersebar di berbagai kota dan pendekatan berbasis data nyata, RintisOne hadir sebagai mitra pertumbuhan bisnis yang siap beradaptasi dengan perubahan zaman.

Daftar member RintisOne:
- Pandu Bagus Witjaksono Athallah (Founder), student at Universitas Padjajaran
- Sabdo Dwiyantoro Aji, student at Universitas Brawijaya
- Fawwaz Absyar Rifai, student at Universitas Sebelas Maret
- Sultan Alexander Muhammad Rasyid, student at Institut Pertanian Bogor
- Fadhli Luthfanhadi, student at Universitas Diponegoro
- Lalu Muhammad Zidan Alfinly, student at Universitas Indonesia
- Silvan Nando Himawan, student at Universitas Pembangunan Nasional "Veteran" Yogyakarta
"""

def complete_with_gpt(prompt):
    # Menggunakan endpoint completions (bukan chat)
    response = client.completions.create(
        model="deepseek-r1-0528-qwen3-8b:free",
        prompt=f"{INSTRUCTIONS}\nUser: {prompt}\nAI:",
        max_tokens=512,
        temperature=0.7,
        stop=["User:", "AI:"]
    )
    return response.choices[0].text.strip()

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        prompt = data.get("prompt", "")

        if not prompt:
            return jsonify({"error": "No prompt provided"}), 400

        response = complete_with_gpt(prompt)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Tidak perlu app.run() di bawah ini untuk production.
# Gunicorn akan menjalankan 'server:app' secara otomatis di
