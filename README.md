# E-commerce Product Name Extraction using NER

This project demonstrates a process for extracting product names from e-commerce website URLs using a fine-tuned Named Entity Recognition (NER) model.

## Overview

The project involves the following steps:

1. **URL Preprocessing**: Reads a list of URLs and filters them to ensure they are accessible and suitable for parsing.
2. **Data Parsing**: Extracts potential product names from the filtered URLs using a combination of HTML tag analysis (h1, h2, h3) and class name keyword matching.
3. **Annotation Preparation**: Creates a text file (`annote.txt`) containing the extracted text snippets for manual annotation. This annotated data is then used to create a training dataset (`annotations.json`) in IOB format.
4. **Model Fine-tuning**: Fine-tunes a pre-trained `bert-base-multilingual-cased` model for token classification (NER) using the annotated dataset.
5. **Model Evaluation**: Evaluates the performance of the fine-tuned model using metrics like precision, recall, F1-score, and accuracy.
6. **Model Saving**: Saves the fine-tuned model for later deployment.
7. **API Deployment**: Provides a FastAPI backend to serve the model predictions.
8. **Web Interface**: Includes a simple HTML frontend to interact with the model.

## Project Structure

```
.
├── index.html              # Frontend interface
├── main.py                 # FastAPI backend
├── model.py               # Core model functionality
├── product_ner_model/     # Fine-tuned model directory
├── README.md              # This file
└── venv/                  # Virtual environment
```

## Setup and Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. **Set up virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

   If you don't have a requirements.txt file, install the following packages manually:
   ```bash
   pip install fastapi uvicorn transformers torch beautifulsoup4 requests
   ```

## Running the Application

1. **Start the FastAPI server**:
   ```bash
   python main.py
   ```

2. **Open the frontend**:
   - Open `index.html` in your browser
   - Enter a URL in the text area and click "Анализировать" (Analyze)

## Dependencies

The project requires the following libraries:

- `fastapi`
- `uvicorn`
- `transformers`
- `torch`
- `requests`
- `beautifulsoup4`
- `python-multipart` (for FastAPI)

## Configuration

The API runs on `http://localhost:8000` by default. You can change this in `main.py`:
```python
uvicorn.run(app, host="0.0.0.0", port=8000)
```

## Usage

1. The frontend sends a POST request to `/predict` endpoint with the URL as plain text
2. The backend:
   - Verifies the URL is accessible
   - Extracts potential product names from the page
   - Runs the NER model on the extracted text
   - Returns the predictions

## Notes

- The model is fine-tuned for e-commerce product name extraction
- For production use, consider:
  - Adding authentication
  - Implementing rate limiting
  - Using a proper web server instead of development Uvicorn
  - Containerizing the application

## Troubleshooting

If you encounter CORS errors:
- Make sure the frontend is accessing the correct API URL
- Verify the CORS middleware is properly configured in `main.py`

For model loading issues:
- Verify the `product_ner_model` directory exists with all required files (if not, run `notebook.ipynb`)
- Check the model path in `model.py`