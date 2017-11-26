from django.shortcuts import render
from classify.models import Image

# Create your views here.
def images(request):
    last_images = Image.objects.all().order_by('-id')[:10]
    return render(request, 'image/images.html', {'images': last_images})