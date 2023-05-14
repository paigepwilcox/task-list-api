from flask import Blueprint, jsonify, abort, make_response, request
from app.models.task import Task
import datetime
from dotenv import load_dotenv
from app import db

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"task {model_id} invalid"}, 400))

    task = cls.query.get(model_id)

    if not task:
        abort(make_response({"message":f"task {model_id} not found"}, 404))

    return task


@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    if "title" not in request_body or "description" not in request_body:
        return make_response({"details": "Invalid data"}, 400)

    new_task = Task(title=request_body["title"],
                    description=request_body["description"],
                    completed_at=None)
    
    db.session.add(new_task)
    db.session.commit()

    return make_response(jsonify({"task":new_task.to_dict()}), 201)


@tasks_bp.route("", methods=["GET"])
def read_all_tasks():
    # tasks = Task.query.get.all()
    sort = request.args.get("sort")
    if sort == "asc":
        tasks = Task.query.order_by(Task.title.asc()).all()
    else:
        tasks = Task.query.order_by(Task.title.desc()).all()
    tasks_response = []

    for task in tasks:
        tasks_response.append(task.to_dict())
    return jsonify(tasks_response)

@tasks_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    task = validate_model(Task, task_id)
    return make_response(jsonify({"task":task.to_dict()}), 200)

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]
    task.completed_at = None

    db.session.commit()
    return make_response({"task":task.to_dict()}, 200)

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response({"details": 'Task 1 "Go on my daily walk 🏞" successfully deleted'}, 200)