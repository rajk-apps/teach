from jelm import Jelm, Edge, Node

from .jelm_models import TeachModelSet

from typing import Union


class DjangoRecord:

    teach_models = TeachModelSet()

    def __init__(self,
                 model_name: str,
                 django_id,
                 jelm_id,
                 attributes):

        self.model_name = model_name
        self.django_id = django_id
        self.jelm_id = jelm_id
        self.attributes = attributes

        self.teach_jelm_cls = self.teach_models.get(self.model_name)

    @classmethod
    def from_django_dump_record(cls, record_dict: dict):

        model_name = record_dict['model'].split('.')[-1]
        django_id = record_dict['pk']
        jelm_id = '{}-{}'.format(model_name,
                                 django_id)

        attributes = record_dict['fields']
        return cls(model_name=model_name,
                   django_id=django_id,
                   jelm_id=jelm_id,
                   attributes=attributes)

    @classmethod
    def from_jelm_object(cls,
                         jelm_object: Union[Edge, Node]):

        jelm_id = jelm_object.id
        attributes = jelm_object.attributes.copy()
        model_name = attributes.pop('model')
        django_id = attributes.pop('pk')

        return cls(model_name=model_name,
                   django_id=django_id,
                   jelm_id=jelm_id,
                   attributes=attributes)

    def save_to_django_db(self):

        inst = self.teach_jelm_cls.cls(pk=self.django_id,
                                       **self.attributes)
        #inst.save()

    def _get_jelm_edge(self):

        record_atts = self.attributes.copy()

        if self.teach_jelm_cls.is_edge:

            source_django_id = record_atts.pop(self.teach_jelm_cls.source_attid)
            source_jelm_id = '{}-{}'.format(self.teach_jelm_cls.source_model,
                                            source_django_id)

            target_django_id = record_atts.pop(self.teach_jelm_cls.target_attid)
            target_jelm_id = '{}-{}'.format(self.teach_jelm_cls.target_model,
                                            target_django_id)

            record_atts[self.teach_jelm_cls.source_attid + '_id'] = source_django_id
            record_atts[self.teach_jelm_cls.target_attid + '_id'] = target_django_id

            return Edge(source=source_jelm_id,
                        target=target_jelm_id,
                        id=self.jelm_id,
                        attributes={
                            'pk': self.django_id,
                            'model': self.model_name,
                            **record_atts})

    def _get_plus_jelm_edges(self):

        record_atts = self.attributes.copy()

        edges = []

        if not self.teach_jelm_cls.is_edge:

            for add_edge_dic in self.teach_jelm_cls.additional_edges:
                attid = add_edge_dic['attid']
                target_model_name = add_edge_dic['model']

                id_or_list = record_atts.get(attid)

                if isinstance(id_or_list, str):
                    id_list = [id_or_list]
                elif isinstance(id_or_list, list):
                    id_list = id_or_list
                elif id_or_list is None:
                    id_list = []
                else:
                    raise ValueError('should be list/str, is {}'.format(type(id_or_list)))

                for target_django_id in id_list:
                    target_jelm_id = '{}-{}'.format(target_model_name,
                                                    target_django_id)

                    edges.append(
                           Edge(source=self.jelm_id,
                                target=target_jelm_id,
                                attributes={'target_model': target_model_name,
                                            'target_django_id': target_django_id,
                                            'source_model': self.model_name,
                                            'source_django_id': self.django_id})
                    )
        return edges

    def add_jelm_nodes_to_instance(self, el: Jelm):

        record_atts = self.attributes.copy()

        if not self.teach_jelm_cls.is_edge:
            for add_edge_dic in self.teach_jelm_cls.additional_edges:
                attid = add_edge_dic['attid']
                try:
                    record_atts.pop(attid)
                except KeyError as e:
                    pass

            el.add_node(id=self.jelm_id,
                        attributes={
                            'pk': self.django_id,
                            'model': self.model_name,
                            **record_atts})

    def jelm_edges(self):

        if self.teach_jelm_cls.is_edge:
            return [self._get_jelm_edge()]
        else:
            return self._get_plus_jelm_edges()
