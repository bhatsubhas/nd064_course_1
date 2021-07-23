import logging
import sqlite3

from flask import (Flask, flash, jsonify, redirect, render_template, request,
                   url_for)

db_connection_count = 0

# Function to get a database connection.
# This function connects to database with the name `database.db`


def get_db_connection():
    global db_connection_count
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    db_connection_count += 1
    return connection

# Function to get a post using its ID


def get_post(post_id):
    connection = get_db_connection()
    post = connection.execute('SELECT * FROM posts WHERE id = ?',
                              (post_id,)).fetchone()
    connection.close()
    return post


# Define the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

# Define health check endpoint


@app.route('/healthz')
def health_check():
    return jsonify(
        {"result": "OK - healthy"}
    ), 200

# Define metrics endpoing


@app.route('/metrics')
def metrics():
    connection = get_db_connection()
    post_count = connection.execute(
        'SELECT count(*) as post_count FROM posts').fetchone()['post_count']
    connection.close()
    return jsonify(
        {
            "db_connection_count": db_connection_count,
            "post_count": post_count
        }
    ), 200

# Define the main route of the web application


@app.route('/')
def index():
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    return render_template('index.html', posts=posts)

# Define how each individual article is rendered
# If the post ID is not found a 404 page is shown


@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    if post is None:
        app.logger.debug(f'Could not find article with post_id {post_id}')
        return render_template('404.html'), 404
    else:
        title = post['title']
        app.logger.debug(f'Article "{title}" retrieved!')
        return render_template('post.html', post=post)

# Define the About Us page


@app.route('/about')
def about():
    app.logger.debug('Accessed About Us page')
    return render_template('about.html')

# Define the post creation functionality


@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            connection = get_db_connection()
            connection.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                               (title, content))
            connection.commit()
            connection.close()
            app.logger.debug(f'New article created with title "{title}"')
            return redirect(url_for('index'))

    return render_template('create.html')


# start the application on port 3111
if __name__ == "__main__":
    log_format = '%(levelname)s:%(name)s:%(asctime)s, %(message)s'
    date_format = '%d/%m/%y, %I:%M:%S'
    logging.basicConfig(format=log_format, datefmt=date_format)
    app.run(host='0.0.0.0', port='3111', debug=True)
