from api.models import Aspirante, PuntuacionTemaAspirante, Tema, Nivel


def get_current_level_for_user(topic: Tema, user):
    """
    > If the user has a score for the topic, return the current level. Otherwise, return the basic level

    :param topic: Tema
    :type topic: Tema
    :param user: The user object
    :return: The current level for the user
    """
    aspirante = Aspirante.objects.filter(user=user).first()
    registro_puntuacion = PuntuacionTemaAspirante.objects.filter(tema=topic, aspirante=aspirante).first()
    if registro_puntuacion:
        return registro_puntuacion.nivel_actual

    return Nivel.DIFFICULTY_BASIC
