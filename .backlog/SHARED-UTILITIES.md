# 🧩 Shared Utilities — Código Reutilizável

**Repositório:** `.backlog/shared/`  
**Última atualização:** 2026-06-26

---

## 📦 Available Utilities

### Currently Available

(None yet — add your reusable code here)

---

## ➕ How to Add a Utility

### Step 1: Create File

```bash
# Create in .backlog/shared/
# Example: .backlog/shared/my_utility.py

def reusable_function():
    """Clear docstring describing what it does."""
    pass
```

### Step 2: Document Here

Add entry to this file:

```markdown
### my_utility.py
- **Purpose:** Brief description
- **Functions:** `reusable_function()`
- **Dependencies:** [None / list]
- **Author:** Your name
- **Status:** ✅ Production-ready
```

### Step 3: Commit

```bash
git add .backlog/shared/my_utility.py
git add .backlog/SHARED-UTILITIES.md
git commit -m "feat: add shared utility - my_utility"
git push ssh-github trabalho-backlog
```

---

## 📖 How to Use a Utility

```python
import sys
sys.path.insert(0, '.backlog/shared')

from my_utility import reusable_function

result = reusable_function()
```

---

## 🔍 Search Utilities

```bash
# List all utilities
ls .backlog/shared/*.py

# Find specific function
grep -r "def my_function" .backlog/shared/

# Check imports
grep "import" .backlog/shared/*.py
```

---

## ✅ Utility Guidelines

- Clear docstrings
- No hardcoded config (use parameters)
- No dependencies on local files
- No credentials in code
- Tests included (if possible)
- No side effects

---

## 📋 Template for New Utility

```python
"""
Module: description of what this utility does

Usage:
    from my_utility import my_function
    result = my_function(param1, param2)

Returns:
    dict: {key: value} or similar
"""

def my_function(param1: str, param2: int = 10) -> dict:
    """
    Brief description.
    
    Args:
        param1 (str): What it is
        param2 (int): What it is (default 10)
    
    Returns:
        dict: What's returned
        
    Raises:
        ValueError: When this happens
        
    Example:
        >>> result = my_function("test")
        >>> result['key']
        value
    """
    # Implementation
    return {"result": "value"}


if __name__ == "__main__":
    # Quick test
    print(my_function("test"))
```

---

## 🚀 Ready to Share

When your utility is ready for team use:
1. Add to this SHARED-UTILITIES.md
2. Update status to ✅
3. Make announcement in #backlog-channel
4. Team can start using immediately

---

**Sharing Knowledge = Better Code 🎯**

Questions? See COORDINATION.md
