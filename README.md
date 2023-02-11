[![Fjlask CI](https://github.com/ofer-shaham/test/actions/workflows/python-app.yml/badge.svg)](https://github.com/ofer-shaham/test/actions/workflows/python-app.yml)

## Library managment system

---

Tools:

- flask
- sqlalchemy
- pytest

---

---

```python
#install
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt

#test
pytest

#coverage
coverage run -m pytest
coverage report
coverage html  # open htmlcov/index.html in a browser

#run
set FLASK_APP=flaskr
set FLASK_ENV=development
flask init-db
flask run


```
- library API tests: [link](https://github.com/ofer-shaham/library-managment-api/blob/main/tests/test_book.py)
- library models: [link](https://github.com/ofer-shaham/library-managment-api/tree/main/flaskr/library)
- original project layout: [link](https://github.com/pallets-eco/flask-sqlalchemy/tree/main/examples/flaskr)
