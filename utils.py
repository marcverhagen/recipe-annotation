import time

style = """
<style>
body { font-size: 16pt; }
sentence { font-size: 16pt; }
action { color: darkred; }
object { color: darkblue; }
id {vertical-align: super; font-size: 14pt; }
action::before, object::before { content: '['; }
action::after, object::after { content: ']'; }
thead tr th:first-child { display:none; }
tbody th { display:none; }
</style>"""


def timestamp() -> str:
    return time.strftime("%y%m%d:%H%M%S")

def protect(text: str):
    # TODO: use xml tools for this
    if text == '<':
        return '&lt;'
    return text
