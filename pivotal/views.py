from django.shortcuts import render

def stories(request):
    return render(request, 'pivotal_stories.html', {})