from django.apps import apps

# from RFID_MGT.users.models import User, Visitor
from django.contrib.sessions.models import Session

user_model = apps.get_model('users', 'User')
visitor_model = apps.get_model('users', 'Visitor')


class OneSessionPerUserMiddleware(object):
    def __init__(self, get_response):
        """
        One-time configuration and initialisation.
        """
        self.get_response = get_response

    def __call__(self, request):
        """
        Code to be executed for each request before the view (and later
        middleware) are called.
        """
        response = self.get_response(request)
        self.process_request(request)
        return response

    # noinspection PyMethodMayBeStatic
    def process_request(self, request):
        try:
            if isinstance(request.user, user_model):
                current_key = request.session.session_key
                if hasattr(request.user, 'visitor'):
                    active_key = request.user.visitor.session_key
                    # print(active_key, current_key)
                    if active_key != current_key:
                        Session.objects.filter(session_key=active_key).delete()
                        request.user.visitor.session_key = current_key
                        request.user.visitor.save()
                    else:
                        pass
                else:
                    visitor_model.objects.create(
                        user=request.user,
                        session_key=current_key,
                    )
        except AttributeError:
            # print(e)
            pass
