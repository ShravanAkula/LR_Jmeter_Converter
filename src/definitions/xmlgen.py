import re

from lxml import etree
from markupsafe import escape


def testplan(headtagname, params_list):
    """
    Generates xml equivalent to jmeter Testplan

    :param headtagname: input - base tag "page_hash"
    :param params_list: input - array, used for populating data in testplan
    :return: no return type as all the functions are being processed in a single file
    """
    page_hash = headtagname
    etree.SubElement(page_hash, 'TestPlan',
                                            guiclass='TestPlanGui',
                                            testclass='TestPlan',
                                            testname='Test Plan',
                                            enabled='true')
    t = extract_latesttag(page_hash, "1",)

    t1 = addelement_withparam(t, "elementProp", "TestPlan.user_defined_variables", "Arguments", "ArgumentsPanel",
                              "Arguments", "User Defined Variables", "true")
    t2 = addStringprop_noparam(t1, "collectionProp", "Arguments.arguments")
    for i in range(0, len(params_list)):
        t3 = addelement_withparam(t2, "elementProp", "HostName", "Argument")
        addprop_withparam(t3, "stringProp", "Argument.name", params_list[i][0])
        addprop_withparam(t3, "stringProp", "Argument.value", params_list[i][1])
        addprop_withparam(t3, "stringProp", "Argument.metadata", "=")
    addprop_withparam(t, "boolProp", "TestPlan.functional_mode", "false")
    addprop_withparam(t, "boolProp", "TestPlan.serialize_threadgroups", "false")
    addprop_withparam(t, "stringProp", "TestPlan.comments", "")
    addprop_withparam(t, "stringProp", "TestPlan.user_define_classpath", "")


def threadgroup_basic(headtagname, params_list):
    """
    Generates a basic thread group under testplan by processing inputs

    :param headtagname: input - base tag "page_hash"
    :param params_list: input - array, used for populating data in thread group
    :return: no return type as all the functions are being processed in a single file
    """
    TG_h = addStringprop_noparam(headtagname, 'hashTree')
    TG_b = addelement_withparam(TG_h, "ThreadGroup", "ThreadGroupGui", "ThreadGroup", "Thread Group", "true")
    addprop_withparam(TG_b, "stringProp", "ThreadGroup.on_sample_error", "continue")
    TG_b_e1 = addelement_withparam(TG_b, "elementProp", "ThreadGroup.main_controller", "LoopController",
                                   "LoopControlPanel", "LoopController", "Loop Controller", "true")
    addprop_withparam(TG_b_e1, "boolProp", "LoopController.continue_forever", "false")
    addprop_withparam(TG_b_e1, "stringProp", "LoopController.loops", "1")
    addprop_withparam(TG_b, "stringProp", "ThreadGroup.num_threads", "${"+params_list[5][0]+"}")
    addprop_withparam(TG_b, "stringProp", "ThreadGroup.ramp_time", "${"+params_list[7][0]+"}")
    addprop_withparam(TG_b, "longProp", "ThreadGroup.start_time", "1")
    addprop_withparam(TG_b, "longProp", "ThreadGroup.end_time", "1")
    addprop_withparam(TG_b, "boolProp", "ThreadGroup.scheduler", "false")
    addprop_withparam(TG_b, "stringProp", "ThreadGroup.duration", "${"+params_list[6][0]+"}")
    addprop_withparam(TG_b, "stringProp", "ThreadGroup.delay", "")


