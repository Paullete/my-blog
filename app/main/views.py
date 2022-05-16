from . import main
from flask import render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from ..models import Blog, Comment
from app import db
from ..request import get_quote


@main.route('/')
@login_required
def home():
    quote = get_quote()
    return render_template('home.html', user=current_user, quote=quote)


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
    current_user_id = current_user.id
    if current_user_id != 1:
        flash('Only the admin can delete it!!!', 'error')
    else:
        if blog:
            db.session.delete(blog)
            db.session.commit()
            flash('Your post has been deleted successfully', category='success')
    return redirect(url_for('main.blogs'))


@main.route('/comment/<blog_id>', methods=['POST', 'GET'])
@login_required
def new_comment(blog_id):
    blog = Blog.query.get(blog_id)
    comments = Comment.query.filter_by(blog_id=blog_id).all()
    comment_count = len(comments)
    if request.method == 'POST':
        nickname = request.form.get('nickname')
        content = request.form.get('content')
        new_comment_obj = Comment(nickname=nickname, content=content, blog_id=blog_id)
        db.session.add(new_comment_obj)
        db.session.commit()
        print(new_comment)
        return redirect(url_for('main.new_comment', blog_id=blog_id))

    return render_template('comments.html', comments=comments, blog=blog, comment_count=comment_count)


@main.route('/remove/<int:comment_id>', methods=['POST', 'GET'])
@login_required
def delete_comment(comment_id):
    # blog = Blog.query.get(blog_id)
    comment = Comment.query.get(comment_id)
    db.session.delete(comment)
    db.session.commit()
    flash('Comment has been deleted successfully', category='success')
    # return render_template('comments.html')
    return redirect(url_for('main.blogs'))


@main.route('/edit/<int:blog_id>', methods=['POST', 'GET'])
@login_required
def edit_blog(blog_id):
    blog = Blog.query.get(blog_id)
    if request.method == 'POST':
        # collect blog details from the form submitted by the user
        blog.author = request.form.get('author')
        blog.title = request.form.get('title')
        blog.content = request.form.get('content')

        # save the new blog obj in our db
        db.session.add(blog)
        db.session.commit()
        flash('Post has been updated', 'success')
        return redirect(url_for('main.blogs'))
    return render_template('blog_edit.html')