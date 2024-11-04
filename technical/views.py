from django.shortcuts import render, redirect,get_object_or_404
from .models import Plot
from django.utils import timezone

def base(request):
    return render(request, 'base.html')

def index(request):
    plot_data = Plot.objects.all().order_by('-plot_number')[:10]

    plot_data_dic = {
        'plot_data' : plot_data
    }
    return render(request, 'technical/index.html', plot_data_dic)


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

         # Get the last plot entry, ordered by ID in descending order
        last_plot = Plot.objects.order_by('-plot_number').first()
    
        # If there’s an existing plot, increment the ID; otherwise, start with 1
        #new_id = (last_plot.id + 1) if last_plot else 1
        pid =f"NOW-IE-{plotnumber}"
        plot1 = Plot(
            plot_number = pid,
            location = loc,
            plot_status = plotstatus,
            land_type = landtype,
            plot_area = plotarea,
            coverd_area = coverdarea,
            created_at = timezone.now(),
        )
        plot1.save()
        return redirect('/technical')
    return render(request, 'technical/test.html')
def edit(request):
    plot_data = Plot.objects.all().order_by('-plot_number')[:10]

    plot_data_dic = {
        'plot_data' : plot_data
    }
    return render(request, 'technical/index.html', plot_data_dic)

def update(request):
    plotnumber = request.POST.get('plotnumber')
    plot = get_object_or_404(Plot, plot_number=plotnumber)  # Get the plot record or return 404 if not found
    print(plot)
    if request.method == 'POST':
        plotnumber = request.POST.get('plotnumber')
        loc = request.POST.get('loc')
        plotstatus = request.POST.get('plotstatus')
        landtype = request.POST.get('landtype')
        plotarea = request.POST.get('plotarea')
        coverdarea = request.POST.get('coverdarea')

        plot1 = Plot(
            plot_number = plotnumber,
            location = loc,
            plot_status = plotstatus,
            land_type = landtype,
            plot_area = plotarea,
            coverd_area = coverdarea,
            updated_at = timezone.now(),
        )
        plot1.save()
        return redirect('/technical')


    

    


