from jelm import Jelm, reads_json
import datetime

from teach.util.django_utils import get_django_dump_of_app

from .django_record_class import DjangoRecord


def full_jelm_exporter():

    django_dump = get_django_dump_of_app("teach")

    el = Jelm(metadata={"created": datetime.datetime.now().isoformat()})
    plus_edges = []

    for django_record_dic in django_dump:

        record_inst = DjangoRecord.from_django_dump_record(django_record_dic)
        record_inst.add_jelm_nodes_to_instance(el)
        plus_edges += record_inst.jelm_edges()

    for e in plus_edges:
        el.add_object(e)

    return el.dict()


def jelm_importer(jelm_dump):

    el = reads_json(jelm_dump)

    later_edges = []
    for o in el:
        if o.id:
            record_inst = DjangoRecord.from_jelm_object(o)
            record_inst.save_to_django_db()
        else:
            later_edges.append(o)

    for e in later_edges:
        pass
    # users = User.objects.filter(email__in=emails)
    # instance = Setupuser.objects.create(organization=org)

    # instance.emails_for_help.set(users)
