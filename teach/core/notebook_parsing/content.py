from teach.models import Content, ContentType
from teach.core.render_content import FormatParser
from teach.core.manage_organization import get_map_md

from .base import NotebookConverter


class ContentNotebook(NotebookConverter):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.content_type_map = {
            "ct_{}".format(ct.pk): ct for ct in ContentType.objects.all()
        }

        self.content_type_vars = {
            ct.pk: ctvar for ctvar, ct in self.content_type_map.items()
        }

        self.format_map = {"ft_{}".format(f): f for f in FormatParser.format_choices}

        self.format_vars = {f: fvar for fvar, f in self.format_map.items()}

        self.ct_ass_codeblock = "\n".join(
            [
                '{} = ContentType.objects.get(pk="{}")  # {}'.format(
                    vname, pk, ContentType.objects.get(pk=pk).name
                )
                for pk, vname in self.content_type_vars.items()
            ]
        )

        self.ft_ass_codeblock = "\n".join(
            ['{} = "{}"'.format(fvar, f) for f, fvar in self.format_vars.items()]
        )

    def parse_cellset(self, cellset, pk):
        meta_cell = cellset[0]["source"]
        text_src = cellset[1]["source"]

        kwargs = eval(
            "dict({})".format(",".join(meta_cell)),
            {**self.content_type_map, **self.format_map},
        )

        kwargs["text"] = "".join(text_src)

        return kwargs

    def parse_object_to_cells(self, o):

        meta_code = "\n".join(
            [
                "title = '{}'".format(o.title),
                "content_type = {}".format(
                    self.content_type_vars[o.content_type.pk]
                ),  # FIXME: not very informative
                "format = {}".format(self.format_vars[o.format]),
            ]
        )

        # TODO: some parser shit here
        if o.format == "md":
            content_cell = self.md_cell_from_src(o.text)
        else:
            content_cell = self.md_cell_from_src("# unknown format")

        return [self.code_cell_from_src(meta_code), content_cell]

    def preamble_cells(self):
        return [
            self.md_cell_from_src("### Possible content types:"),
            self.code_cell_from_src(self.ct_ass_codeblock, {"editable": False}),
            self.md_cell_from_src("### Possible content formats:"),
            self.code_cell_from_src(self.ft_ass_codeblock, {"editable": False}),
            self.md_cell_from_src("## Map of occurrences content in this notebook:"),
            self.md_cell_from_src(get_map_md(self.object_set)),
            self.md_cell_from_src("## Content cells:"),
        ]

    needed_classes = ["ContentType", "Content"]
    obj_model = Content
