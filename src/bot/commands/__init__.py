from bot.commands.AbstractCommand import AbstractCommand
from bot.commands.BalanceCommand import BalanceCommand
from bot.commands.HelpCommand import HelpCommand
from bot.commands.SandboxCommand import SandboxCommand
from bot.commands.StartCommand import StartCommand

command_set: list[AbstractCommand] = [
    BalanceCommand(),
    HelpCommand(),
    SandboxCommand(),
    StartCommand(),
]
