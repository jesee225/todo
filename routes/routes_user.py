from utils import log
from utils import template
from utils import redirect
from utils import http_response

from models import User

import random

session = {}


def random_str():
    seed = 'abcdefjsad89234hdsfkljasdkjghigaksldf89weru'
    s = ''
    for i in range(16):
        random_index = random.randint(0, len(seed) - 2)
        s += seed[random_index]
    return s


def current_user(request):
    session_id = request.cookies.get('user', '')
    user_id = int(session.get(session_id, '-1'))
    u = User.find_by(id=user_id)
    return u


def login_required(route_function):
    def f(request):
        u = current_user(request)
        if u is None:
            return redirect('/login')
        return route_function(request)
    return f


def route_login(request):
    headers = {}
    if request.method == 'POST':
        form = request.form()
        u = User(form)
        if u.validate_login():
            user = User.find_by(username=u.username)
            session_id = random_str()
            session[session_id] = user.id
            headers['Set-Cookie'] = 'user={}'.format(session_id)
            return redirect('/todo', headers)
    body = template('login.html')
    return http_response(body, headers=headers)


def route_register(request):
    if request.method == 'POST':
        form = request.form()
        u = User(form)
        if u.validate_register():
            u.save()
            return redirect('/login')
        else:
            return redirect('/register')
    body = template('register.html')
    return http_response(body)


def route_admin_users(request):
    u = current_user(request)
    if u is not None and u.is_admin():
        us = User.all()
        body = template('admin_users.html', users=us)
        return http_response(body)
    else:
        return redirect('/login')


def route_admin_user_update(request):
    form = request.form()
    user_id = int(form.get('id', -1))
    new_password = form.get('password', '')
    u = User.find_by(id=user_id)
    if u is not None:
        u.password = new_password
        u.save()
    return redirect('/admin/users')


def route_static(request):
    filename = request.query.get('file', 'doge.gif')
    path = 'static/' + filename
    with open(path, 'rb') as f:
        header = b'HTTP/1.1 200 OK\r\nContent-Type: image/gif\r\n\r\n'
        img = header + f.read()
        return img


route_dict = {
    '/login': route_login,
    '/register': route_register,
    '/admin/users': route_admin_users,
    '/admin/user/update': route_admin_user_update,
}
