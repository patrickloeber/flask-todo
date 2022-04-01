from sqlalchemy import create_engine, select, update, delete
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# /// = relative path, //// = absolute path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], connect_args={"check_same_thread": False})

Session = sessionmaker(bind = engine, future = True)
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
    with Session() as session:
        todo_list = session.execute(select(Todo)).scalars().all()
        return render_template("base.html", todo_list=todo_list)


@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")
    with Session() as session: 
        new_todo = Todo(title=title, complete=False)
        session.add(new_todo)
        session.commit() 
    return redirect(url_for("home"))


@app.route("/update/<int:todo_id>")
def update(todo_id):
    with Session() as session: 
        todo = session.execute(select(Todo).filter_by(id=todo_id)).scalar_one()
        todo.complete = not todo.complete
        session.commit()
    return redirect(url_for("home"))


@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    with Session() as session: 
        todo = session.execute(select(Todo).filter_by(id=todo_id)).scalar_one()
        session.delete(todo)
        session.commit()
    return redirect(url_for("home"))

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    app.run(debug=True)
