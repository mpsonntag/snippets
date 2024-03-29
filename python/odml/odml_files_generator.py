import random
import time
import uuid

from abc import ABC, abstractmethod
from os import getcwd, path

import odml
from odml.tools.rdf_converter import RDFReader, RDFWriter
from odml.tools.odmlparser import ODMLWriter

RANDOM_MAX = 1000000000  # might be collisions so better change to uuid
MAX_VALUE_LIST_NUMBER = 5
MAX_PROPERTY_LIST_NUMBER = 6
MIN_NUMBER_OF_ENTITIES_ON_THE_LEVEL = 2
# number of children for the entity until there are available children left
MIN_NUMBER_OF_CHILDREN = 2


def random_list_elem(list_obj):
    return random.choice(list_obj)


def first_list_elem(list_obj):
    return list_obj[0]


def crete_string_value(key, level):
    return key + '-lv-' + str(level) + '-' + str(random.randint(0, RANDOM_MAX))


def create_string_values_list(key, level):
    return [key + '-lv-' + str(level) + '-' + str(random.randint(0, RANDOM_MAX)) for _ in range(random.randint(0, MAX_VALUE_LIST_NUMBER))]


def create_int_value():
    return random.randint(0, RANDOM_MAX)


def create_random_date():
    year = random.randint(1950, 2010)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    return "{y}-{m}-{d}".format(y=year, m=month, d=day)


def create_int_values_list():
    return [random.randint(0, RANDOM_MAX) for _ in range(random.randint(0, MAX_VALUE_LIST_NUMBER))]


def generate_entity_list(entity, gen_func, n, level, entity_list=None):
    if entity_list is None:
        entity_list = []
    for _ in range(n):
        entity_list.append(gen_func(entity, level))

    return entity_list


class OdmlEntityExamples(ABC):

    @abstractmethod
    def create_from_samples(self, **kwargs):
        pass

    @abstractmethod
    def create_random_from_samples(self, **kwargs):
        pass

    # TODO move possible level to **kwargs, maybe other params would need to passed for generation
    @abstractmethod
    def create_random(self, level):
        pass

    def fill_kwargs(self, obj, **kwargs):
        if kwargs:
            for key, value in kwargs.items():
                if key in obj:
                    obj[key] = value

    def _get_obj_dict(self, example, decision_function=random_list_elem):
        return_obj = {}

        for key, value in example.obj.items():
            return_obj[key] = decision_function(value)

        return_obj['oid'] = str(uuid.uuid4())

        return return_obj

    def _get_full_random_obj_dict(self, example, level):
        return_obj = {}

        for key, value in example.obj.items():
            if key == 'value':
                pass
            elif key == 'date':
                return_obj[key] = create_random_date()
            elif key == 'dtype':
                t = random.randint(0, 1)
                if value[t] == 'int':
                    return_obj['dtype'] = 'int'
                    return_obj['value'] = create_int_values_list()
                elif value[t] == 'string':
                    return_obj['dtype'] = 'string'
                    return_obj['value'] = create_string_values_list('val', level)
            # elif isinstance(example, DocExample) and key == 'repository':
            #     return_obj['repository'] = 'repo1'
            else:
                return_obj[key] = crete_string_value(key, level)

        return_obj['oid'] = str(uuid.uuid4())

        return return_obj


class DocExample(OdmlEntityExamples):

    # def __init__(self, **kwargs):
    obj = {
        'version': ['1.0', '1.1', '1.2'],
        'author': ['Prof Jones', 'Dr Mc Gregory'],
        'date': ['2000-01-01', '2000-02-02'],
        # 'repository': ['rep1'],
    }

    # self.fill_kwargs(self.obj, **kwargs)

    def create_from_samples(self, **kwargs):
        return odml.Document(**self._get_obj_dict(self, first_list_elem))

    def create_random_from_samples(self, **kwargs):
        return odml.Document(**self._get_obj_dict(self, random_list_elem))

    def create_random(self, level):
        return odml.Document(**self._get_full_random_obj_dict(DocExample, level))


