from pathlib import Path

import django
from django import forms, template
from django.forms import BoundField
from django.template.loader import get_template
from django.utils.safestring import mark_safe
from django.conf import settings


register = template.Library()
BULMA_COLUMN_COUNT = 1


@register.filter
def bulma(element):
    markup_classes = {
        'label': '',
        'value': '',
        'single_value': '',
    }
    return render(element, markup_classes)


@register.filter
def bulma_inline(element):
    markup_classes = {
        'label': 'sr-only',
        'value': '',
        'single_value': '',
    }
    return render(element, markup_classes)


@register.filter
def bulma_horizontal(element, label_cols='is-2'):
    markup_classes = {
        'label': label_cols,
        'value': '',
        'single_value': '',
    }
    for cl in label_cols.split(' '):
        splitted_class = cl.split('-')
        try:
            value_nb_cols = int(splitted_class[-1])
        except ValueError:
            value_nb_cols = BULMA_COLUMN_COUNT
        if value_nb_cols >= BULMA_COLUMN_COUNT:
            splitted_class[-1] = str(BULMA_COLUMN_COUNT)
        else:
            offset_class = cl.split('-')
            offset_class[-1] = f' offset-{value_nb_cols}'
            splitted_class[-1] = str(BULMA_COLUMN_COUNT - value_nb_cols)
            markup_classes['single_value'] += f' {"-".join(offset_class)}'
            markup_classes['single_value'] += f' {"-".join(splitted_class)}'
        markup_classes['value'] += f' {"-".join(splitted_class)}'
    return render(element, markup_classes)


@register.filter
def add_field_classes(field):
    if not any((
        is_checkbox(field),
        is_multiple_checkbox(field),
        is_radio(field),
        is_file(field)
    )):
        field_classes = field.field.widget.attrs.get('class', '')
        field_classes += ' control'
        field.field.widget.attrs['class'] = field_classes


def render(element, markup_classes):
    if isinstance(element, BoundField):
        add_field_classes(element)
        template = get_template('frontend/forms/field.html')
        context = {
            'field': element,
            'classes': markup_classes,
            'form': element.form,
        }
    else:
        has_management = getattr(element, 'management_form', None)
        if has_management:
            for form in element.forms:
                for field in form.visible_fields():
                    add_field_classes(field)
            template = get_template('frontend/forms/formset.html')
            context = {
                'formset': element,
                'classes': markup_classes,
            }
        else:
            for field in element.visible_fields():
                add_field_classes(field)
            template = get_template('frontend/forms/form.html')
            context = {
                'form': element,
                'classes': markup_classes,
            }
    return template.render(context)


@register.filter
def is_select(field):
    return isinstance(field.field.widget, forms.Select)


@register.filter
def is_multiple_select(field):
    return isinstance(field.field.widget, forms.SelectMultiple)


@register.filter
def is_textarea(field):
    return isinstance(field.field.widget, forms.Textarea)


@register.filter
def is_input(field):
    return isinstance(field.field.widget, (
        forms.TextInput,
        forms.NumberInput,
        forms.EmailInput,
        forms.PasswordInput,
        forms.URLInput
    ))


@register.filter
def is_checkbox(field):
    return isinstance(field.field.widget, forms.CheckboxInput)


@register.filter
def is_multiple_checkbox(field):
    return isinstance(field.field.widget, forms.CheckboxSelectMultiple)


@register.filter
def is_radio(field):
    if django.__version__ >= '4.0':
        return isinstance(field.field.widget, forms.RadioSelect) and not is_multiple_checkbox(field)
    else:
        return isinstance(field.field.widget, forms.RadioSelect)
    

@register.filter
def is_file(field):
    return isinstance(field.field.widget, forms.FileInput)


@register.filter
def addclass(field, css_class):
    if len(field.errors) > 0:
        css_class += ' is-danger'
    field_classes = field.field.widget.attrs.get('class', '')
    field_classes += f' {css_class}'
    return field.as_widget(attrs={'class': field_classes})


@register.filter(name='message_tag')
def bulma_message_tag(tag):
    return {
        'error': 'danger',
    }.get(tag, tag)


@register.simple_tag
def theme_getstatic():
    try:
        dot_path = settings.BULMA_THEME_ENV_PATH
        dot_path = Path(dot_path)
        if not (dot_path.exists() and dot_path.is_file()):
            raise FileNotFoundError(f'Cannot locate "{dot_path}" bulma .env file.')
    except Exception as err:
        return ''
    with open(dot_path, 'r') as file:
        theme = file.read().strip()
    static_path = f'{settings.STATIC_URL}css/{theme}.min.css'
    return mark_safe(static_path)


