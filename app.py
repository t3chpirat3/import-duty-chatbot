from flask import Flask, render_template, request, jsonify
import pandas as pd
import spacy
from fuzzywuzzy import process

app = Flask(__name__)

# Load NLP model
nlp = spacy.load("en_core_web_sm")

# Load Data
file_path = "C:/Users/Shad/Documents/Ores.csv"
df = pd.read_csv(file_path)

# Store user sessions (to maintain conversation context)
user_sessions = {}

def extract_product_name(sentence):
    doc = nlp(sentence)
    keywords = [token.text for token in doc if token.pos_ in ["NOUN", "PROPN"]]
    return " ".join(keywords) if keywords else sentence

def get_import_duty(user_id, query):
    query = extract_product_name(query)
    choices = df["description"].tolist()
    best_match, score = process.extractOne(query, choices)

    if score > 75:
        match = df[df["description"] == best_match].iloc[0]
        response = f"✅ {match['description']} (HS Code: {match['hs code']}) has a tariff rate of {match['tariff rate']}."
        user_sessions[user_id]["history"].append({"user": query, "bot": response})
        return {"response": response}
    
    suggestions = df[df["description"].str.contains(query[:4], case=False, na=False)]
    if not suggestions.empty:
        response = f"❌ No exact match found. Did you mean: {', '.join(suggestions['description'].head(3))}?"
        user_sessions[user_id]["history"].append({"user": query, "bot": response})
        return {"response": response}

    response = "❌ No matching product found. Can you provide more details?"
    user_sessions[user_id]["history"].append({"user": query, "bot": response})
    return {"response": response}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_id = data.get("user_id", "default_user")
    query = data.get("query", "")

    if user_id not in user_sessions:
        user_sessions[user_id] = {"history": []}

    response = get_import_duty(user_id, query)
    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)
