# SF_Security_Issue_Fixer

The Salesforce Security Fixer project aims to enhance the security posture of Salesforce apex code by providing automated tools to fix common security issues and vulnerabilities. This project focuses on addressing various aspects of security, including SOQL query analysis, field-level security, CRUD level security, sharing settings, and debug statement cleanup.

## Functionality

`SOQL Query Analysis`: The project includes functionality to parse SOQL queries and identify all fields and objects referenced in them. This information is stored in a output file for further analysis and processing for User.

`Field-Level Security Fixing`: Using the USER_MODE, the project provides the ability to fix field-level security for SOQL operations. This ensures that only authorized users have access to sensitive fields in queries.

`CRUD Level Security Fixing`: Before performing DML operations, the project pre-checks the user's access permissions to ensure that only users with the necessary CRUD (Create, Read, Update, Delete) permissions can perform these operations.

`Sharing Settings`: Users can choose between With, Without, or Inherited sharing settings for components, allowing for granular control over record access.

`Debug Statement Cleanup`: The project includes functionality to automatically comment out all system.debug statements in the code, reducing log size and potential information disclosure.

`File Data Cleanup`: It simplely clears data of it's own file so that Project will stay working without any issue.

## Project Status

As a Developer of this project, I acknowledges that it may contain bugs. Updates and improvements will be considered when time permits, with a focus on improving functionality and reliability.

<!-- ## Functionality

1. Finding all Fields & Objects of SOQL Query & stored it in file.
2. Fixing Field Level Security of SOQL Operations by using USER_MODE.
3. Fixing CRUD Level Security of DML Operations by pre checking access.
4. Giving `With`/`Without`/`Inherited` Sharing to component as per User Choice.
5. Commenting all the system.debugs lines.
6. Clearning the Files/Cache data. -->

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
