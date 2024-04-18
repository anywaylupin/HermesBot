from . import abstract
from libs import exchange
from helpers import logger
from telegram import Update

COMMAND = "sandbox"
DESCRIPTION = "Toggle the exchange sandbox mode"


class SandboxCommand(abstract.AbstractCommand):
    """
    Command to toggle the exchange sandbox mode.

    Attributes:
        command: The command string.
        sandbox_mode: Indicates whether the sandbox mode is enabled.
    """

    def __init__(self):
        """
        Initializes the SandboxCommand.
        """
        super().__init__(COMMAND)
        self.__sandbox_mode = False

    @property
    def sandbox_mode(self):
        """
        Get the current sandbox mode.
        """
        return self.__sandbox_mode

    @sandbox_mode.setter
    def sandbox_mode(self, enable: bool):
        """
        Set the sandbox mode.

        Args:
            enable: True to enable, False to disable the sandbox mode.
        """
        self.__sandbox_mode = enable

    async def on_execute(self, update: Update):
        """
        Executes the SandboxCommand by toggling the exchange sandbox mode.

        Args:
            update: The incoming update.
        """
        msg_parts = update.message.text.lower().split()
        action = msg_parts[-1]

        if len(msg_parts) == 1:
            enable = not self.sandbox_mode
        elif len(msg_parts) == 2 and action in ["on", "enable", "true"]:
            enable = True
        elif len(msg_parts) == 2 and action in ["off", "disable", "false"]:
            enable = False
        else:
            await logger.update_error(update, "Invalid command format. Use '/sandbox' or '/sandbox on|off|enable|disable|true|false' to toggle sandbox mode.")
            return

        self.sandbox_mode = enable
        exchange.set_sandbox_mode(enable)

        response = f"Sandbox mode {"enabled" if enable else "disabled"}"
        logger.info(response)
        await update.message.reply_text(response)
