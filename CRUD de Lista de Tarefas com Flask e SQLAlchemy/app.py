from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tarefas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Tarefa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(200), unique=True, nullable=False)

    def __repr__(self):
        return f"<Tarefa {self.descricao}>"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        descricao = request.form["descricao"]
        nova_tarefa = Tarefa(descricao=descricao)

        try:
            db.session.add(nova_tarefa)
            db.session.commit()
            return redirect(url_for("index"))
        except:
            return "Erro ao adicionar tarefa (talvez já exista)."

    tarefas = Tarefa.query.all()
    return render_template("index.html", tarefas=tarefas)


@app.route("/deletar/<int:id>")
def deletar(id):
    tarefa = Tarefa.query.get_or_404(id)

    try:
        db.session.delete(tarefa)
        db.session.commit()
        return redirect(url_for("index"))
    except:
        return "Erro ao deletar a tarefa."


@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    tarefa = Tarefa.query.get_or_404(id)

    if request.method == "POST":
        tarefa.descricao = request.form["descricao"]

        try:
            db.session.commit()
            return redirect(url_for("index"))
        except:
            return "Erro ao atualizar a tarefa."
    else:
        return render_template("editar.html", tarefa=tarefa)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
