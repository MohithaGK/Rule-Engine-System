# Rule-Engine-System

This Rule Engine Application allows users to create, combine, and evaluate rules based on various attributes. The application features a web-based interface built with HTML, CSS, and JavaScript, and a backend developed using Flask, Python, and SQLite for data storage.

## Table of Contents
1.Features

2.Technologies Used

3.Prerequisites

4.Usage

5.Architecture

6.Overview/Process

## Features

1.Create Rules: Users can input rules in a specific format, which are then parsed into an Abstract Syntax Tree (AST) for evaluation.

2.Combine Rules: Multiple rules can be combined using logical operators (AND/OR) to create more complex conditions.

3.Evaluate Rules: Users can evaluate rules against provided data to determine eligibility based on the defined conditions.

4.Persist Rules: Rules and their corresponding AST representations are stored in a SQLite database.

## Technologies Used

Frontend: HTML, CSS, JavaScript

Backend: Flask (Python)

Database: SQLite

Logging: Python Logging Module

### Prerequisites

- Python 3.x

- Flask

- SQLite
  
## Usage

1.Create Rule: Enter a rule string (e.g., age < 30) and click "Create Rule" to generate its AST representation.

2.Combine Rules: Enter multiple rules, each on a new line, select the combination type (AND/OR), and click "Combine Rules" to generate a combined AST.

3.Evaluate Rule: Provide JSON data (e.g., {"age": 25, "salary": 30000}) and enter the Rule ID to evaluate the rule against the data.

# Architecture

project/
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── script.js
├── templates/
│   └── index.html
└── main.py (Flask backend)

# Process

1.Installing Flask using PIP

2.Set Up the SQLite Database

3.Run the Flask Application using terminal/power shell

4.Connect to the Frontend: In your browser, navigate to the Flask application's home page by entering http://127.0.0.1:5000/. This will load the frontend interface where you can input rules.

5.Interact with the Application
  5.1-->In the frontend interface, input your logical rules using the provided text box.

  5.2-->Select the combination type (AND/OR) from the dropdown.

  5.3-->When you submit the rules, they will be processed by the Flask backend, which parses the rules into an Abstract Syntax Tree (AST).

6. Save Rules and AST to SQLite Database: When the rule is processed, the Flask application saves the original rule and the generated AST as JSON into the SQLite database. You can view the saved rules and their AST representations in the rules.db database using an SQLite viewer or command line.
