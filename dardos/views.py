# -*- mode: python; tab-width: 4; indent-tabs-mode: nil -*-
from djdardos.dardos.models import *
from django.shortcuts import render_to_response, get_object_or_404

from django.http import HttpResponse, Http404
from django.views.generic import date_based, list_detail
from django.conf import settings
from django.views.generic.simple import direct_to_template
from djdardos.basic.blog.models import *


def index(request, page=0, paginate_by=5, **kwargs):
    #return render_to_response('dardos/index.html')
    page_size = getattr(settings,'BLOG_PAGESIZE', paginate_by)
    return list_detail.object_list(
        request,
        queryset=Post.objects.published(),
        paginate_by=page_size,
        page=page,
        template_name='dardos/index.html',
        extra_context={'divisiones': Division.objects.all()},
        **kwargs
    )
    
def ligas_index(request, **kwargs):
    divisiones = Division.objects.all()
    request.session.clear()
    return direct_to_template(request, 'dardos/divisiones/index.html',
        {'divisiones' : divisiones})
    
def post_detail(request, slug, year, month, day, **kwargs):
    """
    Displays post detail. If user is superuser, view will display 
    unpublished post detail for previewing purposes.
    """
    posts = None
    if request.user.is_superuser:
        posts = Post.objects.all()
    else:
        posts = Post.objects.published()
    return date_based.object_detail(
        request,
        year=year,
        month=month,
        day=day,
        date_field='publish',
        slug=slug,
        queryset=posts,
        **kwargs
    )
post_detail.__doc__ = date_based.object_detail.__doc__
