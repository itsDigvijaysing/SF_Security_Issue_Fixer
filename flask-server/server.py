from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/submit-code', methods=['POST'])
def submit_code():
    data = request.get_json()
    code = data.get('code')
    if not code:
        return jsonify({'error': 'No code provided'}), 400

    try:
        with open('submitted_code.txt', 'w') as file:
            print('Code Received')
            file.write(code)
        return jsonify({'message': 'Code submitted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/output-file', methods=['GET'])
def get_output_file():
    print('Output File Requested')
    return send_file('output_code.txt', as_attachment=False)

if __name__ == '__main__':
    app.run(debug=True)