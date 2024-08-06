import re
from pathlib import Path
import shutil

# Copy file content
def copy_file(source_file, destination_file):
    shutil.copyfile(source_file, destination_file)

# Fix SOQL queries
def soql_query_fixer(apex_code):
    print('Fixing SOQL queries')
    pattern = re.compile(r'Select\s(.*?)\sFrom\s(.*?)(\s*?Where\s.*?)?;', re.IGNORECASE | re.DOTALL)
    fixed_code = apex_code
    
    for match in pattern.finditer(apex_code):
        query = match.group(0)
        # Add 'WITH USER_MODE' to queries with ORDER BY or LIMIT
        if re.search(r'Order By|Limit', query, re.IGNORECASE):
            query = re.sub(r'(Order By|Limit)', r'WITH USER_MODE \1', query, flags=re.IGNORECASE)
        else:
            query = re.sub(r'(];)', r' WITH USER_MODE \1', query)
        
        fixed_code = fixed_code.replace(match.group(0), query)
    return fixed_code

# Write content to file
def write_to_file(filename, content):
    with open(filename, 'w') as file:
        file.write(content)

# Fix DML operations
def dml_operation_fixer(apex_code):
    print('Fixing DML operations')
    pattern = re.compile(r'\b(Insert|Update|Upsert|Delete)\b\s(.*?);', re.IGNORECASE | re.DOTALL)
    fixed_code = apex_code
    
    for match in pattern.finditer(apex_code):
        dml_operation = match.group(1).lower()
        obj_instance = match.group(2)
        query = match.group(0)
        
        # Add permission checks for DML operations
        if dml_operation == "insert":
            query = f"if(<Object_Name>.sObjectType.getDescribe().isCreateable()){{\n\t\t\t{query}\n\t\t}}else{{\n\t\t\t{obj_instance}.addError('No permission to create Object_Name.');\n\t\t}}"
        elif dml_operation == "update":
            query = f"if(<Object_Name>.sObjectType.getDescribe().isUpdateable()){{\n\t\t\t{query}\n\t\t}}else{{\n\t\t\t{obj_instance}.addError('No permission to update Object_Name.');\n\t\t}}"
        elif dml_operation == "upsert":
            query = f"if(<Object_Name>.sObjectType.getDescribe().isCreateable() && <Object_Name>.sObjectType.getDescribe().isUpdateable()){{\n\t\t\t{query}\n\t\t}}else{{\n\t\t\t{obj_instance}.addError('No permission to upsert Object_Name.');\n\t\t}}"
        elif dml_operation == "delete":
            query = f"if(<Object_Name>.sObjectType.getDescribe().isDeleteable()){{\n\t\t\t{query}\n\t\t}}else{{\n\t\t\t{obj_instance}.addError('No permission to delete Object_Name.');\n\t\t}}"
        
        fixed_code = fixed_code.replace(match.group(0), query)
    return fixed_code

# Comment out debug statements
def comment_out_debugs(apex_code):
    print('Commenting out debug statements')
    lines = apex_code.splitlines()
    fixed_code = '\n'.join(['//' + line if re.search(r'\bSystem\.debug\b', line, re.IGNORECASE) else line for line in lines])
    return fixed_code

# Set sharing option
def set_sharing_option(apex_code, sharing_option):
    print('Setting sharing option')
    if sharing_option not in ['with', 'without', 'inherited']:
        raise ValueError("Invalid sharing option.")
    
    lines = apex_code.splitlines()
    for i, line in enumerate(lines):
        if re.match(r'public class|private class', line, re.IGNORECASE):
            lines[i] = re.sub(r'(public|private) class', f'\\1 {sharing_option} sharing class', line, flags=re.IGNORECASE)
            break
    return '\n'.join(lines)

# Clear file content
def clear_file_content(file_path):
    with open(file_path, 'w') as file:
        file.write('')
