# Create your views here.
from django.shortcuts import render,render_to_response
from django.http import HttpResponseRedirect,HttpResponse
from PIL import Image,ImageDraw

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