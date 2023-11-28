
# Flask Templating Language

## Template Structure

Flask uses the Jinja2 templating engine. Templates are typically stored in a folder named `templates` within your Flask project.

## Variables

Use double curly braces `{{ variable }}` to output variables in the template.

Example:
```html
<p>Hello, {{ name }}!</p>
```

## Control Structures

### If Statements

Use `{% if condition %} ... {% endif %}` to conditionally include content.

Example:
```html
{% if user %}
    <p>Welcome, {{ user }}!</p>
{% else %}
    <p>Please log in.</p>
{% endif %}
```

### Loops

Use `{% for item in items %} ... {% endfor %}` for looping through items.

Example:
```html
<ul>
    {% for fruit in fruits %}
        <li>{{ fruit }}</li>
    {% endfor %}
</ul>
```

## Template Inheritance

Create a base template with common structure and extend it in other templates.

Base Template (`base.html`):
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}{% endblock %}</title>
</head>
<body>
    <div id="content">
        {% block content %}{% endblock %}
    </div>
</body>
</html>
```

Extended Template:
```html
{% extends "base.html" %}

{% block title %}Flask Example{% endblock %}

{% block content %}
    <h1>Hello from Flask!</h1>
{% endblock %}
```

## Template Comments

Use `{# comment #}` for adding comments in the template.

Example:
```html
{# This is a comment #}
```