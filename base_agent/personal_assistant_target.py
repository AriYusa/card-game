import asyncio
from pyrit.prompt_target import PromptTarget
from pyrit.models import Message, MessagePiece, construct_response_from_request
from google.genai import types


class PersonalAssistantTarget(PromptTarget):
    def __init__(self, runner, session_service, app_name, user_id):
        super().__init__()
        self._runner = runner
        self._session_service = session_service
        self._app_name = app_name
        self._user_id = user_id
        self._session_counter = 0

    async def send_prompt_async(self, *, message: Message) -> Message:
        session_id = f"pyrit-session-{self._session_counter}"
        self._session_counter += 1

        await self._session_service.create_session(
            app_name=self._app_name,
            user_id=self._user_id,
            session_id=session_id,
        )

        # Pull the last user-role piece as the prompt text
        prompt_text = next(
            (p.original_value for p in reversed(message.message_pieces) if p.role == "user"),
            ""
        )

        user_msg = types.Content(
            role="user",
            parts=[types.Part(text=prompt_text)]
        )

        response_text = ""
        for event in self._runner.run(
            user_id=self._user_id,
            session_id=session_id,
            new_message=user_msg,
        ):
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if hasattr(part, "text") and part.text:
                        response_text += part.text

        # Build response using the same conversation_id as the incoming message
        conversation_id = (
            message.message_pieces[0].conversation_id
            if message.message_pieces else None
        )

        return Message(
            message_pieces=[
                MessagePiece(
                    role="assistant",
                    original_value=response_text or "(no response)",
                    original_value_data_type="text",
                    conversation_id=conversation_id,
                )
            ]
        )
