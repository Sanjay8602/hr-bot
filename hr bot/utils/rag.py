import json
import numpy as np
from sentence_transformers import SentenceTransformer, util
from utils.embeddings import generate_employee_embeddings
from utils.logger import setup_logger

logger = setup_logger()

# Load employee data
try:
    with open('employees.json', 'r') as f:
        EMPLOYEES_DATA = json.load(f)
        EMPLOYEES = EMPLOYEES_DATA["employees"]
except FileNotFoundError:
    logger.error("employees.json not found")
    raise FileNotFoundError("employees.json not found in the project directory")

# Initialize model and embeddings
try:
    model = SentenceTransformer('all-MiniLM-L6-v2')
    EMPLOYEE_EMBEDDINGS = generate_employee_embeddings(EMPLOYEES, model)
except Exception as e:
    logger.error(f"Failed to initialize model or embeddings: {str(e)}")
    raise

def rag_pipeline(query: str, top_k: int = 3, threshold: float = 0.3):
    """
    RAG pipeline: Retrieval, Augmentation, Generation
    Args:
        query: User input query
        top_k: Number of top results to return
        threshold: Minimum relevance score
    Returns:
        response: Formatted natural language response
        employees: List of matching employee profiles
    """
    if not query or not isinstance(query, str):
        logger.warning("Invalid query provided")
        return "Please provide a valid query.", []

    try:
        # Retrieval
        query_embedding = model.encode(query, convert_to_tensor=True)
        cos_scores = util.cos_sim(query_embedding, EMPLOYEE_EMBEDDINGS)[0]
        
        # Debug logging
        logger.info(f"Query embedding shape: {query_embedding.shape}")
        logger.info(f"Employee embeddings shape: {EMPLOYEE_EMBEDDINGS.shape}")
        logger.info(f"Cosine scores shape: {cos_scores.shape}")
        logger.info(f"Number of employees: {len(EMPLOYEES)}")
        
        # Convert to numpy array and ensure it's 1D
        cos_scores_np = cos_scores.cpu().numpy().flatten()
        
        # Get top matches
        # Ensure top_k doesn't exceed available data
        actual_top_k = min(top_k, len(cos_scores_np))
        if actual_top_k > 0 and len(cos_scores_np) > 0:
            top_indices = np.argsort(cos_scores_np)[-actual_top_k:][::-1]
            relevant_employees = []
            for idx in top_indices:
                score = float(cos_scores_np[idx])
                if score > threshold:
                    emp = EMPLOYEES[idx].copy()
                    emp["relevance_score"] = score
                    relevant_employees.append(emp)
        else:
            relevant_employees = []
        
        # Augmentation
        if not relevant_employees:
            response = "No suitable employees found for your query. Try modifying your search terms."
            logger.info(f"No matches found for query: {query}")
            return response, []
        
        # Format context for each employee
        context = []
        for emp in relevant_employees:
            employee_info = (
                "- " + emp['name'] + " (" + str(emp['experience_years']) + " years experience)\n"
                "  Skills: " + ", ".join(emp['skills']) + "\n"
                "  Projects: " + ", ".join(emp['projects']) + "\n"
                "  Availability: " + emp['availability'].capitalize() + "\n"
                "  Relevance: " + f"{emp['relevance_score']:.2%}"
            )
            context.append(employee_info)
        
        # Generation
        response = (
            f"Based on your query '{query}', I found {len(relevant_employees)} suitable candidates:\n\n"
            + "\n\n".join(context) + "\n\n"
            + "Would you like more details about any of these candidates or to refine your search?"
        )
        
        logger.info(f"RAG pipeline processed query: {query}, found {len(relevant_employees)} matches")
        return response, relevant_employees
    
    except Exception as e:
        logger.error(f"Error in RAG pipeline: {str(e)}")
        raise