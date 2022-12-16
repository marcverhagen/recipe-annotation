
RELATIONS = ['=', '<']


class Recipe:

    identifier = 0
    
    def __init__(self, text, ingredients, actions):
        self.identifier = self.new_identifier()
        self.text = text
        self.actions = actions
        self.ingredients = ingredients
        self.ingredients.extend(["%s-RES" % action for action in actions])
        self.relations = RELATIONS

    def __str__(self):
        return ('<Recipe %d with %d ingredients and %d actions>'
                % (self.identifier, self.number_of_ingredients(), self.number_of_actions()))

    def new_identifier(self):
        self.__class__.identifier += 1
        return self.__class__.identifier

    def number_of_ingredients(self):
        # this does not count implicit actions like mix-RES
        return len(self.ingredients) - len(self.actions)

    def number_of_actions(self):
        return len(self.actions)

        
RECIPES = [

    Recipe('**[Whisk]** the [milk] and [eggs]. '
           '**[Mix]** [whisked eggs] with the [sugar] into a [mixture].',
           ['egg', 'milk', 'sugar', 'whisked-eggs', 'mixture'],
           ['mix', 'whisk']),

    Recipe('**[Add]** [two eggs] to the [dough]. '
           '**[Heat]** in the oven for 10 minutes.',
           ['two eggs', 'dough'],
           ['Add', 'Heat'])
]

for recipe in RECIPES:
    print(recipe)

