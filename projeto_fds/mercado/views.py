from django.shortcuts import render
from .models import *
from django.views import View
from django.http import HttpResponse, Http404

# Create your views here.

class ViewFoto(View):
    def get(self, request, foto_id):
        try:
            foto = Foto.objects.get(pk=foto_id)
        except Foto.DoesNotExist:
            raise Http404("Foto não existe")
        context = {'Foto' : foto}
        return render(request, 'detail.html', context)