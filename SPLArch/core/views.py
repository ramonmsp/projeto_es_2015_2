from django.shortcuts import render,render_to_response
from PIL import Image,ImageDraw
from django.http import HttpResponse

from django import http
from django.template.loader import get_template
from django.template import Context
import ho.pisa as pisa
import cStringIO as StringIO
import cgi

def home(request):
	return render_to_response('core/index.html')


def pil_image(request):
    ''' A View that Returns a PNG Image generated using PIL'''
    size = (400,400)             # size of the image to create
    im = Image.new('RGB', size) # create the image
    draw = ImageDraw.Draw(im)   # create a drawing object that is
                                # used to draw on the new image
    cor = (26,255,10)    # color of our text
    text_pos = (100,200) # top-left position of our text
    text = "Pillow 3.0.0 Funcionando!" # text to draw
    # Now, we'll do the drawing: 
    draw.text(text_pos, text, fill=cor)
    
    del draw # I'm done drawing so I don't need this anymore
    
    # We need an HttpResponse object with the correct mimetype
    response = HttpResponse(mimetype="image/png")
    # now, we tell the image to save as a PNG to the 
    # provided file-like object
    im.save(response, 'PNG')

    return response # and we're done!

def gerar_pdf(template_src, context_dict):
    template = get_template(template_src)
    context = Context(context_dict)
    html  = template.render(context)
    result = StringIO.StringIO()
    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return http.HttpResponse(result.getvalue(), mimetype='application/pdf')
    return http.HttpResponse('Erro ao gerar pdf! %s' % cgi.escape(html))

def pdf(request):
    return gerar_pdf('core/pdf.html',{
        'titulo' : 'Testando o PISA',
        'app' : {
            'versao' : '3.0.3'
        }})