def httpdefaults(headtagname, params_list):
    """
    Adds HTTP request defaults based on the inputs

    :param headtagname: input - base tag "page_hash"
    :param params_list: input - array, used for populating data in thread group
    :return: no return type as all the functions are being processed in a single file
    """
    t = extract_latesttag(headtagname, "1")
    Hd_h = addStringprop_noparam(t, 'hashTree')
    Hd_m = addelement_withparam(Hd_h, "ConfigTestElement", "HttpDefaultsGui", "ConfigTestElement",
                                "HTTP Request Defaults", "true")
    Hd_m1 = addelement_withparam(Hd_m, "elementProp", "HTTPsampler.Arguments", "Arguments", "HTTPArgumentsPanel",
                                 "Arguments", "User Defined Variables", "true")
    addStringprop_noparam(Hd_m1, "collectionProp", "Arguments.arguments")
    addprop_withparam(Hd_m, "stringProp", "HTTPSampler.domain", "${"+params_list[0][0]+"}")
    addprop_withparam(Hd_m, "stringProp", "HTTPSampler.port", "${"+params_list[2][0]+"}")
    addprop_withparam(Hd_m, "stringProp", "HTTPSampler.connect_timeout", "${"+params_list[3][0]+"}")
    addprop_withparam(Hd_m, "stringProp", "HTTPSampler.response_timeout", "${"+params_list[4][0]+"}")
    addprop_withparam(Hd_m, "stringProp", "HTTPSampler.protocol", "${"+params_list[1][0]+"}")
    addprop_withparam(Hd_m, "stringProp", "HTTPSampler.contentEncoding", "")
    addprop_withparam(Hd_m, "stringProp", "HTTPSampler.path", "")
    addprop_withparam(Hd_m, "stringProp", "HTTPSampler.concurrentPool", "${"+params_list[5][0]+"}")


def cachemanager(headtagname):
    """
    creates a cache manager element in jmeter

    :param headtagname: input - base tag "page_hash"
    :return: no return type as all the functions are being processed in a single file
    """
    t = extract_latesttag(headtagname, "2")
    addStringprop_noparam(t, 'hashTree')
    cm_m = addelement_withparam(t, "CacheManager", "CacheManagerGui", "CacheManager", "HTTP Cache Manager", "true")
    addprop_withparam(cm_m, "boolProp", "clearEachIteration", "false")
    addprop_withparam(cm_m, "boolProp", "useExpires", "false")


def Transactioncontroller(headtagname, level, headenHash, tailenHash, controllername, doc):
    """
    processes the array generated by strip_transaction_start_end

    :param headtagname: input - base tag "page_hash"
    :param level: input - defines the location of the transaction controller
    :param headenHash: flag - adds a leading hashtree tag in xml
    :param tailenHash: flag - adds a trailing hashtree tag in xml
    :param controllername: input - extracted from LR_parsing.py/strip_transaction_start_end
    :param doc: object - generated xml - gets saved as jmx at the end
    :return: returns object doc
    """
    t = extract_latesttag(headtagname, int(level))
    if int(headenHash) == 1:
        addStringprop_noparam(t, 'hashTree')
    TC_m = addelement_withparam(t, "TransactionController", "TransactionControllerGui", "TransactionController",
                                controllername, "true")
    addprop_withparam(TC_m, "boolProp", "TransactionController.includeTimers", "false")
    addprop_withparam(TC_m, "boolProp", "TransactionController.parent", "true")
    if int(tailenHash) == 1:
        addStringprop_noparam(t, 'hashTree')
    return doc


def if_while_loopcontroller(headtagname, level, if_while, doc):
    """
    processes if condition or while loop; passes true as condition and writes a message to the console

    :param headtagname: input - base tag "page_hash"
    :param level: input - defines the location of the controller
    :param if_while: flag - defines controller type to add
    :param doc: object - generated xml - gets saved as jmx at the end
    :return: returns object doc
    """
    t = extract_latesttag(headtagname, int(level))
    if "while" in if_while.lower():
        guielement = "WhileControllerGui"
    else:
        guielement = "IfControllerPanel"
    if_w_m = addelement_withparam(t, if_while+"Controller", guielement, if_while+"Controller", if_while+" controller", "true")
    if "if" in if_while.lower():
        addprop_withparam(if_w_m, "boolProp", "IfController.evaluateAll", "false")
    addprop_withparam(if_w_m, "stringProp", if_while+"Controller.condition", "true")
    addStringprop_noparam(t, 'hashTree')
    return doc


