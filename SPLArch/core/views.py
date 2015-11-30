# Create your views here.
from django.shortcuts import render,render_to_response
from django.http import HttpResponseRedirect

def home(request):
	return render_to_response('core/index.html')