"""Google Gemini integration for agentic-ifs dialogue.

Provides ``GeminiDialogueProvider`` — a ``DialogueProvider`` backed by
Google's Gemini models via the ``google-genai`` Python SDK.

Requires: ``pip install google-genai``
Or: ``pip install agentic-ifs[google]``

IFS note: The choice of LLM backend does not affect IFS semantics.
The system prompt and dialogue context encode the Part's character;
the LLM is simply the rendering engine.
"""

from __future__ import annotations

import os

from ..dialogue import DialogueContext
from ..parts import IPart


class GeminiDialogueProvider:
    """DialogueProvider backed by Google Gemini.

    Uses the ``google-genai`` Python SDK. Reads ``GEMINI_API_KEY`` or
    ``GENAI_API_KEY`` from environment if not provided explicitly.

    IFS: This is a rendering engine — it takes the Part's system prompt
    (identity, age, intent, strategies) and generates natural-language
    speech consistent with that character. The IFS constraints are
    enforced by ``PartDialogue``, not here.

    Parameters
    ----------
    api_key:
        Google API key. If ``None``, reads from ``GEMINI_API_KEY``
        or ``GENAI_API_KEY`` environment variable.
    model_name:
        Gemini model to use. Default: ``gemini-3-flash-preview``.
    """

    def __init__(
        self,
        api_key: str | None = None,
        model_name: str = "gemini-3-flash-preview",
    ) -> None:
        from google import genai  # lazy import

        key = api_key or os.environ.get("GEMINI_API_KEY") or os.environ.get("GENAI_API_KEY")
        if not key:
            raise ValueError(
                "Google API key required. Pass api_key or set "
                "GEMINI_API_KEY env var."
            )
        self._client = genai.Client(api_key=key)
        self._model_name = model_name

    def generate_part_response(
        self,
        part: IPart,
        context: DialogueContext,
        system_prompt: str,
    ) -> str:
        """Generate a Part response using Google Gemini.

        Builds a message sequence from the conversation history and
        current facilitator message, using ``system_instruction`` for
        the IFS system prompt.

        Parameters
        ----------
        part:
            The Part speaking (used by the protocol; identity is
            already encoded in ``system_prompt``).
        context:
            Dialogue context including history and facilitator message.
        system_prompt:
            The IFS-grounded system prompt built by
            ``build_part_system_prompt()``.

        Returns
        -------
        str
            The generated Part response text.
        """
        from google.genai import types

        # Build message history
        history: list[types.Content] = []
        for msg in context.conversation_history:
            role = "user" if msg.role == "facilitator" else "model"
            history.append(types.Content(role=role, parts=[types.Part(text=msg.content)]))

        # Create chat with system instruction and history
        chat = self._client.chats.create(
            model=self._model_name,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
            ),
            history=history,
        )

        # Send current message
        response = chat.send_message(message=context.facilitator_message)

        return response.text  # type: ignore[return-value]