class SectionExample(OdmlEntityExamples):

    # def __init__(self, **kwargs):
    obj = {
        'type': ['hardware', 'settings', 'DataAcquisition'],
        'name': ['exp-details1', 'exp-details2', 'exp-details3'],
        'definition': ['def1', 'def2'],
    }

    # self.fill_kwargs(self.obj, **kwargs)

    def create_from_samples(self, **kwargs):
        return odml.Section(**self._get_obj_dict(self, first_list_elem))

    def create_random_from_samples(self, **kwargs):
        return odml.Section(**self._get_obj_dict(self, random_list_elem))

    def create_random(self, level):
        s = odml.Section(**self._get_full_random_obj_dict(SectionExample, level))
        # need this because there is no way to specify property field in constructor
        generate_entity_list(PropertyExample(),
                             PropertyExample.create_random,
                             random.randint(1, MAX_PROPERTY_LIST_NUMBER),
                             level,
                             entity_list=s)
        return s


class PropertyExample(OdmlEntityExamples):

    # def __init__(self, **kwargs):
    obj = {
        'name': [],
        'unit': [],
        'definition': [],
        'dtype': ['string', 'int'],  # randomly choosing of a new property
        'value': {'string': [], 'int': []}
    }

    # self.fill_kwargs(self.obj, **kwargs)

    def create_from_samples(self, **kwargs):
        """
        :param kwargs:
            random: True or False
            prop_type: 'string' or 'int'
        :return:
        """
        raise NotImplementedError("In method " + self.create_from_samples.__name__)

    def create_random_from_samples(self, **kwargs):
        raise NotImplementedError("In method " + self.create_random_from_samples.__name__)

    def create_random(self, level):
        return odml.Property(**self._get_full_random_obj_dict(PropertyExample, level))


