from django.template import Library, Node, TemplateSyntaxError, Variable

register = Library()

class RangeNode(Node):
    def __init__(self, num, context_name):
        self.num = Variable(num)
        self.context_name = context_name

    def render(self, context):
        context[self.context_name] = range(int(self.num.resolve(context)))
        return ""
        
@register.tag
def num_range(parser, token):
    """
    Takes a number and iterates and returns a range (list) that can be 
    iterated through in templates
    
    Syntax:
    {% num_range 5 as some_range %}
    
    {% for i in some_range %}
      {{ i }}: Something I want to repeat\n
    {% endfor %}
    
    Produces:
    0: Something I want to repeat 
    1: Something I want to repeat 
    2: Something I want to repeat 
    3: Something I want to repeat 
    4: Something I want to repeat
    """
    try:
        fnctn, num, trash, context_name = token.split_contents()
    except ValueError:
        raise TemplateSyntaxError, "%s takes the syntax %s number_to_iterate\
            as context_variable" % (fnctn, fnctn)
    if not trash == 'as':
        raise TemplateSyntaxError, "%s takes the syntax %s number_to_iterate\
            as context_variable" % (fnctn, fnctn)
    return RangeNode(num, context_name)

class ParejasNode(Node):
    def __init__(self, parejas):
        self.parejas = Variable(parejas)
        print 'init'
        
    def render (self, context):
        print 'aaaa'
        parejas = self.parejas.resolve(context)
        if parejas and len(parejas) > 0:
            res = "<ul>"
            for pareja in parejas:
                res += "<li>" + pareja[0].nombre + " - " + pareja[1].nombre + "</li>"
            res += "</ul>"
        else:
            res = "No hay datos"
        return res
        
@register.tag
def parejas_as_list(parser, token):
    try:
        """
        {% parejas_as_list lista_parejas %}
        """
        fnctn, lista = token.split_contents()
        print 'antes'
        return ParejasNode(lista)
    except:
        import traceback
        import sys
        traceback.print_exc(file=sys.stdout)



