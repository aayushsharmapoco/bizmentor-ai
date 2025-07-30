import os
from flask import Flask, render_template, request
import cohere
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
co = cohere.Client(os.getenv("COHERE_API_KEY"))

@app.route("/", methods=["GET", "POST"])
def index():
    advice = ""
    if request.method == "POST":
        try:
            query = request.form["query"]
            response = co.generate(
                model='command-r-plus',  # ✅ Fixed model name
                prompt=f"Act like a smart business advisor for small Indian shopkeepers. Question: {query}",
                max_tokens=150,
                temperature=0.6
            )
            advice = response.generations[0].text.strip()
        except Exception as e:
            print("❌ Error during POST request:", e)
            advice = "Something went wrong while generating advice. Please try again."
    return render_template("index.html", advice=advice)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
 