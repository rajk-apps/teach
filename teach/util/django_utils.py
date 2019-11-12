import io
import json
from django.core.management import call_command


def get_django_dump_of_app(appname):
    buf = io.StringIO()
    call_command("dumpdata", appname, stdout=buf)
    buf.seek(0)
    dump = json.loads(buf.read())
    buf.close()
    return dump
