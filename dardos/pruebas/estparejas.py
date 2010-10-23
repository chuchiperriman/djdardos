from dardos.models import *

def get_porcentaje(valor, total):
    if total == 0:
        return 0
    return valor * 100 / total
class DatosPareja:
    ganadas_local=0
    ganadas_vis=0
    perdidas_local=0
    perdidas_vis=0
    
    def __init__(self, pareja):
        self.pareja = pareja
        
    def calcular(self):
        self.ganadas_total = self.ganadas_local + self.ganadas_vis
        self.perdidas_total = self.perdidas_local + self.perdidas_vis
        self.total = self.ganadas_total + self.perdidas_total
        self.ganadas_diff = self.ganadas_total - self.perdidas_total
        self.ganadas_por = get_porcentaje(self.ganadas_total, self.total)
        self.perdidas_por = get_porcentaje(self.perdidas_total, self.total)
    def __str__(self):
        return "%40s:%5i%5i%5i%5i%5i%5i%5i%5i%5i" % (str(self.pareja), \
            self.ganadas_local, self.perdidas_local, \
            self.ganadas_vis, self.perdidas_vis,
            self.ganadas_total, self.perdidas_total,
            self.ganadas_diff,
            self.ganadas_por,
            self.perdidas_por)

e = Equipo.objects.filter(nombre="Paris")[0]
print e
jugadores = e.jugador_set.all()
parejas = dict()
for j in jugadores:
    for j2 in jugadores:
        if j != j2:
            key = str(j.id) + '-' + str(j2.id)
            key2 = str(j2.id) + '-' + str(j.id)
            if key not in parejas and key2 not in parejas:
                parejas[key] = [j,j2]
print parejas

lista_datos = list()

for pareja in parejas.values():
    partidas_local = Partida.objects.filter(
        Q(tipo=TIPO_PARTIDA_PAREJAS) &
        Q(jugadores_local=pareja[0])).filter(Q(jugadores_local=pareja[1])).distinct()
    partidas_vis = Partida.objects.filter(
        Q(tipo=TIPO_PARTIDA_PAREJAS) &
        Q(jugadores_visitante=pareja[0])).filter(Q(jugadores_visitante=pareja[1])).distinct()
    
    datos = DatosPareja(pareja)
    
    for p in partidas_local:
        if pareja[0] in p.ganadores.all():
            datos.ganadas_local += 1
        else:
            datos.perdidas_local += 1
    for p in partidas_vis:
        if pareja[0] in p.ganadores.all():
            datos.ganadas_vis += 1
        else:
            datos.perdidas_vis += 1
    datos.calcular()
    print datos
    lista_datos.append(datos)
    
pareja_mas_ganadas = None
pareja_menos_ganadas = None
pareja_mejor_dif = None
pareja_peor_dif = None
pareja_mejor_por = None
pareja_peor_por = None
for d in lista_datos:
    if not pareja_mas_ganadas:
        pareja_mas_ganadas = d
    elif d.ganadas_total > pareja_mas_ganadas.ganadas_total:
        pareja_mas_ganadas = d
    
    if not pareja_mejor_dif:
        pareja_mejor_dif = d
    elif d.ganadas_diff > pareja_mejor_dif.ganadas_diff:
        pareja_mejor_dif = d
        
    if not pareja_mejor_por:
        pareja_mejor_por = d
    elif d.ganadas_por > pareja_mejor_por.ganadas_por:
        pareja_mejor_por = d
    
    #Si son 0 las dos es que no han jugado
    if d.ganadas_total!=0 and d.perdidas_total!=0:
        if not pareja_menos_ganadas:
            pareja_menos_ganadas = d
        elif d.ganadas_total < pareja_menos_ganadas.ganadas_total:
            pareja_menos_ganadas = d
        
        if not pareja_peor_dif:
            pareja_peor_dif = d
        elif d.ganadas_diff < pareja_peor_dif.ganadas_diff:
            pareja_peor_dif = d
            
        if not pareja_peor_por:
            pareja_peor_por = d
        elif d.ganadas_diff < pareja_peor_por.ganadas_diff:
            pareja_peor_por = d

print 'pareja mas ganadas:', pareja_mas_ganadas
print 'pareja menos ganadas:', pareja_menos_ganadas
print 'pareja mejor diferencia:', pareja_mejor_dif
print 'pareja peor diferencia:', pareja_peor_dif
print 'pareja mejor porcentaje:', pareja_mejor_por
print 'pareja peor porcentaje:', pareja_peor_por
print "fin"


