# -*- coding: utf-8 -*-
import sys
import logging
from sabreclient import SabreClient, SabreClientException
from settings import sabre as sabre_settings

logging.basicConfig(stream=sys.stdout, level=logging.ERROR)


def segments(pnr):
    """Returns number of segments in requested PNR"""
    client = SabreClient(sabre_settings['pos'])
    try:
        return client.pnr(pnr)
    except SabreClientException:
        print client.request_text
        print client.response_text
        raise

if __name__ == '__main__':
    from lxml import etree
    pnr = 'MCARCL'
    r = segments(pnr)
    print etree.tostring(r, pretty_print=True)
