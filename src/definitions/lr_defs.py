class http_request:
    lr_web_elements = {
        "web_url": {
            "keywords": ["URL", "TargetFrame", "TargetBrowser", "Resource", "RecContentType", "Snapshot", "Mode",
                         "Referer"],
            "delim": {},
            "terminate": ["EXTRARES", "LAST"],
            "multi_line":[],
            "one_line": False},
        "web_submit_data": {
            "keywords": ["Action", "Method", "TargetFrame", "RecContentType", "Referer", "Snapshot", "Mode", "EncType",
                         "Name", "Value", "File", "ContentType", "FilePath", "ENDITEM"],
            "delim": {"ITEMDATA": ["Name", "Value", "File", "ContentType", "FilePath"], "ENDITEM": ["ENDITEM"]},
            "terminate": ["EXTRARES", "LAST"],
            "multi_line": [],
            "one_line": False},
        "web_custom_request": {
            "keywords": ["Method", "URL", "BodyFilePath", "Body", "TargetFrame", "Resource", "RecContentType",
                         "Referer", "EncType", "Snapshot"],
            "delim": {"ITEMDATA", "EXTRARES"},
            "terminate": ["LAST"],
            "multi_line": ["Body"],
            "one_line": False},
        "web_reg_find": {
            "keywords": ["Text/IC", "SaveCount", "Text", "Fail", "ID", "Search"],
            "delim": {},
            "terminate": ["LAST"],
            "multi_line": [],
            "one_line": False},
        "web_reg_save_param": {
            "keywords": ["ParamName", "LB/IC", "RB/IC", "LB", "RB", "Ordinal", "Ord", "SaveLen", "DFEs", "RegExp", ],
            "delim": {"SEARCH_FILTERS": ["Scope", "RequestUrl"]},
            "terminate": ["LAST"],
            "multi_line": [],
            "one_line": False},
        "web_reg_save_param_ex": {
            "keywords": ["ParamName", "LB/IC", "RB/IC", "LB", "RB", "Ordinal", "SaveLen", "DFEs", "RegExp"],
            "delim": {"SEARCH_FILTERS": ["Scope", "RequestUrl"]},
            "terminate": ["LAST"],
            "multi_line": [],
            "one_line": False},
        "web_reg_save_param_regexp": {
            "keywords": ['ParamName', 'RegExp', 'Ordinal', 'Scope'],
            "delim": {'SEARCH_FILTERS': ['RequestUrl', 'Scope']},
            "terminate": ["SEARCH_FILTERS", "LAST"],
            "multi_line": [],
            "one_line": False},
        "lr_end_transaction": {
            "keywords": [],
            "delim": {},
            "terminate": ["LR_AUTO", "LR_PASS", "LR_FAIL"],
            "multi_line": [],
            "one_line": True},
        "nokeys": ["lr_start_transaction", "lr_end_transaction", "lr_think_time", "web_add_header", "web_add_auto_header", "web_revert_auto_header"],
        "common_script": ["web_add_cookie",],
        "replace_url_from": ['URL', 'Referer', 'Action']
    }


    def http_request(self):
        return self.lr_web_elements


    def extract_definition(self, name):
        extracted_value = self.lr_web_elements.get(name)
        temp_keywords = extracted_value['keywords']
        temp_delim = extracted_value['delim']
        temp_terminate = extracted_value['terminate']
        temp_one_liner = extracted_value['one_line']
        temp_multi_line = extracted_value['multi_line']
        return temp_keywords, temp_delim, temp_terminate, temp_one_liner, temp_multi_line

