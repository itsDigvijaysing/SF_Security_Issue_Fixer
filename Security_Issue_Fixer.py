import re #Regular Expression

def extract_soql_queries(apex_code):
    pattern = re.compile(r'Select\s.*\sFrom\s.*\;', re.IGNORECASE | re.DOTALL)
    queries = pattern.findall(apex_code)
    return queries

# Example usage
apex_code = """
Account[] accounts = [SELECT Id, Name FROM Account WHERE CreatedDate = TODAY];
Contact[] contacts = [SELECT Id, Name FROM Contact 
                      WHERE AccountId IN :accountIds];
asdvasdg
"""
soql_queries = extract_soql_queries(apex_code)
for query in soql_queries:
    print(query)
