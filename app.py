from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import openai
import os
import base64  # <--- 1. Import base64
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
CORS(app, origins=["https://salvador-pokedex.vercel.app"])
# CORS(app)

df = pd.read_csv("pokedex.csv")

@app.route("/")
def home():
    return "Flask is working!"

@app.route("/pokemon/<name>")
def get_pokemon(name):
    pokemon = df[df["Name"].str.lower() == name.lower()]
    if pokemon.empty:
        return jsonify({"error": "Pokemon not found"}), 404
    return jsonify(pokemon.iloc[0].to_dict())

@app.route("/ask", methods=["POST"])
def ask_openai():
    data = request.get_json()
    prompt = data.get("prompt", "")
    
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400

    try:
        print(f"\n[Prompt received]: {prompt}")

        # --- CSV Context Logic (Same as before) ---
        matched_pokemon = None
        for name in df["Name"]:
            if name.lower() in prompt.lower():
                matched_pokemon = df[df["Name"].str.lower() == name.lower()].iloc[0]
                break

        context = ""
        if matched_pokemon is not None:
            context = f"""
            Here is some information about {matched_pokemon['Name']} from the CSV:
            Type 1: {matched_pokemon['Type 1']}
            Type 2: {matched_pokemon['Type 2']}
            Total: {matched_pokemon['Total']}
            HP: {matched_pokemon['HP']}
            Attack: {matched_pokemon['Attack']}
            Defense: {matched_pokemon['Defense']}
            Speed: {matched_pokemon['Speed']}
            Legendary: {matched_pokemon['Legendary']}
            """

        full_prompt = f"""
        You are a Pokédex. Talk about Pokémon in an engaging, encyclopedic way. 
        Try not to give a response that is longer than 5 sentences. 
        Use the following data as reference if helpful:
        {context}
        
        Question: {prompt}
        """

        # 1. Generate Text Response
        response = openai.chat.completions.create(
            model="gpt-4o-mini", 
            messages=[{"role": "user", "content": full_prompt}]
        )
        answer = response.choices[0].message.content
        print(f"[OpenAI answer]: {answer}\n")

        # 2. Generate Audio Response (TTS)
        speech_response = openai.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=answer
        )

        # 3. Convert Audio to Base64 to send over JSON
        # speech_response.content contains the binary audio data
        audio_base64 = base64.b64encode(speech_response.content).decode('utf-8')

        return jsonify({
            "answer": answer,
            "audio": audio_base64  # <--- Sending the audio data
        })

    except Exception as e:
        print(f"[Error]: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)