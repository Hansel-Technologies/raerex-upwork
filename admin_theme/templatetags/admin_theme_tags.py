from django import template

register = template.Library()

@register.inclusion_tag('admin_theme/components/card.html')
def admin_card(title, content):
    return {'title': title, 'content': content}

# Add more custom tags as needed