from .presentation_views import *
from .task_views import *
from .notebook_views import *
from .data_views import *

from django.http import HttpResponse
import random
import json


def status(request):
    i = random.randint(5, 10)
    print(request.data)
    return HttpResponse(json.dumps({"message": "WAAAHEY{}".format(i)}))
    # return HttpResponse('<head><meta http-equiv="refresh" content="1"></head>A-{}'.format(i))
