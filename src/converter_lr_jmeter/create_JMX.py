from definitions import xmlgen
from markupsafe import escape


class jmx_creation:
    func_dict = {}
    value_web_reg_find = []
    value_web_reg_save_param = []
    value_web_add_header = []
    parameters_list = []

    def jmx_creation_fun(self, captured_list, page_hash, level, headenHash, tailenHash, transaction_start_count, doc):
        self.method = captured_list[0]
        self.func_dict = {self.method: self.method}

        try:
            print "calling : " + str(self.method)
            try:
                (page_hash, level, headenHash, tailenHash, transaction_start_count, doc) = eval("self." + self.func_dict.get(self.method))(variable=captured_list, headtagname=page_hash, level=level, headenHash=headenHash, tailenHash=tailenHash, transaction_start_count=transaction_start_count, doc=doc)
            except Exception as e:
                print "error in calling function : " + str(self.method)
                print e

            try:
                if self.method in ['web_url', 'web_submit_data', 'web_custom_request']:
                    if len(self.value_web_add_header) > 0:
                        (page_hash, level, headenHash, tailenHash, transaction_start_count, doc) = self.add_web_add_header(self.value_web_add_header, page_hash, level + 1, headenHash, tailenHash, transaction_start_count, doc)
                    if len(self.value_web_reg_find) > 0:
                        (page_hash, level, headenHash, tailenHash, transaction_start_count, doc) = self.add_web_reg_find(self.value_web_reg_find, page_hash, level + 1, headenHash, tailenHash, transaction_start_count, doc)
                    if len(self.value_web_reg_save_param) > 0:
                        (page_hash, level, headenHash, tailenHash, transaction_start_count, doc) = self.add_web_reg_save_param(self.value_web_reg_save_param, page_hash, level + 1, headenHash, tailenHash, transaction_start_count, doc)
            except Exception as e:
                print "Encountered an exception in calling sub functions like - add header or web_reg_find " + str(e)
            return page_hash, level, headenHash, tailenHash, transaction_start_count, doc
        except Exception as e:
            print "method is not defined for : " + str(self.method)
            return ""


    def web_url(self, variable, headtagname, level, headenHash, tailenHash, transaction_start_count, doc):
        headenHash = 0
        tailenHash = 1

        for items in variable[2]:
            if variable[2][items] > 1:
                print "no repetations expected in web_url items " + str(variable[2])
        (xml_objects, headtagname, level, headenHash, tailenHash, transaction_start_count, doc) = self.common_web_url_submit_link(variable, headtagname, level, headenHash, tailenHash, transaction_start_count, doc)
        (xml_objects, headtagname, level, headenHash, tailenHash, transaction_start_count, doc) = self.common_web_url_submit_link_closing(xml_objects, variable, headtagname, level, headenHash, tailenHash, transaction_start_count, doc)
        return headtagname, level, headenHash, tailenHash, transaction_start_count, doc

    def web_submit_data_adding_variables(self, xml_objects, variable, pos_string, doc):
        Hr_c1 = xmlgen.addStringprop_noparam(xml_objects[2], "elementProp",
                                             escape(variable[1]["Value" + str(pos_string)]),
                                             "HTTPArgument")
        xmlgen.addprop_withparam(Hr_c1, "boolProp", "HTTPArgument.always_encode", "false")
        xmlgen.addprop_withparam(Hr_c1, "boolProp", "HTTPArgument.use_equals", "true")
        xmlgen.addprop_withparam(Hr_c1, "stringProp", "Argument.value",
                                 escape(variable[1]["Value" + str(pos_string)]))
        xmlgen.addprop_withparam(Hr_c1, "stringProp", "Argument.metadata", "=")
        xmlgen.addprop_withparam(Hr_c1, "stringProp", "Argument.name",
                                 escape(variable[1]["Name" + str(pos_string)]))
        xmlgen.addprop_withparam(xml_objects[1], "boolProp", "HTTPSampler.monitor", "false")

        return xml_objects, variable, pos_string, doc

    def web_submit_data(self, variable, headtagname, level, headenHash, tailenHash, transaction_start_count, doc):
        repetitions = []
        headenHash = 0
        tailenHash = 1
        (xml_objects, headtagname, level, headenHash, tailenHash, transaction_start_count, doc) = self.common_web_url_submit_link(variable, headtagname, level, headenHash, tailenHash, transaction_start_count, doc)

        repetitions = [x for x in variable[2] if variable[2][x] > 1]

        if len(repetitions) > 1:
            if variable[2][repetitions[0]] == variable[2][repetitions[1]]:
                for i in range(0, variable[2][repetitions[0]]):
                    if i == 0:
                        k = ""
                    else:
                        k = "_" + str(i + 1)
                    (xml_objects, variable, k, doc) = self.web_submit_data_adding_variables(xml_objects, variable, pos_string=k, doc=doc)

            else:
                print "Mis-match in values/repetitions found " + str(variable[2])
        #else:
        #    (xml_objects, variable, k, doc) = self.web_submit_data_adding_variables(xml_objects, variable, pos_string="", doc=doc)

        (xml_objects, headtagname, level, headenHash, tailenHash, transaction_start_count,
         doc) = self.common_web_url_submit_link_closing(xml_objects, variable, headtagname, level, headenHash,
                                                        tailenHash, transaction_start_count, doc)
        return headtagname, level, headenHash, tailenHash, transaction_start_count, doc

    def web_custom_request(self, variable, headtagname, level, headenHash, tailenHash, transaction_start_count, doc):
        headenHash = 0
        tailenHash = 1

        (xml_objects, headtagname, level, headenHash, tailenHash, transaction_start_count,
         doc) = self.common_web_url_submit_link(variable, headtagname, level, headenHash, tailenHash,
                                                transaction_start_count, doc)

        try:
            if len(str(variable[1]['Body'])) > 0:
                xmlgen.addprop_withparam(xml_objects[1], "boolProp", "HTTPSampler.postBodyRaw", "true")
                Hr_m1 = xmlgen.addelement_withparam(xml_objects[1], "elementProp", "HTTPsampler.Arguments", "Arguments")
                Hr_c = xmlgen.addStringprop_noparam(Hr_m1, "collectionProp", "Arguments.arguments")
                Hr_c1 = xmlgen.addelement_withparam(Hr_c, "elementProp", "", "HTTPArgument")
                xmlgen.addprop_withparam(Hr_c1, "boolProp", "HTTPArgument.always_encode", "false")
                xmlgen.addprop_withparam(Hr_c1, "stringProp", "Argument.value", escape(str(variable[1]['Body']).replace("\\\"", "\"")))
                xmlgen.addprop_withparam(Hr_c1, "stringProp", "Argument.metadata", "=")
        except Exception as e:
            xmlgen.addprop_withparam(xml_objects[1], "boolProp", "HTTPSampler.postBodyRaw", "true")
            Hr_m1 = xmlgen.addelement_withparam(xml_objects[1], "elementProp", "HTTPsampler.Arguments", "Arguments")
            Hr_c = xmlgen.addStringprop_noparam(xml_objects[1], "collectionProp", "Arguments.arguments")
            Hr_c1 = xmlgen.addelement_withparam(Hr_c, "elementProp", "", "HTTPArgument")
            xmlgen.addprop_withparam(Hr_c1, "boolProp", "HTTPArgument.always_encode", "false")
            xmlgen.addprop_withparam(Hr_c1, "stringProp", "Argument.value", "")
            xmlgen.addprop_withparam(Hr_c1, "stringProp", "Argument.metadata", "=")

        (xml_objects, headtagname, level, headenHash, tailenHash, transaction_start_count,
         doc) = self.common_web_url_submit_link_closing(xml_objects, variable, headtagname, level, headenHash,
                                                        tailenHash, transaction_start_count, doc)
        return headtagname, level, headenHash, tailenHash, transaction_start_count, doc

    def lr_start_transaction(self, variable, headtagname, level, headenHash, tailenHash, transaction_start_count, doc):
        tailenHash = 1
        if transaction_start_count == 0:
            headenHash = 1
        else:
            headenHash = 0
        transaction_start_count = transaction_start_count + 1
        start_transaction_name = variable[1][self.method]

        doc = xmlgen.Transactioncontroller(headtagname, level, headenHash, tailenHash, start_transaction_name.strip(),
                                           doc)
        level = level + 1
        return headtagname, level, headenHash, tailenHash, transaction_start_count, doc

    def lr_end_transaction(self, variable, headtagname, level, headenHash, tailenHash, transaction_start_count, doc):
        level = level - 1
        return headtagname, level, headenHash, tailenHash, transaction_start_count, doc

    def lr_think_time(self, variable, headtagname, level, headenHash, tailenHash, transaction_start_count, doc):
        try:
            value = variable[1]['lr_think_time'].strip() + "000"
            doc = xmlgen.testAction(headtagname, level, value, doc)
        except Exception as e:
            print "Exception - lr_think_time" + str(e) + "   " + str(variable[1]['lr_think_time'])
        return headtagname, level, headenHash, tailenHash, transaction_start_count, doc

    def common_web_url_submit_link(self, variable, headtagname, level, headenHash, tailenHash, transaction_start_count, doc):
        t = xmlgen.extract_latesttag(headtagname, int(level))
        end_body = len(variable[1])
        if int(headenHash) == 1:
            t = xmlgen.addStringprop_noparam(t, 'hashTree')
        Hr_m = xmlgen.addelement_withparam(t, "HTTPSamplerProxy", "HttpTestSampleGui", "HTTPSamplerProxy",
                                           str(variable[1][variable[0].strip()]),
                                           "true")
        Hr_m1 = xmlgen.addelement_withparam(Hr_m, "elementProp", "HTTPsampler.Arguments", "Arguments",
                                            "HTTPArgumentsPanel",
                                            "Arguments", "User Defined Variables", "true")
        Hr_c = xmlgen.addStringprop_noparam(Hr_m1, "collectionProp", "Arguments.arguments")

        return [t, Hr_m, Hr_c], headtagname, level, headenHash, tailenHash, transaction_start_count, doc

    def common_web_url_submit_link_closing(self, xml_objects, variable, headtagname, level, headenHash, tailenHash,
                                       transaction_start_count, doc):
        try:
            method_type = variable[1]['Method']
        except Exception as e:
            method_type = "GET"

        try:
            if 'Action' in variable[1].keys():
                path = variable[1]['Action']
            elif 'URL' in variable[1].keys():
                path = variable[1]['URL']
            else:
                path = "NOT_FOUND"
                print "Please verify - cannot find path in " + str(variable)
        except Exception as e:
            path = "NOT_FOUND"
            print "Please verify - cannot find path in " + str(variable)


        t = xml_objects[0]
        Hr_m = xml_objects[1]
        xmlgen.addprop_withparam(Hr_m, "stringProp", "HTTPSampler.domain", "")
        xmlgen.addprop_withparam(Hr_m, "stringProp", "HTTPSampler.port", "")
        xmlgen.addprop_withparam(Hr_m, "stringProp", "HTTPSampler.connect_timeout", "")
        xmlgen.addprop_withparam(Hr_m, "stringProp", "HTTPSampler.response_timeout", "")
        xmlgen.addprop_withparam(Hr_m, "stringProp", "HTTPSampler.protocol", "")
        xmlgen.addprop_withparam(Hr_m, "stringProp", "HTTPSampler.contentEncoding", "")
        xmlgen.addprop_withparam(Hr_m, "stringProp", "HTTPSampler.method", method_type)
        xmlgen.addprop_withparam(Hr_m, "stringProp", "HTTPSampler.path", escape(path))
        xmlgen.addprop_withparam(Hr_m, "stringProp", "HTTPSampler.embedded_url_re", "")
        xmlgen.addprop_withparam(Hr_m, "boolProp", "HTTPSampler.follow_redirects", "true")
        xmlgen.addprop_withparam(Hr_m, "boolProp", "HTTPSampler.auto_redirects", "false")
        xmlgen.addprop_withparam(Hr_m, "boolProp", "HTTPSampler.use_keepalive", "true")
        xmlgen.addprop_withparam(Hr_m, "boolProp", "HTTPSampler.DO_MULTIPART_POST", "false")

        if int(tailenHash) == 1:
            xmlgen.addStringprop_noparam(t, 'hashTree')

        return [Hr_m], headtagname, level, headenHash, tailenHash, transaction_start_count, doc

    def web_add_header(self, variable, headtagname, level, headenHash, tailenHash, transaction_start_count, doc):
        try:
            self.value_web_add_header.extend([variable[1]['web_add_header'].split(",")])
        except Exception as e:
            print e
            print "unable to process " + str(variable)
        return headtagname, level, headenHash, tailenHash, transaction_start_count, doc


    def web_add_auto_header(self, variable, headtagname, level, headenHash, tailenHash, transaction_start_count, doc):
        try:
            self.value_web_add_header.extend([variable[1]['web_add_auto_header'].split(",")])
        except Exception as e:
            print e
            print "unable to process " + str(variable)
        return headtagname, level, headenHash, tailenHash, transaction_start_count, doc


    def add_web_add_header(self, value_web_add_header, headtagname, level, headenHash, tailenHash, transaction_start_count, doc):
        try:
            t = xmlgen.extract_latesttag(headtagname, int(level))
            if int(headenHash) == 1:
                t = xmlgen.addStringprop_noparam(t, 'hashTree')
            Hr_m = xmlgen.addelement_withparam(t, "HeaderManager", "HeaderPanel", "HeaderManager", "HTTP Header Manager",
                                               "true")
            Hr_c = xmlgen.addStringprop_noparam(Hr_m, "collectionProp", "HeaderManager.headers")

            for i in range(0, len(value_web_add_header)):
                Hr_c1 = xmlgen.addelement_withparam(Hr_c, "elementProp", "", "Header")
                xmlgen.addprop_withparam(Hr_c1, "stringProp", "Header.name",
                                             str(value_web_add_header[i][0].replace("\"", "")).strip())
                xmlgen.addprop_withparam(Hr_c1, "stringProp", "Header.value",
                                             str(value_web_add_header[i][1].replace("\"", "")).strip())

            self.value_web_add_header[:] = []

            if int(tailenHash) == 1:
                xmlgen.addStringprop_noparam(t, 'hashTree')

            return headtagname, level - 1 , headenHash, tailenHash, transaction_start_count, doc
        except Exception as e:
            print "error in add_web_add_header : " + str(e)

    def web_reg_find(self, variable, headtagname, level, headenHash, tailenHash, transaction_start_count, doc):
        try:
            self.value_web_reg_find.extend([variable[1]])
        except Exception as e:
            print "Error message : " + str(e)
            print "unable to process " + str(variable)
        return headtagname, level, headenHash, tailenHash, transaction_start_count, doc

    def add_web_reg_find(self, value_web_reg_find, headtagname, level, headenHash, tailenHash, transaction_start_count, doc):
        initial_level = level
        t = xmlgen.extract_latesttag(headtagname, int(level))

        for items in range(0, len(value_web_reg_find)):
            if int(items) == "0":
                ra1 = xmlgen.addStringprop_noparam(t, 'hashTree')
            else:
                ra1 = t

            try:
                if value_web_reg_find[items]['SaveCount'] > 0:

                    try:
                        variable_to_save_param = [{'Ord': 'All', 'LB': ' ', 'RB': value_web_reg_find[items]['Text/IC'], 'web_reg_save_param': value_web_reg_find[items]['Text/IC']}]
                    except Exception as e:
                        try:
                            variable_to_save_param = [{'Ord': 'All', 'LB': ' ', 'RB': value_web_reg_find[items]['Text'], 'web_reg_save_param': value_web_reg_find[items]['Text']}]
                        except Exception as e:
                            variable_to_save_param = [{'Ord': 'All', 'LB': ' ', 'RB': ' ',
                                                      'web_reg_save_param': ' '}]
                            print "something went wrong while processing web_reg_find with savecount " + str(value_web_reg_find[items])

                        (page_hash, level, headenHash, tailenHash, transaction_start_count,doc) = self.add_web_reg_save_param(variable_to_save_param, headtagname, level, headenHash, tailenHash, transaction_start_count, doc)

                    level = initial_level
                    variable_to_save_param[:] = []
            except Exception as e:
                try:
                    name = str(value_web_reg_find[items]['Text/IC'])
                except Exception as e:
                    try:
                        name = str(value_web_reg_find[items]['Text'])
                    except Exception as e:
                        print "cannot process web_reg_find " + str(e)

                doc = xmlgen.responseassertion(ra1, name.replace("\\\"", "\""), doc)
        self.value_web_reg_find[:] = []

        return headtagname, level - 1, headenHash, tailenHash, transaction_start_count, doc

    def web_reg_save_param(self, variable, headtagname, level, headenHash, tailenHash, transaction_start_count, doc):
        try:
            self.value_web_reg_save_param.extend([variable[1]])
        except Exception as e:
            print "Error message : " + str(e)
            print "unable to process " + str(variable)
        return headtagname, level, headenHash, tailenHash, transaction_start_count, doc

    def web_reg_save_param_ex(self, variable, headtagname, level, headenHash, tailenHash, transaction_start_count, doc):
        try:
            self.value_web_reg_save_param.extend([variable[1]])
        except Exception as e:
            print "Error message : " + str(e)
            print "unable to process " + str(variable)
        return headtagname, level, headenHash, tailenHash, transaction_start_count, doc

    def web_reg_save_param_regexp(self, variable, headtagname, level, headenHash, tailenHash, transaction_start_count, doc):
        try:
            self.value_web_reg_save_param.extend([variable[1]])
        except Exception as e:
            print "Error message : " + str(e)
            print "unable to process " + str(variable)
        return headtagname, level, headenHash, tailenHash, transaction_start_count, doc


    def add_web_reg_save_param(self, value_web_reg_save_param, headtagname, level, headenHash, tailenHash, transaction_start_count, doc):
        name = ""
        expression_capture_value = ""

        t = xmlgen.extract_latesttag(headtagname, level)

        for items in range(0, len(value_web_reg_save_param)):
            if int(items) == "0":
                h1 = xmlgen.addStringprop_noparam(t, 'hashTree')
            else:
                h1 = t

            try:
                name = str(value_web_reg_save_param[items]['ParamName'])
            except Exception as e:
                name = str(value_web_reg_save_param[items]['web_reg_save_param'])
            if len(name) < 1:
                print "Something went wrong in capturing name for web_reg_save_param !!! name cannot be empty : " + str(value_web_reg_save_param)

            try:
                captured_ordinal = value_web_reg_save_param[items]['Ordinal'].strip()
            except Exception as e:
                try:
                    captured_ordinal = value_web_reg_save_param[items]['Ord'].strip()
                except Exception as e:
                    print "Error while calculating Ordinal : " + str(e)
                    captured_ordinal = "1"

            if "ALL" in captured_ordinal.upper():
                ordinal = "-1"
            elif captured_ordinal.isdigit():
                ordinal = captured_ordinal
            else:
                ordinal = "1"

            try:
                if len(value_web_reg_save_param[items]['LB/IC']) > 1 or len(value_web_reg_save_param[items]['RB/IC']) > 1:
                    expression_capture_value = str(value_web_reg_save_param[items]['LB/IC']) + "(.*?)" + str(value_web_reg_save_param[items]['RB/IC'])
                else:
                    print "either of LB/IC or RB/IC is empty"
                    expression_capture_value = ""
            except Exception:
                try:
                    if len(value_web_reg_save_param[items]['LB']) > 1 or len(value_web_reg_save_param[items]['RB']) > 1:
                        expression_capture_value = str(value_web_reg_save_param[items]['LB']) + "(.*?)" + str(value_web_reg_save_param[items]['RB'])
                    else:
                        print "either of LB/IC or RB/IC is empty"
                        expression_capture_value = ""
                except Exception as e:
                    try:
                        if len(value_web_reg_save_param[items]['RegExp']) > 1:
                            expression_capture_value = str(value_web_reg_save_param[items]['RegExp'])
                        else:
                            print "Seems RegExp is empty"
                            expression_capture_value = ""
                    except Exception as e:
                        print e
                        print "Cannot create regular expression for : " + str(value_web_reg_save_param[items])

            self.parameters_list.append(name)

            rex_m = xmlgen.addelement_withparam(h1, "RegexExtractor", "RegexExtractorGui", "RegexExtractor", name,
                                                "true")
            xmlgen.addprop_withparam(rex_m, "stringProp", "RegexExtractor.useHeaders", "false")
            xmlgen.addprop_withparam(rex_m, "stringProp", "RegexExtractor.refname", str(name))
            xmlgen.addprop_withparam(rex_m, "stringProp", "RegexExtractor.regex", escape(expression_capture_value).replace("\\",""))
            xmlgen.addprop_withparam(rex_m, "stringProp", "RegexExtractor.template", "$1$")
            xmlgen.addprop_withparam(rex_m, "stringProp", "RegexExtractor.default", "NOT_FOUND")
            xmlgen.addprop_withparam(rex_m, "stringProp", "RegexExtractor.match_number", str(ordinal))
            xmlgen.addStringprop_noparam(h1, 'hashTree')
        self.value_web_reg_save_param[:] = []
        return headtagname, level - 1, headenHash, tailenHash, transaction_start_count, doc

    def get_parameters_list(self):
        return self.parameters_list