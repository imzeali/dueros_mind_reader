# -*- coding: utf-8 -*-

# Copyright (c) 2014 Baidu.com, Inc. All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file
# except in compliance with the License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the
# License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific language governing permissions
# and limitations under the License.

"""
This module provides a client class for EIP.
"""

import copy
import json
import logging
import uuid

from baidubce import utils
from baidubce.auth import bce_v1_signer
from baidubce.bce_base_client import BceBaseClient
from baidubce.http import bce_http_client
from baidubce.http import handler
from baidubce.http import http_methods

_logger = logging.getLogger(__name__)


class EipClient(BceBaseClient):
    """
    eip sdk client
    """
    version = '/v1'
    prefix = '/eip'

    def __init__(self, config=None):
        """
        :type config: baidubce.BceClientConfiguration
        :param config:
        """
        BceBaseClient.__init__(self, config)

    def create_eip(self, bandwidth_in_mbps, name=None, billing=None, client_token=None,
                   config=None):
        """
        Create an eip with the specified options.

        :type bandwidth_in_mbps: int
        :param bandwidth_in_mbps: specify the bandwidth in Mbps

        :type name: string
        :param name: name of eip. The optional parameter

        :type billing: Billing
        :param billing: billing information. The optional parameter, default paymentTiming is Postpaid

        :type client_token: string
        :param client_token: if the clientToken is not specified by the user, a random String
        generated by default algorithm will be used.

        :type config: baidubce.BceClientConfiguration
        :param config:

        :return: created eip address, for example,{"eip":"180.181.3.133"}
        """
        body = {
            'name': name,
            'bandwidthInMbps': bandwidth_in_mbps
        }
        if billing is None:
            body['billing'] = {
               'paymentTiming': 'Postpaid',
               'billingMethod': 'ByBandwidth'
            }
        else:
            body['billing'] = {
                'paymentTiming': billing.payment_timing,
                'billingMethod': billing.billing_method,
                'reservation': {
                    'reservationLength': billing.reservation_length,
                    'reservationTimeUnit': billing.reservation_time_unit
                }
            }
        path = self._get_path()
        if client_token is None:
            client_token = self._generate_default_client_token()
        params = {
            'clientToken': client_token
        }

        return self._send_request(http_methods.POST, path, body=json.dumps(body), params=params,
                                  config=config)

    def resize_eip(self, eip, new_bandwidth_in_mbps, client_token=None, config=None):
        """
        Resizing eip

        :type eip: string
        :param eip: eip address to be resized

        :type new_bandwidth_in_mbps: int
        :param new_bandwidth_in_mbps: specify new bandwidth in Mbps for eip

        :type client_token: string
        :param client_token: if the clientToken is not specified by the user, a random String
        generated by default algorithm will be used.

        :type config: baidubce.BceClientConfiguration
        :param config:

        :return: BceResponse
        """
        body = {
            'newBandwidthInMbps': new_bandwidth_in_mbps
        }
        path = self._get_path() + '/%s' % eip
        if client_token is None:
            client_token = self._generate_default_client_token()
        params = {
            'resize': '',
            'clientToken': client_token
        }
        return self._send_request(http_methods.PUT, path, params=params, body=json.dumps(body),
                                  config=config)

    def purchase_reserved_eip(self, eip, billing=None, client_token=None, config=None):
        """
        PurchaseReserved eip with fixed duration,only Prepaid eip can do this

        :type eip: string
        :param eip: eip address to be renewed

        :type billing: Billing
        :param billing: billing information. The optional parameter, default reservationLength is 1

        :type client_token: string
        :param client_token: if the clientToken is not specified by the user, a random String
        generated by default algorithm will be used.

        :type config: baidubce.BceClientConfiguration
        :param config:

        :return: BceResponse
        """
        if billing is None:
            body = {
                'billing': {
                    'reservation': {
                        'reservationLength': 1,
                        'reservationTimeUnit': 'Month'
                    }
                }
            }
        else:
            body = {
                'billing': {
                    'reservation': {
                        'reservationLength': billing.reservation_length,
                        'reservationTimeUnit': billing.reservation_time_unit
                    }
                }
            }
        path = self._get_path() + '/%s' % eip
        if client_token is None:
            client_token = self._generate_default_client_token()
        params = {
            'purchaseReserved': '',
            'clientToken': client_token
        }
        return self._send_request(http_methods.PUT, path, params=params, body=json.dumps(body),
                                  config=config)

    def bind_eip(self, eip, instance_type, instance_id, client_token=None, config=None):
        """
        bind the eip to a specified instanceId and instanceType

        :type eip: string
        :param eip: eip address to be bound

        :type instance_type: string
        :param instance_type: type of instance to be bound(BCC BLB et.)

        :type instance_id: string
        :param instance_id: id of instance to be bound

        :type client_token: string
        :param client_token: if the clientToken is not specified by the user, a random String
        generated by default algorithm will be used.

        :type config: baidubce.BceClientConfiguration
        :param config:

        :return: BceResponse
        """
        body = {
            'instanceType': instance_type,
            'instanceId': instance_id
        }
        path = self._get_path() + '/%s' % eip
        if client_token is None:
            client_token = self._generate_default_client_token()
        params = {
            'bind': '',
            'clientToken': client_token
        }
        return self._send_request(http_methods.PUT, path, params=params, body=json.dumps(body),
                                  config=config)

    def unbind_eip(self, eip, client_token=None, config=None):
        """
        unbind the eip from a specified instance

        :type eip: string
        :param eip: eip address to be unbound

        :type client_token: string
        :param client_token: if the clientToken is not specified by the user, a random String
        generated by default algorithm will be used.

        :type config: baidubce.BceClientConfiguration
        :param config:

        :return: BceResponse
        """
        path = self._get_path() + '/%s' % eip
        if client_token is None:
            client_token = self._generate_default_client_token()
        params = {
            'unbind': '',
            'clientToken': client_token
        }
        return self._send_request(http_methods.PUT, path, params=params, config=config)

    def release_eip(self, eip, client_token=None, config=None):
        """
        release the eip(delete operation)
        Only the Postpaid instance or Prepaid which is expired can be released.
        if the eip has been bound, must unbind before releasing.

        :type eip: string
        :param eip: eip address to be released

        :type client_token: string
        :param client_token: if the clientToken is not specified by the user, a random String
        generated by default algorithm will be used.

        :type config: baidubce.BceClientConfiguration
        :param config:

        :return: BceResponse
        """
        path = self._get_path() + '/%s' % eip
        if client_token is None:
            client_token = self._generate_default_client_token()
        params = {
            'clientToken': client_token
        }
        return self._send_request(http_methods.DELETE, path, params=params, config=config)

    def list_eips(self, eip=None, instance_type=None, instance_id=None, marker=None, max_keys=1000,
                  config=None):
        """
        get a list of eip owned by the authenticated user and specified conditions.
        we can Also get a single eip function  through this interface by eip condition

        :type eip: string
        :param eip: eip address condition

        :type instance_type: string
        :param instance_type: bound instance type condition

        :type instance_id: string
        :param instance_id: bound instance id condition
        if query by the instanceId or instanceType condition, must provides both of them at the same time

        :type marker: string
        :param marker: The optional parameter marker specified in the original request to specify
        where in the results to begin listing.

        :type max_keys: int
        :param max_keys: The optional parameter to specifies the max number of list result to return.
        The default value is 1000.

        :type config: baidubce.BceClientConfiguration
        :param config:

        :return: list of eip model, for example:
                {
                    "eipList": [
                        {
                            "name":"eip-xrllt5M-1",
                            "eip": "180.181.3.133",
                            "status":"binded",
                            "instanceType": "BCC",
                            "instanceId": "i-IyWRtII7",
                            "bandwidthInMbps": 5,
                            "paymentTiming":"Prepaid",
                            "billingMethod":"ByBandwidth",
                            "createTime":"2016-03-08T08:13:09Z",
                            "expireTime":"2016-04-08T08:13:09Z"
                        },
                        {
                            "name":"eip-scewa1M-1",
                            "eip": "180.181.3.134",
                            "status":"binded",
                            "instanceType": "BCC",
                            "instanceId": "i-KjdgweC4",
                            "bandwidthInMbps": 1,
                            "paymentTiming":"Postpaid",
                            "billingMethod":"ByTraffic",
                            "createTime":"2016-03-08T08:13:09Z",
                            "expireTime":null
                        },
                    ],
                    "marker":"eip-xrllt5M-1",
                    "isTruncated": true,
                    "nextMarker": "eip-DCB50387",
                    "maxKeys": 2
                }
        """
        path = self._get_path()
        params = {}
        if eip is not None:
            params['eip'] = eip
        if instance_type is not None:
            params['instanceType'] = instance_type
        if instance_id is not None:
            params['instanceId'] = instance_id
        if marker is not None:
            params['marker'] = marker
        if max_keys is not None:
            params['maxKeys'] = max_keys
        return self._send_request(http_methods.GET, path, params=params, config=config)

    @staticmethod
    def _generate_default_client_token():
        """
        default client token by uuid1
        """
        return uuid.uuid1()

    @staticmethod
    def _get_path(prefix=None):
        """
        :type prefix: string
        :param prefix: path prefix
        """
        if prefix is None:
            prefix = EipClient.prefix
        return utils.append_uri(EipClient.version, prefix)

    def _merge_config(self, config):
        """

        :type config: baidubce.BceClientConfiguration
        :param config:
        :return:
        """
        if config is None:
            return self.config
        else:
            new_config = copy.copy(self.config)
            new_config.merge_non_none_values(config)
            return new_config

    def _send_request(self, http_method, path, body=None, headers=None, params=None,
                      config=None, body_parser=None):
        """

        :param http_method:
        :param path:
        :param body:
        :param headers:
        :param params:

        :type config: baidubce.BceClientConfiguration
        :param config:

        :param body_parser:

        :return: baidubce.BceResponse
        """
        config = self._merge_config(config)
        if body_parser is None:
            body_parser = handler.parse_json

        if headers is None:
            headers = {'Accept': '*/*', 'Content-Type': 'application/json;charset=utf-8'}

        return bce_http_client.send_request(config, bce_v1_signer.sign,
                                            [handler.parse_error, body_parser],
                                            http_method, path, body, headers, params)


