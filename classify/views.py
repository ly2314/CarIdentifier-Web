from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect

# Create your views here.
def index(request):
    return HttpResponse("Hello World")

def classify(request):
    from .forms import UploadFileForm
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            from .utils import save_file
            path = save_file(request.FILES['image'])
            from .utils import classify
            if classify(path) == True:
                return HttpResponse("Is Car")
            else:
                return HttpResponse("Not Car")
    else:
        form = UploadFileForm()
    return render(request, 'classify/upload.html', {'form': form})