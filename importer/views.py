from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

from importer.models import DataSource
from importer.utils import gc, send_rows_to_sheet

from repertory.utils.drafthouse import AlamoDrafthouse, LOCATIONS
from repertory.utils.spreadsheet import GoogleSheet

@staff_member_required
def export_api(request):
    try:
        sheet = DataSource.objects.get(url__icontains=request.POST.get("sheet"))
    except DataSource.DoesNotExist:
        return JsonResponse({"error": "Sheet not found as data source."})
    sheet_id = sheet.sheet_id
    cols = ['Date', 'Time', 'Title', 'Venue', 'Format', 'Series', 'TMDB', 'Tickets']
    rows = []
    display_titles = request.POST.getlist('display-title')
    series_labels = request.POST.getlist('series-label')
    venues = request.POST.getlist('venue')
    for i in range(len(display_titles)):
        if not display_titles[i]:
            # we'll import empty values except for entries without titles
            continue
        dates = request.POST.getlist('date_%s' % i)
        times = request.POST.getlist('time_%s' % i)
        formats = request.POST.getlist('format_%s' % i)
        links = request.POST.getlist('link_%s' % i)
        for x in range(len(dates)):
            rows.append([dates[x], times[x], display_titles[i], venues[i],
                         formats[x], series_labels[i], "", links[x]])
    try:
        send_rows_to_sheet(sheet_id, cols, rows)
    except:
        raise
    else:
        return JsonResponse({"sheetUrl": sheet.url,
                             "postData": request.POST.lists()})

@staff_member_required
def bridge(request):
    try:
        sheets = gc().openall()
    except:
        sheets = []
    context = {"sheets": sheets, "bridge": True}
    return render(request, "bridge.html", context)

@staff_member_required
def user(request):
    context = {"bridge": False}
    return render(request, "bridge.html", context)

@staff_member_required
def index(request):
    return render(request, "index.html")

@staff_member_required
def drafthouse_api(request):
    results = []

    for theater_id, theater_name in LOCATIONS:
        theater = AlamoDrafthouse(theater_id)
        theater.fetch()
        theater.parse_html()
        theater.auto()

        results.append({
            "theater": theater_name,
            "ignore": theater.ignore.items(),
            "lookup": theater.lookup.items()
        })

    return JsonResponse(results, safe=False)
