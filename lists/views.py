from django.shortcuts import render
from django.http import HttpResponse


def home_page(request):
    if request.method == 'POST':
        new_item_text = request.POST.get('item_text', '')
        context = {
            'new_item_text': new_item_text
        }
        return render(request, 'home.html', context=context)
    return render(request, 'home.html')
