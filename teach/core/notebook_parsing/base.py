import json
import datetime
import time
import os
from IPython.display import Javascript, display

from teach.models import ContentType
from teach.util.utils import get_notebook_name


class NotebookConverter:

    PK_SUFFIX = "### "

    def __init__(self, object_set=None, filename=None):

        self.object_set = object_set
        self.filename = filename

        if object_set is not None:
            self.cell_list = self.parse_objects_to_nb_cells()

        else:
            self.refresh_from_file()

    @classmethod
    def from_current_file(cls):
        filename = get_notebook_name()

        return cls(filename=filename)

    def refresh_from_file(self):
        start_time = time.time()
        display(
            Javascript("IPython.notebook.save_notebook()"),
            include=["application/javascript"],
        )

        while os.path.getmtime(self.filename) < start_time:
            time.sleep(0.1)  # FIXME rather except json decode error
        time.sleep(0.5)

        with open(self.filename) as fp:
            self.cell_list = json.load(fp)["cells"]

    @classmethod
    def django_init_code(cls):
        return "\n".join(
            [
                "import django, os,sys",
                'sys.path.insert(0,"/{}".format(os.environ.get("DJANGO_PROJECT")))',
                "django.setup()",
                "from teach.models import {}".format(", ".join(cls.needed_classes)),
                "from teach.core.notebook_parsing import {}".format(cls.__name__),
                "nb_handler = {}.from_current_file()".format(cls.__name__),
            ]
        )

    def parse_objects_to_nb_cells(self):
        cells = [
            self.md_cell_from_src("## Explanation here!!"),
            self.code_cell_from_src(self.django_init_code(), {"editable": False}),
            # TODO: run these automatically nbextensions
            *self.preamble_cells(),
        ]

        for o in self.object_set:
            cells += self.get_framed_object_cells(o)

        return cells

    @classmethod
    def get_framed_object_cells(cls, o):
        return [
            cls.md_cell_from_src(
                "{}{}".format(cls.PK_SUFFIX, o.pk), {"editable": False}
            ),
            *cls.parse_object_to_cells(o),
            cls.code_cell_from_src(
                'nb_handler.save_object("{}")'.format(o.pk), {"editable": False}
            ),
            cls.md_cell_from_src("---", {"editable": False}),
        ]

    @classmethod
    def get_framed_object_kwargs(cls, cellset):

        pk = cellset[0]["source"][0].replace(cls.PK_SUFFIX, "")

        obj_data = cls.parse_cellset(cellset[1:], pk)

        return {"pk": pk, **obj_data}

    def save_object(self, object_pk):

        self.refresh_from_file()

        for idx, c in enumerate(self.cell_list):
            if c["source"][0] == "{}{}".format(self.PK_SUFFIX, object_pk):
                try:
                    obj = self.obj_model(
                        **self.get_framed_object_kwargs(self.cell_list[idx:])
                    )
                except Exception as e:
                    print("cant parse cells!")
                    print(type(e).__name__)
                    print(e)
                    raise e
                obj.save()
                print(
                    "{} saved {}".format(
                        self.obj_model.__name__, datetime.datetime.now().isoformat()
                    )
                )
                print(obj)

    @classmethod
    def code_cell_from_src(cls, code_src, meta_dic=None):
        return {
            "source": code_src,
            "cell_type": "code",
            "metadata": meta_dic or {},
            "outputs": [],
            "execution_count": None,
        }

    @classmethod
    def md_cell_from_src(cls, md_src, meta_dic=None):
        return {"source": md_src, "cell_type": "markdown", "metadata": meta_dic or {}}

    needed_classes = ["ContentType"]
    obj_model = ContentType

    @classmethod
    def parse_cellset(cls, cellset, pk):
        return {}

    @classmethod
    def parse_object_to_cells(cls, o):
        return []

    @classmethod
    def preamble_cells(cls):
        return []
