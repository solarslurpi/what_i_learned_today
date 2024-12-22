import json
import re

# This function takes in the modelfile that has example questions and answers.  The functin reads through the file and extracts the question/answer 
# pares into a list of dictionaries with the keys "question" and "expected_sql".  
def parse_modelfile(filename: str = "modelfile_template"):
    """Extract test cases from modelfile."""
    with open(filename, 'r') as f:
        content = f.read()
    
    # Find all QUESTION/ANSWER pairs
    pattern = r'QUESTION:\s*(.*?)\nANSWER:\s*(.*?)(?=\n\n|$)'
    matches = re.finditer(pattern, content, re.DOTALL)
    
    test_cases = []
    for match in matches:
        question = match.group(1).strip()
        expected_sql = match.group(2).strip()
        # Strip newlines from sql
        sql = match.group(2).strip()
        sql = ' '.join(line.strip() for line in sql.splitlines())
        test_cases.append({
            "question": question,
            "expected_sql": sql,
        })
    
    return test_cases

TEST_CASES = parse_modelfile()
print(json.dumps(TEST_CASES, indent=2))