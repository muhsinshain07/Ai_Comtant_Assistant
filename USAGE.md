# 📖 AI Content Assistant — User Guide

This guide explains how to **use the app**, from the moment you open it to the moment you have a finished, copy-paste-ready social media post. No coding knowledge is needed for anything in this file.

> Setting the app up or hosting it yourself? See [README.md](README.md) instead. This file is only about *using* it.

---

## Table of contents

- [What this app is](#-what-this-app-is)
- [Before you start](#-before-you-start)
- [Opening the app](#-opening-the-app)
- [The screen at a glance](#-the-screen-at-a-glance)
- [Step-by-step: generating a post](#-step-by-step-generating-a-post)
- [The five inputs explained](#-the-five-inputs-explained)
- [Understanding the output](#-understanding-the-output)
- [Saving and using your post](#-saving-and-using-your-post)
- [Worked examples](#-worked-examples)
- [Writing better prompts (topics)](#-writing-better-prompts-topics)
- [Common messages and what they mean](#-common-messages-and-what-they-mean)
- [Frequently asked questions](#-frequently-asked-questions)

---

## ✨ What this app is

**AI Content Assistant** writes social media posts for you.

You tell it **what** you want to post about, **where** it will be posted, **who** should read it, and **how** it should sound. It then writes:

- a complete **caption** for the post, and
- a set of relevant **hashtags**.

You can copy either part, or download the whole thing as a text file. Each generation takes just a few seconds.

---

## ✅ Before you start

You need two things:

1. **The app open in your browser.** You will receive a link that looks like `https://your-app-name.streamlit.app`. Click it — no installation required.
2. **A Groq API key available.** This is the credential the app uses to talk to the AI model.
   - If the person who shared the app configured it, the key is already set and you can skip this entirely.
   - If not, the sidebar will ask for it. Get a free key:
     1. Open <https://console.groq.com> and sign up (free, no credit card).
     2. Click **API Keys** in the left menu → **Create API Key**.
     3. Copy the key (it starts with `gsk_`) and paste it into the app's sidebar field. It is only ever used for this session and is never displayed back to you.

---

## 🖥 Opening the app

Open the link you were given. On first load the app takes a few seconds to wake up — this is normal for a free-hosted app. You will then see the title **✨ AI Content Assistant** and a form.

---

## 🧭 The screen at a glance

The screen has three areas.

**1. The sidebar (left)** — settings:

| Element | Purpose |
|---|---|
| **Groq API key** | A password field. Paste your key here if one is not already configured. |
| **Model** | A caption at the bottom showing the AI model currently in use. You do not need to change this. |

**2. The form (centre)** — your five choices, laid out in two columns:

| Left column | Right column |
|---|---|
| **Content type** (dropdown) | **Platform** (dropdown) |
| **Topic** (text box) | **Target audience** (text box) |

Below them, spanning the full width, is the **Tone** slider, and finally the big **🚀 Generate post** button.

**3. The results (below the button)** — appears only *after* you click Generate. It shows your post, the caption on its own, the hashtags on their own, and a download button.

---

## 🪜 Step-by-step: generating a post

1. **Check the sidebar.** If there is a key already configured, nothing to do. If the field is empty and you have a key, paste it now.
2. **Pick a Content type** from the first dropdown — for example, *Social Media Post*.
3. **Pick a Platform** from the second dropdown — for example, *Instagram*.
4. **Type your Topic** — the subject of the post — for example, *Launching our new eco water bottle*.
5. **Type your Target audience** — who should read it — for example, *Fitness-conscious Gen Z*.
6. **Drag the Tone slider** to the voice you want — for example, *Friendly*.
7. **Click "🚀 Generate post".** A spinner labelled *Writing your post…* appears. Wait a few seconds.
8. **Read the result.** A green *Done!* message appears, followed by your post.
9. **Copy or download.** Use the copy icon on any box, or click **⬇️ Download as .txt**.
10. **Not happy with it?** Change the Tone — it is the input with the biggest effect on style — or reword the Topic, then click Generate again. Every click produces a fresh post, so you can generate several and keep the best.

---

## 🎛 The five inputs explained

### Content type
The *shape* of the writing.

| Option | Choose it when you want… |
|---|---|
| **Social Media Post** | A general feed post for any platform. |
| **Product Promo** | Something that highlights a product's benefits and pushes a purchase or sign-up. |
| **Blog Intro** | An opening paragraph to hook readers into a longer article. |
| **Email** | A newsletter or campaign email body, complete with a sign-off feel. |
| **Ad Copy** | Short, punchy sales text for an ad placement. |

### Platform
Where the post will live. The model uses this to match the expected style and length — Instagram tends to be visual and hashtag-heavy, LinkedIn more professional and story-driven, X (Twitter) short and snappy, TikTok casual and trend-aware.

Options: Instagram, LinkedIn, X (Twitter), Facebook, TikTok, Threads.

### Topic
The subject. Anything works, but the more specific you are, the better the post. See [Writing better prompts](#-writing-better-prompts-topics).

### Target audience
Who you are speaking to. This changes vocabulary, references, and the kind of call to action. "Budget-conscious students" and "enterprise procurement managers" produce very different posts on the same topic.

### Tone
How it sounds. Drag the slider between six steps:

| Tone | Feels like |
|---|---|
| **Professional** | Polished, credible, business-appropriate. |
| **Friendly** | Warm, approachable, conversational (the default). |
| **Casual** | Relaxed and informal, like talking to a friend. |
| **Funny** | Playful, witty, light. |
| **Inspirational** | Uplifting, motivational, emotive. |
| **Bold** | Confident, direct, high-energy. |

---

## 📄 Understanding the output

After each generation you get up to four blocks.

| Block | What it contains |
|---|---|
| **Your post** | The complete text — caption and hashtags together — in a scrollable, copyable box. |
| **Caption** | The same post *without* the hashtags. Copy this into the main text field of your social platform. |
| **Hashtags** | Just the tags, on a single line, in a monospaced box that is easy to select and copy. |
| **⬇️ Download as .txt** | Saves everything as a file named `generated_post.txt`. |

Typical shape of a result:

```
[Scroll-stopping hook line]

[Short body paragraphs, spaced out with line breaks]

[Clear call to action]

Hashtags: #tag1 #tag2 #tag3 #tag4 #tag5 #tag6 #tag7 #tag8
```

The app expects the hashtags to start with the word `Hashtags:`. That marker is what lets it split the caption from the tags — which is why the separate Caption and Hashtags blocks appear.

---

## 💾 Saving and using your post

**To post immediately:** copy from the **Caption** box, paste it into your platform's composer, then copy from the **Hashtags** box and paste those at the end. Hashtags often work better in the first comment on Instagram — that is your choice.

**To keep for later:** click **⬇️ Download as .txt**. The file lands in your normal Downloads folder and opens in any text editor.

**To reuse a keystroke-friendly flow:** keep the tab open, tweak the Tone, and generate again — the old result is replaced each time, so download anything you want to keep before regenerating.

**One important habit:** read the post before you publish it. The text is AI-generated and can contain small inaccuracies. Treat it as a strong first draft, not a finished, verified piece.

---

## 🧪 Worked examples

### Example 1 — Instagram launch post
| Input | Value |
|---|---|
| Content type | Product Promo |
| Platform | Instagram |
| Topic | Launching our new eco water bottle made from recycled ocean plastic |
| Target audience | Fitness-conscious Gen Z |
| Tone | Friendly |

You would get a bright, emoji-friendly caption opening with a hook about plastic waste or hydration, a short body about the bottle, a "link in bio" style call to action, and a broad-plus-niche hashtag set.

### Example 2 — LinkedIn thought-leadership post
| Input | Value |
|---|---|
| Content type | Social Media Post |
| Platform | LinkedIn |
| Topic | Three lessons we learned scaling our remote team from 5 to 50 people |
| Target audience | Startup founders and people managers |
| Tone | Professional |

Expect a more measured, story-led caption with a numbered insight structure and professional, lower-volume hashtags.

### Example 3 — Short promo for X
| Input | Value |
|---|---|
| Content type | Ad Copy |
| Platform | X (Twitter) |
| Topic | Our note-taking app now syncs offline |
| Target audience | Students and freelance writers |
| Tone | Bold |

Expect one or two tight, high-impact lines and a compact hashtag set.

### Example 4 — Newsletter opener
| Input | Value |
|---|---|
| Content type | Email |
| Platform | Facebook |
| Topic | Our March community meetup recap and what is coming in April |
| Target audience | Members of our local running club |
| Tone | Casual |

Expect a warm greeting-style opener, a short recap, a "see you there" close, and minimal hashtags.

---

## ✍️ Writing better prompts (topics)

The **Topic** field is free text, so a little extra detail goes a long way.

**Weak:** `water bottle`
**Better:** `Launching our new eco water bottle made from recycled ocean plastic`

**Weak:** `AI tips`
**Better:** `Five practical ways small businesses can use AI to save time each week`

**Weak:** `sale`
**Better:** `Black Friday sale: 40% off all winter jackets, this weekend only`

Useful things to include when relevant: the product or subject, a specific angle or benefit, a number, a timeframe, and any offer or price.

Keep the **Target audience** short but concrete — "new dog owners in cities" beats "everyone".

---

## 🚦 Common messages and what they mean

| What you see | What it means | What to do |
|---|---|---|
| **"No API key found. Add GROQ_API_KEY to Streamlit Secrets or paste it in the sidebar."** | The app has no key to call the model with. | Paste your Groq key into the sidebar field, or ask the app's owner to configure it. |
| **"Please fill in both the topic and the target audience."** | You clicked Generate with an empty Topic or Target audience. | Fill in both boxes — they are required. |
| **"Something went wrong: …"** | The model call failed. The text after the colon is the technical reason. | Check the reason: a rate-limit message means wait and retry; an authentication message means the key is wrong or revoked; a model error means the model has been retired. |
| Spinner runs unusually long | The app or the model service is busy. | Wait; if it times out, click Generate again. |
| Blank page | Usually a hosting hiccup. | Reload the page once, then try again. |

---

## ❓ Frequently asked questions

**Do I need to install anything?**
No. The app runs in the browser. Installation is only needed if you want to run or host it yourself — see [README.md](README.md).

**Does it cost anything?**
The app itself is free to use, and Groq's developer tier is free. Very heavy use can hit Groq's free rate limits, in which case you simply wait a moment and try again.

**How many posts can I generate?**
There is no fixed limit in the app, but the free model tier has per-minute limits. For normal use — a handful of posts at a time — you will not notice them.

**Can it post directly to Instagram or LinkedIn for me?**
No. It writes the text only. You copy the caption and hashtags and post them yourself.

**Does it schedule or save my posts?**
No. It holds no history. Download or copy anything you want to keep before generating again.

**Will every generation be identical for the same inputs?**
No — the model varies its wording each time, which is useful for producing several options. Re-run with the same inputs to get a fresh variation.

**Can I change the tone of an existing post without starting over?**
Yes — keep your Topic and audience as they are, move the Tone slider, and click Generate again.

**Is my API key safe?**
The app never stores it and never writes it into the page. If the field is empty, the key used is one configured privately by the app's owner.

**Can I use the output commercially?**
The text is generated for you, but you are responsible for checking it for accuracy, originality, and compliance with the platform's rules before publishing. Add a license file to the repository if you plan to redistribute the software itself.

---

## 🔗 Related documents

- **[README.md](README.md)** — project overview, setup, deployment, and technical troubleshooting.
