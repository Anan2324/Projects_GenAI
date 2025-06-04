from flask import Flask, render_template, request, jsonify
import openai
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Load API key
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/gemini", methods=["POST"])  # we keep the same route
def chat():
    try:
        user_input = request.form.get("user_input")
        print("🧠 Prompt received:", user_input)

        if not user_input:
            return jsonify(content="⚠️ Please enter a valid prompt.")

        # Call ChatGPT API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or use "gpt-4" if your key supports it
            messages=[
                {"role": "user", "content": user_input}
            ]
        )

        reply = response["choices"][0]["message"]["content"]
        print("✅ Response:", reply)
        return jsonify(content=reply)

    except Exception as e:
        print("❌ Error:", e)
        return jsonify(content=f"❌ Error: {str(e)}")

if __name__ == "__main__":
    app.run(debug=True, port=8080)


