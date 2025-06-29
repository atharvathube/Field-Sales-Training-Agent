#FILE: utils/client_profile_parser.py

def extract_client_info(profile_text: str) -> dict:
    info = {
        "age": None,
        "marital_status": None,
        "children": None,
        "occupation": None,
        "employment_type": None,
        "income": None,
        "location": None,
        "health_issues": [],
        "existing_policies": None,
        "goal": None
    }

    lines = profile_text.splitlines()
    for line in lines:
        l = line.lower()
        if "age" in l:
            digits = ''.join(filter(str.isdigit, l))
            info["age"] = int(digits) if digits else None
        elif "marital status" in l:
            info["marital_status"] = line.split(":")[-1].strip()
        elif "children" in l:
            info["children"] = line.split(":")[-1].strip()
        elif "occupation" in l:
            info["occupation"] = line.split(":")[-1].strip()
        elif "employment type" in l:
            info["employment_type"] = line.split(":")[-1].strip()
        elif "annual income" in l:
            income_str = ''.join(c for c in line if c.isdigit())
            info["income"] = int(income_str) if income_str else 0
        elif "location" in l:
            info["location"] = line.split(":")[-1].strip()
        elif "health issues" in l:
            health = line.split(":")[-1].strip()
            info["health_issues"] = [h.strip() for h in health.split(",")] if health.lower() != "none" else []
        elif "existing insurance" in l:
            info["existing_policies"] = line.split(":")[-1].strip()
        elif "specific insurance needs" in l:
            info["goal"] = line.split(":")[-1].strip()
    return info
