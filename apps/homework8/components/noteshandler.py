from py4web import action, URL, request
from yatl.helpers import XML
from py4web.utils.url_signer import URLSigner
from py4web.core import Fixture


class NotesHandler(Fixture):

    ### TODO: Complete.
    NOTESHANDLER = """<noteshandler
                    get_notes="{get_notes}"
                    add_notes="{add_notes}"
                    save_notes="{save_notes}"
                    delete_notes = "{delete_notes}"
                    ></noteshandler>"""

    def __init__(self,url,session,signer=None,db=None,auth=None):
        self.url = url
        self.signer=signer or URLSigner(session)
        self.db = db;
        self.auth=auth

        self.get_notes_url = url;
        self.add_notes_url = url + "/new";
        self.save_notes_url = url + "/edit";
        self.delete_notes_url = url + "/delete";



        self.__prerequisites__ = [session]
        args = list(filter(None,[session,db,auth,self.signer.verify()]));

        self.define_routes(args,["GET"],self.get_notes_url,self.get_notes);
        self.define_routes(args,["GET"],self.add_notes_url,self.add_notes);
        self.define_routes(args,["POST"],self.save_notes_url,self.save_notes);
        self.define_routes(args,["POST"],self.delete_notes_url,self.delete_notes);


        # func = action.uses(*args)(self.set_rating)
        # action(self.callback_url+'/<id>',method=["GET"])(func)

    def __call__(self):
        return XML(NotesHandler.NOTESHANDLER.format(
            get_notes=URL(self.get_notes_url,signer=self.signer),
            add_notes=URL(self.add_notes_url,signer=self.signer),
            save_notes=URL(self.save_notes_url,signer=self.signer),
            delete_notes=URL(self.delete_notes_url,signer=self.signer)
        ))

    def define_routes(self,args,method,url,class_func):
        func = action.uses(*args)(class_func)
        action(url,method=method)(func)

    def get_notes(self):
        user_id=self.auth.current_user.get('id');
        notes=self.db(self.db.notes.author==user_id).select(orderby=~self.db.notes.starred
            |~self.db.notes.updated).as_list()
        return dict(notes=notes)

    def add_notes(self):
        id=self.db.notes.insert()
        return dict(note=self.db.notes[id].as_dict())

    def save_notes(self):
        id = request.json.get('id') # Note: id can be none.
        key = request.json.get('key')
        val = request.json.get('val')
        update_dict ={
            key:val
        }
        self.db(self.db.notes.id==id).update(**update_dict)
        return dict(note=self.db.notes[id].as_dict())

    def delete_notes(self):
        id = request.json.get('id') # Note: id can be none.
        self.db(self.db.notes.id==id).delete();
        return dict(id=id)
