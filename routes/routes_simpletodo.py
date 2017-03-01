from utils import log
from utils import error
from utils import template
from utils import redirect
from utils import http_response
from routes.routes_user import current_user
from routes.routes_user import login_required

from models import Todo


def index(request):
    u = current_user(request)
    todo_list = Todo.find_all(user_id=u.id)
    body = template('simple_todo_index.html', todos=todo_list)
    return http_response(body)


def edit(request):
    todo_id = int(request.query.get('id', -1))
    t = Todo.find_by(id=todo_id)
    u = current_user(request)
    if t.user_id != u.id:
        return error(request)
    body = template('simple_todo_edit.html', todo=t)
    return http_response(body)


def add(request):
    u = current_user(request)
    form = request.form()
    t = Todo(form)
    t.user_id = u.id
    t.created_time = t.change_time()
    t.save()
    return redirect('/todo')


def update(request):
    todo_id = int(request.query.get('id', -1))
    t = Todo.find_by(id=todo_id)
    u = current_user(request)
    if t.user_id != u.id:
        return error(request)
    form = request.form()
    t.task = form.get('task')
    t.save()
    return redirect('/todo')


def delete(request):
    todo_id = int(request.query.get('id', -1))
    t = Todo.find_by(id=todo_id)
    u = current_user(request)
    if t.user_id != u.id:
        return error(request)
    Todo.delete(todo_id)
    return redirect('/todo')


def completed(request):
    todo_id = int(request.query.get('id', -1))
    t = Todo.find_by(id=todo_id)
    u = current_user(request)
    if t.user_id != u.id:
        return error(request)
    t.completed = not t.completed
    t.save()
    return redirect('/todo')


route_dict = {
    '/todo': login_required(index),
    '/todo/add': login_required(add),
    '/todo/edit': login_required(edit),
    '/todo/update': login_required(update),
    '/todo/delete': login_required(delete),
    '/todo/completed': login_required(completed),
}
