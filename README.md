# LR_Jmeter_Converter
**LoadRunner to JMeter converter V3.0  is built on python2.7.**


**How to use the converter:**

* Download the exe (LR_to_jmeter_v2.exe)
* Run “LR_to_jmeter_v2.exe”
* Provide absolute path to the Loadrunner script
* Provide a location to save the logs and converted file
* Converted requests are saved to “converted_lines.log”, the jmx is saved as output.jmx

**NOTE: warning/Errors will be displayed on the console and will not be saved to file**

Note: correlation and text checks are added as a parent node to the request.
	Error handling will be improved in next versions.
	
**Known issues:**
1.	Multiple line post (web_custom_request) are converted with missing “” and extra “\”
2.	lr_start_transaction with "'" in the transaction name is throwing error

**Fixed issues:**

1.	path will be processed only if {url}://{servername:port} is present in the action of either web_submit_data or web_custom_request
2. 	web_reg_save_param is misinterpreted at times
3.	ordinal in web_reg_save_param_regex										
4. 	warning will be dispalyed if web_reg_find has save_count
5.	Sample hirerarchy is managed while converting 

**New features:**

1. 	web_submit_form, web_link are handelled	
2.	Creates If and while condition with "true" as condition										
3.	Reads complete Loadrunner file to process all the .c files 
4.	CSV dataset read will be created with param names and file linking
5.	Parameters are added to http_request_defaults and test plan to ease parameterization
6.	Support for Delete, PUT methods in http request
7.	longer LB, Rb are handelled more efficiently
	
