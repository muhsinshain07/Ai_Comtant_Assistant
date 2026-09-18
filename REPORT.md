# AI Content Assistant — Project Report

**Project:** AI Content Assistant
**Type:** Single-page Streamlit web application
**Entry point:** `app.py`
**Hosting:** Streamlit Community Cloud
**Model provider:** Groq (free developer tier)

---

## Table of contents

1. [Executive summary](#1-executive-summary)
2. [Objectives and scope](#2-objectives-and-scope)
3. [Architecture overview](#3-architecture-overview)
4. [Module-by-module breakdown](#4-module-by-module-breakdown)
5. [Data and API flow](#5-data-and-api-flow)
6. [The prompt design](#6-the-prompt-design)
7. [Configuration and secrets handling](#7-configuration-and-secrets-handling)
8. [Design decisions and rationale](#8-design-decisions-and-rationale)
9. [Error handling and resilience](#9-error-handling-and-resilience)
10. [Testing and verification status](#10-testing-and-verification-status)
11. [Security considerations](#11-security-considerations)
12. [Limitations](#12-limitations)
13. [Operational notes](#13-operational-notes)
14. [Future work](#14-future-work)
15. [File inventory](#15-file-inventory)

---

## 1. Executive summary

AI Content Assistant is a small, self-contained Python application that generates a complete social media post — a caption composed of a hook, body, and call to action, followed by a set of relevant hashtags — from five user-supplied inputs.

The entire application lives in one file, `app.py`, of roughly 170 lines. It uses Streamlit for the interface and a single call to a Groq-hosted large language model for text generation. There is no database, no user account system, no background worker, and no client-side JavaScript of its own.

The design goal was deliberately narrow: **a complete, understandable, deployable app in one file**, where every part of the code is readable by someone new to Python. The trade-off is that state is not persisted and only one API key is supported per deployment — both acceptable for the intended use case of a personal or small-team content helper.

---

## 2. Objectives and scope

### Primary objective

Deliver a working AI content generator that a non-developer can operate safely: choose five options, click one button, receive copy-paste-ready text.

### Functional requirements

| # | Requirement | Status |
|---|---|---|
| F1 | User selects a content type | Implemented — dropdown, 5 options |
| F2 | User selects a platform | Implemented — dropdown, 6 options |
| F3 | User enters a topic | Implemented — free-text input |
| F4 | User enters a target audience | Implemented — free-text input |
| F5 | User selects a tone | Implemented — 6-step slider |
| F6 | App generates a caption | Implemented |
| F7 | App generates relevant hashtags | Implemented — 8–12 tags requested |
| F8 | Output is copyable and downloadable | Implemented — text boxes plus `.txt` download |
| F9 | Uses a free model tier | Implemented — Groq free developer tier |

### Non-functional requirements

| # | Requirement | Status |
|---|---|---|
| N1 | Simple, clean, readable code | One file, two helper functions, no classes |
| N2 | No hard-coded credentials | Key read from Secrets, environment, or the sidebar |
| N3 | Clear failure messages | Handled for missing key, empty input, and API errors |
| N4 | Deployable at zero cost | Streamlit Community Cloud free tier |
| N5 | Understandable by a new reader | README.md and USAGE.md provided |

### Explicitly out of scope

- Publishing directly to social platforms (the app writes text only).
- Multi-user accounts, authentication, or per-user history.
- Image, video, or audio generation.
- Post scheduling.
- Analytics or usage tracking.

---

## 3. Architecture overview

The app is a **stateless two-tier system**: a Streamlit front end running in the browser, and a remote inference API behind it. There is no application server of its own beyond the Streamlit process, and no persistence layer.

```
┌─────────────────────────────────────────────┐
│              User's browser                 │
│   Streamlit-rendered form: 5 inputs         │
│   Sidebar: API key + model caption          │
│   Results: post / caption / hashtags        │
└──────────────────────┬──────────────────────┘
                       │  WebSocket (Streamlit runtime)
                       ▼
┌─────────────────────────────────────────────┐
│   Streamlit app process (app.py)            │
│   ─ input collection                        │
│   ─ get_api_key()   → secrets / env         │
│   ─ build_prompt()  → prompt string         │
│   ─ generate_post() → SDK call              │
│   ─ response parsing and rendering          │
└──────────────────────┬──────────────────────┘
                       │  HTTPS (official groq SDK)
                       ▼
┌─────────────────────────────────────────────┐
│        Groq Inference API                   │
│   model: openai/gpt-oss-120b                │
│   returns: chat completion text             │
└─────────────────────────────────────────────┘
```

**Runtime model.** Streamlit re-executes `app.py` top to bottom on every user interaction. This is why the script contains no `main()` function and no `if __name__ == "__main__"` guard: the file *is* the render loop. Configuration constants sit at module level and are re-bound cheaply on each rerun.

**State.** No `st.session_state` is used. Each click of the Generate button performs one complete request and renders one result. Nothing is remembered between runs — a deliberate simplification.

---

## 4. Module-by-module breakdown

`app.py` is organised into three clearly commented regions. There are no imports beyond `os` (standard library), `streamlit`, and `groq`.

### 4.1 Configuration region

Three module-level constants define everything the UI offers:

| Constant | Contents | Purpose |
|---|---|---|
| `MODEL_ID` | `"openai/gpt-oss-120b"` | The single place the model is named, so retirements can be fixed with a one-line edit. |
| `CONTENT_TYPES` | 5 strings | Populates the Content type dropdown. |
| `PLATFORMS` | 6 strings | Populates the Platform dropdown. |
| `TONES` | 6 strings | Populates the Tone slider. |

Keeping these as plain lists means adding an option is a one-line change and the prompt automatically inherits it, because the prompt is built from whatever the user selected.

### 4.2 Helper functions

Three small functions carry all the logic.

**`get_api_key() -> str`** — Resolves the Groq API key without ever raising. It first attempts `st.secrets["GROQ_API_KEY"]` inside a `try`/`except`, because accessing `st.secrets` when no `secrets.toml` exists raises an exception in a local run; the `except` swallows that case and falls through. If no secret is present it returns `os.getenv("GROQ_API_KEY", "")`, so an environment variable is honoured. An empty string is the failure value, which the UI treats as "no key configured".

**`build_prompt(content_type, platform, topic, audience, tone) -> str`** — Assembles the user's five selections into a single instruction string. This function is the creative core of the app; it is analysed in section 6.

**`generate_post(api_key, prompt) -> str`** — Constructs a `Groq` client with the supplied key and issues one chat completion:

```python
response = client.chat.completions.create(
    model=MODEL_ID,
    messages=[
        {"role": "system", "content": "You are a helpful social media copywriter."},
        {"role": "user", "content": prompt},
    ],
    temperature=0.8,
    max_tokens=1024,
)
return response.choices[0].message.content.strip()
```

`temperature=0.8` biases toward varied, creative phrasing rather than repetitive output — desirable when a user regenerates the same brief several times looking for options. `max_tokens=1024` is ample for a social post and caps cost and latency. The returned content is `.strip()`-ed to remove stray leading or trailing whitespace before rendering.

### 4.3 User interface region

The UI is built top to bottom in the order the user sees it.

| Element | Streamlit call | Notes |
|---|---|---|
| Page config | `st.set_page_config(...)` | Sets browser tab title and icon. |
| Title and caption | `st.title`, `st.caption` | Static. |
| Sidebar | `st.sidebar` block | Header, password field for the key, and a caption showing the active model. |
| Key resolution | `api_key = api_key_input or get_api_key()` | A key typed in the sidebar takes precedence over Secrets or the environment. |
| Two-column form | `st.columns(2)` | Content type and Topic on the left; Platform and Target audience on the right. |
| Tone | `st.select_slider` | Six steps, defaulting to "Friendly". |
| Trigger | `st.button(..., type="primary")` | Full-width primary button. |
| Result area | `st.success`, `st.text_area`, `st.write`, `st.code`, `st.download_button` | Rendered only after a successful generation. |

**Response parsing.** After generation the app checks whether the literal substring `"Hashtags:"` appears in the model's output. If it does, `result.split("Hashtags:", 1)` splits the text into a caption part and a tags part with a single split, and the two are rendered in separate blocks so each can be copied independently. If the model omits the marker, the app still shows the full text in the "Your post" box — it degrades gracefully rather than failing.

**Download.** `st.download_button` writes the raw result to `generated_post.txt` with MIME type `text/plain`, using in-memory data; no file is written to the server's disk.

---

## 5. Data and API flow

A single generation proceeds through ten steps.

| Step | Stage | Detail |
|---|---|---|
| 1 | Input validation | On button click, the app checks the key exists, then that Topic and Target audience are non-empty after `.strip()`. |
| 2 | Prompt assembly | `build_prompt()` interpolates the five selections into the instruction template. |
| 3 | Client creation | `Groq(api_key=api_key)` instantiates the SDK client for this request. |
| 4 | Request | One `chat.completions.create` call with a system message, the user prompt, `temperature=0.8`, `max_tokens=1024`. |
| 5 | Transport | HTTPS to Groq's inference endpoints. |
| 6 | Inference | The model generates the caption and hashtags. |
| 7 | Extraction | `response.choices[0].message.content.strip()` yields a plain string. |
| 8 | Parsing | The string is split on `"Hashtags:"` if present. |
| 9 | Rendering | Post, Caption, and Hashtags blocks are written to the page. |
| 10 | Export | The user may download the full text as `generated_post.txt`. |

**Payload shape.** The request is a standard chat-completions payload: a list of role/content message objects plus model parameters. The app uses two roles — a short `system` message that fixes the persona, and a `user` message carrying the full brief.

**Response shape.** Only two fields of the response are read: `choices[0].message.content` for the text, and nothing else. No token accounting, no finish-reason handling, no streaming. Streaming was deliberately omitted to keep the code minimal; the spinner covers the wait.

**No egress other than Groq.** The app makes no calls to any other service, and none of the user's inputs are stored anywhere.

---

## 6. The prompt design

The template in `build_prompt()` is the part of the app most responsible for output quality. Its structure is:

1. **Role statement** — "You are a professional social media content writer."
2. **Task** — write a *{content type}* for *{platform}*.
3. **Context block** — Topic, Target audience, Tone, each on its own line.
4. **Quality requirements**, stated as five bullets:
   - Start with a scroll-stopping hook.
   - Keep it natural, with short paragraphs and line breaks.
   - Respect the platform's typical style and length.
   - End with a clear call to action.
   - Add a line beginning `"Hashtags:"` followed by 8–12 relevant tags, mixed broad and niche.
5. **Output constraint** — return only the post and the hashtags line; no explanations, titles, or Markdown code fences.

Two design points deserve emphasis.

**The output constraint matters as much as the content instruction.** Asking for "only the post" prevents the model from prefixing its answer with commentary like "Here's your post:", which would otherwise pollute the copyable text. Asking for no code fences prevents a ```` ``` ```` wrapper from appearing around the result.

**The `"Hashtags:"` marker is a contract with the parser.** The requirement that the hashtag line begin with that exact word is what makes step 8 of the flow possible. The instruction and the parsing logic are two halves of one interface, so changing either means revisiting the other.

The `system` message is intentionally minimal — persona only — because all task specifics belong in the user turn where they are easy to inspect and edit.

---

## 7. Configuration and secrets handling

The application resolves its credential from three sources, in this order of precedence:

| Priority | Source | Where it comes from | Typical use |
|---|---|---|---|
| 1 | Sidebar password field | Typed by the user at runtime | Quick local testing; running without any configuration |
| 2 | `st.secrets["GROQ_API_KEY"]` | Streamlit Secrets (`.streamlit/secrets.toml` locally, or the Secrets box on Streamlit Cloud) | Deployment — the recommended path |
| 3 | `GROQ_API_KEY` environment variable | The shell or process environment | Local development scripts |

If all three are empty, the app displays the message *"No API key found. Add GROQ_API_KEY to Streamlit Secrets or paste it in the sidebar."* and does not attempt the API call.

The key is never written to disk by the app, never logged, and never echoed back to the page — the sidebar field uses `type="password"`.

---

## 8. Design decisions and rationale

| Decision | Why it was made | Trade-off accepted |
|---|---|---|
| **Single file** | A new reader can hold the whole app in their head; no import graph, no package layout to explain. | Does not scale to multiple pages or shared modules. |
| **Plain function calls, no classes** | Keeps the code approachable for beginners, which was an explicit goal. | No encapsulation or dependency injection for testing. |
| **No `st.session_state`** | Removes an entire class of bugs around stale state, and there is nothing worth persisting in a one-shot generator. | Regenerating clears the previous result; users must download before re-running. |
| **Streamlit-supplied form widgets only** | No custom HTML or CSS, so the app inherits Streamlit's theme and needs no maintenance when the theme changes. | Limited visual customisation. |
| **Single model constant** | Groq retires model IDs periodically; keeping the ID in one named constant makes the fix a one-line edit. | No automatic fallback if the model disappears. |
| **List-based option sets** | Adding a content type, platform, or tone is a one-line change with no other edits needed. | Options are compile-time constants, not configurable at runtime. |
| **Exactly one API call per click** | Predictable latency and cost; no hidden retries. | A transient network error surfaces to the user rather than self-healing. |
| **Broad `except Exception` around the API call** | Guarantees the user sees an actionable message instead of a bare Streamlit traceback. | Catch-all error handling is coarse; specific exceptions are not distinguished. |
| **Unpinned dependencies** | Streamlit Cloud installs current working versions, avoiding a stale-lock conflict. | A future breaking change in either library could require a code update. |

---

## 9. Error handling and resilience

Three failure classes are handled explicitly, all before or around the model call.

**Missing credential.** Checked first. The user is shown instructions naming the exact secret key and the sidebar alternative.

**Empty required input.** Topic and Target audience are free text, so both are tested with `.strip()` to reject whitespace-only entries. The app warns rather than sending a useless request.

**API failure.** The whole call is wrapped in `try`/`except Exception as e`, and the exception message is shown as *"Something went wrong: …"*. This covers authentication errors, rate-limit responses, model-not-found errors, and network timeouts alike. The underlying text is passed through unchanged so the user can act on it.

**Graceful degradation in parsing.** If the model returns text without the `"Hashtags:"` marker, the split is skipped and the full text still renders in the post box. A formatting deviation therefore does not break the app.

**Not handled.** There is no retry with backoff, no request timeout configuration, and no fallback model. These are deliberate omissions in favour of simplicity, and are the first items in the future-work list.

---

## 10. Testing and verification status

Verification performed on this codebase, and its limits, is stated plainly below.

| Check | Method | Result |
|---|---|---|
| Syntax validity | `python -m py_compile app.py` | Passed — compiles with no errors |
| Dependency resolvability | Installing the two declared packages | `streamlit` and `groq` install successfully |
| SDK call signature | Introspection of `chat.completions.create` | Confirms the parameters used — `model`, `messages`, `max_tokens` — are all accepted |
| Model availability | Review of Groq's published model list | `openai/gpt-oss-120b` is a listed production model |
| Deprecation awareness | Review of Groq's deprecation page | Confirmed the previously common `llama-3.3-70b-versatile` was shut down on 16 August 2026, which is why it is not used |
| **Live end-to-end generation** | Requires a real API key | **Not performed** — no key was available during verification |

**Residual uncertainty.** The code compiles and the SDK interface matches, but a live generation against the real API has not been executed. The first run after deployment should be treated as the acceptance test: confirm that a post and a hashtag line come back, and confirm the Caption/Hashtags split renders. No other aspect is unverified.

---

## 11. Security considerations

**Credential exposure is the main risk, and it is mitigated.** The key lives in Secrets or the environment, never in source. The repository ships a `.gitignore` that excludes `.env` and `.streamlit/secrets.toml` precisely so a key cannot be committed by accident. Because a public repository's contents are visible to everyone, a committed Groq key would be exposed immediately and revoked by the provider — this is called out in the documentation.

**Input handling.** User text is inserted into a prompt string and sent to the model. It is never executed, never used to build a file path, and never used in a database query. The practical risk is limited to prompt injection into the model's own output, which affects text quality rather than system integrity.

**Output handling.** Model output is rendered through Streamlit's Markdown and code widgets. Streamlit escapes raw HTML by default, so the generated text cannot inject scripts into the page.

**Transport.** All API traffic is HTTPS, handled by the SDK.

**Data retention.** No user input and no generated text is stored. Nothing is written to the server filesystem; the download button streams bytes from memory.

**Scope note.** There is no authentication in front of the app. A public Streamlit deployment is reachable by anyone with the URL, and each visitor's generations consume the owner's configured API key quota. For a shared deployment this is the single most important operational consideration, and the reason a per-user key option remains in the sidebar.

---

## 12. Limitations

**Functional**

- Generates text only — it does not publish, schedule, or attach media.
- No saved history; each result replaces the last.
- No multi-language selector; the model mirrors the language of the input.
- One output variant per click; no side-by-side comparison of alternatives.

**Technical**

- Streaming is not used, so the user waits for the full response behind a spinner.
- No retry or backoff on transient failures.
- No automated tests exist.
- No configuration UI for model, temperature, or token limits.

**External dependencies**

- **Model availability.** Groq retires model IDs without long notice. The `MODEL_ID` constant is the single repair point.
- **Rate limits.** The free tier enforces requests-per-minute and tokens-per-minute ceilings. Heavy use yields an HTTP 429, surfaced as the generic error message.
- **Shared key exposure.** On a public deployment, the owner's key backs every visitor's requests.

**Quality**

- AI-generated copy can contain inaccuracies and should be reviewed before publication.
- Tone and hashtag quality vary between generations, which is inherent to sampling-based generation.

---

## 13. Operational notes

**Changing the model.** Edit the `MODEL_ID` constant near the top of `app.py` to an ID from Groq's current model list. No other change is required.

**Adding an option.** Append a string to `CONTENT_TYPES`, `PLATFORMS`, or `TONES`. The dropdown or slider picks it up automatically and the prompt inherits it, because the prompt is built from the selected value.

**Adjusting creativity.** `temperature` in `generate_post()` controls variation: lower values give more consistent, conservative copy, higher values more varied output. `max_tokens` caps the response length.

**Deployment updates.** Any push to the repository's `main` branch triggers an automatic rebuild. Secret changes take effect after the app reboots.

**Cost and quota.** The app runs on Groq's free developer tier. There is no billing integration in the code.

---

## 14. Future work

Ordered roughly by value against effort:

1. **Add a retry with backoff** around the API call to absorb transient rate-limit and network errors.
2. **Pin dependency versions** once a stable combination is confirmed in production.
3. **Add streamed output** so text appears progressively rather than behind a spinner.
4. **Persist results in `st.session_state`** so a regenerated post can be compared against the previous one.
5. **Expose model and temperature in the sidebar** for advanced users.
6. **Add platform-aware length guardrails** — for example, enforce a character budget when the platform is X (Twitter).
7. **Add automated tests** for `build_prompt()`, the key-resolution order, and the hashtag-splitting logic, which are all pure functions and easy to test.
8. **Support multiple output variants** per request for A/B selection.
9. **Add a copy-to-clipboard affordance** and a lightweight history panel.
10. **Harden the shared-key scenario** with either an app-level password gate or enforced per-user keys.

---

## 15. File inventory

| File | Role | Notes |
|---|---|---|
| `app.py` | The complete application | ~170 lines; the only executable file |
| `requirements.txt` | Dependency declaration | Two unpinned lines: `streamlit`, `groq` |
| `.gitignore` | Repository hygiene | Excludes `.env`, `.streamlit/secrets.toml`, `__pycache__/`, `*.pyc`, virtual environments |
| `README.md` | Project overview and setup | For developers and deployers |
| `USAGE.md` | End-user guide | For anyone operating the app |
| `REPORT.md` | This document | Architecture, decisions, verification, and roadmap |

---

## Conclusion

AI Content Assistant meets its stated objective: a single-file, dependency-light Streamlit app that turns five selections into a publishable social post with hashtags, secured so that credentials never enter source control, and documented for both technicians and end users. Its deliberate simplifications — no persistence, no retries, no streaming, one model — keep the codebase small and legible at a known cost that the future-work list addresses in priority order. The one unverified item is a live end-to-end generation against the real API, which the first deployment run will settle.
