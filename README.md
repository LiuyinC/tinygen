# tinygen
Tiny Gen

## Project Overview
Tiny Gen is a FastAPI-based application that integrates with OpenAI's GPT models to suggest code improvements and generate diffs for code repositories. It automates the process of analyzing code and providing recommendations for refactoring or enhancements.

## Project Structure

```
tinygen/
├── app/
│   ├── api/
│   │   ├── endpoints/
│   │   ├── __init__.py
│   ├── core/
│   ├── models/
│   ├── services/
│   ├── main.py
│   └── __init__.py
├── tests/
│   ├── __init__.py
│   └── test_generate_diff.py
└── README.md
```

## Features
- **API Endpoints**: Exposes endpoints for generating diffs based on user prompts and repository URLs.
- **Integration with OpenAI**: Leverages OpenAI's GPT models for code suggestions and summaries.
- **Dynamic Repository Handling**: Clones repositories and handles changes dynamically.

## Getting Started
### Prerequisites
- Python 3.7+
- FastAPI
- Uvicorn
- OpenAI Python Client

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/tinygen.git
   cd tinygen
   ```
2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Set your OpenAI API key in the environment variables:
   ```bash
   export OPENAI_API_KEY='your_openai_api_key'
   ```

### Running the Application
To start the FastAPI server, run:
```bash
uvicorn app.main:app --reload
```

### API Usage
- **Endpoint**: `/generate-diff`
- **Method**: `POST`
- **Request Body**:
   ```json
   {
       "repoUrl": "https://github.com/user/repo",
       "prompt": "convert it to Typescript"
   }
   ```
- **Response**:
   ```json
   {
       "diff": "generated_diff_here"
   }
   ```

## Running Tests
To run tests, use:
```bash
pytest tests/
```

## Contributing
Contributions are welcome! Please open an issue or submit a pull request on GitHub.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments
- [FastAPI](https://fastapi.tiangolo.com)
- [OpenAI](https://openai.com)

---

For more information, please refer to the [documentation](https://yourdoclink.com).
