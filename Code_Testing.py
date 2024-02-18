import re
from pathlib import Path


# Relative path
Input_Apex_path = Path("./Sample_apex.cls")
Output_Apex_path = Path("")

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

# Example usage
# apex_code = """
# 1.
# Account[] accounts = [SELECT Id, Name FROM Account WHERE CreatedDate = TODAY];

# 2.
# Contact[] contacts = [SELECT Id, Name FROM Contact 
#                       WHERE AccountId IN :accountIds];

# 3.
# public class AccountController {
#     public List<Account> getRecentAccounts() {
#         return [SELECT Id, Name, CreatedDate FROM Account ORDER BY CreatedDate DESC LIMIT 5];
#     }
# }

# 4.
# Account[] accounts = [SELECT Id, Name, (SELECT Id, Name FROM Contacts) FROM Account WHERE CreatedDate = TODAY];

# 5.
# Account[] accounts = [SELECT Id, Name, CreatedDate
#                         FROM Account
#                         ORDER BY CreatedDate DESC
#                         LIMIT 5];

# """
soql_queries = extract_soql_queries(Input_Apex_path)
for query in soql_queries:
    # print("Object:", query['object'])
    # print("Fields:", query['fields'])
    print(query)