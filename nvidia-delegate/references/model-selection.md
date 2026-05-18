# Model Selection

Use these as practical defaults. Availability and latency can change with routing or VPN state, so run `--list-models` when a model fails and try another alias when a request times out.

| Need | Suggested model |
| --- | --- |
| Fast general drafting, classification, short summaries | `qwen-large`, then `glm` or `deepseek-flash` |
| Stronger general reasoning, second opinions | `deepseek-pro` |
| Code snippets, refactor ideas, bug hypotheses | `qwen-coder` or `deepseek-coder` |
| Broad model comparison | `glm,deepseek-flash,qwen-coder` |

Prompt pattern for second opinions:

```text
You are a bounded reviewer. Use only the excerpt below. List concrete issues, uncertainties, and one recommended next step. If evidence is missing, say so.
```

Prompt pattern for structured extraction:

```text
Return only valid JSON matching this schema: ...
If a field is unknown, use null. Do not invent values.
```

Prompt pattern for code review snippets:

```text
Review only this snippet for likely bugs and missing tests. Prioritize concrete findings over style. Include file/function names if present.
```

Security boundary: do not send secrets, hidden credentials, private customer data, or large proprietary code without user approval.
