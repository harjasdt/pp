from flask import Flask, redirect, url_for, render_template_string

app = Flask(__name__)

# Template for the home page
home_template = '''
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
    <title>Home</title>
  </head>
  <body>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <a class="navbar-brand" href="{{ url_for('home') }}">FlaskApp</a>
      <div class="collapse navbar-collapse">
        <ul class="navbar-nav mr-auto">
          <li class="nav-item active">
            <a class="nav-link" href="{{ url_for('home') }}">Home</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="{{ url_for('about') }}">Results</a>
          </li>
          
        </ul>
      </div>
    </nav>
    <div class="container">
      <div class="jumbotron mt-4">
        <h1 class="display-4">Home Page</h1>
        <p class="lead">Welcome to the Home Page!</p>
        <hr class="my-4">
        <p>Use the navigation bar to switch between pages.</p>
      </div>
    </div>
  </body>
</html>
'''

# Template for the about page
about_template = '''
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
    <title>About</title>
  </head>
  <body>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <a class="navbar-brand" href="{{ url_for('home') }}">FlaskApp</a>
      <div class="collapse navbar-collapse">
        <ul class="navbar-nav mr-auto">
          <li class="nav-item">
            <a class="nav-link" href="{{ url_for('home') }}">Home</a>
          </li>
          <li class="nav-item active">
            <a class="nav-link" href="{{ url_for('about') }}">About</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="{{ url_for('contact') }}">Contact</a>
          </li>
        </ul>
      </div>
    </nav>
    <div class="container">
      <div class="jumbotron mt-4">
        <h1 class="display-4">About Page</h1>
        <p class="lead">This is the About Page.</p>
        <hr class="my-4">
        <p>Learn more about our application.</p>
      </div>
    </div>
  </body>
</html>
'''

# Template for the contact page
contact_template = '''
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
    <title>Contact</title>
  </head>
  <body>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <a class="navbar-brand" href="{{ url_for('home') }}">FlaskApp</a>
      <div class="collapse navbar-collapse">
        <ul class="navbar-nav mr-auto">
          <li class="nav-item">
            <a class="nav-link" href="{{ url_for('home') }}">Home</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="{{ url_for('about') }}">About</a>
          </li>
          <li class="nav-item active">
            <a class="nav-link" href="{{ url_for('contact') }}">Contact</a>
          </li>
        </ul>
      </div>
    </nav>
    <div class="container">
      <div class="jumbotron mt-4">
        <h1 class="display-4">Contact Page</h1>
        <p class="lead">This is the Contact Page.</p>
        <hr class="my-4">
        <p>Get in touch with us.</p>
      </div>
    </div>
  </body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(home_template)

@app.route('/about')
def about():
    return render_template_string(about_template)

@app.route('/contact')
def contact():
    return render_template_string(contact_template)

@app.route('/redirect_to/<page>')
def redirect_to(page):
    if page == "home":
        return redirect(url_for('home'))
    elif page == "about":
        return redirect(url_for('about'))
    elif page == "contact":
        return redirect(url_for('contact'))
    else:
        return "404: Page not found", 404

if __name__ == '__main__':
    app.run(debug=True)
