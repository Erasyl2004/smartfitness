from app.web.settings import AiSettings
from app.interfaces.services.ai import AiService
from app.interfaces.templates.prompt import PromptTemplate
from app.services.ai_service import AiServiceImpl
from app.templates.prompt_template import PromptTemplateImpl
from dishka import Provider, Scope, provide
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import SecretStr

class AiProvider(Provider):
    ai_settings = provide(AiSettings, scope=Scope.APP)

    @provide(scope=Scope.APP)
    def get_chat_model(self, config: AiSettings) -> ChatGoogleGenerativeAI:
        gpt_model = ChatGoogleGenerativeAI(
            api_key=SecretStr(config.api_key),
            model=config.gpt_model,
            temperature=config.temperature
        )

        return gpt_model

    service = provide(
        source=AiServiceImpl,
        scope=Scope.REQUEST,
        provides=AiService
    )

    template = provide(
        source=PromptTemplateImpl,
        scope=Scope.REQUEST,
        provides=PromptTemplate
    )