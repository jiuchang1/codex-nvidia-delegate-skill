# Codex NVIDIA Delegate Skill

A Codex skill that calls NVIDIA NIM / NVIDIA API Catalog OpenAI-compatible models as lightweight helper delegates.

It is useful for simple drafting, summarization, classification, translation, second opinions, snippet review, and model comparison using models such as DeepSeek, Z.ai GLM, Qwen, Llama, Mistral, or Nemotron.

## Install

Copy the skill folder into your Codex skills directory:

```powershell
Copy-Item -Recurse .\nvidia-delegate "$env:USERPROFILE\.codex\skills\"
```

Set one of these environment variables:

```powershell
$env:NVIDIA_API_KEY = "nvapi-..."
# or
$env:NGC_API_KEY = "nvapi-..."
```

## Use

List matching NVIDIA models:

```powershell
python "$env:USERPROFILE\.codex\skills\nvidia-delegate\scripts\nvidia_delegate.py" --list-models --filter "deepseek|glm|qwen"
```

Ask the default model:

```powershell
python "$env:USERPROFILE\.codex\skills\nvidia-delegate\scripts\nvidia_delegate.py" --prompt "Summarize this in three bullets: ..."
```

Compare several models:

```powershell
python "$env:USERPROFILE\.codex\skills\nvidia-delegate\scripts\nvidia_delegate.py" --compare glm,deepseek-flash,qwen-coder --prompt "Find edge cases in this function: ..."
```

## Notes

This is not a native Codex `spawn_agent` replacement. It gives Codex a reusable way to ask external NVIDIA-hosted models for bounded, low-risk helper work.

Do not send secrets, credentials, private personal data, or large proprietary code to external models unless you have explicit approval.
