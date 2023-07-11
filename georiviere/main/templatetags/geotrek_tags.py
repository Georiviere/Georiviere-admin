from django import template

register = template.Library()


"""
Template in geotrek sensitivity include geotrek_tags without using any tag or filter.
We don't want to install app geotrek.common
"""
