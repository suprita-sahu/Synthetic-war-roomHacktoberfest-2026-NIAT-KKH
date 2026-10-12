# Project Name
Synthetic-war-room
## Team / attendee

- Team name (if applicable):Error404
- Members and GitHub usernames:suprita-sahu,AbhinayM02,sri-charan-sharma
- Profile links (optional):

## Challenge

Select the challenge you are entering:

- [ y ] Best Open-Source AI Project
- [ ] Best Use of Gemma 4

If listing both categories, confirm eligibility with the organizers and complete evidence for each.

## Project links

- Public GitHub repository:
- Open-source license (link to the license file):

## Problem and solution
Synthetic War Room is for founders, product teams, and engineers who want to challenge a startup idea or system design before implementation.

The user enters an idea or design, then a three-role review loop proposes an architecture, attacks it with red-team findings, and produces a hardened specification with key findings and residual risks. The user can choose 1–3 debate rounds, try sample ideas, view the report, and download it as Markdown or as a comparative PDF. The PDF compares the first-pass and hardened proposals and includes the findings by round
## Approach and technologies
1)Model: gemma2:2b through Ollama, run locally.
2)Agent orchestration: LangGraph manages the architect → adversary → moderator flow and repeats it for the selected number of rounds.
3)Model calls: LangChain’s ChatOllama integration sends role-specific prompts to the same local model. The roles are distinct prompts, not separate models.
4)Interface: Streamlit provides the idea prompt, sample suggestions, debate-round slider, live review display, and report downloads
5)PDF generation: ReportLab creates the comparative PDF.

The main review flow and prompts are in engine.py. The user interface and download actions are in app.py; PDF generation is in pdf_report.py. The dependency list is in requirements.txt.

Development credit: AI-assisted development was used in this project, including assistance with the interface, free-form idea entry, PDF export, and report persistence. Add the specific tools and any other reused materials or contributions required by the organizers’ disclosure rules.
## Challenge evidence
Best Open-Source AI Project

1)Open-source/open-weight AI component and its role: Gemma 2 2B (gemma2:2b) is run locally through Ollama. It powers the architect, red-team adversary, and moderator roles in the iterative design review.
2)Code link showing the integration: Gemma 2 setup, role prompts, and LangGraph flow in engine.py. Replace this local link with the corresponding public GitHub link after publishing.
3)Agent Skill Open Standard compliance (if applicable): No Agent Skill implementation is present in the current project; mark not applicable unless you add one.
Complete the relevant section(s) and remove those that do not apply.
4)Original harness implementation or meaningful changes (if applicable): The project implements the LangGraph workflow connecting the architect, adversary, and moderator; user-selected debate rounds; Streamlit prompt and sample-idea interface; session-persistent reports; and Markdown and comparative PDF exports. Confirm code provenance and credit any reused code before submitting.

### Best Open-Source AI Project

- Open-source/open-weight AI component and its role:
- Code link showing the integration:
- Agent Skill Open Standard compliance (if applicable):
- Original harness implementation or meaningful changes (if applicable):

## Current status

- What works:
Users can enter an idea or system design, select 1–3 rounds, run the adversarial review, view the hardened report, and download Markdown or a comparative PDF. Completed reports remain visible across download reruns until the user clears them.

-Known limitations / incomplete features:
Ollama must be installed and running locally, and the gemma2:2b model must be available. The three roles use the same model with different prompts, so they are not independent models. The project has no public Git remote or license file yet. The dependency list is not version-pinned, and the model’s output quality has not been formally benchmarked.

-What you would improve next: Publish the repository with a suitable license and setup instructions; pin and test dependencies; evaluate report quality and failure cases; improve model/runtime error handling; and consider adding report history or configurable model selection.
## Submission checklist

- [Y ] Project repository is public and links work.
- [Y ] Required challenge evidence is included.
- [Y] Project uses an open-source license where required by the challenge.
- [Y] Work and reused materials are represented honestly.
- [Y] No API keys, tokens, passwords, or private data are included.
- [Y] I followed the organizers' build window and submission instructions.
