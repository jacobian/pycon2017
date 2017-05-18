import sqlite3
from contextlib import closing
from bizkit import TemplateResponse, Router

class GreetingDatabase:
    def __init__(self):
        self.conn = sqlite3.connect('greetings.sqlite')
        self.conn.execute('''CREATE TABLE IF NOT EXISTS greeting_counts 
                             (greeting text, name text, greeting_count integer)''')
                            
    def get_and_increment_count(self, greeting, name):
        # RACE CONDITIONS AHOY!
        with closing(self.conn.cursor()) as c:
            c.execute(
                "SELECT greeting_count FROM greeting_counts WHERE greeting=? AND name=?",
                [greeting, name]
            )
            rows = c.fetchall()

            if rows:
                count = rows[0][0] + 1
                c.execute(
                    "UPDATE greeting_counts SET greeting_count=? WHERE greeting=? AND name=?",
                    [count, greeting, name]
                )
            else:
                count = 1
                c.execute(
                    "INSERT INTO greeting_counts (greeting, name, greeting_count) VALUES (?, ?, 1)",
                    [greeting, name]
                )

            self.conn.commit()
            return count

def hello(request, name):
    db = GreetingDatabase()
    count = db.get_and_increment_count("hello", name)
    context = {"greeting": "Hello", "name": name, "count": count}
    return TemplateResponse("greeting.html", context)

def goodbye(request, name):
    db = GreetingDatabase()
    count = db.get_and_increment_count("goodbye", name)
    context = {"greeting": "Goodbye", "name": name, "count": count}
    return TemplateResponse("greeting.html", context)

routes = Router()
routes.add_route(r'/hello/(.*)/$', hello)
routes.add_route(r'/goodbye/(.*)/$', goodbye)
