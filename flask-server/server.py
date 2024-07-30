from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import main_script
import os

app = Flask(__name__)
CORS(app)

@app.route('/submit-code', methods=['POST'])
def submit_code():
    data = request.get_json()
    # print(data)
    code = data.get('code')
    operations = data.get('checkboxes', {})
    shrType = data.get('selectedPicklist')
    print('Things :',operations)
    print('shrType :',shrType)
    
    if not code:
        return jsonify({'error': 'No code provided'}), 400

    try:
        fixed_code = code
        if operations.get('fsoql'):
            fixed_code = main_script.soql_query_fixer(fixed_code)
        if operations.get('fdml'):
            fixed_code = main_script.dml_operation_fixer(fixed_code)
        if operations.get('fcmt'):
            fixed_code = main_script.comment_out_debugs(fixed_code)
        if operations.get('fshr'):
            if shrType:
                fixed_code = main_script.set_sharing_option(fixed_code, shrType)

        with open('output_code.txt', 'w') as file:
            file.write(fixed_code)
        
        return jsonify({'message': 'Code processed successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/output-file', methods=['GET'])
def get_output_file():
    return send_file('output_code.txt', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
