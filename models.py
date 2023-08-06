# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps import db

'''
Define our models -> Tables schemas
'''

# Book Sample -> this table used in forms.py
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))


# Ventilation table
class Ventilation(db.Model):
    __tablename__ = 'Ventilation'
    
    id_operation = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, unique=True)
    exercice = db.Column(db.String)
    mois = db.Column(db.String)
    domaine = db.Column(db.String)
    quinzaine = db.Column(db.Integer)
    cultures = db.Column(db.String)
    surface = db.Column(db.Float, nullable=True)
    tache_principale = db.Column(db.String)
    sous_tache = db.Column(db.String)
    effectif = db.Column(db.Float)
    eff_hr = db.Column(db.Float, nullable=True)