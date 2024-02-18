import re

def add_user_mode_to_soql_queries(apex_code):
    pattern = re.compile(r'Select\s(.*?)\sFrom\s(.*?)(\s*?Where\s.*?)?;', re.IGNORECASE | re.DOTALL)
    modified_code = []
    stack = [apex_code]
    while stack:
        current_code = stack.pop()
        for match in pattern.finditer(current_code):
            fields = match.group(1)
            obj = match.group(2)
            modified_query = match.group(0).replace(']', ' WITH USER_MODE]')
            modified_code.append(current_code.replace(match.group(0), modified_query))
            nested_code = match.group(0).split('SELECT', 1)[-1].rsplit('FROM', 1)[0]
            stack.append(nested_code.strip())
    return modified_code

# Example usage
apex_code = """
Account[] accounts = [SELECT Id, Name, (SELECT Id, Name FROM Contacts) FROM Account WHERE CreatedDate = TODAY];
"""
modified_code = add_user_mode_to_soql_queries(apex_code)
for code in modified_code:
    print(code)


#import re

# def extract_soql_queries(apex_code):
#     pattern = re.compile(r'Select\s(.*?)\sFrom\s(.*?)(\s*?Where\s.*?)?;', re.IGNORECASE | re.DOTALL)
#     queries = []
#     stack = [apex_code]
#     while stack:
#         current_code = stack.pop()
#         for match in pattern.finditer(current_code):
#             fields = match.group(1)
#             obj = match.group(2)
#             queries.append({'fields': fields.strip().split(','), 'object': obj.strip()})
#             nested_code = match.group(0).split('SELECT', 1)[-1].rsplit('FROM', 1)[0]
#             stack.append(nested_code.strip())
#     return queries

# Example usage
# apex_code = """
# Account[] accounts = [SELECT Id, Name FROM Account WHERE CreatedDate = TODAY];
# Contact[] contacts = [SELECT Id, Name FROM Contact 
#                       WHERE AccountId IN :accountIds];
# asdvasdg
# Account[] accounts = [SELECT Id, Name, (SELECT Id, Name FROM Contacts) FROM Account WHERE CreatedDate = TODAY];
# """
# soql_queries = extract_soql_queries(apex_code)
# for query in soql_queries:
#     print("Object:", query['object'])
#     print("Fields:", query['fields'])
#     print()


# Create code to extract SOQL queries from Apex code
def extract_complete_soql_queries(apex_code):
    """
    Extracts complete SOQL queries from a given block of Apex code.

    Parameters:
    apex_code (str): A string containing Apex code.

    Returns:
    list: A list of complete SOQL query strings found within the Apex code.
    """
    pattern = re.compile(
        r'\[SELECT\s.*?\sFROM\s.*?(?:\sWHERE\s.*?|)\](?:\s*(?:AND|OR)\s*\[SELECT.*?\])*(?:;|\])',
        re.IGNORECASE | re.DOTALL
    )
    queries = pattern.findall(apex_code)
    return queries

# Example usage
complete_apex_code = """
Account[] accounts = [SELECT Id, Name FROM Account WHERE CreatedDate = TODAY];
Contact[] contacts = [SELECT Id, Name FROM Contact 
                      WHERE AccountId IN :accountIds];
Account[] moreAccounts = [SELECT Id, Name, (SELECT Id, Name FROM Contacts) FROM Account WHERE CreatedDate = LAST_WEEK];
"""
extracted_queries = extract_complete_soql_queries(complete_apex_code)
for query in extracted_queries:
    print(query)


# Create a code for fractions from 1 to 10
def create_fractions():
    """
    Creates a list of fractions from 1 to 10.
    """
    fractions = []
    for i in range(1, 11):
        fractions.append(f"{i}/10")
    return fractions