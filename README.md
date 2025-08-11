# HR Resource Query Chatbot

A Streamlit-based HR chatbot that helps find employees based on skills, experience, and projects using RAG (Retrieval-Augmented Generation) technology.

## Features

- Natural language queries for finding employees
- Semantic search using sentence transformers
- Employee profile matching with relevance scores
- Interactive chat interface
- Detailed employee information display

## Deployment on Streamlit Cloud

1. **Fork/Clone this repository**
2. **Connect to Streamlit Cloud**
3. **Set the main file path**: `hr bot/app.py`
4. **Deploy**

## Local Development

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Streamlit app**:
   ```bash
   streamlit run app.py
   ```

3. **Run the FastAPI backend** (optional for local testing):
   ```bash
   uvicorn main:app --reload
   ```

## Project Structure

```
hr bot/
├── app.py              # Streamlit frontend
├── main.py             # FastAPI backend
├── requirements.txt    # Python dependencies
├── packages.txt        # System dependencies
├── employees.json      # Employee database
├── utils/              # Utility modules
│   ├── rag.py         # RAG pipeline
│   ├── embeddings.py  # Embedding generation
│   └── logger.py      # Logging setup
└── .streamlit/         # Streamlit configuration
    └── config.toml
```

## Dependencies

- **Frontend**: Streamlit
- **Backend**: FastAPI, Uvicorn
- **ML**: Sentence Transformers, PyTorch
- **Data Processing**: NumPy, Pydantic
- **HTTP**: Requests

## Notes

- The app requires the `employees.json` file to be present
- For production deployment, consider using environment variables for configuration
- The backend API runs on `http://localhost:8000` by default
