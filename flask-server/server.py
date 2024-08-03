from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import main_script
import os

app = Flask(__name__)
CORS(app)

@app.route('/submit-code', methods=['POST'])
def submit_code():
    """
    Endpoint to process submitted Apex code.
    The code is modified based on selected operations and sharing type.
    
    Returns:
        JSON response with a success message or an error message.
    """
    data = request.get_json()
    code = data.get('code')
    operations = data.get('checkboxes', {})
    shrType = data.get('selectedPicklist')

    # Check if code is provided
    if not code:
        return jsonify({'error': 'No code provided'}), 400

    try:
        fixed_code = code

        # Apply SOQL query fixes if selected
        if operations.get('fsoql'):
            fixed_code = main_script.soql_query_fixer(fixed_code)
        
        # Apply DML operation fixes if selected
        if operations.get('fdml'):
            fixed_code = main_script.dml_operation_fixer(fixed_code)
        
        # Comment out debug statements if selected
        if operations.get('fcmt'):
            fixed_code = main_script.comment_out_debugs(fixed_code)
        
        # Set sharing option if selected and sharing type is provided
        if operations.get('fshr') and shrType:
            fixed_code = main_script.set_sharing_option(fixed_code, shrType)

        # Write the modified code to an output file
        output_file_path = 'output_code.txt'
        with open(output_file_path, 'w') as file:
            file.write(fixed_code)
        
        return jsonify({'message': 'Code processed successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/output-file', methods=['GET'])
def get_output_file():
    """
    Endpoint to download the processed output file.
    
    Returns:
        The output file as an attachment.
    """
    output_file_path = 'output_code.txt'
    if os.path.exists(output_file_path):
        return send_file(output_file_path, as_attachment=True)
    else:
        return jsonify({'error': 'Output file not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
