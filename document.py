import os, re, glob
import xml.dom.minidom
from xml.dom.minidom import parseString, Node

class Document:

    identifier = 0

    def __init__(self, name: str, text: str, use_implicit_results=True):
        self.use_implicit_results = use_implicit_results
        self.identifier = self.new_identifier()
        self.name = name
        self.text = text
        self.dom = parseString(text)
        self.sentences = [node for node in self.dom.getElementsByTagName("sentence")]
        self.relations = [n for n in self.dom.getElementsByTagName('action')]
        self.entities = [n for n in self.dom.getElementsByTagName('object')]
        # TODO: need to line up the relations and entities with their identifiers
        self.relations_idx = { i: n for n, i in self.nodes_with_identifiers('action') }
        self.entities_idx = { i: n for n, i in self.nodes_with_identifiers('object') }
        self.annotations = []

    def __str__(self):
        return ('<Document %s %s with %d relations, %d entities and %d annotations>'
                % (self.identifier, self.name,
                   self.number_of_edges(), self.number_of_nodes(), self.number_of_annotations()))

    def new_identifier(self):
        self.__class__.identifier += 1
        return self.__class__.identifier

    def nodes_with_identifiers(self, node_type: str):
        answer = []
        for s in self.sentences:
            for i, node in enumerate(s.childNodes):
                if node.nodeType == Node.ELEMENT_NODE and node.tagName == node_type:
                    identifier = s.childNodes[i+1]
                    answer.append((node.firstChild.data, identifier.firstChild.data))
        return answer

    def number_of_nodes(self):
        return len(self.entities)

    def number_of_edges(self):
        return len(self.relations)

    def number_of_annotations(self):
        return len(self.annotations)

    def sentence_lines(self):
        return '\n<br/>'.join([node.toxml() for node in self.sentences])

    def pp(self):
        print(self)
        for s in self.sentences:
            print('   ', s)
            print('   ', s.nodes)


class Sentence:

    # TODO: this is now obsolete

    def __init__(self, text: str):
        self.text = text
        self.nodes = []
        self.entities = []
        self.relations = []
        self.parse_text()

    def __str__(self):
        return self.text

    def parse_text(self):
        for match in re.finditer("\[([^]]+)]\[(\w+)]", self.text):
            match_string, identifier = match.groups()
            match_string = match_string.lower().replace(" ", "-")
            node = f'{match_string}-{identifier}'
            self.nodes.append(node)
            node_bin = self.entities if identifier.startswith('e') else self.relations
            node_bin.append(node)
            if identifier.startswith('r'):
                implied_node = f'{node}-RES'
                self.nodes.append(implied_node)
                self.entities.append(implied_node)


class Documents:

    def __init__(self, data_directory: str, annotations_file: str):
        # TODO: add annotations to each document
        self.documents = []
        for file_path in sorted(glob.glob("%s/*.xml" % data_directory)):
            print(f'-- reading {file_path}')
            name = os.path.basename(os.path.split(file_path)[-1])
            with open(file_path) as fh:
                data = fh.read().strip()
                self.documents.append(Document(name, data))

    def __iter__(self):
        return iter(self.documents)

    def __getitem__(self, item):
        return self.documents[item]

    def __len__(self):
        return len(self.documents)

    def get_document(self, name: str):
        for d in self.documents:
            if d.name == name:
                return d
        return None

    def table(self):
        return [['%s' % doc.name, doc.number_of_annotations()] for doc in self]

    def print_all(self):
        for doc in self:
            print(doc)


DOCUMENTS = Documents('data/sources', 'data/annotations/annotations.json')


if __name__ == '__main__':

    DOCUMENTS.print_all()
