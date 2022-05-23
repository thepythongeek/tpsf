import os
from flask import Blueprint, current_app
from flask import request
from flask import abort
from flask import jsonify
from flask.views import MethodView
from sqlalchemy import or_
from app.models import Event, MediaAssets, db

import app.utilities as utilities

main = Blueprint('main', __name__)


class Events(MethodView):

    def post(self):
        '''
        creates a new event. Be sure to set Content-Type to 
        "application/form-data".

        The endpoint can accept multiple files, the form values must
        include:
            title
            description
            ...files(one or more files)

        The output format will be 
            {
                "success": True|False,
                "body":"",
            }
        '''
        event = db.session.execute(
            db.select(Event).where(
                Event.title == request.form['title'], Event.description ==
                request.form['description'])).one_or_none()
        if event is not None:
            return {"success": False, "body": "you created this event already"}

        event = Event(title=request.form.get('title'),
                      description=request.form['description'])
        assets = []
        print('******')
        print(request.files)
        for file in request.files.getlist('files'):
            filename = utilities.upload_file(file=request.files[file],
                                             dest='uploads',
                                             app=current_app)
            if filename:
                assets.append(
                    MediaAssets(name=os.path.join('uploads', filename)))
            else:
                abort(
                    jsonify({
                        'success': False,
                        'body': "The file could not be uploaded"
                    }))
        event.assets = assets
        db.session.add(event)
        db.session.commit()
        return {"success": True, "body": "event created successfully"}

    def get(self, id=None):
        '''
        grab all events when 'id' is None.

        The output format will be:
            [
                {
                    "id":int,
                    "title":str,
                    "description":str,
                    "assets":
                        [
                            xxxx.jpg, dfghk.mp4, etc
                        ]
                }
            ]
            'assets' is an array of file locations for your resources
            that is images and videos.
        '''
        if id is not None:
            event = self._isValidId(id)
            if not event:
                return dict(success=True,
                            body="sorry this event doesnot exist")
            return jsonify(body=event.json, success=True)

        return jsonify(success=True,
                       body=[
                           event[0].json
                           for event in db.session.execute(db.select(Event))
                       ])

    def delete(self, id):
        '''
        Deletes an event if the id is valid. All assets for this event will 
        be deleted too.
        '''
        # delete files
        event = self._isValidId(id)
        if not event:
            return dict(success=True, body="sorry this event doesnot exist")

        for asset in event.assets:
            utilities.delete_file(filename=asset.name, )

        # delete from database
        db.session.execute(db.delete(Event).where(Event.id == id))
        db.session.commit()

        return dict(success=True, body='event deleted')

    def put(self, id):
        '''
        Updates an event with a valid 'id'

        accepts json format
            {
                    "id":int,
                    "title":str,
                    "description":str,
                    "assets":
                        [
                            {"type": "path|file","data":'filename|base64 encoded file string'}, etc
                           
                        ]
                }
            The parameters are optional only, only the parameters you wish to 
            update.
        '''

        event = self._isValidId(id)

        if not event:
            return dict(success=True, body="sorry this event doesnot exist")

        data = request.json
        values = dict()
        if 'assets' in data:
            values['assets'] = data['assets']
        if 'title' in data:
            values['title'] = data['title']
        if 'description' in data:
            values['description'] = data['description']

        # if we have the assets parameter check whether
        # it contains some base64 enconded strings and process
        # accordingly otherwise the strings are just urls
        # to the assets in our server.
        if 'assets' in values:
            for value in values['assets']:
                if value['type'] == 'file':
                    filename = utilities.upload_from_string(
                        file_string=value['data'],
                        app=current_app,
                        dest='uploads')
                    event.assets.append(MediaAssets(name=filename))
                else:
                    utilities.delete_file(filename=value)
                    db.session.execute(
                        db.delete(MediaAssets).where(name=value))

        set_parameters = {k: values[k] for k in values if k != 'assets'}
        if set_parameters:
            db.session.execute(
                db.update(Event).where(Event.id == id).values(set_parameters))
        db.session.commit()
        return jsonify(success=True, body='event updated successfully')

    def _isValidId(self, id):
        event = db.session.execute(
            db.select(Event).where(Event.id == id)).one_or_none()
        if event is None:
            return False
        return event[0]


events = Events.as_view('events')
main.add_url_rule('/events', view_func=events, methods=['POST'])
main.add_url_rule('/events', view_func=events, methods=['GET'])
main.add_url_rule('/events/<int:id>',
                  view_func=events,
                  methods=['GET', 'PUT', 'DELETE'])
