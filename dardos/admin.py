from djdardos.dardos.models import *
from django.contrib import admin


class JugadorAdmin(admin.ModelAdmin):
    #fields = ['pub_date', 'question']
    list_display = ('nombre', 'equipo', 'fecha_alta')
    list_filter = ['equipo']
    search_fields = ['nombre']
    date_hierarchy = 'fecha_alta'



admin.site.register(Jugador, JugadorAdmin)
admin.site.register(Equipo)
admin.site.register(Division)
admin.site.register(Liga)
admin.site.register(Partido)
admin.site.register(Partida)
admin.site.register(Jornada)
admin.site.register(EquipoJugadorLiga)
admin.site.register(UserProfile)
