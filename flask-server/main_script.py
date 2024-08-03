import re
from pathlib import Path
import shutil

# Function to copy file
def copy_file(source_file, destination_file):
    shutil.copyfile(source_file, destination_file)

# Function to fix SOQL queries
def soql_query_fixer(apex_code):
    print('Fixing SOQL queries')
    pattern = re.compile(r'Select\s(.*?)\sFrom\s(.*?)(\s*?Where\s.*?)?;', re.IGNORECASE | re.DOTALL)
    queries = []
    fixed_code = apex_code
    for match in pattern.finditer(apex_code):
        query = match.group(0)
        if "Order By" in query or "ORDER BY" in query or "order by" in query:
            query = re.sub(r'(Order By|ORDER BY|order by)', r'WITH USER_MODE \1', query)
        elif "Limit" in query or "limit" or "LIMIT" in query:
            query = re.sub(r'(Limit|limit|LIMIT)', r'WITH USER_MODE \1', query)
        else:
            query = re.sub(r'(];)', r' WITH USER_MODE \1', query)
        
        fixed_code = fixed_code.replace(match.group(0), query)
    return fixed_code

def submit_code():
    data = request.get_json()
    code = data.get('code')
    operations = data.get('checkboxes', {})
    shrType = data.get('selectedPicklist')
    
    if not code:
        return jsonify({'error': 'No code provided'}), 400

    try:
        fixed_code = process_code(code, operations, shrType)
        write_to_file('output_code.txt', fixed_code)
        return jsonify({'message': 'Code processed successfully'}), 200
    except Exception as e:
        logging.error(f"Error processing code: {e}")
        return jsonify({'error': str(e)}), 500

def process_code(code, operations, shrType):
    fixed_code = code
    if operations.get('fsoql'):
        fixed_code = main_script.soql_query_fixer(fixed_code)
    if operations.get('fdml'):
        fixed_code = main_script.dml_operation_fixer(fixed_code)
    if operations.get('fcmt'):
        fixed_code = main_script.comment_out_debugs(fixed_code)
    if operations.get('fshr') and shrType:
        fixed_code = main_script.set_sharing_option(fixed_code, shrType)
    return fixed_code

def write_to_file(filename, content):
    with open(filename, 'w') as file:
        file.write(content)

# Function to fix DML operations
def dml_operation_fixer(apex_code):
    print('Fixing DML operations')
    pattern = re.compile(r'\b(Insert|Update|Upsert|Delete)\b\s(.*?);', re.IGNORECASE | re.DOTALL)
    fixed_code = apex_code
    for match in pattern.finditer(apex_code):
        dml_operation = match.group(1)
        obj_instance = match.group(2)
        query = match.group(0)
        if dml_operation.lower() == "insert":
            query = f"if(<Object_Name>.sObjectType.getdescribe().isCreateable()){{\n\t\t\t{query}\n\t\t}}else{{\n\t\t\t{obj_instance}.adderror('You do not have permission to create a new Object_Name.');\n\t\t}}"
        elif dml_operation.lower() == "update":
            query = f"if(<Object_Name>.sObjectType.getdescribe().isUpdateable()){{\n\t\t\t{query}\n\t\t}}else{{\n\t\t\t{obj_instance}.adderror('You do not have permission to update the Object_Name.');\n\t\t}}"
        elif dml_operation.lower() == "upsert":
            query = f"if(<Object_Name>.sObjectType.getdescribe().isCreateable() && Object_Name.sObjectType.getdescribe().isUpdateable()){{\n\t\t\t{query}\n\t\t}}else{{\n\t\t\t{obj_instance}.adderror('You do not have permission to upsert the Object_Name.');\n\t\t}}"
        elif dml_operation.lower() == "delete":
            query = f"if(<Object_Name>.sObjectType.getdescribe().isDeleteable()){{\n\t\t\t{query}\n\t\t}}else{{\n\t\t\t{obj_instance}.adderror('You do not have permission to delete the Object_Name.');\n\t\t}}"
        
        fixed_code = fixed_code.replace(match.group(0), query)
    return fixed_code

# Function to comment out debug statements
def comment_out_debugs(apex_code):
    print('Commenting out debug statements')
    lines = apex_code.splitlines()
    fixed_code = '\n'.join(['//' + line if re.search(r'\bSystem\.debug\b', line, re.IGNORECASE) else line for line in lines])
    return fixed_code

# Function to set sharing option
def set_sharing_option(apex_code, sharing_option):
    print('Setting sharing option')
    if sharing_option not in ['with', 'without', 'inherited']:
        raise ValueError("Invalid sharing option. Please choose 'with', 'without', or 'inherited'.")
    lines = apex_code.splitlines()
    for i, line in enumerate(lines):
        if line.strip().lower().startswith('public class'):
            lines[i] = line.replace('public class', f'public {sharing_option} sharing class')
            break
        elif line.strip().lower().startswith('private class'):
            lines[i] = line.replace('private class', f'private {sharing_option} sharing class')
            break
    return '\n'.join(lines)

# Function to clear file content
def clear_file_content(file_path):
    with open(file_path, 'w') as file:
        file.write('')
