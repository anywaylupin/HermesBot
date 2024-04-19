from . import abstract
from libs import exchange
from telegram import Update

COMMAND = "sandbox"
DESCRIPTION = "Toggle the exchange sandbox mode"


class SandboxCommand(abstract.AbstractCommand):
    """
    Command to toggle the exchange sandbox mode.

    Args:
        sandbox_mode: True to enable, False to disable the sandbox mode.
    """

    def __init__(self, sandbox_mode=False):
        """
        Initializes the SandboxCommand.
        """
        super().__init__(COMMAND)
        self.__sandbox_mode = sandbox_mode

    @property
    def sandbox_mode(self) -> bool:
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
        if not isinstance(enable, bool):
            raise TypeError("Expected boolean type for enable, got something else")
        self.__sandbox_mode = enable

    async def on_execute(self, update: Update, text: str):
        try:
            msg_parts = text.lower().split()
            action = msg_parts[-1]
            if len(msg_parts) == 1:
                enable = not self.sandbox_mode
            elif len(msg_parts) == 2 and action in ["on", "enable", "true"]:
                enable = True
            elif len(msg_parts) == 2 and action in ["off", "disable", "false"]:
                enable = False
            else:
                raise ValueError("Invalid command format")

            self.sandbox_mode = enable
            exchange.set_sandbox_mode(enable)

            response = f"Sandbox mode {'enabled' if enable else 'disabled'}"
            await self.reply_text(update, response)
        except Exception as e:
            await self.reply_error(
                update,
                f"Failed to toggle sandbox mode. Error: {str(e)}",
            )
