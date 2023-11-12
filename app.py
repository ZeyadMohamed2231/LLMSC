from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import pandas as pd
import xlwings as xl
import os

app = Flask(__name__)
CORS(app)

app.config['UPLOAD_FOLDER'] = './uploads'
app.config['ALLOWED_EXTENSIONS'] = {'xlsx'}  # Modified to accept CSV files

def df_from_excel(path):
    app = xl.App(visible=False)
    book = app.books.open(path)
    book.save()
    app.kill()
    return pd.read_excel(path)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/ask_about_spreadsheet', methods=['POST'])
def ask_about_spreadsheet():

    file = request.files['file']
    print("asd")
    if file and allowed_file(file.filename):
        questions = request.form.get('questions').split('\n')

        filename = 'tmp.csv'  # Modified to save as CSV
        file.save(filename)

        df = df_from_excel(filename)  # Modified to read CSV
        df = df.fillna(0)
        data_str = df.to_string()
        print(df)

        os.remove(filename)

        messages = [
            {
                "role": "user",
                "content": "Here's the content of the spreadsheet:\n" + data_str + "\n\nHere are some questions about the spreadsheet:\n" + "\n".join(questions),
            }
        ]

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=1000
        )
        print(completion)

        return jsonify({"response": completion['choices'][0]['message']['content']})
    else:
        return jsonify({"error": "Invalid file type."}), 400

if __name__ == '__main__':
    openai.api_key = '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'  # Reminder: use environment variables to keep your API key secure
    app.run(host='192.168.56.1', port=5000, debug=True)
