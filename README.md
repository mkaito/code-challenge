# Code Challenge

## Usage

```bash
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ python -m spacy download en_core_web_md
$ uvicorn main:app --reload
$ curl -X POST http://localhost:8000/process -H "Content-Type: application/json" -d '{
           "prompt": "How do I get to the Mun?",
           "context": "My name is Jebediah Kerman. My credit card number is 1234 5678 9012 3456"
         }'
```
