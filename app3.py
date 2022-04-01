from sqlalchemy import create_engine, select, update, delete
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# /// = relative path, //// = absolute path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future = True)
app.session = scoped_session(SessionLocal)

Base = declarative_base(bind = engine)

class Todo(Base):
    __tablename__ = 'todo_list'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    complete = Column(Boolean)

    def __repr__(self):
        return f"Todo(id={self.id!r}, title={self.title!r}, complete={self.complete!r})"


@app.route("/")
def home():
    todo_list = app.session.execute(select(Todo)).scalars().all()
    return render_template("base.html", todo_list=todo_list)


@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")
    new_todo = Todo(title=title, complete=False)
    app.session.add(new_todo)
    app.session.commit() 
    return redirect(url_for("home"))


@app.route("/update/<int:todo_id>")
def update(todo_id):
    todo = app.session.execute(select(Todo).filter_by(id=todo_id)).scalar_one()
    todo.complete = not todo.complete
    app.session.commit()
    return redirect(url_for("home"))


@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = app.session.execute(select(Todo).filter_by(id=todo_id)).scalar_one()
    app.session.delete(todo)
    app.session.commit()
    return redirect(url_for("home"))

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    app.run(debug=True)
