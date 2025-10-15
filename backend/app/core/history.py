from collections import deque

from app.api.restmessage import RestMessage
from app.conf.config import MAX_HISTORY_LEN


class History:

    def __init__(self):
        self.history: deque[RestMessage] = deque(maxlen=MAX_HISTORY_LEN)

    def prompt(self) -> str:
        output = ["生成的回复尽量简短，并且口语化", "---", "对话历史:"]
        if not self.history:
            output.append("目前还没有对话历史")
        else:
            for message in self.history:
                output.append(f"[{message.role}]: {message.text}")
        return "\n".join(output)

    def append(self, role: str, text: str):
        self.history.append(RestMessage(role=role, text=text))
