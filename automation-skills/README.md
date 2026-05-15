# Automation Skills

Reusable skill modules for cross-platform agent automation.

## Categories

### Browser automation
- **CloakBrowser** — stealth Chromium for Cloudflare Turnstile / hCaptcha sites
- **Xvfb** virtual display for headed browser on headless servers
- Persistent profile reuse for session-based workflows

### Social media
- **X / Twitter** — login via Google OAuth + cookie GraphQL for read/follow; CloakBrowser `/compose/post` for write (bypasses datacenter shadow-block)
- **Discord** — self-bot via persistent profile (auto-respond pattern)
- **Telegram** — Telethon-based DM/group automation

### Web3 / crypto
- **EVM wallet** — Base / Mainnet transaction automation via web3.py
- **NFT minting** — automated mint with random delay + rate limit

## Pattern

Every skill follows the same structure:
- `SKILL.md` — frontmatter + step-by-step procedure
- `scripts/*.py` — executable scripts
- Pitfalls section documenting platform-specific quirks

Inspired by [Anthropic's Skills](https://anthropic.com) pattern adapted for the Hermes Agent runtime.
