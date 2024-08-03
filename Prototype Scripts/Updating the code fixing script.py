import re
from pathlib import Path
import shutil

# Relative path
Input_Apex_path = Path("./file_Input_apex.cls")
Output_Apex_path = Path("./file_Output_apex.cls")
FieldsObj_Apex_path = Path("./file_FieldsObj_Apex.txt")

# specify the source file and destination file
source_file = './file_Input_apex.cls'
destination_file = './file_Output_apex.cls'

# use shutil to copy the file
shutil.copyfile(source_file, destination_file)


def fix_soql_query(query):
    if "Order By" in query or "ORDER BY" in query or "order by" in query:
        query = re.sub(r'(Order By|ORDER BY|order by)', r'WITH USER_MODE \1', query)
    elif "Limit" in query or "limit" in query or "LIMIT" in query:
        query = re.sub(r'(Limit|limit|LIMIT)', r'WITH USER_MODE \1', query)
    else:
        query = re.sub(r'(];)', r' WITH USER_MODE \1', query)
    return query


def fix_dml_operation(dml_operation, obj_instance):
    if dml_operation.lower() == "insert":
        return f"if(<Object_Name>.sObjectType.getdescribe().isCreateable()){{\n\t\t\t{dml_operation} {obj_instance};\n\t\t}}else{{\n\t\t\t{obj_instance}.adderror('You do not have permission to create a new Object_Name.');\n\t\t}}"
    elif dml_operation.lower() == "update":
        return f"if(<Object_Name>.sObjectType.getdescribe().isUpdateable()){{\n\t\t\t{dml_operation} {obj_instance};\n\t\t}}else{{\n\t\t\t{obj_instance}.adderror('You do not have permission to update the Object_Name.');\n\t\t}}"
    elif dml_operation.lower() == "upsert":
        return f"if(<Object_Name>.sObjectType.getdescribe().isCreateable() && Object_Name.sObjectType.getdescribe().isUpdateable()){{\n\t\t\t{dml_operation} {obj_instance};\n\t\t}}else{{\n\t\t\t{obj_instance}.adderror('You do not have permission to upsert the Object_Name.');\n\t\t}}"
    elif dml_operation.lower() == "delete":
        return f"if(<Object_Name>.sObjectType.getdescribe().isDeleteable()){{\n\t\t\t{dml_operation} {obj_instance};\n\t\t}}else{{\n\t\t\t{obj_instance}.adderror('You do not have permission to delete the Object_Name.');\n\t\t}}"


