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
        plotnumber = request.POST.get('plotnumber')
        loc = request.POST.get('loc')
        plotstatus = request.POST.get('plotstatus')
        landtype = request.POST.get('landtype')
        plotarea = request.POST.get('plotarea')
        coverdarea = request.POST.get('coverdarea')

        print(f"Plot Number: {plotnumber}, Location: {loc}, Plot Status: {plotstatus}, Land Type: {landtype}")
        pid =f"NOW-IE-{plotnumber}"
        plot1 = Plot(
            plot_number = pid,
            location = loc,
            plot_status = plotstatus,
            land_type = landtype,
            plot_area = plotarea,
            coverd_area = coverdarea
        )
        plot1.save()
        return redirect('test')
    return render(request, 'technical/test.html')
    


