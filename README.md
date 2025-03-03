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
   git clone https://github.com/LiuyinC/tinygen.git
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
4. Set up your local Git configuration to enable cloning public repositories:
   ```bash
   git config --global credential.helper store
   ```

### Running the Application
To start the FastAPI server, run:
```bash
uvicorn app.main:app --reload
```

### API Usage
- **Endpoint**: `/improve-codebase`
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
       "suggested_git_diff": "generated_git_diff"
   }
   ```

## Running Tests
To run tests, use:
```bash
pytest tests/
```

## Telemetry and Logger Service

### Telemetry Event

Telemetry events are used to log significant actions within the service or endpoints. They typically include:
- **Unique event ID**: A unique identifier for each event.
- **Event name**: The name of the event being logged.
- **Timestamp of event creation**: The date and time when the event was created.
- **Additional event-specific data**: Any other relevant information specific to the event. For example, in the `improve_codebase` event, it contains the prompt, suggestion, is_reflected, error, etc. 

### Logger Service

The logger service is responsible for recording telemetry events. Usually, it will connect to a queue, like Kinesis or Kafka, but for this project, we will use a SQLite database for simplicity.
