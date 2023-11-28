

# Flask with Templates
## Importing Flask and render_template
```python
from flask import Flask, render_template, request, redirect, url_for
```

## Creating a Flask App
```python
app = Flask(__name__)
```

## Routing and View Functions
```python
@app.route('/')
def home():
    return 'Hello, World!'
```

## Dynamic URLs
```python
@app.route('/user/<username>')
def show_user_profile(username):
    return f'User: {username}'
```

## Rendering Templates
```python
@app.route('/template')
def render_template_example():
    return render_template('index.html', title='Flask Example', content='Hello from Flask!')
```

## Form Handling
```python
@app.route('/submit', methods=['POST'])
def form_submission():
    if request.method == 'POST':
        username = request.form['username']
        return f'Form submitted by {username}'
```

## Redirects
```python
@app.route('/redirect')
def redirect_example():
    return redirect(url_for('home'))
```

## Running the App
```python
if __name__ == '__main__':
    app.run(debug=True)
```

## Template (index.html)
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
</head>
<body>
    <h1>{{ content }}</h1>
</body>
</html>
```

