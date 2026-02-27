"""Anthropic Claude integration for agentic-ifs dialogue.

Provides ``AnthropicDialogueProvider`` — a ``DialogueProvider`` backed by
Anthropic's Claude models via the ``anthropic`` Python SDK.

Requires: ``pip install anthropic>=0.40``
Or: ``pip install agentic-ifs[anthropic]``

IFS note: The choice of LLM backend does not affect IFS semantics.
The system prompt and dialogue context encode the Part's character;
the LLM is simply the rendering engine.
"""

from __future__ import annotations

import os
from typing import Any

from ..dialogue import DialogueContext
from ..parts import IPart


class AnthropicDialogueProvider:
    """DialogueProvider backed by Anthropic Claude.

    Uses the ``anthropic`` Python SDK. Reads ``ANTHROPIC_API_KEY``
    from environment if not provided explicitly.

    IFS: This is a rendering engine — it takes the Part's system prompt
    (identity, age, intent, strategies) and generates natural-language
    speech consistent with that character. The IFS constraints are
    enforced by ``PartDialogue``, not here.

    Parameters
    ----------
    api_key:
        Anthropic API key. If ``None``, reads from ``ANTHROPIC_API_KEY``
        environment variable.
    model_name:
        Claude model to use. Default: ``claude-sonnet-4-20250514``.
    """

    def __init__(
        self,
        api_key: str | None = None,
        model_name: str = "claude-sonnet-4-20250514",
    ) -> None:
        import anthropic  # lazy import

        key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not key:
            raise ValueError(
                "Anthropic API key required. Pass api_key or set "
                "ANTHROPIC_API_KEY env var."
            )
        self._client = anthropic.Anthropic(api_key=key)
        self._model_name = model_name

    def generate_part_response(
        self,
        part: IPart,
        context: DialogueContext,
        system_prompt: str,
    ) -> str:
        """Generate a Part response using Anthropic Claude.

        Builds a message sequence from the conversation history and
        current facilitator message, using the ``system`` parameter for
        the IFS system prompt. Maps dialogue roles to Anthropic roles:
        "facilitator" -> "user", "part" -> "assistant".

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
        # Build messages from conversation history
        messages: list[dict[str, Any]] = []
        for msg in context.conversation_history:
            role = "user" if msg.role == "facilitator" else "assistant"
            messages.append({"role": role, "content": msg.content})

        # Add current facilitator message
        messages.append({
            "role": "user",
            "content": context.facilitator_message,
        })

        # Call the API
        response = self._client.messages.create(
            model=self._model_name,
            max_tokens=1024,
            system=system_prompt,
            messages=messages,  # type: ignore[arg-type]
        )

        return response.content[0].text  # type: ignore[union-attr]
