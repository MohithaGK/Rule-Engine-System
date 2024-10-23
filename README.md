# Rule-Engine-System
This Rule Engine Application allows users to create, combine, and evaluate rules based on various attributes. The application features a web-based interface built with HTML, CSS, and JavaScript, and a backend developed using Flask, Python, and SQLite for data storage.

## Table of Contents
1.Features

2.Technologies Used

3.Prerequisites

4.Usage

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
