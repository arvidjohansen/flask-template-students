
# Eksempel på flask-kode

```py
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return 'Velkommen til Flask webapplikasjonen!'


app.run(debug=True)
```

For å kunne kjøre må du ha installert flask-modulen med:

```
pip install flask
```

## Oppgave: Utvid koden til å bruke templates - programmet skal rendre en template og sende den tilbake.