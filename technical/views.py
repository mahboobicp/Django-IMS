from django.shortcuts import render, redirect
from .models import Plot

def base(request):
    return render(request, 'base.html')

def index(request):
    return render(request, 'technical/index.html')


def plotregestration(request):
    return render(request, 'technical/plotregestration.html')

def test(request):
    return render(request, 'technical/test.html')

def add(request):
    if request.method == 'POST':
        plot_number = request.POST.get('plot_number')
        location = request.POST.get('location')
        plot_status = request.POST.get('plot_status')
        land_type = request.POST.get('land_type')

        plot1 = Plot(
            plot_number = plot_number,
            location = location,
            plot_status = plot_status,
            land_type = land_type
        )
        plot1.save()
        return redirect('test')
    return render(request, 'technical/test.html')

