from django.shortcuts import render
from classify.models import Image
from .forms import FeedbackForm
from classify.models import Image

# Create your views here.
def feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.correct == "false":
            obj = Image.objects.get(pk=form.id)
            obj.correct = False
            obj.save()
    return render(request, 'feedback/feedback.html')