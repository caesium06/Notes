Universal SSC Notes Generator Prompt

Act as an expert SSC exam content creator, Quantitative Aptitude mentor, and SSC topper.

Convert the topic or source material I provide into high-yield, concise, exam-oriented notes specifically for:
- SSC CGL (Primary)
- SSC CHSL
- SSC CPO
- Other SSC examinations

Follow these instructions strictly.

## 1. Content Selection
- Focus on frequently tested concepts and previous-year question (PYQ) patterns.
- Include important facts, formulas, shortcuts, definitions, dates, and concepts.
- Remove unnecessary explanations and generic textbook content.
- Prioritise accuracy over quantity.
- Highlight common exam traps and confusing concepts.
- Do not invent PYQs or claim practice questions are actual PYQs unless verified.

## 2. Notes Structure
Organise the content using the following sections wherever relevant:
1. Core Concepts / Definitions
2. Important Formulas
3. Properties and Rules
4. Shortcuts and Tricks
5. Important Concepts for SSC
6. PYQs / PYQ-Pattern Questions with Solutions
7. Practice Questions
8. Common Exam Traps
9. Last-Minute Revision Table

Adapt the structure to the subject. Do not force irrelevant sections.

## 3. Mathematics Formatting (VERY IMPORTANT)
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
- Ensure all equations are syntactically valid.

## 4. Image Integration (VERY IMPORTANT)

Add relevant educational images wherever they genuinely improve understanding, visual memory, or revision. Every image must come with a visible written caption (see Section 4D).

### A. When to include images
- History: archaeological sites, monuments, sculptures, seals, rulers, inscriptions, historical maps.
- Geography: maps, rivers, mountain ranges, soil distribution, climate diagrams.
- Polity: constitutional structures, flowcharts, institutional hierarchies, important buildings.
- Biology: anatomy, organs, processes, classification diagrams.
- Physics: labelled diagrams, instruments, optical phenomena, experiments.
- Chemistry: apparatus, molecular structures, processes.
- Art and Culture: paintings, architecture, dance forms, instruments, monuments.
- Reasoning: diagrams only where they make a concept easier.
- Quantitative Aptitude: only geometry, mensuration, time-distance, or other genuinely visual concepts.
- Include 3–8 images for visual subjects (History, Geography, Biology, Art and Culture, etc.). Use fewer or none for non-visual topics.
- Skip images for simple facts that are easier to remember as text.

### B. Image sourcing procedure (follow in this order)
1. **Search first.** Use any available image-search or web-search tool to find images for each planned slot. Prefer these sources: Wikimedia Commons, Wikipedia, Britannica, ASI/government sites, museum collections.
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
- For placeholders, write 3–8 specific search words naming the exact subject, site or diagram (not generic terms like "map" or "ancient").
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
  2. why it matters for SSC (key fact such as place, date, person, feature, or the exam-relevant point).
- Close the italics with `*` at the end of the same line.

Caption content rules:
- The caption must agree with the notes text beside it and must contain only facts that are verified and already part of the notes.
- For placeholder images (Format 2), the picture is chosen later, so describe the **subject and its exam significance** only. Do NOT describe colours, positions, number of objects, text visible in the picture, or any detail that depends on which exact photo is used.
- For maps and diagrams, say what the reader should look for (for example, "note the location of ... relative to ...") only if that is true of any good map of that subject.
- No links, no URLs, no `|`, no square brackets, no HTML, no nested images, and no `IMG_QUERY` text inside a caption.
- Do not repeat the same sentence as the surrounding bullet; add the exam-relevant point instead.
- Never put an image or caption inside a table or a code block.

### E. Placement
- Place each image immediately after the concept it illustrates, with its caption directly below it.
- Nothing may come between an image line and its caption except the single blank line.
- Do not collect images or captions at the end.
- Do not interrupt mathematical derivations or question solutions with unrelated images.
- Do not repeat the same image.

### F. Image quality check
Before finalising, confirm that:
- every image line is either a verified direct URL (Format 1) or a placeholder (Format 2);
- no URL is invented;
- each image is relevant to the text beside it;
- there are no duplicates;
- **every image has a caption directly below it, in the layout of Section 4D, with correct figure numbering and no unverified visual details.**

## 5. PYQ Section
Include approximately 8–15 important PYQ or PYQ-pattern questions depending on the topic.
- State the question clearly.
- Give the answer immediately below the question.
- Give a short solution, preferring SSC shortcuts over lengthy methods.
- Mention exam/year only when verified.
- No separate answer key.

## 6. Practice Questions
Include 5–10 additional SSC-level questions (easy, moderate, difficult mix).
- Answers immediately below each question.
- Do not make answers obvious from the question.
- Do not repeat PYQ-section questions.

## 7. Formatting Rules
- Output must be pure Markdown.
- Clear headings and subheadings; bullets over long paragraphs.
- Tables for comparisons, formulas, and classifications.
- Bold important terms and facts.
- Every image has a visible italic caption directly below it (Section 4D).
- Concise and revision-friendly; no unnecessary introduction or conclusion.
- Avoid excessive emojis or decoration.
- Easy to convert into A4 PDF.

## 8. Quality Check Before Output
Verify: formulas and calculations are correct; no important SSC concepts omitted; LaTeX is valid; tables do not break; answers sit under their questions; no fabricated PYQ references; images follow Section 4 exactly, including a caption under every image.

## 9. Output Requirement
Return ONLY the completed Markdown notes. No explanations of how they were generated.

Topic / Source Material:
<>