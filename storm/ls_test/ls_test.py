from common import *
from srm import *
from exceptions import Exception
from jarray import array
from net.grinder.script import Test
from net.grinder.script.Grinder import grinder
import random
import time
import traceback
import uuid

# Test: create width x height elements, save surls and ls one element random each run

error          = grinder.logger.error
info           = grinder.logger.info
debug          = grinder.logger.debug

props          = grinder.properties

utils          = Utils(grinder.properties)

# Get common variables:
TEST_STORAGEAREA = props['common.test_storagearea']

# Test specific variables
TEST_DIRECTORY  = props['ls_test.directory']
TEST_NUM_FILES  = int(props['ls_test.num_files'])

def get_base_dir():
    
    return "%s/%s" % (TEST_STORAGEAREA, TEST_DIRECTORY)

def setup():
    
    info("Setting up ls test.")
    endpoint, client = utils.get_srm_client()
    
    dir_name = str(uuid.uuid4())
    base_dir = get_base_dir()
    test_dir = "%s/%s" % (base_dir, dir_name)
    
    info("Creating remote test directory ... " + base_dir)
    srmMkDir(client, get_surl(endpoint, base_dir))
    
    info("Creating ls-test specific test dir: " + test_dir)
    test_dir_surl = get_surl(endpoint, test_dir)
    check_success(srmMkDir(client, test_dir_surl))
    
    surls = []
    for i in range(1, TEST_NUM_FILES + 1):
        surl = get_surl(endpoint, "%s/file_%s" % (test_dir, i))
        surls.append(surl)
        debug("appended: %s" % surl)
    
    info("Creating ls-test test dir files ... ")
    token, response = srmPtP(client,surls,[])
    check_success(response)
    check_success(srmPd(client,surls,token))

    surls.append(test_dir_surl)

    info("ls setup completed successfully.")
    return test_dir, surls

def ls_test(surl):
    
    endpoint, client = utils.get_srm_client()
    response = srmLs(client, surl)
    info("LS %s - [%s %s]" % (surl, response.returnStatus.statusCode, response.returnStatus.explanation))
    check_success(response)

def cleanup(test_dir):
    
    info("Cleaning up for ls-test.")
    endpoint, client = utils.get_srm_client()
    check_success(client.srmRmdir(get_surl(endpoint, test_dir), 1))
    info("ls-test cleanup completed successfully.")

class TestRunner:

    def __init__(self):
        
        (self.test_dir, self.surls) = setup()

    def __call__(self):
        
        try:

            test = Test(TestID.LS_TEST, "StoRM LS test")
            test.record(ls_test)
            ls_test(random.choice(self.surls))

        except Exception, e:

            error("Error executing ls test: %s" % traceback.format_exc())
            raise
    
    def __del__(self):
        
        cleanup(self.test_dir)