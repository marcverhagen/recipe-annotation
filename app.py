"""Simple recipe annotation

See README.md for more information.

"""

import streamlit as st
import pandas as pd

import data
from model import annotation, annotations, message
from model import reset_annotation, reset_annotations, get_graph


current_recipe = data.RECIPES[0]

st.set_page_config(layout="wide")

st.write(current_recipe.text)
st.info(' '.join(annotation))
st.warning(' '.join(message))


def add_annotation():
    annotations.append(annotation.copy())
    reset_annotation()

def clear():
    reset_annotation()

def next_recipe():
    pass

def add_ingredient(text):
    annotation.append('[%s]' % text)

def add_relation(rel):
    annotation.append(rel)

st.sidebar.button('Add Annotation', on_click=add_annotation)
st.sidebar.button('Clear Annotation', on_click=clear)
st.sidebar.button('Next Recipe', on_click=next_recipe)

'---'
ingredients_column, actions_column, relations_column, playpen = st.columns([2, 2, 2, 6])

ingredients_column.markdown('#### Ingredients')
for ingredient in current_recipe.ingredients:
    ingredients_column.button(ingredient, on_click=add_ingredient, args=[ingredient])

actions_column.markdown('#### Actions')
for action in current_recipe.actions:
    actions_column.button(action, on_click=add_relation, args=[action])

relations_column.markdown('#### Relations')
for rel in current_recipe.relations:
    relations_column.button(rel, on_click=add_relation, args=[rel])

playpen.graphviz_chart(get_graph())

st.table(pd.DataFrame(annotations))

