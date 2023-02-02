import graphviz
from utils import timestamp

RELATIONS = ['=', '<', '>']


class State:

    """Keep track of the current state of elements in the model."""

    # TODO: it might be more appropriate to move these to st.session_state

    def __init__(self):
        self.document = None
        self.annotation = ''
        self.info = []
        self.warnings = []
        self.log = []

    def add_info(self, message):
        self.info.append(message)
        self.log.append((timestamp(), 'INFO', message))

    def add_warning(self, message):
        self.warnings.append(message)
        self.log.insert(0, (timestamp(), 'WARNING', message))

    def add_to_log(self, message: str):
        self.log.insert(0, (timestamp(), 'LOG', message))

    def reset_messages(self):
        self.info = []
        self.warnings = []

    def reset_annotation(self):
        """Clear out the current annotation."""
        self.annotation = ''

    def reset_document(self):
        """Reset the document to its original state by removing all annotations."""
        self.document.annotations = []


state = State()


class Graph:

    def __init__(self, document):
        self.document = document
        self.dot = graphviz.Digraph('graph')
        self.object_nodes = []
        self.action_nodes = []
        self.edges = []
        self.add_annotations()
        self.build()
        self.style_nodes()

    def add_annotations(self):
        for annotation in self.document.annotations:
            inputs, relation, outputs = annotation
            for node in inputs + outputs:
                if node not in self.object_nodes:
                    self.object_nodes.append(node)
            if relation not in self.action_nodes:
                self.action_nodes.append(relation)

    def build(self):
        for annotation in self.document.annotations:
            inputs, relation, outputs = annotation
            if relation == '=':
                for node1 in inputs:
                    for node2 in outputs:
                        self.dot.edge(node1, node2, label=relation, arrowhead='none')
            else:
                for node in inputs:
                    self.dot.edge(node, relation)
                for node in outputs:
                    self.dot.edge(relation, node)

    def style_nodes(self):
        for node in self.object_nodes:
            self.dot.node(node, shape='box', color='blue3')
        for node in self.action_nodes:
            if node != '=':
                self.dot.node(node, color='firebrick3')

    def graphviz(self):
        return self.dot


class Annotation:

    # these are for the recipe flavor
    relations = ('>', '=')

    def __init__(self, annotation: str, document):
        self.document = document
        self.is_valid = True
        self.messages = []
        state.add_to_log(f'adding "{annotation}"')
        self.elements = self.get_annotation_elements(annotation)
        if not self.is_valid:
            state.message = f'Error parsing "{annotation}", <br/>see list of message below for details'
            self.messages.append(f'Error parsing "{annotation}"')
            for message in self.messages:
                state.add_warning(message)
            return
        state.add_to_log(str(self.elements))
        self.check_annotation()
        if self.is_valid:
            pass
        else:
            for message in self.messages:
                state.add_warning(message)

    def get_annotation_elements(self, annotation: str):
        elements = []
        for element in annotation.split():
            print('gae', element)
            if self.element_is_relation_symbol(element):
                elements.append(element)
            elif node := self.element_node(element):
                elements.append((element, node))
            else:
                print('gae invalid')
                self.messages.append(f'Unknown identifier or relation: "{element}"')
                self.is_valid = False
        return elements

    def element_is_relation_symbol(self, element: str) -> bool:
        return element in self.__class__.relations

    def element_node(self, element: str):
        if node := self.document.relations_idx.get(element):
            print('n', node)
            return node
        elif node := self.document.entities_idx.get(element):
            print('n', node)
            return node
        else:
            return None

    def check_annotation(self):
        return self.is_process() or self.is_simple_relation()

    def is_process(self):
        """Return True of the annotation is a valid process."""
        #print(self.elements)
        return True

    def is_simple_relation(self):
        """Return True if the annotation is a simple basic relation, like x=y."""
        return True



def parse_annotation(annotation: str, document):
    # this is for the recipe/action flavor, where you have things like
    # "e1 e2 > r1 > e3" and "e1 e2 e3 > r2".
    anno = Annotation(annotation, document)
    inputs = []
    relation = None
    outputs = []
    copied_annotation = annotation.split().copy()
    while copied_annotation:
        element = copied_annotation.pop(0)
        if element.startswith('[') and element.endswith(']'):
            element = element.strip('[]')
            node_bin = inputs if relation is None else outputs
            node_bin.append(element)
        elif relation is None:
            relation = element
    return [inputs, relation, outputs]
