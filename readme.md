# PyCommander

A Python library used to define custom commands.

# Usage

Create a Commander object and add Commands using any the methods described below.
Note that the Commander class creates help and exit commands by default.

There are 3 primary ways to create commands...

## Use Commander with functions/lambdas

This is likely the most simple version. It requires creating a `Commander` class instance and adding commands via a Regular Expression and function (either a named function or a lambda).

**Example**

```python
from pycommander.all import Command, Commander

# Global variables
message = ''

# Create the Commander
commander = Commander()

# Add commands
# Note that cmd refers to a Command instance.
#   cmd.groups is the groups evaluated from the passed-in regular expression.
#   There is only one group in the regex we defined, so the first group is the only useful item.
commander.add_def(r'echo (.+)', lambda cmd, text: print(cmd.groups[0])

# May use named functions as well as lambdas
def set_message_cmd(self, cmd, text):
    global message

    # May use named capture groups
    message = cmd.groups['msg']

# Can optionally specify help text
# (Named capture group definition)
commander.add_def(r'set (?P<msg>.+)', set_message_cmd, help='set\n\tSet global message')

# May define optional prompt parameter.
#    If prompt is a string, it will be calculated once and used for every prompt.
#    If prompt is a function (accepting no parameters and returning the prompt string),
#        the callback is called with each iteration.
commander.handle_loop(lambda: '%s> ' % message)
```

## Use Commander with Command classes

The `Command` class is instantiated with the regular expression used to match against potential input command text.
The `Command` class should be extended with the `act(text: str)` method overridden.
The `can_handle()` and `handle()` methods may optionally be overridden (for more information, see `help(Command.can_handle))` and `help(Command.handle())`).

**Example**

```python
from pycommander.all import Command, Commander

# Command implementations
class EchoCommand(Command):
    def __init__(self):
        super().__init__(self, r'echo (.+)')
    def act(self, text: str):
        print(text)
    # Help method may optionally be defined
    def help(self):
        return 'echo <text>\n\tPrint <text> to console'

class ExitCommand(Command):
    def __init__(self):
        super().__init__(self, r'echo (.+)')
    def act(self, text: str):
        global loop
        loop = False

# Global variables
loop = True

# Create the Commander
commander = Commander()

commander.add_cls(EchoCommand)
commander.add_cls(ExitCommand)

commander.handle_loop()
```

## Implement Command chain

This is nearly identical to the previous process, but Commands may be created, chained, and used without the `Commander` class.

```python
from pycommander.all import Command, Commander

# Command implementations
class EchoCommand(Command):
    def __init__(self):
        super().__init__(r'echo (.+)')
    def act(self, text: str):
        print(text)

class ExitCommand(Command):
    def __init__(self):
        super().__init__(r'exit')
    def act(self, text: str):
        global loop
        loop = False

# Global variables
loop = True

echo_cmd = EchoCommand()
exit_cmd = ExitCommand()

echo_cmd.next = exit_cmd

# Subsequent Commands must be attached to the most recently attached Command

# A custom command handling loop may be used
while loop:
    command_string = input('< ')
    
    # Only commands attached "down-stream" are evaluated, so the handle() method is usually called on the first Command
    echo_cmd.handle(command_string)
```
