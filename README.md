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

Known errors:
1.	Multiple line post (web_custom_request) are converted with missing “” and extra “\”

Reach to Shravanakula@ymail.com for more details or enhancements. 
	
