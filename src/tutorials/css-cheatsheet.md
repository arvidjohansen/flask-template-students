# CSS Basics

## Selectors
```css
/* Selects all paragraphs */
p {
    color: blue;
}

/* Selects elements with class "example" */
.example {
    font-size: 16px;
}

/* Selects elements with id "header" */
#header {
    background-color: #eee;
}
```

## Colors
```css
/* Using color names */
p {
    color: red;
}

/* Using hexadecimal values */
.example {
    background-color: #00ff00;
}

/* Using RGB values */
#header {
    border: 1px solid rgb(255, 0, 0);
}
```

## Margins and Padding
```css
/* Setting margins */
.example {
    margin: 10px;
}

/* Setting padding */
#content {
    padding: 20px;
}
```

## Font Styling
```css
/* Font size */
p {
    font-size: 18px;
}

/* Font family */
.example {
    font-family: 'Arial', sans-serif;
}

/* Font weight */
#header {
    font-weight: bold;
}
```

## Text Alignment
```css
/* Aligning text to the center */
.example {
    text-align: center;
}

/* Justifying text */
p {
    text-align: justify;
}
```

## Borders
```css
/* Adding a border */
.example {
    border: 1px solid #000;
}

/* Border radius for rounded corners */
#box {
    border-radius: 10px;
}
```

# Linking CSS in HTML

To link an external CSS file to an HTML document, you can use the following:

```html
<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" type="text/css" href="styles.css">
    <title>Document Title</title>
</head>
<body>
    <!-- Content goes here -->
</body>
</html>
```

In this example, the `href` attribute in the `<link>` tag specifies the path to the external CSS file (`styles.css`). Make sure to adjust the file path accordingly based on your project structure.