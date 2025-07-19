# refactor_assistant.py

import os

def analyze_repository(repo_path):
    result = {}
    for root, dirs, files in os.walk(repo_path):
        for file in files:
            if file.endswith(".py"):
                full_path = os.path.join(root, file)
                with open(full_path, "r", encoding="utf-8") as f:
                    code = f.read()
                suggestions = analyze_code(code)
                if suggestions:
                    result[os.path.relpath(full_path, repo_path)] = suggestions
    return result

def analyze_code(code):
    suggestions = []

    if "eval(" in code:
        suggestions.append({
            "issue": "Use of eval() is dangerous and can lead to code injection.",
            "code": "eval(...)",
            "suggested_fix": "Avoid using eval(); use ast.literal_eval or safer parsing."
        })

    if len(code.splitlines()) > 300:
        suggestions.append({
            "issue": "File too long — consider splitting into modules.",
            "code": code[:200] + "...",
            "suggested_fix": "Split long files into multiple logical modules."
        })

    if "import *" in code:
        suggestions.append({
            "issue": "Wildcard imports pollute the namespace.",
            "code": "from module import *",
            "suggested_fix": "Import only what is needed explicitly."
        })

    return suggestions
