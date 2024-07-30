# Salesforce Security Issues Fixer

The Salesforce Security Fixer project enhances Salesforce Apex code security by automating the resolution of common vulnerabilities. Utilizing a Flask server for backend processing and a React frontend for user interaction, the tool addresses critical security aspects such as SOQL query analysis, field-level security (FLS), CRUD level security, sharing settings, and debug statement cleanup. It modifies SOQL queries and DML operations to comply with best practices, configures class sharing settings, and comments out debug statements to protect sensitive information, providing a comprehensive solution for securing Salesforce code.

## Functionality

`SOQL Query Analysis`: The project includes functionality to parse SOQL queries and identify all fields and objects referenced in them. This information is stored in a output file for further analysis and processing for User.

`Field-Level Security Fixing`: Using the USER_MODE, the project provides the ability to fix field-level security for SOQL operations. This ensures that only authorized users have access to sensitive fields in queries.

`CRUD Level Security Fixing`: Before performing DML operations, the project pre-checks the user's access permissions to ensure that only users with the necessary CRUD (Create, Read, Update, Delete) permissions can perform these operations.

`Sharing Settings`: Users can choose between With, Without, or Inherited sharing settings for components, allowing for granular control over record access.

`Debug Statement Cleanup`: The project includes functionality to automatically comment out all system.debug statements in the code, reducing log size and potential information disclosure.

`File Data Cleanup`: It simplely clears data of it's own file so that Project will stay working without any issue.

<!-- ## Functionality

1. Finding all Fields & Objects of SOQL Query & stored it in file.
2. Fixing Field Level Security of SOQL Operations by using USER_MODE.
3. Fixing CRUD Level Security of DML Operations by pre checking access.
4. Giving `With`/`Without`/`Inherited` Sharing to component as per User Choice.
5. Commenting all the system.debugs lines.
6. Clearning the Files/Cache data. -->

---

## Working Details:

**Enhancing Salesforce Security with a Flask and React Application**

In the world of Salesforce development, maintaining code security and compliance is paramount. The Salesforce Security Issue Fixer project is an innovative solution designed to address common security issues in Salesforce code through a web application powered by Flask and React.

**Backend: Flask Server**

At the core of this solution is a Flask server, which provides a robust backend for processing Salesforce code. The server exposes two main endpoints:

1. **/submit-code**: This endpoint accepts POST requests containing Salesforce code along with various operations selected by the user. The server processes the code based on the selected operations, which include fixing SOQL queries, adjusting DML operations, commenting out debug statements, and setting sharing options. It then writes the processed code to a file and returns a success message. If any errors occur during processing, the server responds with an error message.

2. **/output-file**: This endpoint allows users to download the processed code file. It serves the `output_code.txt` file created during the code submission process, enabling users to easily retrieve and review the modified code.

The `main_script` module contains functions to handle specific code fixes:

- **`soql_query_fixer`**: Adjusts SOQL queries to ensure they comply with best practices.
- **`dml_operation_fixer`**: Modifies DML operations to include appropriate permissions checks.
- **`comment_out_debugs`**: Comments out debug statements to enhance security.
- **`set_sharing_option`**: Configures sharing options for Salesforce classes based on user input.

**Frontend: React Application**

The React frontend provides an intuitive user interface for interacting with the Flask server. Users can input their Salesforce code, select the desired operations via checkboxes, and specify sharing options through a dropdown menu. The application manages state with React hooks and communicates with the Flask server using Axios for HTTP requests.

Key features of the React app include:

- **Code Input and Output Display**: Users can enter their code into a text area and view the processed output in real-time.
- **Checkboxes for Operations**: Users can select which operations to apply, including fixes for SOQL queries, DML operations, debug statements, and sharing options.
- **Dynamic Sharing Options**: A dropdown menu allows users to choose the sharing settings for their Salesforce classes.
- **File Download**: Once the code is processed, users can download the output file containing the modified code.

**Conclusion**

The Salesforce Security Issue Fixer project is a practical tool for developers seeking to enhance the security and compliance of their Salesforce code. By leveraging Flask for backend processing and React for a user-friendly frontend, this project offers a comprehensive solution for addressing common Salesforce security issues efficiently.

---

## Project Status

As a Developer of this project, I acknowledges that it may contain bugs. Updates and improvements will be considered when time permits, with a focus on improving functionality and reliability.

---

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
