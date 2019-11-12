

def all_subclass_dic(cls,
                     from_module=None):
    children = cls.__subclasses__()

    if from_module:
        children = filter(lambda c: from_module in c.__module__,
                          children)

    out_dic = {c.__name__.lower(): c for c in
               children}

    for n, c in out_dic.items():
        out_dic = {**out_dic,
                   **all_subclass_dic(c)}
    return out_dic


def add_to_level(elem, l1, organize_attr='topic'):
    added = False
    for l2 in l1['content']:
        if l2['name'] == elem.__getattribute__(organize_attr).name:
            if elem.id not in l2['eids']:
                l2['content'].append(elem)
                l2['eids'].append(elem.id)
            added = True
    if not added:
        try:
            desc = elem.__getattribute__(organize_attr).description
        except AttributeError:
            desc = ''
        l1['content'].append({'name': elem.__getattribute__(organize_attr).name,
                              'description': desc,
                              'content': [elem],
                              'eids': [elem.id]})