# Library management system


Done:
----
- testing: 
```sh
coverage run -m pytest tests/test_book.py tests/test_db.py  
ptw --runner "pytest --testmon" #run in watch mode

```

- files I added to the project:
```yaml
flaskr
├── library
│   ├── Author.py
│   ├── Base.py
│   ├── Book.py
│   ├── Copy.py
│   ├── __init__.py
│   ├── Loan.py
│   ├── Member.py
│   └── views.py <------- routes are here
└── utils
    ├── constants.py
    ├── __init__.py
    └── utils.py
____ tests/test_book.py
____ tests/test_db.py
    
```


Library management system
--------------

tech stack:
- flask
- flask-sqlalchemy
- DB: sqlite3


this project is a work in progress
-----------
- based upon flaskr example which had working setup for running tests using pytest


Todos:
----
- user authentication
- user authorization
- open api / postman
- add docker-compose
- integrate github actions
