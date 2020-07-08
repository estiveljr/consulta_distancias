CALL cd D:\Users\estivel.ramos\Documents\Distancias_prod
CALL conda activate dist
set FLASK_APP=app.py
set FLASK_ENV=production
CALL flask run --host 0.0.0.0
dsd
