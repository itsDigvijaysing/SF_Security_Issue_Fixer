import re
from pathlib import Path
import shutil

# Relative path
Input_Apex_path = Path("./file_Sample_apex.cls")
Output_Apex_path = Path("./file_Output_apex.cls")
FieldsObj_Apex_path = Path("./file_FieldsObj_Apex.txt")

# specify the source file and destination file
source_file = './file_Sample_apex.cls'
destination_file = './file_Output_apex.cls'

# use shutil to copy the file
shutil.copyfile(source_file, destination_file)

# Extracts SOQL queries from an Apex code file. & update the file line items while not replacing the original file.
# Add WITH USER_MODE at the end of soql query but before ORDER BY or LIMIT & also create new line above the soql query and add the comment with Comment as "SOQL Query Fixed as per Codescan Rule"
def soql_query_fixer(Output_Apex_path):
    with open(Output_Apex_path, 'r') as file:
        apex_code = file.read()
        pattern = re.compile(r'Select\s(.*?)\sFrom\s(.*?)(\s*?Where\s.*?)?;', re.IGNORECASE | re.DOTALL)
        queries = []
        stack = [apex_code]
        a=0
        while stack:
            a += 1
            current_code = stack.pop()
            for match in pattern.finditer(current_code):
                fields = match.group(1)
                obj = match.group(2)
                query = match.group(0)
                if "Order By" in query or "ORDER BY" in query or "order by" in query:
                    # print("Order By")
                    query = re.sub(r'(Order By|ORDER BY|order by)', r'WITH USER_MODE \1', query)
                    # print(query)
                    # query = f"// SOQL Query Fixed as per Codescan Rule\n{query}"
                elif "Limit" in query or "limit" in query or "LIMIT" in query:
                    # print("Limit")
                    query = re.sub(r'(Limit|limit|LIMIT)', r'WITH USER_MODE \1', query)
                    # query = f"// SOQL Query Fixed as per Codescan Rule\n{query}"
                    # print(query)
                else:
                    # print("Normal")
                    # query = f"// SOQL Query Fixed as per Codescan Rule\n{query}"
                    query = re.sub(r'(];)', r' WITH USER_MODE \1', query)
                    # print(query)
                
                nested_code = match.group(0).split('SELECT', 1)[-1].rsplit('FROM', 1)[0] # Extract the query & check for nested soql query good to have for future work
                stack.append(nested_code.strip())

                apex_code = apex_code.replace(match.group(0), query)
                with open(Output_Apex_path, 'w') as file:
                    file.write(apex_code)

# Finds DML operations in an Apex code file & replace it with Codescan Rule
def dml_operation_fixer(file_path):
    with open(file_path, 'r') as file:
        apex_code = file.read()
        pattern = re.compile(r'(Insert|Update|Upsert|Delete|Merge|Undelete)\s(.*?);', re.IGNORECASE | re.DOTALL)
        queries = []
        stack = [apex_code]
        index = 0
        while stack:
            index += 1
            current_code = stack.pop()
            for match in pattern.finditer(current_code):
                dml_operation = match.group(1)
                obj = match.group(2)
                query = match.group(0)
                query = f"// DML Operation Fixed as per Codescan Rule\n{query}"
                nested_code = match.group(0).split(dml_operation, 1)[-1].rsplit(obj, 1)[0]
                stack.append(nested_code.strip())
                apex_code = apex_code.replace(match.group(0), query)
                with open(file_path, 'w') as file:
                    file.write(apex_code)


def comment_out_debugs(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    with open(file_path, 'w') as file:
        for line in lines:
            if re.search(r'\bSystem\.debug\b', line, re.IGNORECASE):
                # print("In 1st Scenario ",line)
                line = '//' + line
            file.write(line)

# Mine: Object_Name.sObjectType.getdescribe().isCreateable()
# Colleague: sobject.getdescribe().object_name.iscreteable() (Maybe)


# if(Object_Name.sObjectType.getdescribe().isCreateable()){
#     # check the field
# }else{
#     variable_name.adderror('You do not have permission to create a new Object_Name.');
# }

# if(Object_Name.sObjectType.getdescribe().isUpdateable()){
#     # Update object
# }else{
#     variable_name.adderror('You do not have permission to update the Object_Name.');
# }

# if(Object_Name.sObjectType.getdescribe().isDeletable()){
#     # Delete object
# }else{
#     variable_name.adderror('You do not have permission to delete the Object_Name.');
# }

# Extracts SOQL queries from an Apex code file.
def extract_soql_queries(file_path):
    with open(file_path, 'r') as file:
        apex_code = file.read()
        pattern = re.compile(r'Select\s(.*?)\sFrom\s(.*?)(\s*?Where\s.*?)?;', re.IGNORECASE | re.DOTALL)
        queries = []
        stack = [apex_code]  # Complete code Present in stack
        index = 0
        while stack: # Loop through the stack
            index += 1
            current_code = stack.pop()
            for match in pattern.finditer(current_code):
                fields = match.group(1)
                obj = match.group(2)
                queries.append({'fields': fields.strip().split(','), 'object': obj.strip()})
                nested_code = match.group(0).split('SELECT', 1)[-1].rsplit('FROM', 1)[0]
                stack.append(nested_code.strip())
        return queries

soql_queries = extract_soql_queries(Input_Apex_path)
print("-------------------")
soql_query_fixer(Output_Apex_path)
print("-------")
comment_out_debugs(Output_Apex_path)

# open the file in write mode and write each item on a new line
with open(FieldsObj_Apex_path, 'w') as file:  # move file opening outside the loop
    for query in soql_queries:
        query['fields'] = [field.replace("SELECT", "") for field in query['fields']]
        # print("Fields:", query['fields'])
        # print("Object:", query['object'])
        print(query)
        file.write(f"{query}\n")
        
        # Created a condition so that Order by, Limit and other where clause condition present in query then it will remove the right side of query and write it to the file
        # if "Order By" in query['object'] or "ORDER BY" in query['object'] or "order by" in query['object']:
        #     query = query['object'].split("Order By")[0]
        #     print("Order By")
        #     print(query)
        #     file.write(f"{query}\n")
        # elif "Limit" in query['object'] or "limit" in query['object'] or "LIMIT" in query['object']:
        #     query = query['object'].split("Limit")[0]
        #     print("Limit")
        #     print(query)
        #     file.write(f"{query}\n")
        # else:
        #     print("Normal")
        #     print(query)
        #     file.write(f"{query}\n")