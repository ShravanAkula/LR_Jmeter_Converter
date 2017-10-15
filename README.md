# LR_Jmeter_Converter
LoadRunner to JMeter converter V1.0  is built on python2.7.


How to use the converter:
Download the zip file,
Unzip to any desired location.
Run “LR_Parsing.exe”
Provide “.c” file from LoadRunner as input when prompted.
Provide a location to save the logs and converted file.
Converted requests are saved to “converted_lines.log”
And the jmx is saved as output.jmx.

On successful conversion, arrange the requests as per the desired flow.

Note: correlation and text checks are added as a parent node to the request.
	Error handling will be improved in next versions.
	
Known issues:
1.	Multiple line post (web_custom_request) are converted with missing “” and extra “\”
2.	web_reg_save_param is misinterpreted at times
3.	lr_start_transaction with "'" in the transaction name is throwing error

Fixed issues:

1.	path will be processed only if {url}://{servername:port} is present in the action of either web_submit_data or web_custom_request

Reach to Shravanakula@ymail.com for more details or enhancements. 
	
