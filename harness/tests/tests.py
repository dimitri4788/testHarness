from collections import OrderedDict
from enum import Enum
import json

from ..definitions import POST_TESTS, GET_TESTS, PUT_TESTS, DELETE_TESTS


class TestType(Enum):
    """This class represents the enum for the test-type."""

    UNKNOWN_TYPE, POST_TYPE, GET_TYPE, PUT_TYPE, DELETE_TYPE = range(5)


class Test():
    """This class represents a single test.

    Attributes:
        description (str): The description of the test
        testNumber (str): The test-number of the test
        testType (TestType): The type of the test
        disableTest (int): Integer denoting whether the test if disabled or not
        dependOnTests (list): A list of other tests that the current test depends on
        attributes (dict): A dictionary of the attributes belonging to a test
    """

    def __init__(self,
                 description="",
                 testNumber="",
                 testType=TestType.UNKNOWN_TYPE.name,
                 disableTest=0,
                 executed=False,
                 executeStatus="P",
                 dependOnTests=None,
                 attributes=None):
        self.description = description
        self.testNumber = testNumber
        self.testType = testType
        self.disableTest = disableTest
        self.executed = executed
        self.executeStatus = executeStatus  # Either "P" (passed) or "F" (failed)
        if dependOnTests is None:
            self.dependOnTests = []
        else:
            self.dependOnTests = dependOnTests
        if attributes is None:
            self.attributes = {}
        else:
            self.attributes = attributes

    def __repr__(self):
        """Returns a string representation of Test object."""

        return "%s:#%s - %s" % (self.testType, self.testNumber, self.description)

    # __str__ is the same as __repr__
    __str__ = __repr__

    @property
    def attributesJson(self):
        """This property method returns a json representation of the test's attributes."""

        try:
            jsonData = json.dumps(self.attributes)
            return jsonData
        except(TypeError, ValueError) as err:
            print 'ERROR: json.dumps() did not succeed:', err

    @property
    def jsonRequest(self):
        """This property method returns a json request of the test's attributes."""

        requestDict = {}
        if "method" in self.attributes.keys():
            requestDict["method"] = self.attributes["method"]
        if "username" in self.attributes.keys():
            requestDict["username"] = self.attributes["username"]
        if "password" in self.attributes.keys():
            requestDict["password"] = self.attributes["password"]
        if "paths" in self.attributes.keys():
            requestDict["paths"] = self.attributes["paths"]

        try:
            jsonReq = json.dumps(requestDict)
            return jsonReq
        except(TypeError, ValueError) as err:
            print 'ERROR: json.dumps() did not succeed:', err


class TestsBase():
    """This class represents the base class for all the tests.

    This class loads the tests and returns all the tests to
    the user.
    """

    listsOfTests = OrderedDict()
    totalNumberOfTests = 0

    @classmethod
    def loadTests(cls, testMacro=None):
        """Creates a list of tests and fills in listsOfTests.

        Args:
            testMacro (list): The list of the test macros (POST_TESTS, GET_TESTS, PUT_TESTS, DELETE_TESTS).
        """

        if testMacro is None:
            # By default, run all the tests
            testMacro = ["POST_TESTS", "GET_TESTS", "PUT_TESTS", "DELETE_TESTS"]

        for macro in testMacro:
            dictTestObj = eval(macro)
            dictTestObj = iter(sorted(dictTestObj.iteritems()))

            for testKey, testValue in dictTestObj:
                disableTestChecker = False

                # Create a new Test object
                testObj = Test()
                testObj.testNumber = testKey
                if macro is "POST_TESTS":
                    testObj.testType = TestType.POST_TYPE.name
                elif macro is "GET_TESTS":
                    testObj.testType = TestType.GET_TYPE.name
                elif macro is "PUT_TESTS":
                    testObj.testType = TestType.PUT_TYPE.name
                elif macro is "DELETE_TESTS":
                    testObj.testType = TestType.DELETE_TYPE.name

                # Loop over all the keys-values in a test
                for k, v in testValue.iteritems():
                    # Check if the test is supposed to be disabled
                    if "disableTest" in k:
                        if v:
                            testObj.disableTest = v
                            if v is "1":
                                disableTestChecker = True
                                break
                            else:
                                cls.totalNumberOfTests += 1

                    if "description" in k:
                        if v:
                            testObj.description = v

                    if "dependOnTests" in k:
                        if v:
                            testObj.dependOnTests = v.split()

                    if "method" in k:
                        if v:
                            testObj.attributes["method"] = v

                    if "username" in k:
                        if v:
                            testObj.attributes["username"] = v

                    if "password" in k:
                        if v:
                            testObj.attributes["password"] = v

                    if "paths" in k:
                        if v:
                            testObj.attributes["paths"] = v

                    if "serverResponse" in k:
                        if v:
                            testObj.attributes["serverResponse"] = v

                # Don't add the test to listsOfTests if it was disabled
                if disableTestChecker:
                    continue
                else:
                    cls.listsOfTests[macro+":"+testKey] = testObj

    @classmethod
    def getTest(cls, fullQualifiedName):
        """This method returns the test object based on the fully-qualified name of the test.

        Args:
            fullQualifiedName (str): The fully qualified name of the test.
        """

        return cls.listsOfTests[fullQualifiedName]

    @classmethod
    def getAllTestsGenerator(cls):
        """This method returns the generator for the list of all the tests.

        Yields:
            Testname (str), Test: The next test-name and Test Object in the listsOfTests
        """

        keys = cls.listsOfTests.iterkeys()
        for key in keys:
            yield key, cls.listsOfTests[key]

    @classmethod
    def getTotalNumberOfTests(cls):
        """This method returns the total number of tests.

        Returns:
            The total number of Test objects in listsOfTests
        """

        return cls.totalNumberOfTests
