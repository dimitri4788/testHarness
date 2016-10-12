#!/usr/bin/env python

###################################################
#
# testharness - Test Harness tool for <your-ZeroMQ-application-name>
# written by Deep Aggarwal (deep.uiuc@gmail.com)
#
###################################################

import json
import re
import sys
import warnings

import argparse
import configparser
import zmq

from . import __version__
from client import Client
from tests import Test, TestsBase

# Global variables
protocol, interface, port, configFileName = [None] * 4
totalNumOfTestsPassed = 0


class TEXT_COLOR:
    """This defines colors for the output stream text."""

    HEADER = '\033[95m'
    FOOTER = '\033[95m'
    PASS = '\033[32m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


def printHeader():
    """This function prints the header when the harness starts."""

    print TEXT_COLOR.HEADER + " --- Testing the <your-ZeroMQ-application-name> server STARTED" + TEXT_COLOR.ENDC


def printFooter():
    """This function prints the footer when the harness ends."""

    print TEXT_COLOR.FOOTER + " --- Testing the <your-ZeroMQ-application-name> server ENDED" + TEXT_COLOR.ENDC


def printFinalResult():
    """This function prints the final results."""

    totalNumOfTests = TestsBase.getTotalNumberOfTests()
    totalNumOfTestsFailed = totalNumOfTests - totalNumOfTestsPassed

    print
    print "#"*40
    print " "*10 + "Total tests: " + str(totalNumOfTests)
    print " "*10 + TEXT_COLOR.PASS + "Passed tests: " + str(totalNumOfTestsPassed) + TEXT_COLOR.ENDC
    print " "*10 + TEXT_COLOR.FAIL + "Failed tests: " + str(totalNumOfTestsFailed) + TEXT_COLOR.ENDC
    print "#"*40


def printResult(dependTestObj, success):
    """This function prints the result to the output stream.

    Args:
        dependTestObj (Test): The Test object which needs to be printed
        success (bool): The success of the Test execution
    """

    global totalNumOfTestsPassed

    if configFileName:
        with open(configFileName, 'a+') as f:
            f.write(repr(dependTestObj))
            f.write(": ")
            if success:
                f.write("PASSED")
            else:
                f.write("FAILED")
            f.write("\n")
    else:
        if success:
            print repr(dependTestObj), TEXT_COLOR.PASS + "PASSED" + TEXT_COLOR.ENDC
            totalNumOfTestsPassed += 1
        else:
            print repr(dependTestObj), TEXT_COLOR.FAIL + "FAILED" + TEXT_COLOR.ENDC


def asciiEnc(x):
    """This function encodes x as ascii encoding.

    Args:
        x (str): The string data that needs to be encoded as ascii
    """

    return x.encode('ascii')


def asciiEncodeDict(data):
    """This function converts unicode strings to byte strings.

    Args:
        data (str): The string data that needs to be converted to byte string
    """

    return dict(map(asciiEnc, pair) for pair in data.items())


def ordered(obj):
    """This function recursively sorts any lists it finds (and converts dictionaries
    to lists of (key, value) pairs so that they're orderable.)

    Args:
        obj (object): An object instance of a class, type or a tuple containing classes, types or other tuples
    """

    if isinstance(obj, dict):  # Return true if the obj argument is an instance of the dict argument
        return sorted((k, ordered(v)) for k, v in obj.items())
    if isinstance(obj, list):  # Return true if the obj argument is an instance of the list argument
        return sorted(ordered(x) for x in obj)
    else:
        return obj


def successOfATest(testAttributes, resultOfTestRun):
    """This function checks if the test passed or not.

    Args:
        testAttributes (dict): The attributes of a test
        resultOfTestRun (str): The actual response results of the test execution
    """

    testSucceeded = True
    for responseString in testAttributes["serverResponse"]:
        stringMatch = re.findall(r'%s' % (responseString), resultOfTestRun)
        if not stringMatch:
            testSucceeded = False
            break

    return testSucceeded


def executeTest(testObj):
    """This function runs the test. It does it by sending
    requests to the server using Client.

    Args:
        testObj (Test): The Test object

    Returns:
        The received data from the server.
    """

    # Create client object and connect to the server
    client = Client(protocol, interface, port, zmq.REQ)
    client.connect()

    client.sendData(testObj.jsonRequest)
    recData = client.receiveData()

    return recData


def harness():
    """This is the master function where magic happens."""

    # Load and get all the tests
    TestsBase.loadTests()
    listsOfTests = TestsBase.getAllTestsGenerator()

    # Loop over all the tests and execute them
    for fullTestName, test in listsOfTests:
        # Continue with next test if this one is already executed or failed in the past execution
        if test.executed or test.executeStatus is "F":
            continue

        # Check if the test depends on the other test and execute them first
        resultOfTestRun = ""
        checkSuccess = True
        if test.dependOnTests:
            for dependTestName in test.dependOnTests:
                dependTestObj = TestsBase.getTest(dependTestName)

                if not dependTestObj.executed:  # Execute it if not executed yet
                    resultOfTestRun = executeTest(dependTestObj)
                    checkSuccess = successOfATest(dependTestObj.attributes, resultOfTestRun)
                    printResult(dependTestObj, checkSuccess)
                    if checkSuccess:
                        dependTestObj.executed = True
                    else:
                        dependTestObj.executeStatus = "F"  # To prevent the execution again for a failed test
                        break  # Break since we want all the dependent tests to succeed

        # Execute the current test
        if checkSuccess:
            resultOfTestRun = executeTest(test)
            checkSuccess = successOfATest(test.attributes, resultOfTestRun)
            printResult(test, checkSuccess)
            if checkSuccess:
                test.executed = True
            else:
                test.executeStatus = "F"


def getParser():
    """This function creates an argparse.ArgumentParser object.

    Returns:
        The argparse.ArgumentParser object
    """

    parser = argparse.ArgumentParser(description='Test Harness tool for <your-ZeroMQ-application-name>')
    parser.add_argument('-c', '--config', help='path to configuration file to start test-harness', type=str, metavar='CONFIG')
    parser.add_argument('-f', '--file', help='file name to save the results in', metavar='FILE')
    parser.add_argument('-v', '--version', help='displays the current version of test-harness', action='store_true')
    return parser


def main():
    """This function is where the test-harness starts."""

    # Get global variables since we will modify them
    global protocol, interface, port, configFileName

    # Get the argument parser and arguments
    parser = getParser()
    args = vars(parser.parse_args())

    # If nothing is passed, print usage
    if not args['version'] and not args['config'] and not args['file']:
        parser.print_help()
        return

    # If only file is passed is passed, print usage
    if not args['version'] and not args['config'] and args['file']:
        parser.print_help()
        return

    # If version is passed, print it
    if args['version']:
        print(__version__)
        return

    # If file is passed, use it for writing output
    if args['file']:
        configFileName = args['file']

    # Get the configurations
    config = configparser.ConfigParser()
    if args['config']:
        # Get the values from the configuration file
        config.read(args['config'])
        protocol = config['ZeroMQServerInfo']['protocol']
        interface = config['ZeroMQServerInfo']['interface']
        port = config['ZeroMQServerInfo']['port']

    # Print the header as we are starting the harness
    printHeader()

    # Call the master function
    harness()

    # Print the footer as we are ending the harness
    printFooter()

    # Print final results
    printFinalResult()


# Execute only if run as a script
if __name__ == "__main__":
    main()
