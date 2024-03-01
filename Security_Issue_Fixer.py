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

# Extracts SOQL queries from an Apex code file.
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
        return queries

soql_queries = extract_soql_queries(Input_Apex_path)

# open the file in write mode and write each item on a new line
with open(FieldsObj_Apex_path, 'w') as file:  # move file opening outside the loop
    for query in soql_queries:
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