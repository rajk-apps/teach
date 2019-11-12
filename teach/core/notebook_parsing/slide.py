import pprint

from teach.models import Slide

from .base import NotebookConverter


def parse_ss_to_code(ss):
    dic = {
            att: ss.__getattribute__(att)
            for att in ['ordernum', 'css_style',
                        'animate', 'print_title',
                        'fragment_no', 'upto_level']
        }

    return pprint.pformat(dic, width=20)


class SlideNotebook(NotebookConverter):


    @classmethod
    def parse_cellset(cls, cellset, pk):  # TODO: delete and redo all slidestructures
        layout_cell = cellset[0]['source']
        meta_cell = cellset[1]['source']

        return {}

    @classmethod
    def parse_object_to_cells(cls, o: Slide) -> list:

        meta_code = '\n'.join(
            [
                'title = "{}"'.format(o.title),
                'hastitle = {}'.format(o.hastitle)
            ]
        )

        layout_code = "layout = {}".format(o.layout)

        structure_code = '\n'.join(
            [
                parse_ss_to_code(ss)
                for idx, ss in
                enumerate(o.slidestructure_set.all().order_by('ordernum'))
            ]
        )

        preview_md = '\n'.join(
            ['**preview on [this](http://146.110.60.131:6969/teach/slide/{}) link on full screen**'.format(o.pk),
             '\nor iframe it in the notebook (might look different!)'
             ]
        )

        preview_code = "IFrame('http://146.110.60.131:6969/teach/slide/{}', **default_res)".format(o.pk)

        return [cls.code_cell_from_src(meta_code),
                cls.code_cell_from_src(structure_code),
                cls.code_cell_from_src(layout_code),
                cls.md_cell_from_src(preview_md),
                cls.code_cell_from_src(preview_code)]

    def preamble_cells(self):
        import_code = '\n'.join(
            ['from IPython.display import IFrame',
             'pxcount = 60',
             'default_res = {"width": 16 * pxcount, "height": 9 * pxcount}'
            ]
        )
        return [
            self.code_cell_from_src(import_code),
            self.md_cell_from_src('## Slide cells:')
        ]

    needed_classes = ['Slide', 'SlideStructure']
    obj_model = Slide
