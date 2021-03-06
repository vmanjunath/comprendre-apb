# coding=utf-8

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config.setdefault(
    "SQLALCHEMY_DATABASE_URI",
    os.environ.get("DATABASE_URL", "postgres://localhost:5432/apb")
)
app.config.from_pyfile("settings.cfg", silent=True)

db = SQLAlchemy(app)


@app.route("/")
def accueil():
    return render_template("index.html")


@app.route("/vider_bdd")
def vider_base():
    from apb.models import Academie, Eleve, Etablissement, Filiere, Formation, Voeu
    Voeu.query.delete()
    Formation.query.delete()
    Filiere.query.delete()
    Etablissement.query.delete()
    Eleve.query.delete()
    Academie.query.delete()

    return "La base de données a été vidée"


@app.route("/bdd_exemple")
def initialiser_base():
    from apb.models import Academie, Eleve, Etablissement, Filiere, Formation, Voeu

    academie = Academie("Académie")
    db.session.add(academie)
    db.session.commit()

    eleve = Eleve(academie=academie)
    db.session.add(eleve)
    db.session.commit()

    etablissement = Etablissement(nom="Exemple", academie=academie)
    db.session.add(etablissement)
    db.session.commit()

    filiere = Filiere(nom="Exemple")
    db.session.add(filiere)
    db.session.commit()

    formation = Formation(filiere=filiere, etablissement=etablissement, capacite=50)
    db.session.add(formation)
    db.session.commit()

    voeu = Voeu(eleve=eleve, formation=formation, classement=1)
    db.session.add(voeu)
    db.session.commit()


    return "Une base de données exemple a été générée"


@app.route("/etablissements")
def liste_etablissements():
    from apb.models import Etablissement
    return render_template(
        "etablissements/liste.html",
        etabs=Etablissement.query
    )


@app.route("/etablissements/<id_etab>")
def detail_etablissement(id_etab):
    from apb.models import Etablissement
    etab = Etablissement.query.filter_by(id=id_etab).first()
    return render_template("etablissements/detail.html", etab=etab)


@app.route("/formations/<id_formation>")
def detail_formation(id_formation):
    from apb.models import Formation
    formation = Formation.query.filter_by(id=id_formation).first()
    return render_template("etablissements/detail_formation.html", formation=formation)
