from typing import List, TypedDict, Literal, Sequence
from langchain_ollama import ChatOllama
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage
from langgraph.config import get_stream_writer
from langgraph.graph import StateGraph, END

class WarRoomState(TypedDict):
    topic: str
    round: int
    max_rounds: int
    architect_points: List[str]
    adversary_critiques: List[str]
    current_defense: str
    current_attack: str
    final_verdict: str

# Configured for local Gemma via Ollama
llm = ChatOllama(model="gemma2:2b", temperature=0.7)

def stream_response(messages: Sequence[BaseMessage], agent: str) -> str:
    writer = get_stream_writer()
    writer({"agent": agent, "event": "start"})

    content = []
    for chunk in llm.stream(messages):
        text = chunk.content
        if not isinstance(text, str):
            text = "".join(
                part.get("text", "")
                for part in text
                if isinstance(part, dict) and part.get("type") == "text"
            )
        if text:
            content.append(text)
            writer({"agent": agent, "event": "token", "text": text})

    response = "".join(content)
    writer({"agent": agent, "event": "done"})
    return response


def architect_node(state: WarRoomState) -> WarRoomState:
    topic = state["topic"]
    current_round = state["round"]
    attack = state.get("current_attack", "")

    if current_round == 1:
        prompt = (
            f"You are Agent Alpha (The System Architect). Propose a resilient, high-standard "
            f"proposal or architecture for: {topic}. Provide concrete mechanics, defensive measures, "
            f"and clear boundaries."
        )
    else:
        prompt = (
            f"The Adversary attacked your design with:\n{attack}\n\n"
            f"Defend your design. Concede real flaws, propose concrete technical "
            f"patches, and harden the system."
        )

    response = stream_response([
        SystemMessage(content="You are a senior system architect defending a rigorous engineering design."),
        HumanMessage(content=prompt)
    ], "architect")
    
    architect_points = state.get("architect_points", []) + [response]
    return {
        **state,
        "current_defense": response,
        "architect_points": architect_points
    }

def adversary_node(state: WarRoomState) -> WarRoomState:
    defense = state["current_defense"]
    prompt = (
        f"You are Agent Beta (The Adversary / Red Teamer). Scrutinize this proposal:\n\n{defense}\n\n"
        f"Identify at least 3 critical vulnerabilities: race conditions, edge cases, "
        f"security flaws, or economic exploit loops. Be direct and concise."
    )

    response = stream_response([
        SystemMessage(content="You are an uncompromising red-team security analyst and vulnerability researcher."),
        HumanMessage(content=prompt)
    ], "adversary")

    critiques = state.get("adversary_critiques", []) + [response]
    return {
        **state,
        "current_attack": response,
        "adversary_critiques": critiques
    }

def moderator_node(state: WarRoomState) -> WarRoomState:
    defense = state["current_defense"]
    attack = state["current_attack"]
    
    prompt = (
        f"Topic: {state['topic']}\n\n"
        f"Latest Proposal:\n{defense}\n\n"
        f"Adversary Attacks:\n{attack}\n\n"
        f"As the Chief Auditor, produce a structured Hardened Specification Report:\n"
        f"1. Key Battleground Points (What broke?)\n"
        f"2. Hardened Architecture (The definitive surviving spec)\n"
        f"3. Residual Unresolved Risks\n"
        f"Use Markdown headings and bullets."
    )

    response = stream_response([
        SystemMessage(content="You are an objective auditor synthesizing an adversarial debate into a hardened spec."),
        HumanMessage(content=prompt)
    ], "moderator")

    return {
        **state,
        "round": state["round"] + 1,
        "final_verdict": response
    }

def should_continue(state: WarRoomState) -> Literal["architect", "__end__"]:
    if state["round"] > state["max_rounds"]:
        return END
    return "architect"

# LangGraph state machine assembly
workflow = StateGraph(WarRoomState)
workflow.add_node("architect", architect_node)
workflow.add_node("adversary", adversary_node)
workflow.add_node("moderator", moderator_node)

workflow.set_entry_point("architect")
workflow.add_edge("architect", "adversary")
workflow.add_edge("adversary", "moderator")
workflow.add_conditional_edges("moderator", should_continue, {
    "architect": "architect",
    END: END
})

war_room_graph = workflow.compile()