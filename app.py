from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
CORS(app)

# Load your CSV
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
        print(f"\n[Prompt received]: {prompt}")  # Print prompt in terminal

        # Check if a Pokémon from CSV is mentioned in the prompt
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
            Sp. Atk: {matched_pokemon['Sp. Atk']}
            Sp. Def: {matched_pokemon['Sp. Def']}
            Speed: {matched_pokemon['Speed']}
            Generation: {matched_pokemon['Generation']}
            Legendary: {matched_pokemon['Legendary']}
            """

        full_prompt = f"""
        You are a Pokémon expert. Talk about Pokémon in an engaging way. You have to mention Pokémon no matter what. 
        Use the following data as reference if helpful, but you can also add general Pokémon knowledge:
        {context}
        
        Question: {prompt}
        """

        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": full_prompt}]
        )
        answer = response.choices[0].message.content

        print(f"[OpenAI answer]: {answer}\n")
        return jsonify({"answer": answer})
    except Exception as e:
        print(f"[Error]: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # Render's dynamic PORT environment variable
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
