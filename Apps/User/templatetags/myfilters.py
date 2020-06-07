from django import template

register = template.Library()

@register.filter(name='addclass')
def addclass(value, arg):
    return value.as_widget(attrs={'class': arg})

@register.filter(name='addClassAndPlaceH')
def addClassAndPlaceH(value, arg):
    argSplit = arg.split(",")
    argClass = argSplit[0]
    argPlace = argSplit[1]
    return value.as_widget(attrs={'class': argClass, 'placeholder': argPlace})
    

    