def loopcontroller(headtagname, level, headenHash, tailenHash, doc):
    """
    Adds loop controller to the jmx file

    :param headtagname: input - base tag "page_hash"
    :param level: input - defines the location of the controller
    :param headenHash: flag - adds a leading hashtree tag in xml
    :param tailenHash: flag - adds a trailing hashtree tag in xml
    :param doc: object - generated xml - gets saved as jmx at the end
    :return: returns object doc
    """
    t = extract_latesttag(headtagname, int(level))
    if int(headenHash) == 1:
        addStringprop_noparam(t, 'hashTree')
    TC_m = addelement_withparam(t, "LoopController", "LoopControlPanel", "LoopController", "Loop Controller", "true")
    addprop_withparam(TC_m, "boolProp", "LoopController.continue_forever", "false")
    addprop_withparam(TC_m, "stringProp", "LoopController.loops", "1")
    if int(tailenHash) == 1:
        addStringprop_noparam(t, 'hashTree')
    return doc


def csvdataset(headtagname, doc, *varlist):
    """
    Adds csv dataset extractor based on the output from parameterfile

    :param headtagname: input - base tag "page_hash"
    :param doc: object - generated xml - gets saved as jmx at the end
    :param varlist: enables method overriding
    :return: returns object doc
    """
    t = extract_latesttag(headtagname, "2")
    addStringprop_noparam(t, 'hashTree')
    cs_m = addelement_withparam(t, "CSVDataSet", "TestBeanGUI", "CSVDataSet", varlist[0], "true")
    addprop_withparam(cs_m, "stringProp", "delimiter", varlist[2])
    addprop_withparam(cs_m, "stringProp", "fileEncoding", "")
    addprop_withparam(cs_m, "stringProp", "filename", varlist[0])
    addprop_withparam(cs_m, "boolProp", "quotedData", "false")
    addprop_withparam(cs_m, "boolProp", "recycle", "false")
    addprop_withparam(cs_m, "stringProp", "shareMode", "shareMode.all")
    addprop_withparam(cs_m, "boolProp", "stopThread", "true")
    addprop_withparam(cs_m, "stringProp", "variableNames", varlist[1])
    return doc


def regextractor(headtagname, level, val, array_tostrip, doc):
    """
    Adds regex extractor to the jmeter file

    :param headtagname: input - base tag "page_hash"
    :param level: input - defines the location of the post processor
    :param val: flag - adds a hashtree in set to 1
    :param array_tostrip: input - array processed by regextractor in processing_web_reg_save
    :param doc: object - generated xml - gets saved as jmx at the end
    :return: returns object doc
    """
    try:
        name = ""



        if "web_reg_save_param_regexp" not in array_tostrip[0]:
            name = array_tostrip[0]
            regex = escape(array_tostrip[1]) + "(.*?)" + escape(array_tostrip[2])
        else:
            name = str(array_tostrip[0]).replace("web_reg_save_param_regexp","")
            regex = escape(array_tostrip[1])


    except IndexError:
        print "Correlation " + array_tostrip[0] + " isn't in expected format"
        print "Desired format is to either have web_reg_* till LAST in same line or each of the elements in web_reg_* in seperate lines - LAST should atleast be in a seperate line"
    except Exception as e:
        print e
        print "OOPS!! Couldnt convert the script! please validate the Loadrunner script - error in function regextractor"
    return doc


def testAction(headtagname, level, delay_timer, doc):
    """
    Adds pause to the jmeter file

    :param headtagname: input - base tag "page_hash"
    :param level: input - defines the location of the post processor
    :param delay_timer: input - value by processed by html_file_processing in LR_Parsing.py
    :param doc: object - generated xml - gets saved as jmx at the end
    :return: returns object doc
    """
    t = extract_latesttag(headtagname, level)
    ta_m = addelement_withparam(t, "TestAction", "TestActionGui", "TestAction", "Test Action", "true")
    addprop_withparam(ta_m, "intProp", "ActionProcessor.action", "1")
    addprop_withparam(ta_m, "intProp", "ActionProcessor.target", "0")
    addprop_withparam(ta_m, "stringProp", "ActionProcessor.duration", str(delay_timer.strip()))
    addStringprop_noparam(t, 'hashTree')
    return doc


