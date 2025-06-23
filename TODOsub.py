from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# Flaskアプリの作成
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
db = SQLAlchemy(app)

# データベースのモデル（テーブル定義）
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)
    done = db.Column(db.Boolean, default=False)

# 初回リクエスト時にデータベース作成
with app.app_context():
    db.create_all()

# タスク一覧を取得（GET/todos)
@app.route("/todos", methods=["GET"])
def get_todos():
    todos = Todo.query.all()
    return jsonify([{"id": t.id, "task": t.task, "done": t.done} for t in todos])

# タスクを追加（POST/todos<id>）
@app.route("/todos", methods=["POST"])
def add_todo():
    data = request.json
    new_todo = Todo(task=data["task"])
    db.session.add(new_todo)
    db.session.commit()
    return jsonify({"message": "Task added"}), 201

# タスクを更新（PUT/todos/<id>）
@app.route("/todos/<int:todo_id>", methods=["PUT"])
def update_todo(todo_id):
    todo = Todo.query.get(todo_id)
    if not todo:
        return jsonify({"error": "Task not found"}), 404
    data = request.json
    todo.task = data.get("task", todo.task)
    todo.done = data.get("done", todo.done)
    db.session.commit()
    return jsonify({"message": "Task updated"})

# タスクを削除(DELETE/todos/<id>)
@app.route("/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    todo = Todo.query.get(todo_id)
    if not todo:
        return jsonify({"error": "Task not found"}), 404
    db.session.delete(todo)
    db.session.commit()
    return jsonify({"message": "Task deleted"})

# ルート設定
@app.route("/")
def home():
    return "Flask is running! Use /todos to manage tasks."

# @app.route("/todos")
# def get_todos():
#     return "TODO List"

# アプリの実行
if __name__ == "__main__":
    app.run(debug=True)