class OdmlFilesGenerator:

    def __init__(self):
        self.width = None
        self.height = None
        self.randomness = None
        self.number_entities = None
        self.max_sec_sec_children = None
        self.max_sec_prop_children = None
        self.tree = []

    def to_rdf(self, doc, filename, format='turtle'):
        RDFWriter(doc).write_file(filename, format)

    def _add_sections(self):
        pass

    def _add_properties(self):
        pass

    def _create_empty_tree(self, height):
        self.tree = [[] * height]

    def _merge_entities(self, tree):
        if len(tree) == 1:
            return tree

        for lindex in range(1, len(tree)):
            # parents less than children
            #  TODO move to another function condition below
            if len(tree[lindex - 1]) < len(tree[lindex]):
                children_n = int(len(tree[lindex]) / len(tree[lindex - 1]))
                if children_n < MIN_NUMBER_OF_CHILDREN:
                    children_n = MIN_NUMBER_OF_CHILDREN
                i = 0
                parent = tree[lindex - 1][i]
                for eindex in range(len(tree[lindex])):  # iterating through children
                    parent.append(tree[lindex][eindex])
                    # making parents have equal number of children, last have the rest
                    if (eindex + 1) % children_n == 0 and i + 1 < len(tree[lindex - 1]):
                        i += 1
                        parent = tree[lindex - 1][i]
            else:  # parents more or equal number comparing to children
                i = 0
                parent = tree[lindex - 1][i]
                for eindex in range(len(tree[lindex])):  # iterating through children
                    parent.append(tree[lindex][eindex])
                    if (eindex + 1) % MIN_NUMBER_OF_CHILDREN == 0 and i + 1 < len(tree[lindex - 1]):
                        i += 1
                        parent = tree[lindex - 1][i]

        return tree

    def merge_rdf_files(self):
        """
        Create one big graph from multiple rdf files. Merges without serializing rdf files
        :return:
        """
        pass

    def generate(self, width, height, randomness, number_entities,
                 max_min_sec_sec_children=(10, 2), max_min_sec_prop_children=(10, 1),
                 from_samples=False, random_number_of_children=False):
        self.width = width
        self.height = height
        self.randomness = randomness
        self.number_entities = number_entities
        self.max_sec_sec_children = max_min_sec_sec_children
        self.max_sec_prop_children = max_min_sec_prop_children

    def _tree_section_append(self, width, height):
        sec = SectionExample()
        sec_random = SectionExample.create_random

        curr_list = generate_entity_list(sec, sec_random, width, height)
        self.tree.append(curr_list)

    def generate_by_width_height_entitiesnumber(self, width, height, randomness, number_entities):
        self.width = width
        self.height = height
        self.randomness = randomness
        self.number_entities = number_entities

        # self._create_empty_tree(height)

        if number_entities < width:
            #  TODO return one level
            pass

        entities_left = number_entities - width  # nodes left to build a tree
        levels_left = height - 1  # number of levels to fill,
        # maximum of nodes on the current level depending of levels_left and entities_left
        # maybe introduce better system - bias to create more like tree structure (top level < bottom)
        level_max = int(entities_left / levels_left)
        if level_max < MIN_NUMBER_OF_ENTITIES_ON_THE_LEVEL:
            level_max = MIN_NUMBER_OF_ENTITIES_ON_THE_LEVEL

        while levels_left > 0:

            current_level_n = random.randint(MIN_NUMBER_OF_ENTITIES_ON_THE_LEVEL, level_max)
            if current_level_n > width:
                current_level_n = width

            self._tree_section_append(current_level_n, height - levels_left)

            entities_left -= current_level_n
            level_max = int(entities_left / levels_left)
            levels_left -= 1

            if level_max < MIN_NUMBER_OF_ENTITIES_ON_THE_LEVEL:
                level_max = MIN_NUMBER_OF_ENTITIES_ON_THE_LEVEL

            if entities_left < MIN_NUMBER_OF_ENTITIES_ON_THE_LEVEL:
                break

        if entities_left > width:
            self._tree_section_append(width, height - levels_left)
        elif entities_left > MIN_NUMBER_OF_ENTITIES_ON_THE_LEVEL:
            self._tree_section_append(entities_left, height - levels_left)

        # append max level, might be any level
        self._tree_section_append(width, height - levels_left + 1)

        self.tree = self._merge_entities(self.tree)

        doc = DocExample().create_random(0)
        for s in self.tree[0]:
            doc.append(s)

        self.tree = []

        return doc

    def generate_by_width_children(self, width, randomness,
                                   max_min_sec_sec_children=(10, 2),
                                   max_min_sec_prop_children=(10, 1)):
        self.max_sec_sec_children = max_min_sec_sec_children
        self.max_sec_prop_children = max_min_sec_prop_children
        self.randomness = randomness
        self.width = width

    def generate_by_width_height(self):
        pass

    def generate_by_height_entitiesnumber(self):
        pass

    def run_create_graph_test(self, use_width=1, use_height=1, use_entities=1,
                              save_format="turtle", file_path=None, randomness=None):

        if not file_path:
            file_path = getcwd()

        use_ext = "ttl"
        if save_format == "xml":
            use_ext = "xml"

        use_name = "w%dh%dn%d.%s" % (use_width, use_height, use_entities, use_ext)
        use_file_name = path.join(file_path, use_name)

        c = time.time()
        doc = self.generate_by_width_height_entitiesnumber(width=use_width,
                                                           height=use_height,
                                                           number_entities=use_entities,
                                                           randomness=randomness)

        print(time.time() - c)

        self.to_rdf(doc, path.join(file_path, use_file_name), format=save_format)

    def time_create_graph(self):
        use_width = 10
        use_height = 6
        use_entities = 30
        self.run_create_graph_test(use_width, use_height, use_entities)

        # use_width = 500
        # use_height = 100
        # use_entities = 3000
        # self.run_create_graph_test(use_width, use_height, use_entities)

        # use_width = 5000
        # use_height = 300
        # use_entities = 30000
        # self.run_create_graph_test(use_width, use_height, use_entities, "xml")

    def write_rdf_to_odml(self, file_path=None):
        if not file_path:
            file_path = getcwd()

        use_width = 10
        use_height = 6
        use_entities = 30
        name_base = "w%dh%dn%d" % (use_width, use_height, use_entities)

        docs = RDFReader().from_file(path.join(file_path, "%s.ttl" % name_base), "turtle")
        ODMLWriter().write_file(docs[0], path.join("%s.odml" % name_base))


# OdmlFilesGenerator().write_rdf_to_odml()
OdmlFilesGenerator().time_create_graph()
