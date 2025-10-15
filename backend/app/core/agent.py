import logging
from typing import Optional, ClassVar

import instructor
from instructor import AsyncInstructor
from openai import AsyncOpenAI

from app.conf.config import OPENAI_API_KEY
from app.core.history import History
from app.core.models import IntentionResponse, Intention, CyptoPriceInfoResponse
from app.core.tools import get_latest_price

logger = logging.getLogger(__name__)


class Agent:
    find_intention_guide: ClassVar[str] = "结合历史对话，理解用户这句对话的意图，结构化的输出相应的枚举类型"
    extract_crypto_info_guide: ClassVar[str] = ("结合历史对话，获取用户想要了解的虚拟币的种类，交易所，以及结算价格的币种，返回结构化的输出。"
                                                "如果不能获得，或者信息不完整，不要假设用户的选择，返回 None")

    def __init__(self):
        self.client: AsyncInstructor = instructor.from_openai(AsyncOpenAI(api_key=OPENAI_API_KEY))
        self.history: History = History()

    async def process_message(self, message: str) -> Optional[str]:
        if not message:
            return None

        self.history.append(role="user", text=message)

        intention = await self.find_intention(message)

        if intention == Intention.FIND_CRYPTO_PRICE:
            crypto_price_response = await self.extract_crypto_price_info(message)
            if crypto_price_response.crypto_price_info is None:
                reason = (f"试图从用户的对话中获取虚拟币的种类，交易所以及价格结算的币种，但是没有成功，"
                          f"因为{crypto_price_response.explanation}。参考之前的对话历史纪录，"
                          f"生成一句向用户继续询问澄清的话，以获得更清楚的信息。")
                answer = await self.generate_response(reason)
            else:
                try:
                    price = get_latest_price(crypto_price_info=crypto_price_response.crypto_price_info)
                    reason = f"已经获得了用户想知道的价格: {price}，结合对话历史，生成回复给用户的话"
                    answer = await self.generate_response(reason)
                except Exception as e:
                    reason = f"在获取价格的时候失败了，发生了意外: {str(e)}，结合对话历史生成给用户的回复，并询问是需要继续查询还是换个其他的话题"
                    answer = await self.generate_response(reason)
        else:
            reason = "用户并没有询问虚拟币的价格，而是聊其他的话题，结合对话历史做合宜的回答，合适的时机下询问用是否对虚拟币的价格感兴趣"
            answer = await self.generate_response(reason)

        self.history.append(role="ai", text=answer)
        return answer

    async def find_intention(self, message: str) -> Intention:
        system_prompts = [Agent.find_intention_guide, self.history.prompt()]
        system_prompt = "\n".join(system_prompts)
        messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": message}, ]
        response: IntentionResponse = await self.client.chat.completions.create(
            model="gpt-4o",
            response_model=IntentionResponse,
            messages=messages
        )
        logger.debug(f"Message: {message}, Intention: {response.intention}, Explanation: {response.explanation}")
        return response.intention

    async def extract_crypto_price_info(self, message: str) -> CyptoPriceInfoResponse:
        system_prompts = [Agent.extract_crypto_info_guide, self.history.prompt()]
        system_prompt = "\n".join(system_prompts)
        messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": message}, ]
        response: CyptoPriceInfoResponse = await self.client.chat.completions.create(
            model="gpt-4o",
            response_model=CyptoPriceInfoResponse,
            messages=messages
        )
        return response

    async def generate_response(self, reason: str) -> str:
        system_prompt = self.history.prompt()
        messages = [{"role": "system", "content": system_prompt},
                    {"role": "user", "content": reason}, ]
        response: str = await self.client.chat.completions.create(
            model="gpt-4o",
            response_model=str,
            messages=messages
        )
        return response
