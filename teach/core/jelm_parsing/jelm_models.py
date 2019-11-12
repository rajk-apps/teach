from teach.models import *
from django.db import models

from teach.util import all_subclass_dic


class NotJelmModelError(Exception):

    pass


class TeachModelJelm:
    def __init__(self, teach_cls):

        try:
            assert teach_cls.jelm_type in ["edge", "node"]
        except AttributeError:
            print("{} not a jelm model".format(teach_cls.__name__))
            raise NotJelmModelError(teach_cls.__name__)
        except AssertionError:
            raise ValueError(
                "unknown jelm_type {} in model {}".format(
                    teach_cls.jelm_type, teach_cls.__name__
                )
            )

        self.cls = teach_cls
        self.name = teach_cls.__name__.lower()
        self.is_edge = self.cls.jelm_type == "edge"

        self.source_attid = None
        self.source_model = None
        self.target_attid = None
        self.target_model = None

        self.additional_edges = []

        if self.is_edge:
            self.get_edge_ends()
        else:
            self.get_additional_edges()

    def get_edge_ends(self):

        for attid, att in self.cls.__dict__.items():

            if isinstance(
                att, models.fields.related_descriptors.ForwardManyToOneDescriptor
            ):
                model_name = att.field.related_model.__name__.lower()
                if self.source_attid is None:
                    self.source_attid = attid
                    self.source_model = model_name
                elif self.target_attid is None:
                    self.target_attid = attid
                    self.target_model = model_name
                else:
                    raise ValueError("too many ends on model {}".format(self.name))

    def get_additional_edges(self):

        for attid, att in self.cls.__dict__.items():

            target_model_name = None
            if isinstance(
                att, models.fields.related_descriptors.ManyToManyDescriptor
            ) & (not attid.endswith("_set")):

                target_model_name = att.rel.model.__name__.lower()

            if isinstance(
                att, models.fields.related_descriptors.ForwardManyToOneDescriptor
            ) & (not attid.endswith("_set")):
                target_model_name = att.field.related_model.__name__.lower()

            if target_model_name:
                self.additional_edges.append(
                    {"attid": attid, "model": target_model_name}
                )


class TeachModelSet:
    def __init__(self):

        self.jelm_cls_dic = {}
        for k, v in all_subclass_dic(models.Model, "teach").items():
            try:
                self.jelm_cls_dic[k] = TeachModelJelm(v)
            except NotJelmModelError:
                pass

    def get(self, k: str) -> TeachModelJelm:
        return self.jelm_cls_dic.get(k)
