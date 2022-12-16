import graphviz

message = []
annotation = []
annotations = []


def reset_annotation():
    while annotation:
        annotation.pop()

def reset_annotations():
    while annotations:
        annotations.pop()


def get_graph():
    dot = graphviz.Digraph('graphp')
    for annotation in annotations:
        inputs, relations, outputs = parse_annotation(annotation.copy())
        for input in inputs:
            for relation in relations:
                arrow = 'none' if relation == '=' else 'normal'
                for output in outputs:
                    dot.edge(input, output, label=relation, arrowhead=arrow)
    return dot


def parse_annotation(annotation):
    inputs = []
    relations = []
    outputs = []
    while annotation:
        element = annotation.pop(0)
        if element.startswith('[') and element.endswith(']'):
            if relations:
                outputs.append(element)
            else:
                inputs.append(element)
        else:
            relations.append(element)
    print(inputs, relations, outputs)
    return inputs, relations, outputs
