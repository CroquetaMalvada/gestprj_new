from gestprj.models import TUsuarisXarxa,Responsables
from django.db.models import Q
def usuari_xarxa_a_user(request):
    username = request.user.username
    try:
        usuariXarxa = TUsuarisXarxa.objects.get(nom_xarxa=username)
        return usuariXarxa
    except:
        return None


def usuari_a_responsable(request):
    username = request.user.username
    errores={}
    try:
        usuariXarxa = TUsuarisXarxa.objects.get(nom_xarxa=username)
        responsable = Responsables.objects.get(~Q(codi_resp=81), id_usuari=usuariXarxa.id_usuari) # Excluimos los responsables 81 ya que es u caso excepcion referente a maria mayol y marc estiarte (Ramon y cajal)
        return responsable
    except Exception as e:
        errores.update({'error': str(e)})
        return None
def id_resp_a_codi_responsable(id_r):
    try:
        codigo = Responsables.objects.get(id_resp=id_r)
        return codigo["id_resp"]
    except:
        return None