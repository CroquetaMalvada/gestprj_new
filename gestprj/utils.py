from gestprj.models import TUsuarisXarxa,Responsables

def usuari_xarxa_a_user(request):
    username = request.user.username
    try:
        usuariXarxa = TUsuarisXarxa.objects.get(nom_xarxa=username)
        return usuariXarxa
    except:
        return None


def usuari_a_responsable(request):
    username = request.user.username
    try:
        usuariXarxa = TUsuarisXarxa.objects.get(nom_xarxa=username)
        responsable = Responsables.objects.get(id_usuari=usuariXarxa.id_usuari)
        return responsable
    except:
        return None
def id_resp_a_codi_responsable(id_r):
    try:
        codigo = Responsables.objects.get(id_resp=id_r)
        return codigo["id_resp"]
    except:
        return None