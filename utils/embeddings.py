from sentence_transformers import SentenceTransformer

def generate_employee_embeddings(employees: list, model: SentenceTransformer):
    """
    Generate embeddings for employee profiles.
    Args:
        employees: List of employee dictionaries
        model: SentenceTransformer model
    Returns:
        embeddings: Tensor of profile embeddings
    """
    profiles = [
        f"{emp['name']} has {emp['experience_years']} years of experience with skills: "
        f"{', '.join(emp['skills'])}. Projects: {', '.join(emp['projects'])}. "
        f"Availability: {emp['availability']}"
        for emp in employees
    ]
    return model.encode(profiles, convert_to_tensor=True)