# srget
## 1. Components of a program
### a) Function
* __make_request__ - take in request command, path, details, and version to construct http request and return it in string.
* __parse_url__- take in URL of a destination (in string) and return host, path, and port. If no port provided, it will return 80.
* __getHead__- take in socket that is alrady connected and sent request then return a header in string.
* __checkCode__- take in list of header and return the 100th number of http response code. eg. HTTP 200 --> return 2.
* __isHeader__ - take in a string and return boolean whether it contains "\r\n\r\n".
* __extractFromHeader__ - take in output of checkCode and list of header and return content of header according to checkCode.
If it is 2, then return either content length of header or chunked detail.
If it is 3, then return location to redirect.
otherwise, return -1.
* __isResumeFromNormal_to_multi__ - take in name of file to download and return boolean which indicate whether it is resume case in simultaneous download from single download and same destination.
* __multiDL__ - it takes in URL, filename, content length of file to download, host, output of isResumeFromNormal_to_multi, and number of simultaneous download.
This function then return list of object of class HTTPClient with conditions depending on imput details. It can create HTTPClient object in download and resume case.
* __myreceive__ - take in size of body receiving, HTTPClient object, opened file, and opened data-file.
This function will receive data from http response and write it in opended file.

### b) Class
* __HTTPClient(asyncore.dispatcher)__ take in URL, filename, request detail (None as default), isResume (False as default), isMulti (False as default), and old header (None as default).
This class import asyncore as superclass and it would create socket connection, send http request, and recieve and record http response ccording to the input given.
It will make http request according to request details provided or make normal GET request if nothing provided.
isResume and isMulti (both as boolean) would determine whether a download case is normal or resume, and single or simultaneous then it will create http request and receive response that suit each case.
This class will receive file when asyncore.loop() is ran.

### c) main()
When you run srget in terminal, it will check whether your command line is valid.
If it is invalid, it will print "Can't proceed, killing self [invalid input parameters]" and exit a system.
If it is valid, it will enter neccessary functions and create HTTPClient object that is suitable to command line given to download and save in file given in command line.

## 2. Command line
1. __srget -o <output file> URL__ - this will download file and save it as the name of output file by using single connection.
2. __srget -o <output file> -c URL__ - this will download file and save it as the name of output file by using 5 simultaneous connections.
3. __srget -o <output file> -c n URL__ - this will download file and save it as the name of output file by using n simultaneous connections.
* If a download is interrupted, by typing command line again, the program will resume download from the interrupted point if destination and filename provided are the same as interrupted one.
If they are different, program will download the new one from the beginning.
