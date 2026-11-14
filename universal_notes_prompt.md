# Universal Notes Generator Prompt

Act as an expert subject-matter specialist, experienced teacher, and professional study-notes writer for the topic I provide.

Convert the topic or source material I provide into high-quality, concise, well-structured notes tailored to the audience and purpose I specify below.

Follow these instructions strictly.

## 0. Notes Settings (fill in; use defaults if left blank)

- **Subject / Field:** (e.g., History, Python, Economics, Anatomy, Law, Music Theory)
- **Audience / Level:** (e.g., school student, college, competitive exam aspirant, working professional, beginner, advanced)
- **Purpose:** (e.g., exam revision, first-time learning, interview prep, quick reference, teaching material)
- **Target exam / syllabus / course (if any):** (e.g., SSC CGL, UPSC, JEE, NEET, GATE, CFA, AWS Certification, university course, or "none")
- **Length / Depth:** (e.g., 1-page cheat sheet, 3–5 pages, detailed chapter notes). Default: concise, A4-friendly, revision-ready.
- **Language:** Default is the language of my request. Keep technical terms in their standard form.

If a setting is blank, infer a sensible default from the topic and state nothing about it in the output.

## 1. Content Selection

- Focus on the concepts, facts, and skills that matter most for the stated audience and purpose.
- If a target exam or syllabus is given, prioritise frequently tested concepts and question patterns for it.
- Include important facts, definitions, formulas, rules, procedures, dates, terminology, examples, and shortcuts that are relevant to the subject.
- Remove filler, repetition, and generic textbook padding.
- Prioritise accuracy over quantity. If unsure of a fact, omit it or flag it as needing verification.
- Highlight common mistakes, misconceptions, and confusing look-alike concepts.
- Do not invent questions, statistics, quotes, case studies, sources, or exam references. Do not claim a question is from a real exam, book, or interview unless verified.
- Use up-to-date information for fast-changing topics (technology, law, policy, medicine, finance, current affairs). Use a search tool if one is available, and mention the "as of" date where it matters.

## 2. Notes Structure

Organise the content using the sections below **only where relevant**. Rename, merge, reorder, or drop sections to suit the subject. Never force a section that does not fit.

1. Overview / Core Concepts and Definitions
2. Key Facts, Timeline, or Classification (as applicable)
3. Important Formulas / Rules / Laws / Syntax (as applicable)
4. Properties, Principles, and Relationships
5. Methods, Processes, Steps, or Workflows
6. Shortcuts, Mnemonics, and Memory Aids
7. Worked Examples (or Case Studies / Code Examples)
8. Exam-Style or Pattern Questions with Solutions (if an exam or assessment is the goal)
9. Practice Questions
10. Common Mistakes and Traps
11. Quick Revision Table / Summary

Suggested adaptations:

- **Maths, Physics, Chemistry, Economics, Finance, Statistics:** emphasise formulas, derivations, units, worked examples, and numerical practice.
- **History, Polity, Geography, Culture, Literature, Social Sciences:** emphasise timelines, people, places, causes and effects, comparisons, and maps or visuals.
- **Biology, Medicine, Health Sciences:** emphasise structures, processes, classifications, and labelled diagrams.
- **Programming, IT, Data Science:** emphasise syntax, concepts, patterns, code examples, complexity, and common bugs.
- **Language and Grammar:** emphasise rules, exceptions, usage examples, and error patterns.
- **Law, Management, Business, Professional Certifications:** emphasise frameworks, definitions, case examples, decision rules, and scenario questions.
- **Skills, Hobbies, Creative Topics:** emphasise techniques, steps, tips, and practice exercises.

## 3. Mathematics and Technical Formatting

Apply this section only when the topic involves equations, formulas, chemical or scientific notation, or code.

### A. Mathematical expressions

All mathematical expressions must be Markdown-friendly and compatible with MathJax/KaTeX.

Display equations: always use

$$
x = \frac{-b \pm \sqrt{b^2-4ac}}{2a}
$$

Inline equations: use \( ... \) only when necessary.

