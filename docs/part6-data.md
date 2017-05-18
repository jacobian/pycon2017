# Part 6: Data Storage

Note:
- web apps aren't particularly interesting if they don't store data

---

# Decision Point:

## To ORM or not to ORM?

---

### Benefits of ORMs

- Relational databases are the best general purpose data storage solution (and not just for relational data any more)
- Object-Relational Mappers smooth other the impedance mismatch between relational databases and object-oriented languages
- Relational databases are similar enough that ORMs let you smoothly switch
- If you're taking the "Best of Breed" route, SQLAlchemy is spectacularly good

---

### Downsides of ORMs

- Increasingly, apps require special-purpose data storage engines
- ORMs tend to hide the best features of your chosen database
- Non-relational databases differ so widely that a general "ON-RM" probably isn't possible
- Inventing a new ORM in 2017 is... a great way to learn more about ORMs!

---

### Exercise 6-1: data storage

Record and display the number of times a greeting has been shown (e.g., `/hello/pycon` should display "Hello, pycon. pycon has been greeted 17 times.")

Where should you store data?
- Try [SQLAlchemy](http://www.sqlalchemy.org/) (if you're familiar with it already)
- [Redis](https://redis.io/) would be perfect (again if you're already familiar)
- Use the stdlib `sqlite3` module
- Just store data in a flat file!

Feel free to ignore race conditions. Or, if you're masochistic, don't.

---

### Exercise 6-1: my controller

```python
def hello(request, name):
    db = GreetingDatabase()
    count = db.get_and_increment_count("hello", name)
    context = {"greeting": "Hello", "name": name, "count": count}
    return TemplateResponse("greeting.html", context)
```

---

### Exercise 6-1: my storage layer

Are you sure you want to see this? It isn't pretty.

---

### Exercise 6-1: my storage layer

Don't say I didn't warn you:

```python
class GreetingDatabase:
    def __init__(self):
        self.conn = sqlite3.connect('greetings.sqlite')
                            
    def get_and_increment_count(self, greeting, name):
        c = self.conn.corsor()
        c.execute("""SELECT greeting_count FROM greeting_counts 
                      WHERE greeting=? AND name=?""", [greeting, name])
        rows = c.fetchall()
        if rows:
            count = rows[0][0] + 1
            c.execute("""UPDATE greeting_counts 
                         SET greeting_count=? 
                         WHERE greeting=? AND name=?""", [count, greeting, name])
        else:
            count = 1
            c.execute("""INSERT INTO greeting_counts 
                         (greeting, name, greeting_count) 
                         VALUES (?, ?, 1)""", [greeting, name])
        
        self.conn.commit()
        return count
```
