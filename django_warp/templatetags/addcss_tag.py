from django import template

register = template.Library()

@register.filter(name='addcss')
def addcss(value, css):
   return value.as_widget(attrs={"class":css})
