from . import main
from flask import render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from ..models import Blog
from app import db


@main.route('/')
@login_required
def home():
    return render_template('home.html', user=current_user)


@main.route('/quote')
@login_required
def quote():
    return render_template('quote.html')


@main.route('/blog', methods=['POST', 'GET'])
@login_required
def blog():
    if request.method == 'POST':
        # collect blog details from the form submitted by the user
        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')
        user_id = current_user._get_current_object().id
        # create a new blog object from our Blog class
        new_blog = Blog(author=author, title=title, content=content, user_id=user_id)
        # save the new blog obj in our db
        db.session.add(new_blog)
        db.session.commit()
        return redirect(url_for('main.blogs'))

    return render_template('blog.html')


@main.route('/blogs')
@login_required
def blogs():
    blogs = Blog.query.all()
    return render_template('blog_display.html', blogs=blogs)


@main.route('/delete/<int:blog_id>', methods=['POST', 'GET'])
@login_required
def delete_blog(blog_id):
    blog = Blog.query.get(blog_id)
    db.session.delete(blog)
    db.session.commit()
    flash('Your post has been deleted successfully', category='success')
    return redirect(url_for('main.blogs'))