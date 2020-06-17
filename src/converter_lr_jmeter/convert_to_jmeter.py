from definitions import lr_defs
import re

def multiline_extract(keyword_array, file_input, index_processed_file):
    i = index_processed_file
    http_object = lr_defs.http_request()
    temp_out_dict = {}
    keyword_match_counts = {}

    try:
        (keywords, delim, terminate, one_liner, multi_line) = http_object.extract_definition(name=keyword_array[0].strip())

        if len(keywords) >= 1:
            if len([x for x in terminate if x in file_input[i]]) >= 1:
                temp_file_input = file_input[i]
                (temp_out_dict, keyword_match_counts) = multiline_extract_sub_function(keywords, delim, terminate, one_liner, multi_line,
                                                               temp_file_input.strip().split("\","), keyword_array, i=0)
            else:
                (temp_out_dict, keyword_match_counts) = multiline_extract_sub_function(keywords, delim, terminate, one_liner, multi_line,
                                                               file_input, keyword_array, i=index_processed_file)
        else:
            temp_out_dict = {
                keyword_array[0].strip(): file_input[index_processed_file].replace(keyword_array[0], "").replace("\"", "").strip()[1:-1]}

    except Exception as e:
        temp_out_dict = {keyword_array[0].strip(): file_input[index_processed_file].replace(keyword_array[0], "").replace("\"","").strip()[1:-2]}

    return (temp_out_dict, keyword_match_counts)


def multiline_extract_sub_function(keywords, delim, terminate, one_liner, multi_line, file_input, keyword_array, i):
    passed_i = i
    temp_out_dict = {}
    multiple_lines_object = False
    keyword_match_counts = {}
    matched_string = []


    while len([x for x in terminate if x in file_input[i]]) <= 0:
        temp_input_line = file_input[i]
        ##processing keywords
        pattern = re.compile("=(.*)?", re.IGNORECASE)
        match_keywords = [y for y in keywords if y.upper() == pattern.sub("", temp_input_line).strip()[1:].upper()]

        for keyword_items in match_keywords:
            try:
                keyword_match_counts.update({keyword_items: keyword_match_counts[keyword_items] + 1})
            except Exception as e:
                keyword_match_counts.update({keyword_items: 1})


        if one_liner == False:
            if keyword_array[0].strip() in temp_input_line:
                temp_out_dict.update({keyword_array[0].strip(): temp_input_line.replace(keyword_array[0], "").strip()[2:-2]})
        else:
            if keyword_array[0].strip() in temp_input_line:
                temp_out_dict = {}
                temp_out_dict.update({keyword_array[0].strip(): ""})
                if keyword_array[1] > 2:
                    pattern = re.compile(keyword_array[0].strip() + "(.*?)\"", re.IGNORECASE)
                    temp_input_line = pattern.sub("\"", temp_input_line.strip())

                    pattern = re.compile("=(.*)?", re.IGNORECASE)
                    match_keywords = [y for y in keywords if
                                      y.upper() == pattern.sub("", temp_input_line).strip()[1:].upper()]

        if len(match_keywords) > 0:
            if [z for z in multi_line if z.upper() == pattern.sub("", temp_input_line).strip()[1:].upper()]:
                multiple_lines_object = True


            try:
                if keyword_match_counts[match_keywords[0].strip()] == 1:
                    key_to_dict = match_keywords[0].strip()
                else:
                    key_to_dict = match_keywords[0].strip() + "_" + str(keyword_match_counts[match_keywords[0].strip()])
            except Exception as e:
                print "Something went wrong while processing " + str(keyword_array) + " - " + str(key_to_dict)


            if keyword_array in match_keywords:
                temp_input_line.replace(keyword_array, "")
            if passed_i == 0:
                temp_out_dict.update({key_to_dict: temp_input_line.replace(match_keywords[0], "").strip()[2:-2]})
            else:
                temp_out_dict.update(
                    {key_to_dict: temp_input_line.replace(match_keywords[0], "").strip()[2:-2]})

        i = i + 1

    if multiple_lines_object == True:
        temp_out_dict = multi_line_argument(keywords, delim, terminate, multi_line, file_input, keyword_array, temp_out_dict, passed_i)

    return temp_out_dict, keyword_match_counts


def multi_line_argument(keywords, delim, terminate, multi_line, file_input, keyword_array, temp_out_dict, cursor_position):
    pattern = re.compile("=(.*)?", re.IGNORECASE)
    temp_value_string = ""
    temp_string = ""
    len_summation = 0

    for i in range(cursor_position, len(file_input)):
        if len([x for x in multi_line if x.upper() == pattern.sub("", file_input[i]).strip()[1:].upper()]) > 0:
            temp_value_string = file_input[i].strip()
            cursor_position = i + 1
            matched_keywords = [y1 for y1 in keywords if
                                y1.upper() == pattern.sub("", file_input[i]).strip()[1:].upper()]

            break

    for i in range(cursor_position, len(file_input)):
        if (not temp_value_string == ""):
            match_keywords_2 = [y1 for y1 in keywords if
                                y1.upper() == pattern.sub("", file_input[i]).strip()[1:].upper()]
            match_delim_2 = [x for x in delim if x.upper() == pattern.sub("", file_input[i]).strip()[:-1].upper()]
            match_terminate_2 = [x for x in terminate if
                                 x.upper() == pattern.sub("", file_input[i]).strip().replace(");", "").upper()]
            len_summation = len(match_keywords_2) + len(match_delim_2) + len(match_terminate_2)

            if len_summation > 0:
                break
            else:
                temp_string = temp_string + file_input[i].strip()[1:-1]

    if temp_string == "":
        value_string = temp_value_string[1:-2] + temp_string[:-1]
    else:
        value_string = temp_value_string[1:-1] + temp_string[:-1]

    temp_out_dict.update({matched_keywords[0].strip() : value_string.replace(matched_keywords[0], "").strip()[1:]})
    return temp_out_dict

