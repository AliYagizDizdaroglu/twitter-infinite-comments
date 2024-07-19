from flask import Flask, render_template, request, redirect, url_for
from uuid import uuid4

app = Flask(__name__)

data = {"comments": {}}

def generate_id():
    return str(uuid4())

def add_comment(parent_id, content, user):
    comment_id = generate_id()
    new_comment = {
        "id": comment_id,
        "content": content,
        "user": user,
        "replies": {}
    }
    if parent_id == "None":
        data["comments"][comment_id] = new_comment
    else:
        parent_comment = find_comment(data["comments"], parent_id)
        if parent_comment:
            parent_comment["replies"][comment_id] = new_comment
        else:
            print(f"Parent comment with id {parent_id} not found.")
    return comment_id

def edit_comment(comment_id, new_content):
    comment = find_comment(data["comments"], comment_id)
    if comment:
        comment["content"] = new_content
    else:
        print(f"Comment with id {comment_id} not found.")

def delete_comment(comment_id):
    if not remove_comment(data["comments"], comment_id):
        print(f"Comment with id {comment_id} not found.")

def find_comment(comments, comment_id):
    if comment_id in comments:
        return comments[comment_id]
    for comment in comments.values():
        result = find_comment(comment["replies"], comment_id)
        if result:
            return result
    return None

def remove_comment(comments, comment_id):
    if comment_id in comments:
        del comments[comment_id]
        return True
    for comment in comments.values():
        if remove_comment(comment["replies"], comment_id):
            return True
    return False

@app.route('/')
def index():
    return render_template('index.html', comments=data["comments"])

@app.route('/add_comment', methods=['POST'])
def handle_add_comment():
    parent_id = request.form.get('parent_id', 'None')
    content = request.form.get('content')
    user = request.form.get('user')
    add_comment(parent_id, content, user)
    return redirect(url_for('index'))

@app.route('/edit_comment', methods=['POST'])
def handle_edit_comment():
    comment_id = request.form.get('comment_id')
    new_content = request.form.get('new_content')
    edit_comment(comment_id, new_content)
    return redirect(url_for('index'))

@app.route('/delete_comment', methods=['POST'])
def handle_delete_comment():
    comment_id = request.form.get('comment_id')
    delete_comment(comment_id)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
