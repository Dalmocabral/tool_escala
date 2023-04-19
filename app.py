from datetime import datetime
from flask import Flask, render_template, request, make_response, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import json
import os
from flask_migrate import Migrate
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://escal_ade_servico_user:MVDuEzAI99kgIve9Z7w6HJXlr1X353LI@dpg-cgvhq69euhlhlbngkaq0-a.oregon-postgres.render.com/escal_ade_servico'
# "sqlite:///project.db"
# postgres://escal_ade_servico_user:MVDuEzAI99kgIve9Z7w6HJXlr1X353LI@dpg-cgvhq69euhlhlbngkaq0-a.oregon-postgres.render.com/escal_ade_servico


app.config['SECRET_KEY'] = 'minha_chave_secreta'

db = SQLAlchemy(app)
migrate = Migrate(app, db)
admin = Admin(app, name='Admin Panel', template_mode='bootstrap3')


@app.route("/")
def index():
    return render_template('index.html')


class User_Azul(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    ultima_dispensa = db.Column(db.DateTime)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'data_ultima_dispensa': self.ultima_dispensa.strftime('%d-%m-%Y') if self.ultima_dispensa else None
        }


class User_Vermelha(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    ultima_dispensa = db.Column(db.DateTime)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'data_ultima_dispensa': self.ultima_dispensa.strftime('%d-%m-%Y') if self.ultima_dispensa else None
        }


class User_Moral(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    ultima_dispensa = db.Column(db.DateTime)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'data_ultima_dispensa': self.ultima_dispensa.strftime('%d-%m-%Y') if self.ultima_dispensa else None
        }


@app.route("/escala_azul")
def escala_azul():
    users_azul = [user.to_dict() for user in User_Azul.query.order_by(
        User_Azul.ultima_dispensa).all()]

    return render_template("escala_azul.html", users=users_azul)


@app.route('/escala_vermelha')
def escala_vermelha():
    users_vermelha = [user.to_dict() for user in User_Vermelha.query.order_by(
        User_Vermelha.ultima_dispensa).all()]

    return render_template('escala_vermelha.html', users=users_vermelha)


@app.route('/escala_moral')
def escala_moral():
    users_moral = [user.to_dict() for user in User_Moral.query.order_by(
        User_Moral.ultima_dispensa).all()]
    return render_template('escala_moral.html', users=users_moral)


@app.route("/liberar/<int:user_id>")
def liberar(user_id):
    user_Azul = User_Azul.query.get(user_id)
    if user_Azul:
        user_Azul.ultima_dispensa = datetime.now()
        db.session.commit()

    return redirect(url_for("escala_azul"))


@app.route("/liberar_vermelho/<int:user_id>")
def liberar_vermelho(user_id):
    user_Vermelha = User_Vermelha.query.get(user_id)
    if user_Vermelha:
        user_Vermelha.ultima_dispensa = datetime.now()
        db.session.commit()

    return redirect(url_for("escala_vermelha"))


@app.route("/liberar_moral/<int:user_id>")
def liberar_moral(user_id):
    user_moral = User_Moral.query.get(user_id)
    if user_moral:
        user_moral.ultima_dispensa = datetime.now()
        db.session.commit()

    return redirect(url_for("escala_moral"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        admin.add_view(ModelView(User_Azul, db.session))
        admin.add_view(ModelView(User_Vermelha, db.session))
        admin.add_view(ModelView(User_Moral, db.session))

    app.run(debug=True)
