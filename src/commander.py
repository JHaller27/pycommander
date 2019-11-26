import re


class Command:
    """
    Represents a single executable command.
    To define a command, extend this class, override act(text), and call handle(text).
    Optionally override can_handle(text) to define more complex logic.
    By default, handle() will call act() if can_handle() returns True, but this behavior
    can be overridden.
    """
    __slots__ = ['regex', 'groups', 'next']

    def __init__(self, regex: str):
        self.regex = re.compile(regex)
        self.groups = None
        self.next = None

    def set_matches(self, text: str):
        matches = self.regex.match(text)

        if matches is None:
            self.groups = None
        elif len(matches.groupdict()) > 0:
            self.groups = matches.groupdict()
        elif len(matches.groups()) > 0:
            self.groups = matches.groups()
        else:
            self.groups = matches.string

    def can_handle(self, text: str) -> bool:
        self.set_matches(text)
        return self.groups is not None

    def handle(self, text: str):
        if self.can_handle(text):
            self.act(text)
        else:
            self.next_handle(text)

    def act(self, text):
        raise NotImplementedError()


    def next_handle(self, text):
        if self.next is not None:
            self.next.handle(text)


class _GenericCommand(Command):
    def __init__(self, regex, act_func):
        super().__init__(regex)
        self.act_func = act_func

    def act(self, text):
        return self.act_func(self, text)


class Commander:
    """
    Attach new Command implementations in a chain. Commands are evaluated in the order they are linked.
    Evaluate commands with handle(text).
    """
    def __init__(self):
        self.head = None
        self.tail = None

    def add_cls(self, cls, *args, **kwargs):
        """
        Pass a class (not an Object) and any constructor arguments.
        Creates a new instance of that class and attaches it to the end of the chain.
        """
        cmd = cls(*args, **kwargs)
        if self.head is None:
            self.head = cmd
            self.tail = cmd
        else:
            self.tail.next = cmd
            self.tail = cmd
        return self

    def add_def(self, regex, func):
        """
        Pass a regular expression to evaluate input against, and a function to act with.
        Function definition must match: func(cmd: Command, text: str).
        """
        self.link_cls(_GenericCommand, regex, func)

    def handle(self, text):
        return self.head.handle(text)


if __name__ == '__main__':
    print('Testing PyCommander')

    stack = []
    loop = True

    class PopCommand(Command):
        def __init__(self):
                super().__init__(r'pop')

        def act(self, text):
            global stack

            try:
                print(stack.pop())
            except IndexError:
                print('Stack empty!')

    class ClearCommand(Command):
        def __init__(self):
            super().__init__(r'clear')

        def act(self, text):
            global stack

            stack.clear()

    class ShowCommand(Command):
        def __init__(self):
            super().__init__(r'show')

        def act(self, text):
            global stack

            print(stack)

    def exit_cmd(self, text):
        global loop

        loop = False

    chain = Commander()
    chain.link_def(r'add (.+)', lambda self, text: stack.append(self.groups[0]))
    chain.link_cls(PopCommand)
    chain.link_cls(ClearCommand)
    chain.link_cls(ShowCommand)
    chain.link_def(r'exit', exit_cmd)

    while loop:
        chain.handle(input('> '))
