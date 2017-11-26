from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect

# Create your views here.

def classify(request):
    from .forms import UploadFileForm
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            from .utils import save_file
            img_url, img_path = save_file(request.FILES['image'])
            from .utils import classify
            if classify(img_path) == True:
                return render(request, 'classify/result.html', {'is_car': True, 'uploaded_file_url': img_url })
            else:
                return render(request, 'classify/result.html', {'is_car': False, 'uploaded_file_url': img_url })
    else:
        form = UploadFileForm()
    return render(request, 'classify/upload.html', {'form': form})