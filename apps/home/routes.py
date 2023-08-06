from apps.home import blueprint
from flask import render_template, request
from flask_login import login_required
from jinja2 import TemplateNotFound
from apps.models import *
from apps.config import API_GENERATOR

def get_data():
    data_from_db = Ventilation.query.all()
    aggregated_data = {}

    for item in data_from_db:
        # Get the label/exercice for the current item
        label = item.exercice
    
        # If the label is not already in the dictionary, initialize the values to 0
        if label not in aggregated_data:
            aggregated_data[label] = {
                'eff_sum': 0,
                'eff_hr_sum': 0,
                'surface_sum': 0
            }
        
        # Add the current item's values to the corresponding sums in the dictionary
        aggregated_data[label]['eff_sum'] += item.effectif
        aggregated_data[label]['eff_hr_sum'] += item.eff_hr
        aggregated_data[label]['surface_sum'] += item.surface

    data = {
    'labels': list(aggregated_data.keys()),
    'values_eff': [item['eff_sum'] for item in aggregated_data.values()],
    'values_eff_hr': [item['surface_sum'] for item in aggregated_data.values()],
    'values_surface': [item['eff_hr_sum'] for item in aggregated_data.values()],
    }
    return data


@blueprint.route('/index')
@login_required
def index():
    return render_template('home/index.html', segment='index', API_GENERATOR=len(API_GENERATOR), data = get_data())


@blueprint.route('/<template>')
@login_required
def route_template(template):
        
    try:
        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment, API_GENERATOR=len(API_GENERATOR), data = get_data())

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500

    

# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
