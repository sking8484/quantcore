from django.shortcuts import render

def about_data_page(request):
    return render(request, 'about/about_data_page.html', {'about':'this is the about page'})

def about_strategies_page(request):
    return render(request, 'about/about_strategies_page.html', {'wait':'This page is in progress'})
