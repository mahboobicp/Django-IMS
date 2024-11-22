from django.shortcuts import render, redirect,get_object_or_404
from django.db.models import Sum, Count  # Import Sum and Count for aggregations
from .models import Plot
from django.utils import timezone
from django.db.models import Q
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import xlwt
from django.http import HttpResponse


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

from django.db.models import Sum

def dashboard(request):
    # Fetch total covered area from the database
    total_area = Plot.objects.aggregate(Sum('coverd_area'))['coverd_area__sum']  # Assuming 'coverd_area' is the field name
    total_plots = Plot.objects.filter(cluped=False, as_bifurcate=False).count()
    
    # Count of plots based on land type
    commercial_clumped_plot_count = Plot.objects.filter(land_type="Commercial", cluped=False, as_bifurcate=False).count()
    industrial_clumped_plot_count = Plot.objects.filter(land_type="Industrial", cluped=False, as_bifurcate=False).count()

    # Count of plots for each status
    vacant_count = Plot.objects.filter(plot_status="Vacant", cluped=False, as_bifurcate=False).count()
    available_count = Plot.objects.filter(plot_status="Available", cluped=False, as_bifurcate=False).count()
    under_construction_count = Plot.objects.filter(plot_status="Under Construction", cluped=False, as_bifurcate=False).count()
    operational_count = Plot.objects.filter(plot_status="Operational", cluped=False, as_bifurcate=False).count()

    # Total area for each status
    vacant_area = Plot.objects.filter(plot_status="Vacant", cluped=False, as_bifurcate=False).aggregate(Sum('coverd_area'))['coverd_area__sum']
    available_area = Plot.objects.filter(plot_status="Available", cluped=False, as_bifurcate=False).aggregate(Sum('coverd_area'))['coverd_area__sum']
    under_construction_area = Plot.objects.filter(plot_status="Under Construction", cluped=False, as_bifurcate=False).aggregate(Sum('coverd_area'))['coverd_area__sum']
    operational_area = Plot.objects.filter(plot_status="Operational", cluped=False, as_bifurcate=False).aggregate(Sum('coverd_area'))['coverd_area__sum']

    # Total area for each land type
    commercial_area = Plot.objects.filter(land_type="Commercial", cluped=False, as_bifurcate=False).aggregate(Sum('plot_area'))['plot_area__sum']
    industrial_area = Plot.objects.filter(land_type="Industrial", cluped=False, as_bifurcate=False).aggregate(Sum('plot_area'))['plot_area__sum']
    print(industrial_area)
    # Calculate percentages for each plot status
    vacant_percentage = round((vacant_count / total_plots * 100),2) if total_plots > 0 else 0
    available_percentage = round((available_count / total_plots * 100),2) if total_plots > 0 else 0
    under_construction_percentage = round((under_construction_count / total_plots * 100),2) if total_plots > 0 else 0
    operational_percentage = round((operational_count / total_plots * 100),2) if total_plots > 0 else 0

    # Calculate percentage of commercial vs industrial plots
    total_land_plots = commercial_clumped_plot_count + industrial_clumped_plot_count
    commercial_percentage = round((commercial_clumped_plot_count / total_land_plots * 100),2) if total_land_plots > 0 else 0
    industrial_percentage = round((industrial_clumped_plot_count / total_land_plots * 100),2) if total_land_plots > 0 else 0

    # Prepare the context with all data
    context = {
        'total_plots': total_plots,
        'total_area': total_area,
        'comm_plot': commercial_clumped_plot_count,
        'ind_plot': industrial_clumped_plot_count,
        'vacant_plot': vacant_count,
        'available_plot': available_count,
        'under_cons': under_construction_count,
        'operational_plot': operational_count,
        
        # Percentages for each status
        'vacant_percentage': vacant_percentage,
        'available_percentage': available_percentage,
        'under_construction_percentage': under_construction_percentage,
        'operational_percentage': operational_percentage,
        
        # Commercial vs Industrial Plot Distribution
        'commercial_percentage': commercial_percentage,
        'industrial_percentage': industrial_percentage,
        
        # Area data for each plot status
        'vacant_area': vacant_area or 0,
        'available_area': available_area or 0,
        'under_construction_area': under_construction_area or 0,
        'operational_area': operational_area or 0,
        
        # Area data for each land type
        'commercial_area': commercial_area or 0,
        'industrial_area': industrial_area or 0,
    }

    return render(request, 'technical/dashboard.html', context)

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
        )
        plot1.save()
        plot.save()
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
       
    


def plotdetails(request):
    # Start with all plots
    plots = Plot.objects.all()
    print(plots)
    # Get filter values from the request, if any
    plot_status = request.GET.get('plot_status')
    land_type = request.GET.get('land_type')
    plot_number = request.GET.get('plot_number')

    # Apply filters only if a value is selected
    if plot_status:
        plots = plots.filter(plot_status=plot_status)
    if land_type:
        plots = plots.filter(land_type=land_type)
    if plot_number:
        plots = plots.filter(plot_number__icontains=plot_number)
    else:
         plots = Plot.objects.all()

    context = {
        'plots': plots,
        'plot_status': plot_status,
        'land_type': land_type,
        'plot_number': plot_number,
    }
    print(context)
    return render(request, 'technical/plotdetails.html', context)

def plot_search(request):
    query = request.GET.get("query", "")  # Get search query from GET parameters
    if query:
        # Perform a wildcard search across relevant fields
        plots = Plot.objects.filter(
            Q(plot_number__icontains=query) |
            Q(location__icontains=query) |
            Q(plot_status__icontains=query) |
            Q(plot_area__icontains=query) |
            Q(land_type__icontains=query)
        )
    else:
        plots = Plot.objects.all()  # Return all plots if no query provided

    context = {
        "plots": plots,
    }
    return render(request, "technical/plotdetails.html", context)

def plot_search_index(request):
    query = request.GET.get("query", "")  # Get search query from GET parameters
    if query:
        # Perform a wildcard search across relevant fields
        plots = Plot.objects.filter(
            Q(plot_number__icontains=query) |
            Q(location__icontains=query) |
            Q(plot_status__icontains=query) |
            Q(plot_area__icontains=query) |
            Q(land_type__icontains=query)
        )
    else:
        plots = Plot.objects.all()  # Return all plots if no query provided

    context = {
        "plot_data": plots,
    }
    return render(request, "technical/index.html", context)

def export_plot_to_excel(request):
    # Create the HttpResponse object with the appropriate Excel content type
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="plots.xls"'

    # Create a workbook and a worksheet
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Plots')

    # Define the header style
    header_style = xlwt.XFStyle()
    font = xlwt.Font()
    font.bold = True
    header_style.font = font

    # Write the header row
    columns = ['Plot Number', 'Location', 'Plot Status', 'Land Type', 'Plot Area', 'Covered Area', 'Created At', 'Updated At']
    for col_num, column_title in enumerate(columns):
        ws.write(0, col_num, column_title, header_style)

    # Write the data rows
    rows = Plot.objects.values_list('plot_number', 'location', 'plot_status', 'land_type', 'plot_area', 'coverd_area', 'created_at', 'updated_at')
    for row_num, row in enumerate(rows, start=1):
        for col_num, cell_value in enumerate(row):
            ws.write(row_num, col_num, str(cell_value) if cell_value else '')

    # Save the workbook to the response
    wb.save(response)
    return response   