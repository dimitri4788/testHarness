from tests.common import *  # NOTE: Not a good practice in general, but it is not going to matter in this case


POST_TESTS = {
    "1":
    {
        "description": "create new account with @username1 and @password1",
        "method": "POST",
        "username": "%s" % (username1),
        "password": "%s" % (password1),
        "paths": {"name": "deep", "age": "28"},
        "serverResponse": ["201", "Created"],
        "dependOnTests": "",
        "disableTest": "0"
    },
    "2":
    {
        "description": "create existing account with @username1 and @password1",
        "method": "POST",
        "username": "%s" % (username1),
        "password": "%s" % (password1),
        "paths": {"name": "deep", "age": "28"},
        "serverResponse": ["409", "Conflict"],
        "dependOnTests": "",
        "disableTest": "0"
    },
    "3":
    {
        "description": "add new attributes in existing account with @username1 and @password1",
        "method": "POST",
        "username": "%s" % (username1),
        "password": "",
        "paths": {"office": "london", "phone-number": "999-999-0000"},
        "serverResponse": ["200", "OK"],
        "dependOnTests": "POST_TESTS:1",
        "disableTest": "0"
    },
    "4":
    {
        "description": "authenticate account with @username1 and @password1",
        "method": "POST",
        "username": "%s" % (username1),
        "password": "%s" % (password1),
        "paths": {},
        "serverResponse": ["200", "OK"],
        "dependOnTests": "POST_TESTS:1",
        "disableTest": "0"
    }
}

GET_TESTS = {
    "1":
    {
        "description": "get all attributes from account with @username1",
        "method": "GET",
        "username": "%s" % (username1),
        "password": "",
        "paths": [],
        "serverResponse": ["name", "deep", "age", "28", "OK", "200", "password"],
        "dependOnTests": "POST_TESTS:1",
        "disableTest": "0"
    },
    "2":
    {
        "description": "get a non existing attribute from account with @username1",
        "method": "GET",
        "username": "%s" % (username1),
        "password": "",
        "paths": ["fav-movie-name"],
        "serverResponse": ["200", "OK", "fav-movie-name", "Not Exist/Error"],
        "dependOnTests": "POST_TESTS:1",
        "disableTest": "0"
    },
    "3":
    {
        "description": "get name attribute from account with @username1 after deleting name",
        "method": "GET",
        "username": "%s" % (username1),
        "password": "",
        "paths": ["name"],
        "serverResponse": ["200", "OK", "Not Exist/Error"],
        "dependOnTests": "POST_TESTS:1 DELETE_TESTS:1",
        "disableTest": "0"
    }
}

PUT_TESTS = {
    "1":
    {
        "description": "update attribute - name - in account @username1",
        "method": "PUT",
        "username": "%s" % (username1),
        "password": "",
        "paths": {"name": "mike"},
        "serverResponse": ["200", "OK", "name"],
        "dependOnTests": "POST_TESTS:1",
        "disableTest": "0"
    },
    "2":
    {
        "description": "update attribute - office - in non-existing account @incorrectUsername",
        "method": "PUT",
        "username": "%s" % (incorrectUsername),
        "password": "",
        "paths": {"office": "china"},
        "serverResponse": ["404", "Not Found"],
        "dependOnTests": "",
        "disableTest": "0"
    }
}

DELETE_TESTS = {
    "1":
    {
        "description": "delete - name - attribute from account with @username1",
        "method": "DELETE",
        "username": "%s" % (username1),
        "password": "",
        "paths": ["name"],
        "serverResponse": ["200", "OK"],
        "dependOnTests": "POST_TESTS:1",
        "disableTest": "0"
    },
    "2":
    {
        "description": "delete - age - attribute from non-existing account with @incorrectUsername",
        "method": "DELETE",
        "username": "%s" % (incorrectUsername),
        "password": "",
        "paths": ["age"],
        "serverResponse": ["404", "Not Found"],
        "dependOnTests": "",
        "disableTest": "0"
    }
}
