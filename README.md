# tinygen
Tiny Gen

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

# set up the server
```
uvicorn app.main:app --reload
```
