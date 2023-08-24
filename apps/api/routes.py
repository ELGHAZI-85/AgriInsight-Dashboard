import json
from flask import request
from flask_restx import Api, Resource
from werkzeug.datastructures import MultiDict
from apps.api import blueprint
from apps.authentication.decorators import token_required
from apps.api.forms import *
from apps.models    import *
from datetime import datetime

api = Api(blueprint)

# Post -> ADD 
# Get -> READ 
# PUT -> UPDATE 

@api.route('/ventilation/', methods=['POST', 'GET', 'DELETE', 'PUT'])
@api.route('/ventilation/<int:model_id>/', methods=['GET', 'DELETE', 'PUT'])
class VentilationRoute(Resource):
    def get(self, model_id: int = None):
        if model_id is None:
            all_objects = Ventilation.query.all()
            output = [{'id_operation': obj.id_operation,'mois': obj.mois, 'surface': obj.surface, 'date': obj.date.strftime('%Y-%m-%d'), 'domaine': obj.domaine, 'cultures': obj.cultures, 'tache_principale': obj.tache_principale,'sous_tache':obj.sous_tache, 'effectif':obj.effectif, 'eff_hr':obj.eff_hr } for obj in all_objects]
            print(" Output : ",output)
        else:
            obj = Ventilation.query.get(model_id)
            if obj is None:
                return {
                           'message': 'matching record not found',
                           'success': False
                       }, 404
            output = {'id': obj.id_operation, **VentilationForm(obj=obj).data}
        
        return {
                   'data': output,
                   'success': True
               }, 200

    def post(self):
        try:
            body_of_req = request.form
 
            if not body_of_req:
                raise Exception()
        except Exception:
            if len(request.data) > 0:
                body_of_req = json.loads(request.data)
            else:
                body_of_req = {}
                
        body_of_req = dict(body_of_req)
        form = VentilationForm(MultiDict(body_of_req))
        if form.validate():
            try:
                body_of_req['date'] = datetime.strptime(body_of_req['date'], '%Y-%m-%d').date()
                obj = Ventilation(**body_of_req)
                Ventilation.query.session.add(obj)
                Ventilation.query.session.commit()
            except Exception as e:
                return {
                           'message': str(e),
                           'success': False
                       }, 400
        else:
            return {
                       'message': form.errors,
                       'success': False
                   }, 400
        return {
                   'message': 'record saved!',
                   'success': True
               }, 200

    
    def put(self, model_id: int):
        try:
            body_of_req = request.form
            print(body_of_req)
            if not body_of_req:
                raise Exception()
        except Exception:
            if len(request.data) > 0:
                body_of_req = json.loads(request.data)
            else:
                body_of_req = {}

        to_edit_row = Ventilation.query.filter_by(id_operation=model_id)

        if not to_edit_row:
            return {
                       'message': 'matching record not found',
                       'success': False
                   }, 404

        obj = to_edit_row.first()

        if not obj:
            return {
                       'message': 'matching record not found',
                       'success': False
                   }, 404

        form = VentilationForm(MultiDict(body_of_req), obj=obj)
        if not form.validate():
            return {
                       'message': form.errors,
                       'success': False
                   }, 404

        table_cols = [attr.name for attr in to_edit_row.__dict__['_raw_columns'][0].columns._all_columns]

        for col in table_cols:
            value = body_of_req.get(col, None)
            if value:
                setattr(obj, col, value)
        Ventilation.query.session.add(obj)
        Ventilation.query.session.commit()
        return {
            'message': 'record updated',
            'success': True
        }

    def delete(self, model_id: int):
        to_delete = Ventilation.query.filter_by(id_operation =model_id)
        if to_delete.count() == 0:
            return {
                       'message': 'matching record not found',
                       'success': False
                   }, 404
        to_delete.delete()
        Ventilation.query.session.commit()
        return {
                   'message': 'record deleted!',
                   'success': True
               }, 200
