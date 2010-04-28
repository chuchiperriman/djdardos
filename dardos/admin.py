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
admin.site.register(Liga)
admin.site.register(Partido)
admin.site.register(PartidaIndividual)
admin.site.register(PartidaParejas)
