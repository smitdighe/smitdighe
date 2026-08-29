<p align="center">
  <img src="./assets/header.svg" width="100%" alt="Smit Dighe — Full-Stack Dev, AI/ML Builder" />
</p>

<p align="center">
  <a href="https://smit-dighe-portfolio.vercel.app">
    <img src="https://img.shields.io/badge/Portfolio-000000?style=for-the-badge&logo=vercel&logoColor=white" alt="Portfolio" />
  </a>
  <a href="https://www.linkedin.com/in/smit-dighe-a02422337/">
    <img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" />
  </a>
  <a href="mailto:smitdighe@gmail.com">
    <img src="https://img.shields.io/badge/Gmail-EA4335?style=for-the-badge&logo=gmail&logoColor=white" alt="Email" />
  </a>
</p>

<img src="./assets/divider.svg" width="100%" alt="" />

## About

Engineering student who ships. I train the model, wrap it in an API, build the UI, and put it on the internet — the whole path, not just the notebook.

- Working across full-stack + applied ML: scikit-learn models, FastAPI services, React frontends
- Currently deep in **LangChain, LangGraph and multi-agent systems**
- 6 projects live in production, not just in a repo
- **Judge's Special Award** — n8n Community Hackathon @ CMPICA, CHARUSAT
- Shipped **Revvy**, an AI code reviewer, in under 48 hours at a hackathon

<img src="./assets/divider.svg" width="100%" alt="" />

## Stack

<p align="center">
  <img src="./assets/orbit.svg" width="62%" alt="Tech stack" />
</p>

<details>
<summary><b>Full breakdown</b></summary>

<br />

| Layer | Tools |
| :--- | :--- |
| **Languages** | Python, TypeScript, JavaScript, C |
| **Frontend** | React, Vite, Tailwind, Bootstrap |
| **Backend** | FastAPI, Flask, Node.js, Express |
| **AI / ML** | LangChain, LangGraph, scikit-learn, SHAP, Groq, NumPy, Pandas |
| **Data** | PostgreSQL, Supabase, MySQL, SQLite |
| **Real-time** | Server-Sent Events, Uvicorn, PyGitHub |
| **Automation** | n8n |
| **Tooling** | Git, Docker, Postman, VS Code, Vercel |

</details>

<img src="./assets/divider.svg" width="100%" alt="" />

## How FinDocAgent works

<p align="center">
  <img src="./assets/findocagent-flow.svg" width="100%" alt="FinDocAgent architecture" />
</p>

A router plans which agents to call, a hybrid retriever pulls the relevant chunks out of parsed 10-K/10-Q filings, an analyst agent reasons over them and checks its own claims, and every sentence in the answer links back to the filing it came from.

<img src="./assets/divider.svg" width="100%" alt="" />

## Projects

| Project | What it does | Live |
| :--- | :--- | :--- |
| **[FinDocAgent](https://fin-doc-agent.vercel.app/)** | Multi-agent RAG over SEC filings — cited answers, no hallucinated numbers | [![status](https://img.shields.io/website?url=https%3A%2F%2Ffin-doc-agent.vercel.app&up_message=live&down_message=down&style=flat-square&color=FF7B54&cacheSeconds=1800)](https://fin-doc-agent.vercel.app/) |
| **[Fathom](https://fathom-dev.vercel.app/)** | Autonomous research agent — searches, reflects on gaps, writes a cited report | [![status](https://img.shields.io/website?url=https%3A%2F%2Ffathom-dev.vercel.app&up_message=live&down_message=down&style=flat-square&color=FF7B54&cacheSeconds=1800)](https://fathom-dev.vercel.app/) |
| **[Undertow](https://undertow-dev.vercel.app/)** | AI incident triage — classifies, deduplicates and routes alerts to resolution | [![status](https://img.shields.io/website?url=https%3A%2F%2Fundertow-dev.vercel.app&up_message=live&down_message=down&style=flat-square&color=FF7B54&cacheSeconds=1800)](https://undertow-dev.vercel.app/) |
| **[Verity](https://verity-iota-two.vercel.app/)** | Job-posting fraud detector — LogisticRegression + SHAP so you see *why* it flagged | [![status](https://img.shields.io/website?url=https%3A%2F%2Fverity-iota-two.vercel.app&up_message=live&down_message=down&style=flat-square&color=FF7B54&cacheSeconds=1800)](https://verity-iota-two.vercel.app/) |
| **[Revvy](https://revvy-iota.vercel.app/)** | AI pair reviewer — flags bugs, security holes and perf traps, ships the fix | [![status](https://img.shields.io/website?url=https%3A%2F%2Frevvy-iota.vercel.app&up_message=live&down_message=down&style=flat-square&color=FF7B54&cacheSeconds=1800)](https://revvy-iota.vercel.app/) |
| **[BinRoute](https://bin-route.vercel.app/)** | Live waste-collection command center for fleet managers | [![status](https://img.shields.io/website?url=https%3A%2F%2Fbin-route.vercel.app&up_message=live&down_message=down&style=flat-square&color=FF7B54&cacheSeconds=1800)](https://bin-route.vercel.app/) |

More in [my repositories](https://github.com/smitdighe?tab=repositories).

<img src="./assets/divider.svg" width="100%" alt="" />

## Award

<table>
<tr>
<td width="62%">

**Judge's Special Award — n8n Community Hackathon**
*FCA, CMPICA, CHARUSAT*

Built an AI-powered helpdesk automation system in n8n: it reads incoming tickets, classifies them with an LLM, routes them to the right department, tracks SLA breaches in real time, auto-escalates the urgent ones, and writes trend reports for admins.

Defended every design decision under judge cross-questioning — including flagging records instead of deleting them, and the guardrails against prompt injection in the LLM calls.

</td>
<td width="38%" align="center">

<img src="./assets/Certificate.jpg" width="100%" alt="Judge's Special Award certificate" />

</td>
</tr>
</table>

<img src="./assets/divider.svg" width="100%" alt="" />

## Activity

<p align="center">
  <img src="./assets/commit-race.svg" width="100%" alt="Contributions per month" />
</p>

<p align="center">
  <img src="./assets/snake-dark.svg" width="100%" alt="Contribution snake" />
</p>

<img src="./assets/divider.svg" width="100%" alt="" />

<details>
<summary><b>How this README builds itself</b></summary>

<br />

Every animated graphic here is generated by [`scripts/gen_svg.py`](./scripts/gen_svg.py) and committed by a [GitHub Action](./.github/workflows/readme-assets.yml) on a daily cron. No third-party image hosts, so nothing rate-limits or renders blank.

- `header.svg` — stroke-drawn wordmark + drifting particles
- `orbit.svg` — stack labels on three counter-rotating rings
- `commit-race.svg` — contributions per month, pulled from the GitHub GraphQL API
- `divider.svg` — gradient sweep
- `findocagent-flow.svg` — hand-authored, agents light up in sequence

Animation is pure SMIL, theming is a `prefers-color-scheme` block inside each SVG. Stdlib Python only.

```bash
GH_LOGIN=smitdighe GITHUB_TOKEN=$YOUR_PAT python scripts/gen_svg.py
```

</details>
