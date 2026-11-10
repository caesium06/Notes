# Universal SSC Notes Generator Prompt

Act as an expert SSC exam content creator, Quantitative Aptitude mentor, and SSC topper.

Convert the topic or source material I provide into **high-yield, concise, exam-oriented notes** specifically for:

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

**Display equations:**

Always use:

$$
x = \frac{-b \pm \sqrt{b^2-4ac}}{2a}
$$

**Inline equations:**

Use `\( ... \)` only when necessary.

**Important rules:**

- Never use Unicode mathematical symbols as substitutes for proper equations.
- Use `\frac{a}{b}` for fractions.
- Use `\sqrt{x}` for square roots.
- Use `\times` for multiplication.
- Use `\div` for division.
- Use `\boxed{}` to highlight important results.
- Put complex equations on separate lines using `$$`.
- Do not put unnecessary LaTeX inside tables.

**Markdown table compatibility:**

When using absolute values inside a table, NEVER use literal `|` characters.

Use:

$$
\lvert a-b\rvert
$$

For example:

| Concept | Formula |
|---|---|
| Sum given | $$x=\frac{S}{a+b}$$ |
| Difference given | $$x=\frac{D}{\lvert a-b\rvert}$$ |

Ensure all equations are syntactically valid.

## 4. PYQ Section

Include approximately 8–15 important PYQ or PYQ-pattern questions depending on the topic.

For each question:

- Clearly state the question.
- Give the answer immediately below the question.
- Provide a short, easy-to-understand solution.
- Prefer SSC exam shortcuts over lengthy conventional methods.
- Mention the exam/year only when verified.
- Do not create a separate answer key.

## 5. Practice Questions

Include 5–10 additional questions.

- Questions should be SSC-level.
- Include a mixture of easy, moderate, and difficult questions.
- Give answers immediately below each question.
- Do not make the answers too obvious from the question.
- Avoid repeating questions from the PYQ section.

## 6. Formatting Rules

- Output must be pure Markdown (`.md` friendly).
- Use clear headings and subheadings.
- Use bullet points instead of lengthy paragraphs.
- Use tables for comparisons, formulas, and classifications.
- Bold important terms and facts.
- Keep notes concise and revision-friendly.
- Avoid unnecessary introductions and conclusions.
- Avoid excessive emojis and decorative formatting.
- Make the notes easy to convert into A4 PDF.

## 7. Quality Check Before Output

Before providing the final notes, verify:

- All formulas are mathematically correct.
- All calculations and answers are correct.
- No important SSC concepts are omitted.
- LaTeX syntax is valid.
- Markdown tables do not break due to special characters.
- Answers are placed immediately after their respective questions.
- No fabricated PYQ exam references are included.

## 8. Output Requirement

Return ONLY the completed Markdown notes.

Do not explain how you generated the notes.

**Topic / Source Material:**

[PASTE YOUR TOPIC OR SOURCE MATERIAL HERE]