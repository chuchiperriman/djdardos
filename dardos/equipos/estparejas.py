from dardos.models import *

def get_porcentaje(valor, total):
    if total == 0:
        return 0
    return valor * 100 / total
    
class EstadisticaPareja:

    def __init__(self, pareja):
        self.pareja = pareja
        self.ganadas_local=0
        self.ganadas_vis=0
        self.perdidas_local=0
        self.perdidas_vis=0
        self.ganadas_501=0
        self.ganadas_cricket=0
        self.perdidas_501=0
        self.perdidas_cricket=0
        
    def jugador1(self):
        return self.pareja[0]
    def jugador2(self):
        return self.pareja[1]
    def han_jugado (self):
        return self.total > 0
        
    def calcular(self):
        self.ganadas_total = self.ganadas_local + self.ganadas_vis
        self.perdidas_total = self.perdidas_local + self.perdidas_vis
        self.total = self.ganadas_total + self.perdidas_total
        self.total_cricket = self.ganadas_cricket + self.perdidas_cricket
        self.ganadas_diff = self.ganadas_total - self.perdidas_total
        self.ganadas_diff_cricket = self.ganadas_cricket - self.perdidas_cricket
        self.ganadas_por = get_porcentaje(self.ganadas_total, self.total)
        self.ganadas_por_cricket = get_porcentaje(self.ganadas_cricket, self.total_cricket)
        self.perdidas_por = get_porcentaje(self.perdidas_total, self.total)
        self.perdidas_por_cricket = get_porcentaje(self.perdidas_cricket, self.total_cricket)
        
class EstadisticaDatosTotal:
    def __init__(self):
        self.dato = 0
        self.parejas = None
        
    def comparar_mejor (self, pareja, dato):
        if not self.parejas or dato > self.dato:
            self.dato = dato
            self.parejas = [pareja]
        elif dato == self.dato:
            self.parejas.append(pareja)
    def comparar_peor (self, pareja, dato):
        if not self.parejas or dato < self.dato:
            self.dato = dato
            self.parejas = [pareja]
        elif dato == self.dato:
            self.parejas.append(pareja)
            
class EstadisticaParejasTotal:
    
    def __init__(self):
        self.parejas = list()
        self.mas_ganadas = EstadisticaDatosTotal()
        self.menos_ganadas = EstadisticaDatosTotal()
        self.mejor_dif = EstadisticaDatosTotal()
        self.peor_dif = EstadisticaDatosTotal()
        self.mejor_por = EstadisticaDatosTotal()
        self.peor_por = EstadisticaDatosTotal()
        self.mejor_dif_cricket = EstadisticaDatosTotal()
        self.peor_dif_cricket = EstadisticaDatosTotal()
        self.mejor_por_cricket = EstadisticaDatosTotal()
        self.peor_por_cricket = EstadisticaDatosTotal()
    
    def calcular(self):
        for d in self.parejas:
            self.mas_ganadas.comparar_mejor(d.pareja, d.ganadas_total)
            self.mejor_dif.comparar_mejor(d.pareja, d.ganadas_diff)
            self.mejor_por.comparar_mejor(d.pareja, d.ganadas_por)
            self.mejor_dif_cricket.comparar_mejor(d.pareja, d.ganadas_diff_cricket)
            self.mejor_por_cricket.comparar_mejor(d.pareja, d.ganadas_por_cricket)
            #Si son 0 las dos es que no han jugado
            if d.han_jugado():
                self.menos_ganadas.comparar_peor(d.pareja, d.ganadas_total)
                self.peor_dif.comparar_peor(d.pareja, d.ganadas_diff)
                self.peor_dif_cricket.comparar_peor(d.pareja, d.ganadas_diff_cricket)
                #Aqui es comparar_mejor porque el peor es el que tiene mas perdidas
                self.peor_por.comparar_mejor(d.pareja, d.perdidas_por)
                self.peor_por_cricket.comparar_mejor(d.pareja, d.perdidas_por_cricket)
    
def get_estadistica_parejas(equipo, liga):
    #e = Equipo.objects.filter(nombre="Paris")[0]
    jugadores = equipo.jugador_set.all()
    parejas = dict()
    for j in jugadores:
        for j2 in jugadores:
            if j != j2:
                key = str(j.id) + '-' + str(j2.id)
                key2 = str(j2.id) + '-' + str(j.id)
                if key not in parejas and key2 not in parejas:
                    parejas[key] = [j,j2]

    esttotal = EstadisticaParejasTotal()

    for pareja in parejas.values():
        partidas_local = Partida.objects.filter(
            Q(tipo=TIPO_PARTIDA_PAREJAS) &
            Q(partido__jornada__liga=liga) &
            Q(jugadores_local=pareja[0])).filter(Q(jugadores_local=pareja[1])).distinct()
        partidas_vis = Partida.objects.filter(
            Q(tipo=TIPO_PARTIDA_PAREJAS) &
            Q(partido__jornada__liga=liga) &
            Q(jugadores_visitante=pareja[0])).filter(Q(jugadores_visitante=pareja[1])).distinct()
        
        datos = EstadisticaPareja(pareja)
        
        for p in partidas_local:
            if pareja[0] in p.ganadores.all():
                datos.ganadas_local += 1
                if int(p.tipo_juego) == TIPO_JUEGO_501:
                    datos.ganadas_501 += 1
                else:
                    datos.ganadas_cricket += 1
            else:
                datos.perdidas_local += 1
                if int(p.tipo_juego) == TIPO_JUEGO_501:
                    datos.perdidas_501 += 1
                else:
                    datos.perdidas_cricket += 1
        for p in partidas_vis:
            if pareja[0] in p.ganadores.all():
                datos.ganadas_vis += 1
                if int(p.tipo_juego) == TIPO_JUEGO_501:
                    datos.ganadas_501 += 1
                else:
                    datos.ganadas_cricket += 1
            else:
                datos.perdidas_vis += 1
                if int(p.tipo_juego) == TIPO_JUEGO_501:
                    datos.perdidas_501 += 1
                else:
                    datos.perdidas_cricket += 1
                
        datos.calcular()
        esttotal.parejas.append(datos)
    esttotal.calcular()
    return esttotal
    
