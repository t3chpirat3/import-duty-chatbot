import pandas as pd
import spacy
from fuzzywuzzy import process  # For spell-check

# Load NLP model
nlp = spacy.load("en_core_web_sm")

# Load Data
file_path = "C:/Users/Shad/Documents/Ores.csv"
df = pd.read_csv(file_path)

# Function to extract product name from sentence
def extract_product_name(sentence):
    doc = nlp(sentence)
    keywords = [token.text for token in doc if token.pos_ in ["NOUN", "PROPN"]]
    return " ".join(keywords) if keywords else sentence

# Function to check duties
def get_import_duty(query):
    # Extract key terms
    query = extract_product_name(query)
    
    # Use fuzzy matching to find the closest match in "description"
    choices = df["description"].tolist()
    best_match, score = process.extractOne(query, choices)

    # If match confidence is high, use it
    if score > 75:
        match = df[df["description"] == best_match].iloc[0]
        return f"\n✅ Product: {match['description']}\n📌 HS Code: {match['hs code']}\n💰 Tariff Rate: {match['tariff rate']}\n"
    
    # If no confident match, suggest similar products
    suggestions = df[df["description"].str.contains(query[:4], case=False, na=False)]
    if not suggestions.empty:
        suggestion_list = "\n🔹 ".join(suggestions["description"].head(3))
        return f"\n❌ No exact match found. Did you mean:\n🔹 {suggestion_list}"
    
    return "❌ No matching product found."

# Continuous interaction loop
while True:
    query = input("\n💬 Ask your question (or type 'exit' to quit): ")
    
    if query.lower() == "exit":
        print("\n👋 Goodbye! Have a great day.")
        break
    
    response = get_import_duty(query)
    print(response)
