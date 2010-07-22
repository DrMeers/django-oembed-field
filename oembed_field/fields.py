import re

from django.core import exceptions
from django.db import models

DEFAULT_PROVIDER_RULES = (
    r'http://vimeo.com/\S*',
    r'http://\S*.youtube.com/watch\S*',
    r'http://video.google.com/videoplay?\S*',
    r'http://qik.com/\S*',
    r'http://\S*?flickr.com/\S*',
)

class OEmbedField(models.URLField):
    """
    A URL pointing to an oEmbed provider.
    
    See http://www.oembed.com/ for information on providers
    """
    
    description = "A URL pointing to an oEmbed provider"
    
    def __init__(self, provider_rules=None, *args, **kwargs):
        """
        Initialise with `provider_rules`, an iterable of regex patterns
        defining valid oEmbed provider url schemes.
        """
        self._provider_rules = provider_rules
        super(OEmbedField, self).__init__(*args, **kwargs)

    @property
    def provider_rules(self):
        """
        As this field will likely be used in conjunction with Eric Florenzano's
        django-oembed (http://github.com/ericflo/django-oembed), where
        `provider_rules` is not provided, an attempt is made to take access
        provider rules through django-oembed's ProviderRule model. If neither
        is available, a selection of default rules are used.
        """
        if self._provider_rules is None:
            try:
                from oembed.models import ProviderRule
                rules = [r.regex for r in ProviderRule.objects.all()]
            except ImportError:
                rules = DEFAULT_PROVIDER_RULES
            self._provider_rules = rules
        return self._provider_rules
        
    def validate(self, value, model_instance):
        for rule in self.provider_rules:
            if re.match(rule, value):
                return
        raise exceptions.ValidationError('Not a valid oEmbed link')


try:
    from south.modelsinspector import add_introspection_rules
except ImportError:
    pass # no south, nevermind
else:
    # tell south to treat OEmbedFields just like URLFields
    rules = ['^%s\.OEmbedField' % (__name__.replace('.','\.'),)]
    add_introspection_rules([], rules)