def comment_out_debugs(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    with open(file_path, 'w') as file:
        for line in lines:
            if re.search(r'\bSystem\.debug\b', line, re.IGNORECASE):
                line = '//' + line
            file.write(line)


def extract_soql_queries(file_path):
    with open(file_path, 'r') as file:
        apex_code = file.read()
        pattern = re.compile(r'Select\s(.*?)\sFrom\s(.*?)(\s*?Where\s.*?)?;', re.IGNORECASE | re.DOTALL)
        queries = []
        stack = [apex_code]
        while stack:
            current_code = stack.pop()
            for match in pattern.finditer(current_code):
                fields = match.group(1)
                obj = match.group(2)
                queries.append({'fields': fields.strip().split(','), 'object': obj.strip()})
                nested_code = match.group(0).split('SELECT', 1)[-1].rsplit('FROM', 1)[0]
                stack.append(nested_code.strip())
        with open(FieldsObj_Apex_path, 'w') as file:
            for query in queries:
                query['fields'] = [field.replace("SELECT", "") for field in query['fields']]
                file.write(f"{query}\n")


def set_sharing_option(file_path, sharing_option):
    if sharing_option not in ['with', 'without', 'inherited']:
        print("Invalid sharing option. Please choose 'with', 'without', or 'inherited'.")
        return

    with open(file_path, 'r') as file:
        lines = file.readlines()

    for i, line in enumerate(lines):
        if line.strip().lower().startswith('public class'):
            lines[i] = lines[i].replace('public class', f'public {sharing_option} sharing class')
            break
        elif line.strip().lower().startswith('private class'):
            lines[i] = lines[i].replace('private class', f'private {sharing_option} sharing class')
            break

    with open(file_path, 'w') as file:
        file.writelines(lines)
    
    print(f"\nSharing option set to {sharing_option} Sharing for this class.")


def clear_file_content(file_path):
    with open(file_path, 'w') as file:
        file.write('')


def main():
    while True:
        print("\n\n---------------------------")
        print("Select an option:")
        print("---------------------------")
        print("1. Extract SOQL queries")
        print("2. Fix SOQL queries")
        print("3. Fix DML operations")
        print("4. Comment out debugs")
        print("5. Enforce Sharing Rules Setting")
        print("6. Clear All Files & Start Fresh")
        print("0. Exit")

        option = input("Enter option number: ")

        if option == "1":
            extract_soql_queries(Input_Apex_path)
            print("\nOutput: ")
            print("Fields & Obj Information of SOQL Queries stored in File")
        elif option == "2":
            with open(Output_Apex_path, 'r') as file:
                apex_code = file.read()
            pattern = re.compile(r'Select\s(.*?)\sFrom\s(.*?)(\s*?Where\s.*?)?;', re.IGNORECASE | re.DOTALL)
            queries = []
            stack = [apex_code]
            while stack:
                current_code = stack.pop()
                for match in pattern.finditer(current_code):
                    fields = match.group(1)
                    obj = match.group(2)
                    query = match.group(0)
                    query = fix_soql_query(query)
                    nested_code = match.group(0).split('SELECT', 1)[-1].rsplit('FROM', 1)[0]
                    stack.append(nested_code.strip())
                    apex_code = apex_code.replace(match.group(0), query)
                    with open(Output_Apex_path, 'w') as file:
                        file.write(apex_code)
            print("\nOutput: ")
            print("SOQL Queries Fixed as per Codescan Rule")
            print("Used WITH USER_MODE at the end of soql query but before ORDER BY or LIMIT")
        elif option == "3":
            with open(Output_Apex_path, 'r') as file:
                apex_code = file.read()
            pattern = re.compile(r'\b(Insert|Update|Upsert|Delete)\b\s(.*?);', re.IGNORECASE | re.DOTALL)
            stack = [apex_code]
            while stack:
                current_code = stack.pop()
                for match in pattern.finditer(current_code):
                    dml_operation = match.group(1)
                    obj_instance = match.group(2)
                    query = match.group(0)
                    query = fix_dml_operation(dml_operation, obj_instance)
                    apex_code = apex_code.replace(match.group(0), query)
                    with open(Output_Apex_path, 'w') as file:
                        file.write(apex_code)
            print("\nOutput: ")
            print("DML Operations Fixed as per Codescan Rule")
            print("Checked for CRUD Permission before DML Operations")
        elif option == "4":
            comment_out_debugs(Output_Apex_path)
            print("\nOutput: ")
            print("Debugs Commented Out")
        elif option == "5":
            print("-*-*-*-*-*-*-\nSelect Sharing Option: ")
            print("1. With Sharing\n2. Without Sharing\n3. Inherited Sharing\n0. Back")
            sharing_option = input("Enter option number: ")
            if sharing_option == "1":
                set_sharing_option(Output_Apex_path, 'with')
            elif sharing_option == "2":
                set_sharing_option(Output_Apex_path, 'without')
            elif sharing_option == "3":
                set_sharing_option(Output_Apex_path, 'inherited')
            elif sharing_option == "0":
                continue
            else:
                print("Invalid option. Please try again.")
                continue
            print("\nOutput: ")
            print("Enforced Sharing Rules Setting Successfully")
        elif option == "6":
            clear_file_content(Input_Apex_path)
            clear_file_content(Output_Apex_path)
            clear_file_content(FieldsObj_Apex_path)
            print("\nOutput: ")
            print("All Files Cleared & Start Fresh")
        elif option == "0":
            break
        else:
            print("\nInvalid option. Please try again.")


if __name__ == "__main__":
    main()
