from django import template
register = template.Library()

@register.filter
def is_favorited_by(job, user):
    if not getattr(user, 'is_authenticated', False):
        return False
    return job.favorited_by.filter(pk=user.pk).exists()