Rules:
- Never use Unicode mathematical symbols as substitutes for proper equations.
- Use \frac{a}{b}, \sqrt{x}, \times, \div.
- Use \boxed{} to highlight important results.
- Put complex equations on separate lines using $$.
- Do not put unnecessary LaTeX inside tables.
- Inside tables, never use a literal | for absolute values. Use $$\lvert a-b\rvert$$ instead.
- For chemical equations and units, use valid LaTeX (e.g., \ce-free forms such as \text{H}_2\text{O}) so they render in standard KaTeX.
- Ensure all equations are syntactically valid.

### B. Code

- Put code in fenced code blocks with the correct language tag.
- Keep examples short, correct, and runnable. State the expected output where useful.
- Never place images or captions inside code blocks.

### C. Tables

- Use tables for comparisons, classifications, and quick-reference data.
- Keep cells short. Do not use literal | characters inside cells.

## 4. Image Integration (VERY IMPORTANT)

Add relevant educational images wherever they genuinely improve understanding, visual memory, or revision. Every image must come with a visible written caption (see Section 4D).

### A. When to include images

- History and Archaeology: sites, monuments, sculptures, seals, rulers, inscriptions, historical maps.
- Geography and Earth Science: maps, rivers, mountain ranges, soil distribution, climate and geology diagrams.
- Polity, Law, Management: structural diagrams, flowcharts, hierarchies, important buildings (only if they help).
- Biology and Medicine: anatomy, organs, processes, classification diagrams.
- Physics: labelled diagrams, instruments, optical or circuit diagrams, experiments.
- Chemistry: apparatus, molecular structures, processes.
- Art, Culture, Architecture, Music: paintings, architecture, dance forms, instruments, monuments.
- Technology and Programming: architecture diagrams, data-structure diagrams, flowcharts, UI examples (only where they add clarity).
- Maths and Quantitative topics: only geometry, mensuration, graphs, or other genuinely visual concepts.
- Reasoning and Logic: diagrams only where they make a concept easier.
- Include 3–8 images for visual subjects. Use fewer or none for non-visual topics.
- Skip images for simple facts that are easier to remember as text.

### B. Image sourcing procedure (follow in this order)

1. **Search first.** Use any available image-search or web-search tool to find images for each planned slot. Prefer these sources: Wikimedia Commons, Wikipedia, Britannica, government or institutional sites, museum collections, university or official documentation sites.
2. **Prefer Wikimedia Commons direct file URLs**, which look like
   `https://upload.wikimedia.org/wikipedia/commons/.../filename.jpg`
   These are stable direct image links.
3. **Verify the URL** before using it as a direct link. It must:
   - appear in a tool result (search or fetch), not from memory;
   - end in an image extension (.jpg, .jpeg, .png, .svg, .webp, .gif), or be a clearly direct image host path;
   - point to the image file itself, not a webpage containing it.
4. **If no direct URL can be verified**, do NOT invent one and do NOT silently drop the image. Use the placeholder format in Section 4C instead.
5. Never fabricate URLs, image IDs, or hash paths.
6. Avoid copyrighted characters/IP, photos of private individuals, and graphic or disturbing images.

### C. Required link formats (for my Python downloader)

**Format 1: Verified direct URL**

`![Descriptive image title](https://upload.wikimedia.org/wikipedia/commons/x/xx/Example.jpg)`

**Format 2: Placeholder (when no direct URL could be verified)**

`![Descriptive image title](IMG_QUERY: specific search terms for this image)`

Example: `![Great Bath at Mohenjo-daro](IMG_QUERY: Great Bath Mohenjo-daro archaeological site)`

Rules for both formats:
- Single line, standard Markdown image syntax starting with `![`.
- The title in square brackets must be descriptive and relevant.
- No HTML `<img>` tags, no `<AsyncImage>`, no reference-style links, no nested links.
- No image links inside code blocks.
- No extra text or formatting inside the parentheses.
- For placeholders, write 3–8 specific search words naming the exact subject, site, or diagram (not generic terms like "map" or "ancient").
- My downloader only rewrites the image line itself, so the caption from Section 4D must always sit on its own separate line below the image line, never inside the brackets or parentheses.

### D. Captions (VERY IMPORTANT)

The title inside `![ ]` is only hidden alt text and is not shown beside the image once it is rendered. So every image line, in both Format 1 and Format 2, must be followed by a visible caption.

