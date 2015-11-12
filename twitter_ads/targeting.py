# Copyright (C) 2015 Twitter, Inc.

"""Container for all targeting related logic used by the Ads API SDK."""

from twitter_ads.enum import *
from twitter_ads.account import *
from twitter_ads.http import *


class ReachEstimate(object):

    RESOURCE = '/0/accounts/{account_id}/reach_estimate'

    @classmethod
    def fetch(klass, account, product_type, objective, user_id, **kwargs):
        resource = klass.RESOURCE.format(account_id=account.id)

        params = {
            'product_type': product_type,
            'objective': objective,
            'user_id': user_id
        }.update(kwargs)

        response = Request(
            account.client(), 'get', resource, params=params).perform()

        return response.body['data']
