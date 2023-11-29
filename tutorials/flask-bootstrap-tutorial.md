# Flask Project with Bootstrap Templates

## Project Structure

```
/my_flask_project
|-- /templates
|   |-- base.html
|   |-- home.html
|   |-- about_us.html
|-- app.py
|-- /static
|   |-- /css
|       |-- styles.css
|   |-- /js
|   |-- /img
```

## Setting Up Flask App

### Install Flask
```bash
pip install flask==2.3.3
```

### Create Project Structure
```bash
mkdir my_flask_project
cd my_flask_project
mkdir templates static
touch app.py templates/base.html templates/home.html templates/about_us.html static/css/styles.css
```

## HTML Templates

### Base Template (`templates/base.html`)
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}My Flask App{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/styles.css') }}">
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" integrity="sha384-B4gt1jrGC7Jh4AgTPSdUtOBvfO8sh+WyqJS8f5l5P04PPvPbExk+V4NKeN4u" crossorigin="anonymous">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
        <a class="navbar-brand" href="{{ url_for('home') }}">My Flask App</a>
        <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav">
                <li class="nav-item active">
                    <a class="nav-link" href="{{ url_for('home') }}">Home</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="{{ url_for('about_us') }}">About Us</a>
                </li>
            </ul>
        </div>
    </nav>
    
    <div class="container mt-4">
        {% block content %}{% endblock %}
    </div>

    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js" integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.11.6/dist/umd/popper.min.js" integrity="sha384-oBqDVmMz9ATKxIep9tiCxS/Z9fNfEXg+rRtBSEUyIvZlLq5TaPh5oe3haCIbY/Hj" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js" integrity="sha384-B4gt1jrGC7Jh4AgTPSdUtOBvfO8sh+WyqJS8f5l5P04PPvPbExk+V4NKeN4u" crossorigin="anonymous"></script>
</body>
</html>
```

### Home Page (`templates/home.html`)
```html
{% extends "base.html" %}

{% block title %}Home{% endblock %}

{% block content %}
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">Welcome to My Flask App</h5>
            <p class="card-text">This is the home page.</p>
            <a href="#" class="btn btn-primary">Learn More</a>
        </div>
    </div>
{% endblock %}
```

### About Us Page (`templates/about_us.html`)
```html
{% extends "base.html" %}

{% block title %}About Us{% endblock %}

{% block content %}
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">About Us</h5>
            <p class="card-text">We are a cool team doing awesome things!</p>
            <a href="#" class="btn btn-primary">Contact Us</a>
        </div>
    </div>
{% endblock %}
```

## Flask App (`app.py`)

```python
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about-us')
def about_us():
    return render_template('about_us.html')

if __name__ == '__main__':
    app.run(debug=True)
```

## CSS Styles (`static/css/styles.css`)

```css
/* Add your custom styles here */
body {
    padding-top: 60px; /* Adjusted for the fixed navbar */
}
```

## Running the Flask App

```bash
python app.py
```

Visit [http://127.0.0.1:5000/](http://127.0.0.1:5000/) in your browser to see the home page. Click on the "About Us" link in the navbar to navigate to the about-us page. Customize and expand the templates and styles according to your project's requirements.