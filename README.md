# SF_Security_Issue_Fixer
Fixing Salesforce Code Scan Issues


## Basic Things to Know

```sql
pattern = re.compile(r'Select\s.*\sFrom\s.*\;', re.IGNORECASE | re.DOTALL)
```

This line of code defines a regular expression pattern using the `re.compile` function with two flags: `re.IGNORECASE` and `re.DOTALL`. Here's an explanation of each part:

- `re.compile`: This function is used to compile a regular expression pattern into a regex object, which can then be used for matching operations.
- `r'Select\s.*\sFrom\s.*\;'`: This is the regular expression pattern itself. It looks for a string that starts with "Select" (case-insensitive), followed by any whitespace character (`\s`), followed by any character zero or more times (`.*`), then followed by "From" (case-insensitive), again followed by any whitespace character and any character zero or more times, and finally ends with a semicolon (`\;`). This pattern is used to match SOQL queries.
- `re.IGNORECASE`: This flag makes the pattern match in a case-insensitive manner, so it will match "Select" and "FROM" regardless of the case.
- `re.DOTALL`: This flag makes the `.` in the pattern match any character, including newline (`\n`). Without this flag, `.` matches any character except newline. This is important for matching multi-line SOQL queries, as it allows the pattern to span multiple lines.

Putting it all together, this pattern with the specified flags is used to find SOQL queries in Apex code, including queries that span multiple lines.