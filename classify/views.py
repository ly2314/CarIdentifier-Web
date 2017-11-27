from django.shortcuts import render
from django.http import HttpResponse
from .models import Image

# Create your views here.

def classify(request):
    from .forms import UploadFileForm
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            from .utils import save_file
            img_url, img_path = save_file(request.FILES['image'])
            from .utils import classify
            is_car = classify(img_path)
            if is_car is None:
                return render(request, 'classify/error.html', {'error_message': "error occured" })
            model = Image(is_car=is_car, source=img_url, correct=True)
            model.save()
            return render(request, 'classify/result.html', {'image': model })
    else:
        form = UploadFileForm()
    return render(request, 'classify/upload.html', {'form': form})