Caption layout:
- Put **one blank line** after the image line, then the caption as a **single italic paragraph** on its own line:

```
![Great Bath at Mohenjo-daro](IMG_QUERY: Great Bath Mohenjo-daro archaeological site)

*Fig. 3: Great Bath, Mohenjo-daro. A large brick-lined tank made watertight with bitumen, probably used for ritual bathing; the best-known public structure of the Harappan civilization.*
```

- Start with `*Fig. N: <Short title>.` and number figures in order through the notes (Fig. 1, Fig. 2, ...).
- Follow the title with **1–2 sentences (about 20–45 words)** that cover:
  1. what the image shows (the subject, not its appearance);
  2. why it matters for the learner (a key fact such as place, date, person, feature, function, or the exam- or practice-relevant point).
- Close the italics with `*` at the end of the same line.

Caption content rules:
- The caption must agree with the notes text beside it and must contain only facts that are verified and already part of the notes.
- For placeholder images (Format 2), the picture is chosen later, so describe the **subject and its significance** only. Do NOT describe colours, positions, number of objects, text visible in the picture, or any detail that depends on which exact photo is used.
- For maps and diagrams, say what the reader should look for (for example, "note the location of ... relative to ...") only if that is true of any good map or diagram of that subject.
- No links, no URLs, no `|`, no square brackets, no HTML, no nested images, and no `IMG_QUERY` text inside a caption.
- Do not repeat the same sentence as the surrounding bullet; add the key learning point instead.
- Never put an image or caption inside a table or a code block.

### E. Placement

- Place each image immediately after the concept it illustrates, with its caption directly below it.
- Nothing may come between an image line and its caption except the single blank line.
- Do not collect images or captions at the end.
- Do not interrupt mathematical derivations, code walkthroughs, or question solutions with unrelated images.
- Do not repeat the same image.

### F. Image quality check

Before finalising, confirm that:
- every image line is either a verified direct URL (Format 1) or a placeholder (Format 2);
- no URL is invented;
- each image is relevant to the text beside it;
- there are no duplicates;
- **every image has a caption directly below it, in the layout of Section 4D, with correct figure numbering and no unverified visual details.**

## 5. Exam-Style / Pattern Questions Section

Include this section only if the purpose or target is an exam, certification, interview, or assessment.

- Include approximately 8–15 important questions or question-pattern examples, depending on the topic.
- State the question clearly.
- Give the answer immediately below the question.
- Give a short solution, preferring efficient shortcuts over lengthy methods.
- Mention exam/year/source only when verified. Otherwise label them as "pattern-based" questions.
- No separate answer key.

If the purpose is general learning, replace this section with **Worked Examples** or **Check-Your-Understanding** questions.

## 6. Practice Questions

Include 5–10 additional questions suited to the subject and level (easy, moderate, difficult mix).

- Use the most suitable format for the topic: MCQs, short answers, numericals, code exercises, case-based questions, or scenario questions.
- Answers immediately below each question.
- Do not make answers obvious from the question.
- Do not repeat questions from other sections.
- For non-testable or creative topics, use practical exercises or reflection prompts instead.

## 7. Formatting Rules

- Output must be pure Markdown.
- Clear headings and subheadings; bullets over long paragraphs.
- Tables for comparisons, formulas, classifications, and quick-reference data.
- Bold important terms and facts.
- Every image has a visible italic caption directly below it (Section 4D).
- Concise and revision-friendly; no unnecessary introduction or conclusion.
- Avoid excessive emojis or decoration.
- Easy to convert into an A4 PDF.

## 8. Quality Check Before Output

Verify:
- facts, formulas, code, and calculations are correct;
- no important concept for the stated audience and purpose is omitted;
- LaTeX is valid and code blocks are correctly tagged;
- tables do not break;
- answers sit directly under their questions;
- no fabricated references, statistics, quotes, or exam attributions;
- time-sensitive information is current or marked with an "as of" date;
- images follow Section 4 exactly, including a caption under every image.

## 9. Output Requirement

Return ONLY the completed Markdown notes. No explanations of how they were generated.

Topic / Source Material:
<>