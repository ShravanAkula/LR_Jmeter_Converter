from definitions import lr_defs
from converter_lr_jmeter import convert_to_jmeter
from definitions import xmlgen
from lxml import etree
from converter_lr_jmeter import create_JMX
from converter_lr_jmeter import parameter_processing
import re

print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
print "Jmeter to Loadrunner script converter - Python"
print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
print "Version  :   v3.0"
print "Supports conversion on loadrunner http/html scripts to jmeter"
print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n\n"



# --------------------Start of Main function-----------------------------

filepath = raw_input("Enter a file to process : ")
outputfile = raw_input("Enter a location to save logs and jmx : ")

if outputfile[-1:] == "/" or outputfile[-1:] == "\\":
    outputfile = outputfile[:-1]

if filepath[-1:] == "/" or filepath[-1:] == "\\":
    filepath = filepath[:-1]

# -------------------------------------------------------------------------#
# loop through all the files and append to processedfile
# -------------------------------------------------------------------------#


temp_parmeters = lr_defs.http_request().lr_web_elements
array_unique_terminate = []
complete_list_keywords = []

for elements in temp_parmeters.keys():
    if elements.upper() not in ["NOKEYS", "COMMON_SCRIPT", "REPLACE_URL_FROM"]:
        array_unique_terminate.extend(temp_parmeters[elements]['terminate'])
        complete_list_keywords.extend(temp_parmeters[elements]['keywords'])


processedfile = ""

try:
    tree = etree.parse(filepath + "\ScriptUploadMetadata.xml")

    for i in tree.getiterator("ActionFiles"):
        for j in i.getchildren():
            try:
                fo = open(filepath + "\\" + j.attrib.get('Name'), 'r')
                fout = open(filepath + "\\" + j.attrib.get('Name')[:-2] + "_temp.c", 'w')

                pattern = re.compile('"\n(.*?)"', re.IGNORECASE)
                fout.write(pattern.sub("", fo.read()))
                fout.close()
                fo.close()

                fo = open(filepath + "\\" + j.attrib.get('Name')[:-2] + "_temp.c", 'r')
                fout = open(filepath + "\\" + j.attrib.get('Name')[:-2] + "_temp_1.c", 'w')

                for lines in fo.readlines():
                    matched_words = [x for x in list(set(complete_list_keywords)) if x in lines]
                    for matches in matched_words:
                        lines = lines.replace("\"" + matches + "=", "\n\"" + matches + "=")
                    lines = lines.replace("ENDITEM", "\nENDITEM")

                    for i in list(set(array_unique_terminate)):
                        lines = lines.replace(i, "\n" + i)
                    fout.write(lines)
                fout.close()
                fo.close()

                fin = open(filepath + "\\" + j.attrib.get('Name')[:-2] + "_temp_1.c", 'r')
                processedfile = processedfile + fin.read()
                fin.close()

            except IOError:
                print "Cannot continue as " + filepath + "\\" + j.attrib.get('Name') + " isn't available to process\n Terminating!!!"
            except Exception as e:
                print e
                print "OOPS!! Couldn't convert the script! please validate the Loadrunner script - error at line 348"
except IOError:
    print "Cannot continue as " + filepath + "\ScriptUploadMetadata.xml isn't available to process -   to continue, open the file in LR and save again (no changes expected)\n\nTerminating!!!"
    wait_for_input = raw_input("press Enter to exit !!! ")
    exit(1)
except Exception as e:
    print e
    print "OOPS!! Couldnt convert the script! please validate the Loadrunner script - error at line 354"

print "\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
print "Started with Processing the file"
print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n\n"

print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
print "Warnings are listed below"
print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n\n"


# ----------------Stripping off commented sections--------------------------
processedfile = processedfile.replace("://", ":--")
processedfile = re.sub('//.*?\n|/\*.*?\*/', '\n', processedfile, flags=re.S)
processedfile = processedfile.replace(":--", "://")

for i1 in lr_defs.http_request().lr_web_elements['replace_url_from']:
    processedfile = re.sub(str(i1) + '=h(.*?)://(.*?)/', str(i1) +'=/', processedfile, )

for items in lr_defs.http_request().lr_web_elements['nokeys']:
    processedfile_matches = re.findall(items + "(.*?)\n", processedfile)

    print "################################### - start ------------------"
    print items, processedfile_matches
    print "################################### - END ------------------"

    for values in processedfile_matches:
        print str(items + values)
        re.sub(items + values + "(.*?)\n", items + values, processedfile)





###-------------------------------------- Main function --------------------------------------###

file_input = dict(enumerate(processedfile.splitlines()))

def_functions = lr_defs.http_request().lr_web_elements.keys()

index_processedfile = 0
temp_out_dict = {}

#++++++++++++++++++++++ Writing to JMX +++++++++++++++++++++++++++#

if outputfile[-1:] == "/" or outputfile[-1:] == "\\":
    outputfile = outputfile[:-1]

#if filepath[-1:] == "/" or filepath[-1:] == "\\":
#    filepath = filepath[:-1]


page1 = etree.Element('jmeterTestPlan', version='1.2', properties='2.4', jmeter='2.9 r1437961')
params_list = [['Hostname', 'app hostname'], ['Protocol', 'http/https'], ['Port', 'enter your app port number'],
               ['connect_timeout', '999999'], ['response_timeout', '999999'], ['user_count', '1'],
               ['steady_state', '300'], ['Ramp_up', '1']]
doc = etree.ElementTree(page1)
page_hash = etree.SubElement(page1, 'hashTree')

try:
    doc = xmlgen.Startjmeter(page_hash, params_list, doc)
    fo = open(outputfile + '\converted_lines.log', 'w+')
    doc = xmlgen.loopcontroller(page_hash, 2, 1, 1, doc)

    level = 3
    transaction_start_count = 1
    temp = {}
    headenHash= 0
    tailenHash = 0
    index_processedfile = 0

    for items in file_input.itervalues():
        keyword = items.split("(")
        if len([x for x in def_functions if x in keyword[0].strip()]) > 0 or len(
                [x for x in temp_parmeters['nokeys'] if x in keyword[0].strip()]):
            try:
                (temp_out_dict, keyword_match_counts) = convert_to_jmeter.multiline_extract(keyword, file_input, index_processedfile)
                (page_hash, level, headenHash, tailenHash, transaction_start_count,
                 doc) = create_JMX.jmx_creation().jmx_creation_fun(
                    captured_list=[keyword[0].strip(), temp_out_dict, keyword_match_counts], page_hash=page_hash,
                    level=level, headenHash=headenHash, tailenHash=tailenHash,
                    transaction_start_count=transaction_start_count, doc=doc)
            except Exception as e:
                print e
                print "something went wrong while processing " + str(keyword)

        index_processedfile = index_processedfile + 1

    fin.close()

    parameter_processing.parameter_processing(doc=doc, parameters_list=create_JMX.jmx_creation().get_parameters_list()).replacing_lr_parameters()

    fo.close()
    #doc.write(outputfile + '\outFile.jmx', xml_declaration=True, encoding='utf-8')
except Exception as e:
    print e