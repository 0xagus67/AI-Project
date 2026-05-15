# AI-Project

Personal AI tooling, agent automation, and LLM integration experiments by **0xagus67**.

## Focus Areas

- **Autonomous agents** — long-running AI agents with persistent memory, skills, and tool access (Hermes Agent framework)
- **LLM gateway routing** — multi-model inference via 9Router (OpenAI-compatible API)
- **Browser automation** — stealth Chromium (CloakBrowser / patchright) for sites with anti-bot protection
- **Crypto + AI** — autonomous on-chain interactions (EVM, Base) driven by LLM agents
- **Voice synthesis** — ElevenLabs / xTTS pipelines for agent voice replies

## Stack

| Layer | Tools |
|---|---|
| Models | Claude Sonnet 4 / Haiku, GPT-4o, DeepSeek V3, Qwen 2.5 Coder, Llama 3.1 |
| Agent runtime | Hermes Agent, Claude Code CLI, Codex CLI, OpenCode |
| Inference gateway | 9Router (`/v1/chat/completions` OpenAI-compatible) |
| Browser | CloakBrowser (patched Chromium) + Xvfb |
| Voice | ElevenLabs (`eleven_multilingual_v2`) |
| Languages | Python 3.11, Node.js 20, TypeScript |

## Active Projects

- `agent-soul/` — agent constitution & persona framework (SOUL.md pattern)
- `gateway-config/` — multi-model routing configs for Hermes / OpenCode / Claude Code
- `automation-skills/` — reusable skill modules (Discord, X/Twitter, Gleam, Telegram)
- `mining-experiments/` — solo mining + crypto wallet automation

## Mi MO Integration (planned)

Will integrate **Xiaomi MiMo V2.5** as an additional model in the routing layer once API access is available, with public benchmarks vs Claude Sonnet on agent-style tasks.

## Contact

- X / Twitter: [@0xagusXD](https://x.com/0xagusXD)
- Email: 0xagussedunia [at] gmail [dot] com
