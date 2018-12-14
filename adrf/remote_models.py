import requests


class RemoteObjectNotFound(Exception):
    pass


class DummyObject:
    """ Dummy class to add remote fields"""
    pass


class RemoteModel:
    """ Remote Model represents a model that is created by remote data.
    Required fields:
        - remote_host
        - remote_endpoint
        - remote_id_field
    """
    # TODO: can this code be improved using this?
    # https://stackoverflow.com/questions/6578986/how-to-convert-json-data-into-a-python-object

    @staticmethod
    def set_fields(this, remote_object):
        for field_name in remote_object:
            value = remote_object[field_name]
            if isinstance(value, dict):
                dict_field = RemoteModel.set_fields(DummyObject(), value)
                setattr(dict_field, field_name, dict_field)
            elif isinstance(value, list):
                list_field = [RemoteModel.set_fields(DummyObject(), sub_value) for sub_value in value]
                setattr(this, field_name, list_field)
            else:
                setattr(this, field_name, value)
        return this

    def __init__(self, dfrn, remote_url=None):
        self.dfrn = dfrn
        self.remote_object = None
        self.id = None
        self.remote_url = remote_url
        remote_object = self.get_remote_object()
        RemoteModel.set_fields(self, remote_object)

    def remote_object_url(self):
        return '{0}?{1}={2}&format=json'.format(self.remote_endpoint, self.remote_id_field, self.dfrn)

    def get_remote_object(self):
        if self.remote_url is None:
            remote_object_url = self.remote_object_url()
        else:
            remote_object_url = self.remote_url
        response = requests.get(url=remote_object_url)
        if response.status_code == 200:
            self.remote_object = response.json()
            if isinstance(self.remote_object, list):
                self.remote_object = self.remote_object[0]
            RemoteModel.set_fields(self, self.remote_object)
            len_re = len(self.remote_endpoint)
            self.id = self.url[len_re + 1 : len_re + 2]
            return self.remote_object
        else:
            raise RemoteObjectNotFound('Error getting {0} identified by {1}.'.format(self.model, self.dfrn))

    def to_json(self):
        return self.get_remote_object()

    def refresh(self):
        self.get_remote_object()

    @property
    def metadata(self):
        return self.remote_object


# class User(RemoteModel):
#     ''' Remote Dataset model
#     '''
#     remote_host = "http://docker.for.mac.localhost:8000"
#     remote_endpoint = remote_host + "/api/v1/users"
#     remote_id_field = 'username'
#     model = 'User'
