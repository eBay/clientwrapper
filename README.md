# clientwrapper (licensed under Apache 2.0)
Util class enabled CLI/dictionary syntax: allows separation of concerns between CLI and Python code.

## installation
```bash
pip install clientwrapper
```

## usage 
### overview
ClientWrapper is a class that allows you to define functions that can be run in both CLI and Python syntax.

### run in CLI
Running as a CLI requires all functions with arguments to run in one combined function. The below command will not run as a CLI.
```bash
python3 -m yourmodule authenticate --arg1 value1 --arg2 value2
# self.attributes like authentication tokens are erased every time the CLI is run; combine your functions to avoid NullPointerExceptions
python3 -m yourmodule query --argument value # will not work: relying on any attributes in self
```
Below is an example of how to run as a CLI.
```bash
python3 -m yourmodule authenticate_and_query --arg1 value1 --arg2 value2 --argument value
```

### usage example
Define your class here and inherit from ClientWrapper; combined function is required to run as a CLI.
```python
class Impl(ClientWrapper):
    def __init__(self):
        super().__init__("Some API Requests")

    def login(self, username, password):
        print("login called with username: " + username + " and password: " + password)

    def getRequest(self, argument):
        print("getRequest called with argument: " + argument)

    def postRequest(self, **kwargs):
        print("postRequest called with arguments: " + str(kwargs))  

    def login_and_get_request_and_post_request(self, username, password, argument, **kwargs):
        self.login(username, password)
        self.getRequest(argument)
        self.postRequest(**kwargs)
```

### test in CLI
Use CLI syntax to run your functions. 
```bash
python3 -m yourmodule login_and_get_request_and_post_request --username myusername --password mypassword --argument [1, 2] --arg1 value1 --arg2 value2
```

### test in Python 
Use argparse-like syntax in Python for testing purposes.
Note that Clientwrapper takes strings, ints, lists, tuples, and dictionaries as arguments but containers must be passed as strings.
```python
impl = Impl()
impl.run([
    'login_and_get_request_and_post_request --username myusername --password mypassword --argument "[1, 2]" --arg1 value1 --arg2 value2'.split()
])
>>> login called with username: myusername and password: mypassword
>>> getRequest called with argument: [1, 2]
>>> postRequest called with arguments: {'arg1': 'value1', 'arg2': 'value2'}
```

### test in CMD prompt as CLI
Your module will require a __main__.py in order to run as a CLI; here is a simple example.
```python
from src.etc.package import Impl

def main():
    impl = Impl()
    impl.run()

if __name__ == '__main__':
    main()
```