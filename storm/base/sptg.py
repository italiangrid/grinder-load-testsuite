from common import TestID, log_surl_call_result
from eu.emi.security.authn.x509.impl import PEMCredential
from exceptions import Exception
from gov.lbl.srm.StorageResourceManager import TStatusCode
from jarray import array
from java.io import FileInputStream
from javax.net.ssl import X509ExtendedKeyManager
from net.grinder.plugin.http import HTTPRequest
from net.grinder.script import Test
from net.grinder.script.Grinder import grinder
from org.italiangrid.srm.client import SRMClient, SRMClientFactory
import random
import time
import traceback

error = grinder.logger.error
info = grinder.logger.info
debug = grinder.logger.debug

props = grinder.properties

def sptg(ptg_resp, client):
    token = ptg_resp.requestToken
    debug("SPTG for token: %s" % token )

    res = client.srmSPtG(ptg_resp)
    log_surl_call_result("sptg",res)
    return res

class TestRunner:
    def __call__(self, ptg_resp, client = None):
        if ptg_resp is None:
            raise Exception("Please set a non-null PtG response!")

        if client is None:
            raise Exception("Please set a non-null SRM client!")

        test = Test(TestID.SPTG, "StoRM Status PTG")
        test.record(sptg)

        try:
            return sptg(ptg_resp, client)
        except Exception, e:
            error("Error executing sptg: %s" % traceback.format_exc())
            raise