def responseassertion(base_object, name, doc):
    """
    Adds response assertion to the output jmeter file

    :param headtagname: input - base tag "page_hash"
    :param level: input - defines the location of the post processor
    :param val: flag - if enabled adds a hashtree tag to doc
    :param array_tostrip: input - array processed by html_file_processing in LR_Parsing.py
    :param doc: object - generated xml - gets saved as jmx at the end
    :return: returns object doc
    """
    ra1 = base_object
    ra_m = addelement_withparam(ra1, "ResponseAssertion", "AssertionGui", "ResponseAssertion",
                                       "Response Assertion - " + name, "true")
    ra_c = addStringprop_noparam(ra_m, "collectionProp", "Asserion.test_strings")
    addprop_withparam(ra_c, "stringProp", "response_Assertion", escape(name))
    addprop_withparam(ra_m, "stringProp", "Assertion.test_field", "Assertion.response_data")
    addprop_withparam(ra_m, "boolProp", "Assertion.assume_success", "false")
    addprop_withparam(ra_m, "intProp", "Assertion.test_type", "16")
    addStringprop_noparam(ra1, 'hashTree')

    return doc


'''
basic methods
'''


def addStringprop_noparam(tagname, stringProp, *varlist):
    """
    Basic method, used by multiple methods to add elements to doc

    :param tagname: input - object id in xml structure
    :param stringProp: input - element properties
    :param varlist: enables method overriding
    :return: returns an xml object
    """
    if len(varlist) == 1:
        tagname_propname = etree.SubElement(tagname, stringProp, name=varlist[0])
    elif len(varlist) == 0:
        tagname_propname = etree.SubElement(tagname, stringProp)
    elif len(varlist) == 2:
        tagname_propname = etree.SubElement(tagname, stringProp, name=varlist[0], elementType=varlist[1])
    return tagname_propname


def addprop_withparam(tagname, elename, propname, propvalue):
    """
    Basic method, used by multiple methods to add elements to doc

    :param tagname: input - object id in xml structure
    :param elename: input - name of the element to add for xml
    :param propname: input - name of the property in element
    :param propvalue: input - value of the property
    :return: no return type
    """
    s1 = propvalue
    s2 = "<" + elename + " name='" + propname + "'>{0}</" + elename + ">"
    s2 = s2.format(s1)
    tagname_propname = etree.fromstring(s2)
    tagname.append(tagname_propname)


def addelement_withparam(tagname, propname, *varlist):
    """
    Basic method, used by multiple methods to add elements with parameters to doc

    :param tagname: input - object id in xml structure
    :param propname: input - name of the property in element
    :param varlist: enables method overriding
    :return: no return type
    """
    temp_array = varlist

    if len(temp_array) == 6 and propname != "ConfigTestElement":
        tagname_propname = etree.SubElement(tagname, 'elementProp',
                                            name=temp_array[0],
                                            elementType=temp_array[1],
                                            guiclass=temp_array[2],
                                            testclass=temp_array[3],
                                            testname=temp_array[4],
                                            enabled=temp_array[5])
        return tagname_propname
    elif len(temp_array) == 4:
        tagname_propname = etree.SubElement(tagname, propname,
                                            guiclass=temp_array[0],
                                            testclass=temp_array[1],
                                            testname=temp_array[2],
                                            enabled=temp_array[3])
        return tagname_propname

    elif len(temp_array) == 5 and propname != "ConfigTestElement":
        tagname_propname = etree.SubElement(tagname, 'elementProp',
                                            name=temp_array[0],
                                            elementType=temp_array[1],
                                            guiclass=temp_array[2],
                                            testclass=temp_array[3],
                                            enabled=temp_array[4])
        return tagname_propname
    elif len(temp_array) == 2:
        tagname_propname = etree.SubElement(tagname, 'elementProp',
                                            name=temp_array[0],
                                            elementType=temp_array[1])
        return tagname_propname
    else:
        print "no match found for element prop tag creation"


def extract_latesttag(parenttagname, level):
    for i in range(0, int(level)):
        for j in parenttagname.getchildren():
            t = j
        parenttagname = j
    return parenttagname


def Startjmeter(page_hash, params_list, doc):
    """
    Basic method, creates basic structure for adding elements

    :param page_hash: input - base tag "page_hash"
    :param params_list: input - array, used for populating data
    :param doc: object - generated xml - gets saved as jmx at the end
    :return: returns object doc
    """
    testplan(page_hash, params_list)
    threadgroup_basic(page_hash, params_list)
    httpdefaults(page_hash, params_list)
    cachemanager(page_hash)
    return doc
