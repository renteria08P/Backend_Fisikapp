from parametros.models import Parametro


def get_parametro(clave):
    try:
        return Parametro.objects.get(clave=clave).valor
    except Parametro.DoesNotExist:
        return None