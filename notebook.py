import json
import datetime

class Notebook:
    def __init__(self):
        self.notes = {}

    def __str__(self):
        s = ""
        for i in self.notes.values():
            s += "  "
            s += str(i)
            s += "\n"
        return s
        
    def to_json(self):
        j = []
        for k in self.notes:
            item = self.notes[k]
            j.append(item.to_json())
        return j
    
    def from_json(self, js):
        self.notes = {}
        for item in js:
            headline = item['headline']
            body = item['body']
            note = Note(headline, body)
            note.id = item['id']
            note.time_created = datetime.datetime.fromtimestamp(item['time_created'])
            note.time_updated = datetime.datetime.fromtimestamp(item['time_updated'])
            self.notes[note.id] = note
    
def notebook_create():
    return Notebook()

def notebook_load(fname):
    n = Notebook()
    with open(fname) as f:
        n.from_json(json.load(f))
    return n


def notebook_save(n, fname):
    with open(fname, 'w') as f:
        json.dump(n.to_json(), f, ensure_ascii=False)
    return;

def notebook_delete_item(n, id):
    return n.notes.pop(id)

def notebook_update_item(n, item):
    n.notes[item.id] = item
    return;

class Note:
    note_id = 0
    def __init__(self, headline, body):
        self.id = str(Note.note_id)
        Note.note_id += 1
        self.headline = headline
        self.body = body
        now = datetime.datetime.now()
        self.time_created = now
        self.time_updated = now
    def __str__(self):
        return f"id: {self.id}, headline: {self.headline}, body: {self.body}, created: {self.time_created}, updated: {self.time_updated}"
    
    def to_json(self):
        return {
            'id': self.id, 
            'headline': self.headline, 
            'body': self.body, 
            'time_created': self.time_created.timestamp(), 
            'time_updated': self.time_updated.timestamp()
        }

def enter(str):
    return input(str)
    
def do_create_notebook_item(n):
    headline = enter("Введите заголовок:")
    body = enter("Введите тело:")
    note = Note(headline, body)
    notebook_update_item(n, note)
    print(f"Заметка создана: {note}")
    return;
        
def do_update_notebook_item(n):
    id = enter("Введите номер заметки:");
    if (id not in n.notes):
        print("Заметка не найдена")
        return
    note = n.notes[id]
    note.headline = enter("Введите новый заголовок:")
    note.body = enter("Введите новое тело:")
    note.time_updated = datetime.datetime.now()
    print(f"Заметка сохранена: {note}")
    return;
        
def do_delete_notebook_item(n):
    id = enter("Введите номер заметки:")
    if (id not in n.notes):
        print("Заметка не найдена")
        return
    note = notebook_delete_item(n, id)
    print(f"Заметка удалена: {note}")
    return;
        
def do_save_notebook(n):
    fname = enter("Введите имя файла:")
    return notebook_save(n, fname);
        
def do_load_notebook():
    fname = enter("Введите имя файла:")
    return notebook_load(fname)
        
def do_list_notebook(n):
    print(f"Содержимое ноутбука: {str(n)}")


pr = """
Нажмите: 
C для создания заметки, 
U для редактирования заметки, 
D для удаления заметки, 
S чтобы сохранить файл, 
L чтобы загрузить из файла  
N чтобы создать новую ноутбук:
    """
def do_work():
    n = notebook_create()
    while (True):
        line = input(pr)
        print(line)
        if (line == "C"):
            do_create_notebook_item(n)
        elif (line == "U"):
            do_update_notebook_item(n)
        elif (line == "D"):
            do_delete_notebook_item(n)
#        elif (line == "V"):
#            do_view_notebook_item(n)
        elif (line == "I"):
            do_list_notebook(n)
        elif (line == "S"):
            do_save_notebook(n)
        elif (line == "L"):
            n = do_load_notebook()
        elif (line == "N"):
            n = notebook_create()
        else:
            print("Выходим")
            break
            
do_work()
