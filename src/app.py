from flask import Flask, request, jsonify
import random
from flask import Flask, request, jsonify
from flask_cors import CORS  # Import the CORS extension




app = Flask(__name__)
CORS(app)  # Enable CORS for your Flask app
@app.route('/ask', methods=['POST'])
def ask_question():
    data = request.get_json()
    question = data.get('question')

    # Replace this with your logic to generate an answer based on the question.
    # For now, let's generate a random answer for demonstration purposes.
    possible_answers = ["Answer 1", "Answer 2", "Answer 3"]
    answer = random.choice(possible_answers)

    return jsonify({"response": answer})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
