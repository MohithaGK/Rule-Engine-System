// Function to create a rule
function createRule() {
    const ruleInput = document.getElementById('ruleInput').value.trim();
    document.getElementById('createRuleResult').innerText = ""; // Clear previous result

    if (!ruleInput) {
        alert("Please enter a valid rule.");
        return; // Exit if input is invalid
    }

    fetch('/create_rule', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ rule_string: ruleInput }),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok: ' + response.statusText);
        }
        return response.json();
    })
    .then(data => {
        // Ensure that data.message is present
        document.getElementById('createRuleResult').innerText = data.message || 'Rule created successfully.';
        console.log(data);
    })
    .catch((error) => {
        console.error('Error:', error);
        document.getElementById('createRuleResult').innerText = 'Error: ' + error.message; // Show error message to user
    });
}

// Function to combine rules
function combineRules() {
    const rulesInput = document.getElementById('combineRulesInput').value.split('\n').map(rule => rule.trim()).filter(rule => rule);
    const combinationType = document.getElementById('combination-type').value; // Get selected combination type
    document.getElementById('combineRulesResult').innerText = ""; // Clear previous result
    document.getElementById('combinedASTResult').innerText = ""; // Clear previous AST result

    // Ensure that at least one rule is provided
    if (rulesInput.length === 0) {
        document.getElementById('combineRulesResult').innerText = "Please enter at least one rule.";
        return;
    }

    // Log the rules input and combination type to the console for debugging
    console.log('Rules input:', rulesInput);
    console.log('Combination type:', combinationType);

    // Send the rules and combination type to the backend
    fetch('/combine_rules', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ rules: rulesInput, combination_type: combinationType }), // Include combination type
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok: ' + response.statusText);
        }
        return response.json(); // Parse the response as JSON
    })
    .then(data => {
        // Display the result message
        document.getElementById('combineRulesResult').innerText = data.message || 'Rules combined successfully!';

        // If AST is returned, display it
        if (data.ast) {
            document.getElementById('combinedASTResult').innerText = JSON.stringify(data.ast, null, 2);
        } else {
            document.getElementById('combinedASTResult').innerText = 'No AST returned.';
        }
    })
    .catch((error) => {
        console.error('Error:', error);
        document.getElementById('combineRulesResult').innerText = 'Error: ' + error.message; // Show error message to user
    });
}

// Function to evaluate a rule
function evaluateRule() {
    const evaluationData = document.getElementById('evaluationData').value.trim();
    const ruleId = document.getElementById('ruleId').value.trim();
    document.getElementById('evaluationResult').innerText = ""; // Clear previous result

    if (!evaluationData || !ruleId) {
        alert("Please provide evaluation data and rule ID.");
        return; // Exit if input is invalid
    }

    try {
        const parsedData = JSON.parse(evaluationData); // Parse the evaluation data
        fetch('/evaluate_rule', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ data: parsedData, rule_id: ruleId }),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok: ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            // Check if result is boolean
            if (typeof data.result === 'boolean') {
                document.getElementById('evaluationResult').innerText = data.result ? 'true' : 'false';
            } else if (data.message) {
                document.getElementById('evaluationResult').innerText = data.message; // Show any message from the server
            } else {
                document.getElementById('evaluationResult').innerText = "Unexpected result format.";
            }
            console.log(data);
        })
        .catch((error) => {
            console.error('Error:', error);
            document.getElementById('evaluationResult').innerText = 'Error: ' + error.message; // Show error message to user
        });
    } catch (error) {
        console.error('JSON Parsing Error:', error);
        document.getElementById('evaluationResult').innerText = 'Error parsing JSON: ' + error.message; // Show JSON parse error
    }
}
