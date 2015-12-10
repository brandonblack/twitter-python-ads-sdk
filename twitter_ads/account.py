# Copyright (C) 2015 Twitter, Inc.

"""
A Twitter supported and maintained Ads API SDK for Python.
"""

from twitter_ads.http import *
from twitter_ads.cursor import *

from twitter_ads.resource import *
from twitter_ads.campaign import *
from twitter_ads.creative import *
from twitter_ads.audience import *


@resource
class Account(Resource):
    """
    The Ads API :class:`Account` class which functions as a context container
    for the advertiser and nearly all interactions with the API.
    """

    RESOURCE_COLLECTION = '/0/accounts'
    RESOURCE = '/0/accounts/{id}'
    FEATURES = '/0/accounts/{id}/features'
    SCOPED_TIMELINE = '/0/accounts/{id}/scoped_timeline'

    PROPERTIES = {
        'id': {'readonly': True},
        'name': {'readonly': True},
        'salt': {'readonly': True},
        'timezone': {'readonly': True},
        'timezone_switch_at': {'readonly': True, 'transform': 'time'},
        'created_at': {'readonly': True, 'transform': 'time'},
        'updated_at': {'readonly': True, 'transform': 'time'},
        'deleted': {'readonly': True}
    }

    def __init__(self, client):
        self._client = client

    def client(self):
        """
        Returns the :class:`Client` instance stored in this account object.
        """
        return self._client

    @classmethod
    def load(klass, client, id, **kwargs):
        """Returns an object instance for a given resource."""
        resource = klass.RESOURCE.format(id=id)
        request = Request(client, 'get', resource, params=kwargs)
        return Cursor(klass, request, init_with=[client])

    @classmethod
    def all(klass, client, **kwargs):
        """Returns a Cursor instance for a given resource."""
        resource = klass.RESOURCE_COLLECTION
        request = Request(client, 'get', resource, params=kwargs)
        return Cursor(klass, request, init_with=[client])

    def reload(self, **kwargs):
        """
        Reloads all attributes for the current object instance from the API.
        """
        if not self.id:
            return self

        params = {'with_deleted': True}.update(kwargs)
        resource = klass.RESOURCE.format(
            account_id=self.account.id, id=self.id)
        response = Request(
            self.account.client, 'get', resource, params=params).perform()

        self.from_response(response.body['data'])

    def features(self):
        """
        Returns a collection of features available to the current account.
        """
        self._validate_loaded()

        resource = self.FEATURES.format(id=self.id)
        response = Request(self.client(), 'get', resource).perform()

        return response.body['data']

    def promotable_users(self, id=None, **kwargs):
        """
        Returns a collection of promotable users available to the
        current account.
        """
        return self._load_resource(PromotableUser, id, **kwargs)

    def funding_instruments(self, id=None, **kwargs):
        """
        Returns a collection of funding instruments available to
        the current account.
        """
        return self._load_resource(FundingInstrument, id, **kwargs)

    def campaigns(self, id=None, **kwargs):
        """
        Returns a collection of campaigns available to the current account.
        """
        return self._load_resource(Campaign, id, **kwargs)

    def line_items(self, id=None, **kwargs):
        """
        Returns a collection of line items available to the current account.
        """
        return self._load_resource(Campaign, id, **kwargs)

    def app_lists(self, id=None, **kwargs):
        """
        Returns a collection of app lists available to the current account.
        """
        return self._load_resource(AppList, id, **kwargs)

    def tailored_audiences(self, id=None, **kwargs):
        """
        Returns a collection of tailored audiences available to the
        current account.
        """
        return self._load_resource(TailoredAudience, id, **kwargs)

    def videos(self, id=None, **kwargs):
        """
        Returns a collection of videos available to the current account.
        """
        return self._load_resource(videos, id, **kwargs)

    def scoped_timeline(self, *ids, **kwargs):
        """
        Returns the most recent promotable Tweets created by one or more
        specified Twitter users.
        """
        self._validate_loaded()

        if isinstance(ids, list):
            ids = ','.join(map(str, ids))

        params = {'user_ids': ids}.update(kwargs)
        resource = self.SCOPED_TIMELINE.format(id=self.id)
        response = Request(
            self.client(), 'get', resource, params=params).perform()

        return response.body['data']

    def _validate_loaded(self):
        if not self.id:
            raise ValueError("""
            Error! {klass} object not yet initialized,
            call {klass}.load first.
            """).format(klass=self.__class__)

    def _load_resource(self, klass, id, **kwargs):
        self._validate_loaded()
        if id is None:
            return klass.all(self, **kwargs)
        else:
            return klass.load(self, id, **kwargs)
