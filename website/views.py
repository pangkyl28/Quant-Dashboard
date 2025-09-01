from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user
from .models import Note
from flask import request, flash
from . import db
import json
from .services.gbm import run_gbm_simulation
from .services.data import yfinance_fetch, estimate_drift, estimate_volatility


views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')
        if len(note) < 1:
            flash("Note is too short!", category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash("Note Added!", category='success')
    return render_template("home.html", user=current_user)

@views.route('/gbm_simulation', methods=['GET', 'POST'])
@login_required
def gbm_simulation():
    has_results = False
    days = []
    paths = {}
    path_keys = []
    terminal = []
    error = None
    if request.method == 'POST':
        try:
            selected_stock = request.form.get('selected_stock')
            time_horizon = int(request.form.get('time_horizon'))
            num_simulations = int(request.form.get('num_simulations'))
            if (time_horizon <= 0) or (num_simulations <= 0):
                flash("Invalid input!", category='error')
            else:
                # rows = day 0..N, cols = path_1..path_M
                results = run_gbm_simulation(selected_stock, time_horizon, num_simulations)
                has_results = bool(results is not None and not results.empty)
                if has_results:
                    days = results.index.tolist()
                    paths = results.to_dict(orient='list')
                    path_keys = list(paths.keys())
                    terminal = results.iloc[-1].tolist()
        except Exception as e:
            flash("Error Occurred", category='error')
            error = str(e)

    return render_template("gbm_simulation.html", user=current_user, has_results=has_results, days=days, paths=paths, path_keys=path_keys, terminal=terminal, error=error)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    return jsonify({})
