doorlook/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── endpoints/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── companies.py
│   │   │   │   ├── employees.py
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── config.py
│   │   │   ├── security.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── company.py
│   │   │   ├── employee.py
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── company.py
│   │   │   ├── employee.py
│   │   ├── crud/
│   │   │   ├── __init__.py
│   │   │   ├── company.py
│   │   │   ├── employee.py
│   │   ├── tests/
│   │   │   ├── __init__.py
│   │   │   ├── test_companies.py
│   │   │   ├── test_employees.py
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── alembic/
│   │   ├── env.py
│   │   ├── script.py.mako
│   │   ├── versions/
│   ├── alembic.ini
│   ├── README.md
├── frontend/
│   ├── public/
│   │   ├── index.html
│   ├── src/
│   │   ├── components/
│   │   │   ├── CompanyList.js
│   │   │   ├── EmployeeList.js
│   │   ├── pages/
│   │   │   ├── HomePage.js
│   │   │   ├── CompanyPage.js
│   │   │   ├── EmployeePage.js
│   │   ├── services/
│   │   │   ├── api.js
│   │   ├── App.js
│   │   ├── index.js
│   ├── package.json
│   ├── Dockerfile
│   ├── README.md
├── .gitignore
├── docker-compose.yml
├── README.md
