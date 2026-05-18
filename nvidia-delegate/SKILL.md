---
name: nvidia-delegate
description: Use NVIDIA NIM / NVIDIA API Catalog OpenAI-compatible models as lightweight helper delegates for simple or parallelizable language tasks. Trigger when Codex should ask external NVIDIA-hosted models such as DeepSeek, Z.ai GLM, Qwen, Llama, Mistral, or Nemotron for drafting, summarization, classification, translation, brainstorming, rubric scoring, second opinions, quick code review snippets, model comparison, or low-risk analysis without needing repo write access. Use when the user mentions NVIDIA API, NIM, nvapi, DeepSeek, Z.ai, GLM, Qwen, or wanting cheap/simple tasks handled by other models.
---

# NVIDIA Delegate

## Overview

Use this skill to call NVIDIA-hosted OpenAI-compatible chat models as lightweight external helpers. This is a delegation aid, not a replacement for Codex's local reasoning, filesystem access, or native `spawn_agent` subagents.

The API key must already be available as `NVIDIA_API_KEY` or `NGC_API_KEY`. Never print full secret values.

## Good Fits

Use `scripts/nvidia_delegate.py` for:

- Drafting alternate wording, outlines, summaries, commit messages, PR descriptions, emails, or Chinese/English translations.
- Getting a second opinion on a bounded snippet, design choice, error message, or short diff.
- Classifying, scoring, ranking, tagging, extracting fields, or rewriting text.
- Comparing responses from multiple external models.
- Asking DeepSeek/GLM/Qwen/Llama-style models for a quick independent read while Codex continues primary work.

Avoid external delegation for:

- Secrets, private keys, credentials, personal data, or proprietary material the user has not clearly approved sending out.
- Tasks that require live filesystem changes, authenticated local tools, browser state, or exact repo-wide context.
- High-stakes legal, medical, financial, security, or production decisions unless the output is only a low-trust draft to be verified.
- Large files or full codebases. Send small, relevant excerpts instead.

## Quick Start

Run from PowerShell:

```powershell
python "$env:USERPROFILE\.codex\skills\nvidia-delegate\scripts\nvidia_delegate.py" --model llama-small --prompt "Summarize this in three bullets: ..."
```

Use stdin for longer prompts:

```powershell
Get-Content .\notes.txt -Raw | python "$env:USERPROFILE\.codex\skills\nvidia-delegate\scripts\nvidia_delegate.py" --model deepseek-flash --system "Be concise."
```

Compare models:

```powershell
python "$env:USERPROFILE\.codex\skills\nvidia-delegate\scripts\nvidia_delegate.py" --compare glm,deepseek-flash,qwen-coder --prompt "Find edge cases in this function: ..."
```

List available NVIDIA models:

```powershell
python "$env:USERPROFILE\.codex\skills\nvidia-delegate\scripts\nvidia_delegate.py" --list-models --filter "deepseek|glm|qwen"
```

## Workflow

1. Decide whether external delegation is appropriate. If the prompt contains sensitive local data, keep the work inside Codex unless the user explicitly asked to use NVIDIA.
2. Choose a small prompt with only the relevant context. Add a system message that limits scope, format, and uncertainty.
3. Select a model alias or full model ID. See `references/model-selection.md` when model choice matters.
4. Treat the returned answer as advisory. Verify facts, code, and recommendations before acting.
5. When reporting back, say that an NVIDIA-hosted model was used if it affected the result.

## Model Aliases

The helper script includes aliases for known working model IDs:

- `glm`: `z-ai/glm-5.1`
- `llama-small`: `meta/llama-3.1-8b-instruct` (script default; useful fallback when hosted routes are slow)
- `deepseek-flash`: `deepseek-ai/deepseek-v4-flash`
- `deepseek-pro`: `deepseek-ai/deepseek-v4-pro`
- `deepseek-coder`: `deepseek-ai/deepseek-coder-6.7b-instruct`
- `qwen-coder`: `qwen/qwen3-coder-480b-a35b-instruct`
- `qwen-large`: `qwen/qwen3.5-397b-a17b`

Full NVIDIA model IDs can be passed directly with `--model`.

## Output Handling

Prefer concise outputs. For structured extraction, pass `--json-output` and instruct the model to return only JSON. If the output will guide code changes, include only small excerpts and then verify locally with tests or direct inspection.
