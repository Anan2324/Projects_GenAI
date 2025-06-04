from flask import Flask, render_template, request, jsonify
import os
from vertexai.preview.generative_models import GenerativeModel
from dotenv import load_dotenv
import vertexai

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Load from .env
project_id = os.getenv("project_id")
region = os.getenv("region")

# Check if keys exist
if not project_id or not region:
    raise ValueError("❌ project_id or region not set in .env")

# Initialize VertexAI
vertexai.init(project=project_id, location=region)

# Load model
model = GenerativeModel("gemini-1.0-pro")

# Homepage route
@app.route("/")
def home():
    return render_template("index.html")

# Chat endpoint
@app.route('/gemini', methods=['POST'])
def vertex_ai():
    try:
        user_input = request.form.get('user_input')
        print("📨 Input:", user_input)

        if not user_input:
            return jsonify(content="⚠️ Please enter a prompt.")

        responses = model.generate_content(user_input, stream=True)

        # Extract streamed output
        res = [r.candidates[0].content.parts[0].text for r in responses]
        final_res = "".join(res)

        print("✅ Response:", final_res)
        return jsonify(content=final_res)

    except Exception as e:
        print("❌ Error in backend:", e)
        return jsonify(content=f"❌ Error: {str(e)}")

# Run app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)

