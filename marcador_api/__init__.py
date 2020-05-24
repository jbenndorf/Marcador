from collections import OrderedDict

from django.urls import NoReverseMatch

from rest_framework.reverse import reverse
from rest_framework.viewsets import ViewSetMixin

from .apps import MarcadorApiConfig


def get_extra_action_url_map(self):
    """
    Build a map of {names: urls} for the extra actions.

    This method will noop if `detail` was not provided as a view initkwarg.
    """
    action_urls = OrderedDict()

    # exit early if `detail` has not been provided
    if self.detail is None:
        return action_urls

    # filter for the relevant extra actions
    actions = [
        action for action in self.get_extra_actions()
        if action.detail == self.detail
    ]

    for action in actions:
        try:
            url_name = '%s:%s-%s' % (
                MarcadorApiConfig.name,
                self.basename,
                action.url_name
            )
            url = reverse(url_name, self.args, self.kwargs, request=self.request)
            view = self.__class__(**action.kwargs)
            action_urls[view.get_view_name()] = url
        except NoReverseMatch:
            pass  # URL requires additional arguments, ignore

    return action_urls


ViewSetMixin.get_extra_action_url_map = get_extra_action_url_map
