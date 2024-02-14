import re #Regular Expression

def extract_soql_queries(apex_code):
    pattern = re.compile(r'Select\s.*?\sFrom\s.*?(\s*?Where\s.*?)?;', re.IGNORECASE | re.DOTALL)
    queries = []
    stack = [apex_code]
    while stack:
        current_code = stack.pop()
        for match in pattern.finditer(current_code):
            query = match.group(0)
            queries.append(query)
            nested_code = query.split('SELECT', 1)[-1].rsplit('FROM', 1)[0]
            stack.append(nested_code.strip())
    return queries

# Example usage
apex_code = """
Account[] accounts = [SELECT Id, Name FROM Account WHERE CreatedDate = TODAY];
Contact[] contacts = [SELECT Id, Name FROM Contact 
                      WHERE AccountId IN :accountIds];
asdvasdg
Account[] accounts = [SELECT Id, Name, (SELECT Id, Name FROM Contacts) FROM Account WHERE CreatedDate = TODAY];
"""
soql_queries = extract_soql_queries(apex_code)
for query in soql_queries:
    print(query)
