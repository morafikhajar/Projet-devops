import os
from flask import Flask, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

db_url = os.environ.get("DATABASE_URL", "sqlite:///todo.db")
app.config["SQLALCHEMY_DATABASE_URI"] = db_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

status_list = ["todo", "in_progress", "review", "done"]
status_labels = {"todo": "To Do", "in_progress": "In Progress", "review": "Review", "done": "Done"}
status_colors = {"todo": "#3B82F6", "in_progress": "#F97316", "review": "#8B5CF6", "done": "#10B981"}


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    tags = db.Column(db.String(200), default="General")
    date = db.Column(db.String(20), default="")
    status = db.Column(db.String(20), default="todo")


back_icon = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 12H5M12 19l-7-7 7-7"/></svg>'
next_icon = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>'
trash_icon = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 6h18M8 6V4h8v2M6 6l1 14h10l1-14"/></svg>'
calendar_icon = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/></svg>'
bell_icon = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/><path d="M13.7 21a2 2 0 0 1-3.4 0"/></svg>'
logo_icon = '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#10B981" stroke-width="2"><rect x="5" y="3" width="14" height="18" rx="2"/><path d="M9 3v2h6V3M8 10h8M8 14h5"/></svg>'


@app.route("/")
def index():
    board_html = ""

    for status in status_list:
        tasks = Task.query.filter_by(status=status).all()
        color = status_colors[status]

        cards_html = ""
        for task in tasks:
            tag_list = task.tags.split(",")
            labels_html = ""
            for tag in tag_list:
                labels_html = labels_html + '<span class="label" style="background:' + color + '20;color:' + color + '">' + tag.strip() + '</span>'

            back_link = ""
            next_link = ""
            pos = status_list.index(status)
            if pos > 0:
                back_link = '<a href="/move/' + str(task.id) + '/prev" title="Back">' + back_icon + '</a>'
            if pos < len(status_list) - 1:
                next_link = '<a href="/move/' + str(task.id) + '/next" title="Next">' + next_icon + '</a>'

            cards_html = cards_html + """
            <div class="card" draggable="true" data-id=\"""" + str(task.id) + """\">
              <p class="card-title">""" + task.title + """</p>
              <div class="labels">""" + labels_html + """</div>
              <div class="card-bottom">
                <div class="avatars">
                  <div class="avatar">H</div>
                  <div class="avatar"  >R</div>
                </div>
                <div class="date">""" + calendar_icon + " " + task.date + """</div>
              </div>
              <div class="card-actions">
                """ + back_link + next_link + """
                <a href="/delete/""" + str(task.id) + """" class="delete-link" title="Delete">""" + trash_icon + """</a>
              </div>
            </div>
            """

        empty_text = ""
        if len(tasks) == 0:
            empty_text = '<p class="empty-text">No tasks yet</p>'

        board_html = board_html + """
        <div class="column" data-status=\"""" + status + """\">
          <div class="column-head">
            <h3>""" + status_labels[status] + """</h3>
            <span class="count" style="background:""" + color + """20;color:""" + color + """">""" + str(len(tasks)) + """</span>
          </div>

          """ + cards_html + """

          <button class="toggle-form-btn" onclick="openModal('""" + status + """')">+ Add New Task</button>
          """ + empty_text + """
        </div>
        """

    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <title>TaskBoard</title>
      <link rel="preconnect" href="https://fonts.googleapis.com">
      <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
      <link rel="stylesheet" href="/static/style.css">
    </head>
    <body>

      <div class="sidebar">
        <div class="logo">""" + logo_icon + """ TaskBoard</div>
        <a class="nav-item">Dashboard</a>
        <a class="nav-item active">Projects</a>
        <a class="nav-item">Team</a>
        <a class="nav-item">Calendar</a>
        <a class="nav-item">Settings</a>
      </div>

      <div class="main-area">

        <div class="topbar">
          <div class="topbar-right">
            """ + bell_icon + """
            <div class="avatar big">M</div>
          </div>
        </div>

        <div class="content-wrap">
          <div class="page-title">
            <h1>Current Projects</h1>
            <p>Overview of ongoing tasks and progress</p>
          </div>

          <div class="board">
            """ + board_html + """
          </div>
        </div>

      </div>

      <div class="modal-overlay hidden" id="modal-overlay">
        <div class="modal-box">
          <h3>New Task</h3>
          <form action="/add" method="post">
            <input type="hidden" name="status" id="modal-status" value="todo">
            <input type="text" name="title" placeholder="Task title" required>
            <input type="text" name="tags" placeholder="Labels (comma separated)">
            <input type="text" name="date" placeholder="Due date (ex: Nov 5)">
            <div class="modal-buttons">
              <button type="button" onclick="closeModal()" class="cancel-btn">Cancel</button>
              <button type="submit" class="save-btn">Save Task</button>
            </div>
          </form>
        </div>
      </div>

      <script src="/static/app.js"></script>
    </body>
    </html>
    """

    return html


@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title", "").strip()
    tags = request.form.get("tags", "").strip() or "General"
    date = request.form.get("date", "").strip()
    status = request.form.get("status", "todo")

    if title != "" and status in status_list:
        new_task = Task(title=title, tags=tags, date=date, status=status)
        db.session.add(new_task)
        db.session.commit()

    return redirect(url_for("index"))


@app.route("/move/<int:task_id>/<direction>")
def move(task_id, direction):
    task = Task.query.get_or_404(task_id)
    pos = status_list.index(task.status)

    if direction == "next" and pos < len(status_list) - 1:
        task.status = status_list[pos + 1]
    if direction == "prev" and pos > 0:
        task.status = status_list[pos - 1]

    db.session.commit()
    return redirect(url_for("index"))


@app.route("/move-to/<int:task_id>/<status>", methods=["POST"])
def move_to(task_id, status):
    task = Task.query.get_or_404(task_id)
    if status in status_list:
        task.status = status
        db.session.commit()
    return "", 204


@app.route("/delete/<int:task_id>")
def delete(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/health")
def health():
    return {"status": "ok"}, 200


with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
