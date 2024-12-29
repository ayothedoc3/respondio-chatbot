import google.generativeai as genai
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Configure Gemini
genai.configure(api_key="AIzaSyCqRCLlOZIEbh6rmkTdrpzJNjyc6ub7Abk")
model = genai.GenerativeModel("gemini-pro")

# Function to detect language and translate
def detect_and_translate(text, target_language):
    prompt = f"Detect the language of the following text and translate it into {target_language}: '{text}'"
    response = model.generate_content(prompt)
    return response.text

# Function to query knowledge base
def query_knowledge_base(query):
    prompt = f"Answer the following question based on the knowledge base: '{query}'"
    response = model.generate_content(prompt)
    return response.text

# Endpoint to process messages
@app.route("/process-message", methods=["POST"])
def process_message():
    data = request.json
    contact_id = data.get("contact_id")
    message = data.get("message")

    # Step 1: Detect language and translate query
    translated_query = detect_and_translate(message, "en")

    # Step 2: Query knowledge base
    knowledge_base_response = query_knowledge_base(translated_query)

    # Step 3: Translate response back to user's language
    translated_response = detect_and_translate(knowledge_base_response, "es")

    # Step 4: Send response back to Respond.io
    send_response(contact_id, translated_response)

    return jsonify({"status": "success"})

# Function to send response to Respond.io
def send_response(contact_id, message):
    url = "https://api.respond.io/v2/message"
    headers = {
        "Authorization": f"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MTA2ODIsInNwYWNlSWQiOjE5MDk4Nywib3JnSWQiOjE5MTIwNiwidHlwZSI6ImFwaSIsImlhdCI6MTczNTQyMTQ0OX0.cy4BvU8auA3_FnFkFsh3OpeI5VteSyvqQ1IyKvXyBZs",
        "Content-Type": "application/json",
    }
    payload = {
        "contact_id": contact_id,
        "message": message,
    }
    requests.post(url, json=payload, headers=headers)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)