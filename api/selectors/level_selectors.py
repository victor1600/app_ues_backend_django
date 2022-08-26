from api.models import Nivel


def get_mastered_levels(current_level: str):
    """
    It returns a list of all the levels that are mastered by the user, given the current level

    :param current_level: The current level of the user
    :type current_level: str
    :return: A list of mastered levels.
    """
    mastered_levels = {
        Nivel.DIFFICULTY_BASIC: [Nivel.DIFFICULTY_BASIC],
        Nivel.DIFFICULTY_INTERMEDIATE: [Nivel.DIFFICULTY_BASIC, Nivel.DIFFICULTY_INTERMEDIATE],
        Nivel.DIFFICULTY_ADVANCED: [Nivel.DIFFICULTY_BASIC, Nivel.DIFFICULTY_INTERMEDIATE, Nivel.DIFFICULTY_ADVANCED]
    }
    return mastered_levels.get(current_level)
