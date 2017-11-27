from django.shortcuts import render
from classify.models import Image
from .forms import FeedbackForm
from classify.models import Image

# Create your views here.
def feedback(request):
    print("feedback start")
    if request.method == 'POST':
        print("is post")
        form = FeedbackForm(request.POST)
        if form.is_valid():
            print("is valid")
            correct = form.cleaned_data['correct']
            img_id = form.cleaned_data['id']
            print(correct)
            print(img_id)
            if correct == "false":
                print("not correct")
                obj = Image.objects.get(pk=img_id)
                obj.correct = False
                obj.save()
    return render(request, 'feedback/feedback.html')