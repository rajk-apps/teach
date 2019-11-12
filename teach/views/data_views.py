from django.http import HttpResponse
import json

from teach.core.jelm_parsing import full_jelm_exporter


def jelm_export(request):
    jelm_dump = full_jelm_exporter()
    return HttpResponse(json.dumps(jelm_dump))
