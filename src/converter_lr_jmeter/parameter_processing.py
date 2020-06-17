from lxml import etree
from definitions import xmlgen

class parameter_processing:

    def __init__(self, doc, parameters_list):
        self.doc = doc
        self.parameters_list = list(set(parameters_list))
        self.outputfile = ""

    def replacing_lr_parameters(self):
        #for parameters in self.parameters_list:
        self.doc.write(self.outputfile + '\outFile_trail.jmx', xml_declaration=True, encoding='utf-8')
        fp = open(self.outputfile + '\outFile_trail.jmx', 'r')
        fout = open(self.outputfile + '\outFile_final.jmx', 'w')
        temp = fp.read()
        fp.close()
        for parameters in self.parameters_list:
            temp = temp.replace("{" + str(parameters) + "}", "${" + str(parameters) + "}")

        fout.write(temp)
        fout.close()

class extract_parameters:
    def __init__(self):
        pass

    def parameterfile(filepath, headtagname, doc):
        """
        processes parameter files to add csvdataset, throws a message on console if custom parameters are present

        :param filepath: input - location of prm files
        :param headtagname: input - base tag "page_hash"
        :param doc: object - generated xml - gets saved as jmx at the end
        :return: returns object doc
        """
        param_details = ""
        tree = etree.parse(filepath + "\ScriptUploadMetadata.xml")

        for elements in tree.getiterator("GeneralFiles"):
            for filenames in elements.getchildren():
                if filenames.attrib.get('Name').endswith("prm"):
                    param_details = filenames.attrib.get('Name')
                    break

        try:
            fo = open(filepath + "\\" + param_details, 'r')
            filetoprocess = dict(enumerate(fo.read().splitlines()))
            breakinarray = []
            breakinarray_table = []
            param_notprocesed = []

            for i in range(0, len(filetoprocess)):
                if "[parameter:" in filetoprocess[i]:
                    breakinarray.append(i)
            breakinarray_dup = breakinarray

            for i in range(0, len(breakinarray)):
                if i < len(breakinarray) - 1:
                    gap = breakinarray[i + 1] - breakinarray[i]
                else:
                    gap = len(filetoprocess) - breakinarray[i]

                if gap == 14:
                    int_temp = ""
                    int_paramname = ""
                    int_delim = ""
                    for j in range(breakinarray[i], breakinarray[i] + 13):
                        if "table=" in filetoprocess[j].lower():
                            int_temp = j
                        if "paramname=" in filetoprocess[j].lower():
                            int_paramname = j
                        if "delimiter=" in filetoprocess[j].lower():
                            int_delim = j
                    if "table=" in filetoprocess[int_temp].lower():
                        breakinarray_table.append(
                            filetoprocess[int_temp].lower().replace('table=', "").replace("\"", ""))
                        breakinarray_dup[i] = breakinarray[i]
                    else:
                        print "Couldn't process as Pattern mismatch in param file at " + str(breakinarray[i] + 1)
                        print "Please reach to Shravanakula@ymail.com for further enhancements"
                else:
                    param_notprocesed.append(breakinarray_dup[i])
                    breakinarray_dup[i] = "**"

            for elements in breakinarray_dup:
                try:
                    breakinarray_dup.remove('**')
                except Exception as e:
                    pass

            temp = list(set(breakinarray_table))
            params = ""

            cons_table = int_temp - breakinarray_dup[len(breakinarray_dup) - 1]
            cons_paramname = int_paramname - breakinarray_dup[len(breakinarray_dup) - 1]
            cons_delim = int_delim - breakinarray_dup[len(breakinarray_dup) - 1]

            for j in temp:
                for i in range(0, len(breakinarray_dup)):
                    if "**" not in str(breakinarray_dup[i]):
                        if j in filetoprocess[breakinarray_dup[i] + cons_table].lower():
                            params = params + "," + filetoprocess[breakinarray_dup[i] + cons_paramname]
                params = params.replace("\",", ",,").replace(",ParamName=\"", "").replace("\"", "")
                params = params.replace("\",", ",,").replace(",ParamName=\"", "").replace("\"", "")
                xmlgen.csvdataset(headtagname, doc, j, params,
                                  filetoprocess[breakinarray_dup[i] + cons_delim].lower().replace("delimiter=",
                                                                                                  "").replace("\"", ""))
                params = ""

            for elements in param_notprocesed:
                print "\nAdd parameter " + filetoprocess[elements].lower().replace("parameter:", "") + " manually"
        except IOError:
            print "Parameters cannot be extracted as there are one more missing files"
        except Exception as e:
            print e
            print "OOPS!! Couldnt convert the script! please validate the Loadrunner script - error in function parameterfile"
        return doc



