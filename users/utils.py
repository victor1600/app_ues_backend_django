from .models import CustomUser as User


def authenticate(email=None, password=None):
    # TODO: connect to external API, right now, we don't care about password.
    user = User.objects.filter(email=email).first()
    if user:
        return user
    return None
