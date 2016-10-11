Test Harness
============
It is a collection of software and test data configurations to test your --- ZeroMQ based server application --- that is by running it under varying conditions and monitoring its outputs. It is easily scalable to add more test cases.  

The typical objectives here are to:  
- Automate the testing process  
- Execute test suites of test cases  
- Easily add more tests  
- Generate associated test report  

It provides the following benefits:  
- Increased productivity due to automation of the testing process  
- Increased probability that regression testing will occur  
- Increased quality of software components and application  

<br>

Dependencies
------------
- configparser==3.3.0.post2
- enum34==1.1.2
- pyzmq==15.2.0

Follow below instructions to install the libraries.

<br>

Installation
------------
```sh
# Change directory to where testharness tool is located
$ cd <PathToYourApplicationDirectory>/tools/testHarness

# Install pip
$ sudo easy_install pip

# First install virtualenv
$ sudo pip install virtualenv

# Create a new virtual environment
$ virtualenv env
# NOTE: Since we are using a version control system (Git), you shouldn't commit the env directory. Add it to your .gitignore file if it is not there.

# Activate the environment
$ source env/bin/activate
# NOTE: You should always activate the virtual environment before you start working with testHarness

# Install the dependencies for testHarness into this virtual environment
$ pip install -r requirements.txt

# Finally, install the testHarness so it is ready to be used. This will create a command line tool called "harness"
$ python setup.py install
$ python setup.py install --record files.txt  # Run this if you want to save the installed stuff for easy deletion later on

# Deactivate the virtual environment when you are done using testHarness
$ deactivate


# ######### Additional commands #########
# To delete the installed testharness binaries and other data
$ cat files.txt | xargs rm -rf

# If you want to output installed packages in requirements format (this will be saved to requirements.txt)
# This should only be ran if you install new libraries in the virtual environment that testharness depends on
$ pip freeze > requirements.txt
```

<br>

How to run it
-------------
- Make sure your ZeroMQ based server application is up-and-running
- Modify **config.cfg** according to your setup
- Add more tests to **harness/definitions.py** as per your need, or you can run the currently available tests
- From the terminal, run

```sh
$ python setup.py install  # Needed to be run only when you update any file(s), for example, say you add more tests to definitions.py

# This will run the testharness
$ harness -c <path-to-config-file>

# This will give you the usage options for CLI "harness"
$ harness
```

<br>

Adding more tests
-----------------
- Add more tests by updating description and definition in **description.md** and **definitions.py** respectively.

<br>

Author
------
Deep Aggarwal  
deep.uiuc@gmail.com  
