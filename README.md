```bash
python -m venv jam

jam\scripts\activate
```

```python
pip install "fastapi[all]" sqlalchemy passlib[bcrypt] python-jose[cryptography] aiosqlite

uvicorn main:app --reload
```
