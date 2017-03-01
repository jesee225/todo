import json
import time

from utils import log


def db_save(data, path):
    s = json.dumps(data, indent=2, ensure_ascii=False)
    with open(path, 'w+', encoding='utf-8') as f:
        f.write(s)


def db_load(path):
    with open(path, 'r', encoding='utf-8') as f:
        s = f.read()
        return json.loads(s)


class Model(object):
    @classmethod
    def db_path(cls):
        classname = cls.__name__
        path = 'dbfiles/{}.txt'.format(classname)
        return path

    @classmethod
    def all(cls):
        path = cls.db_path()
        models = db_load(path)
        ms = [cls(m) for m in models]
        return ms

    @classmethod
    def find_all(cls, **kwargs):
        ms = []
        k, v = '', ''
        for key, value in kwargs.items():
            k, v = key, value
        all = cls.all()
        for m in all:
            if v == m.__dict__[k]:
                ms.append(m)
        return ms

    @classmethod
    def find_by(cls, **kwargs):
        k, v = '', ''
        for key, value in kwargs.items():
            k, v = key, value
        all = cls.all()
        for m in all:
            if v == m.__dict__[k]:
                return m
        return None

    @classmethod
    def find(cls, id):
        return cls.find_by(id=id)

    @classmethod
    def delete(cls, id):
        models = cls.all()
        index = -1
        for i, e in enumerate(models):
            if e.id == id:
                index = i
                break
        if index == -1:
            pass
        else:
            models.pop(index)
            l = [m.__dict__ for m in models]
            path = cls.db_path()
            db_save(l, path)

    def save(self):
        models = self.all()
        if self.id is None:
            if len(models) == 0:
                self.id = 1
            else:
                self.id = models[-1].id + 1
            models.append(self)
        else:
            index = -1
            for i, m in enumerate(models):
                if m.id == self.id:
                    index = i
                    break
            models[index] = self
        l = [m.__dict__ for m in models]
        path = self.db_path()
        db_save(l, path)

    @classmethod
    def change_time(cls):
        fmt = '%Y/%m/%d %H:%M:%S'
        value = time.localtime(int(time.time()))
        dt = time.strftime(fmt, value)
        return dt

    def __repr__(self):
        classname = self.__class__.__name__
        properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]
        s = '\n'.join(properties)
        return '< {}\n{} \n>\n'.format(classname, s)


class User(Model):
    def __init__(self, form):
        self.id = form.get('id', None)
        self.username = form.get('username', '')
        self.password = form.get('password', '')
        self.role = int(form.get('role', 10))

    def is_admin(self):
        return self.role == 1

    def validate_login(self):
        u = User.find_by(username=self.username)
        if u is not None:
            return u.password == self.password
        else:
            return False

    def validate_register(self):
        return len(self.username) > 2 and len(self.password) > 2


class Todo(Model):
    def __init__(self, form):
        self.id = form.get('id', None)
        self.task = form.get('task', '')
        self.completed = form.get('completed', False)
        self.user_id = form.get('user_id', None)
        self.created_time = form.get('created_time', None)

    def do_completed(self):
        d = {
            False: '未完成',
            True: '完成',
        }
        return d.get(self.completed)
