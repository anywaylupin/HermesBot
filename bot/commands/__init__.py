from .AbstractCommand import AbstractCommand
from .BalanceCommand import BalanceCommand
from .BottomFishingCommand import BottomFishingCommand
from .HelpCommand import HelpCommand
from .SandboxCommand import SandboxCommand
from .StartCommand import StartCommand

command_set: list[AbstractCommand] = [
    BalanceCommand(),
    BottomFishingCommand(),
    HelpCommand(),
    SandboxCommand(),
    StartCommand(),
]
