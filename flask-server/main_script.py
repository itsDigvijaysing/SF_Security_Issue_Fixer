import re
from pathlib import Path
import shutil

# Function to copy file
def copy_file(source_file, destination_file):
    """
    Copies the content of source_file to destination_file.
    """
    shutil.copyfile(source_file, destination_file)

# Function to fix SOQL queries
def soql_query_fixer(apex_code):
    """
    Fixes SOQL queries in the given Apex code to include 'WITH USER_MODE' if necessary.
    
    Parameters:
        apex_code (str): The Apex code containing SOQL queries.
    
    Returns:
        str: The Apex code with fixed SOQL queries.
    """
    print('Fixing SOQL queries')
    pattern = re.compile(r'Select\s(.*?)\sFrom\s(.*?)(\s*?Where\s.*?)?;', re.IGNORECASE | re.DOTALL)
    fixed_code = apex_code
    
    for match in pattern.finditer(apex_code):
        query = match.group(0)
        # Check for ORDER BY or LIMIT clauses and add 'WITH USER_MODE'
        if "Order By" in query or "ORDER BY" in query or "order by" in query:
            query = re.sub(r'(Order By|ORDER BY|order by)', r'WITH USER_MODE \1', query)
        elif "Limit" in query or "limit" or "LIMIT" in query:
            query = re.sub(r'(Limit|limit|LIMIT)', r'WITH USER_MODE \1', query)
        else:
            query = re.sub(r'(];)', r' WITH USER_MODE \1', query)
        
        fixed_code = fixed_code.replace(match.group(0), query)
    return fixed_code

def write_to_file(filename, content):
    """
    Writes the given content to a file.
    
    Parameters:
        filename (str): The name of the file to write to.
        content (str): The content to write to the file.
    """
    with open(filename, 'w') as file:
        file.write(content)

# Function to fix DML operations
def dml_operation_fixer(apex_code):
    """
    Adds permission checks to DML operations in the given Apex code.
    
    Parameters:
        apex_code (str): The Apex code containing DML operations.
    
    Returns:
        str: The Apex code with fixed DML operations.
    """
    print('Fixing DML operations')
    pattern = re.compile(r'\b(Insert|Update|Upsert|Delete)\b\s(.*?);', re.IGNORECASE | re.DOTALL)
    fixed_code = apex_code
    
    for match in pattern.finditer(apex_code):
        dml_operation = match.group(1).lower()
        obj_instance = match.group(2)
        query = match.group(0)
        
        # Adding permission checks based on the type of DML operation
        if dml_operation == "insert":
            query = f"if(<Object_Name>.sObjectType.getDescribe().isCreateable()){{\n\t\t\t{query}\n\t\t}}else{{\n\t\t\t{obj_instance}.addError('You do not have permission to create a new Object_Name.');\n\t\t}}"
        elif dml_operation == "update":
            query = f"if(<Object_Name>.sObjectType.getDescribe().isUpdateable()){{\n\t\t\t{query}\n\t\t}}else{{\n\t\t\t{obj_instance}.addError('You do not have permission to update the Object_Name.');\n\t\t}}"
        elif dml_operation == "upsert":
            query = f"if(<Object_Name>.sObjectType.getDescribe().isCreateable() && <Object_Name>.sObjectType.getDescribe().isUpdateable()){{\n\t\t\t{query}\n\t\t}}else{{\n\t\t\t{obj_instance}.addError('You do not have permission to upsert the Object_Name.');\n\t\t}}"
        elif dml_operation == "delete":
            query = f"if(<Object_Name>.sObjectType.getDescribe().isDeleteable()){{\n\t\t\t{query}\n\t\t}}else{{\n\t\t\t{obj_instance}.addError('You do not have permission to delete the Object_Name.');\n\t\t}}"
        
        fixed_code = fixed_code.replace(match.group(0), query)
    return fixed_code

# Function to comment out debug statements
def comment_out_debugs(apex_code):
    """
    Comments out System.debug statements in the given Apex code.
    
    Parameters:
        apex_code (str): The Apex code containing debug statements.
    
    Returns:
        str: The Apex code with debug statements commented out.
    """
    print('Commenting out debug statements')
    lines = apex_code.splitlines()
    fixed_code = '\n'.join(['//' + line if re.search(r'\bSystem\.debug\b', line, re.IGNORECASE) else line for line in lines])
    return fixed_code

# Function to set sharing option
def set_sharing_option(apex_code, sharing_option):
    """
    Sets the sharing option for the given Apex code.
    
    Parameters:
        apex_code (str): The Apex code.
        sharing_option (str): The sharing option to set ('with', 'without', or 'inherited').
    
    Returns:
        str: The Apex code with the sharing option set.
    """
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
    """
    Clears the content of the specified file.
    
    Parameters:
        file_path (str): The path to the file to clear.
    """
    with open(file_path, 'w') as file:
        file.write('')
