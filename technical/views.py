from django.shortcuts import render, redirect,get_object_or_404
from django.db.models import Sum, Count  # Import Sum and Count for aggregations
from .models import Plot
from django.utils import timezone
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def base(request):
    return render(request, 'base.html')

def index(request):
    plot_data = Plot.objects.filter(cluped=False,as_bifurcate=False).order_by('-plot_number')[:10]

    plot_data_dic = {
        'plot_data' : plot_data
    }
    return render(request, 'technical/index.html', plot_data_dic)


def plotregestration(request):
    return render(request, 'technical/plotregestration.html')

def dashboard(request):
      # Fetch plot data from the database
    total_area = Plot.objects.aggregate(Sum('coverd_area'))  # Assuming 'area' field is in Plot model
    total_plots = Plot.objects.filter(cluped=False).count()
    # Count of plots where land_type is "Commercial" and cluped is True
    commercial_clumped_plot_count = Plot.objects.filter(land_type="Commercial", cluped=False).count()
    industerial_clumped_plot_count = Plot.objects.filter(land_type="Industrial", cluped=False).count()

    # Count of plots for each status
    vacant_count = Plot.objects.filter(plot_status="Vacant",cluped=False).count()
    available_count = Plot.objects.filter(plot_status="Available",cluped=False).count()
    under_construction_count = Plot.objects.filter(plot_status="Under Construction",cluped=False).count()
    operational_count = Plot.objects.filter(plot_status="Operational",cluped=False).count()


    context = {
        'total_plots': total_plots,
        'total_area': total_area,
        'comm_plot': commercial_clumped_plot_count,
        'ind_plot' : industerial_clumped_plot_count,
        'vacant_plot' : vacant_count,
        'available_plot' : available_count,
        'under_cons' : under_construction_count,
        'operational_plot' : operational_count,
    }
    return render(request, 'technical/dashboard.html',context)

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


def delete_plot(request):
    if request.method == 'POST':
        plot_id = request.POST.get('plot_id')
        plot = get_object_or_404(Plot, plot_number=plot_id)  # Adjust field to your model
        plot.delete()
    return redirect('/technical')


def clup(request):
    if request.method == 'POST':
        # Parse the JSON data from the request body
        data = json.loads(request.body)
        plot_numbers = data.get('plot_numbers', [])

        # Query to get all the selected plots
        selected_plots = Plot.objects.filter(plot_number__in=plot_numbers)

        # Update the 'cluped' status for each selected plot
        selected_plots.update(cluped=True)

        # Calculate the sum of plot areas
        total_area = sum(plot.plot_area or 0 for plot in selected_plots)

        # Calculate the sum of plot areas
        coverd_area1 = sum(plot.coverd_area or 0 for plot in selected_plots)

        # Generate a new plot number with the format NOW-IE-Plot1-Plot2
        # Get only the plot numbers from the selected plots, excluding the NOW-IE prefix
        plot_number_list = [plot.plot_number[7:] for plot in selected_plots]  # Slicing off 'NOW-IE-'
        new_plot_number = 'NOW-IE-MRG-' + '-'.join(plot_number_list)  # Join selected plot numbers without the prefix

        # Create a new plot record using data from the first selected plot
        if selected_plots.exists():
            first_plot = selected_plots.first()  # Get the first plot for reference

            # Create a new plot instance with the desired fields
            new_plot = Plot(
                plot_number=new_plot_number,
                location=first_plot.location,
                plot_status=first_plot.plot_status,
                land_type=first_plot.land_type,
                plot_area=total_area,  # Use the summed area
                coverd_area=coverd_area1,  # Copy the covered area from the first plot
                cluped=False,  # Assuming the new plot is not marked as cluped initially
            )
            new_plot.save()
            return redirect('/technical')
        return redirect('/technical')
        


    
@csrf_exempt
def bifurcate_plots(request):
    if request.method == 'POST':
      
        data = json.loads(request.body)
        plot_numbers = data.get('plot_numbers', [])
        print(plot_numbers)
        try:
            # Update selected plots
            Plot.objects.filter(plot_number__in=plot_numbers).update(as_bifurcate=True)
            return JsonResponse({"status": "success"}, status=200)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
       
    


