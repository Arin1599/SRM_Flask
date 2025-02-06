from flask import Flask, render_template,jsonify,request
from main import app as workflow_app  # Import your workflow

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    query = request.json.get('message')
    inputs = {"question": query}
    
    result = []
    for output in workflow_app.stream(inputs):
        for key, value in output.items():
            result.append(value)
    
    return jsonify({
        "response": result[-1]['headlines']
    })


if __name__ == '__main__':
    app.run(debug=True)