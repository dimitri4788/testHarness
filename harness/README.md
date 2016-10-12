Description of a test format
============================

This file describes the format of a test. The user can add more tests as needed.  
The test(s) should be added to the file **definitions.py** and should follow the template format described here.

<br>

Template
--------
This is a template for a test definition:  

```sh
"<testNumber>":
{
    "description": "<Description of the test>",
    "method": "<HTTP method name: GET, POST, PUT or DELETE>",
    "username": "<username>",
    "password": "<password>",
    "paths": "<Request paths for the server: either a list or a dictionary>",
    "serverResponse": "<A list of expected strings in the response from the server>",
    "dependOnTests": "<A space separated list of TEST_MACRO:testNumber that this test depends on>",
    "disableTest": "<value of 0 or 1 to signify test should be disabled or not>"
}
```

Example
-------
This is an example for a test definition:  

```sh
"7":
{
    "description": "get value of attribute groupName and age",
    "method": "GET",
    "username": "bob",
    "password": "bob123Qe!2",
    "paths": "["groupName", "age"]",
    "serverResponse": "["groupName", "age"]",
    "dependOnTests": "POST_TESTS:3 DELETE_TESTS:2",
    "disableTest": "0"
}
```

<br>

###NOTE
- The **username** and **password** attributes can be used from the module common.py
- **TEST_MACRO** can be either of: POST_TESTS, GET_TESTS, PUT_TESTS, DELETE_TESTS
- **responseStatus** can be one of the following

```sh
200 : OK
201 : Created
204 : No Content
400 : Bad Request
401 : Unauthorized
403 : Forbidden
404 : Not Found
409 : Conflict
410 : Gone
415 : Unsupported Media Type
500 : Internal Server Error
501 : Not Implemented
```
