"""Simple relation annotation

See README.md for more information.

"""

import streamlit as st
import pandas as pd

import utils
from document import DOCUMENTS
from model import state, parse_annotation, Graph


def select_document(identifier=None):
    state.reset_messages()
    state.reset_annotation()
    state.add_to_log(f'Selected document "{document_name}"')
    if identifier is not None:
        state.document = DOCUMENTS[identifier]
    else:
        pass

def add_annotation(anno: str):
    state.reset_messages()
    parsed_annotation = parse_annotation(anno, state.document)
    state.document.annotations.append(parsed_annotation)

def clear_all():
    state.reset_messages()
    state.reset_annotation()
    state.reset_document()

def undo():
    state.add_warning('"Undo Last Annotation" is not yet implemented')

def example(n: int):
    state.reset_messages()
    if n == 1:
        example_annotations = (
            [['milk-e1', 'eggs-e2'], 'whisk-r1', ['whisk-r1-RES']],
            [["whisked-eggs-e3", "sugar-e4"], 'mix-r2', ["mixture-e5"]],
            [["it-e6", "cheese-e7"], 'mix-r3', ["mix-r3-RES"]],
            [["whisked-eggs-e3"], '=', ["whisk-r1-RES"]],
            [["mixture-e5"], '=', ["it-e6"]])
        for a in example_annotations:
            state.document.annotations.append(a)


if state.document is None:
    state.document = DOCUMENTS[0]

st.set_page_config(layout="wide")

st.markdown(utils.style, unsafe_allow_html=True)

st.sidebar.markdown('# Relation Annotation')
st.sidebar.info("Annotation tool to build graphs for documents that "
                "already have entities and relations (predicates).")

flavor = st.sidebar.radio('Flavor', ['Recipes', 'Arguments'])

st.sidebar.markdown('# Document Actions')
document_name = st.sidebar.selectbox(
    'Select document',
    [f'{document.name}' for document in DOCUMENTS],
    on_change=select_document)
state.document = DOCUMENTS.get_document(document_name)

st.sidebar.button('Clear Annotations', on_click=clear_all)
st.sidebar.button('Undo Last Annotation', on_click=undo)
st.sidebar.button('Add Example Annotations', on_click=example, args=[1])

st.header(f'{state.document.name}')
st.write(state.document)
st.markdown(state.document.sentence_lines(), unsafe_allow_html=True)
with st.form("link_form", clear_on_submit=True):
    state.annotation = st.text_input('link', label_visibility="collapsed")
    submitted = st.form_submit_button("Add Relation")
    if submitted:
        add_annotation(state.annotation)

status_table = pd.DataFrame(data=DOCUMENTS.table(), columns=['document', 'n'])
st.sidebar.markdown('# Status')
st.sidebar.info('Number of annotations added per document')
st.sidebar.table(status_table)

for message in state.info:
    st.info(message)

for message in state.warnings:
    st.warning(message)

graph_tab, list_tab, log_tab, help_tab, debug_tab \
    = st.tabs(['Graph', 'List', 'Log', 'Help', 'Debug'])

with graph_tab:
    st.graphviz_chart(Graph(state.document).graphviz())
with list_tab:
    st.table(pd.DataFrame(state.document.annotations))
with log_tab:
    st.table(pd.DataFrame(state.log, columns=['timestamp', 'type', 'message']))
with help_tab:
    with open('data/help/help.md') as fh:
        st.markdown(fh.read())
with debug_tab:
    st.write('st.session_state')
    st.json(st.session_state)
