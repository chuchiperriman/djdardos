from djbolos.bolos.models import *
from django.contrib import admin


class JugadorAdmin(admin.ModelAdmin):
    #fields = ['pub_date', 'question']
    list_display = ('nombre', 'equipo', 'fecha_alta')
    list_filter = ['equipo']
    search_fields = ['nombre']
    date_hierarchy = 'fecha_alta'



admin.site.register(Jugador, JugadorAdmin)
admin.site.register(Equipo)
admin.site.register(TipoPartida)
