# Successive Percentage Change

**Exam relevance:** SSC CGL (Tier 1 & 2), CHSL, CPO. It is tested directly and also underlies Profit & Loss, Discount, Mensuration, Population and Salary problems.

---

## 1. Core Concepts / Definitions

- **Percentage change** is the change expressed as a percentage of the **original (base) value**.

$$
\text{\% change} = \frac{\text{Final value} - \text{Initial value}}{\text{Initial value}} \times 100
$$

- **Successive percentage change** means two or more percentage changes applied one after another. Each new change is calculated on the **latest value**, not the original one.
- **Net (overall) change** is the single equivalent percentage change that gives the same final result.
- **Sign convention:** increase is **+**, decrease is **−**.
- **Multiplier idea:** an increase of \( x\% \) multiplies the value by \( 1 + \frac{x}{100} \), and a decrease of \( x\% \) multiplies it by \( 1 - \frac{x}{100} \).

---

## 2. Important Formulas

**Two successive changes** of \( a\% \) and \( b\% \) (use signs):

$$
\boxed{\text{Net change} = a + b + \frac{ab}{100}\ \%}
$$

**Three successive changes** of \( a\%, b\%, c\% \):

$$
\boxed{\text{Net change} = a + b + c + \frac{ab + bc + ca}{100} + \frac{abc}{10000}\ \%}
$$

**Multiplier (final value) method:**

$$
\text{Final} = \text{Initial} \times \left(1 + \frac{a}{100}\right)\left(1 + \frac{b}{100}\right)
$$

**Same percentage change applied twice:**

$$
\text{Net (increase twice)} = 2a + \frac{a^2}{100}\ \%
$$

**Increase by \( x\% \) then decrease by \( x\% \)** (or the reverse):

$$
\boxed{\text{Net decrease} = \frac{x^2}{100}\ \%}
$$

**Returning to the original value:**

| Situation | Required change |
|---|---|
| Value increased by x%, how much to decrease to return | x / (100 + x) × 100 % decrease |
| Value decreased by x%, how much to increase to return | x / (100 − x) × 100 % increase |

**Successive discounts** \( d_1\% \) and \( d_2\% \):

$$
\text{Single equivalent discount} = d_1 + d_2 - \frac{d_1 d_2}{100}\ \%
$$

---

## 3. Properties and Rules

- The order of changes does **not** matter: +20% then −10% gives the same net result as −10% then +20%.
- Successive changes **never add directly**; the cross term \( \frac{ab}{100} \) is always present.
- If one change is an increase and the other a decrease, the cross term is **negative**.
- If both changes are decreases, the cross term is **positive** because \( (-a)(-b) \) is positive.
- Net percentage change is always calculated on the **original** value, not the intermediate one.
- Final value is **greater than the original** if the multiplier product is greater than 1, and **less** if it is less than 1.

---

## 4. Shortcuts and Tricks

**Trick 1: Fraction method.** Convert the percentages to fractions and multiply.

| Percentage | Fraction | Meaning |
|---|---|---|
| 10% | 1/10 | multiply by 11/10 (increase) or 9/10 (decrease) |
| 12.5% | 1/8 | multiply by 9/8 or 7/8 |
| 16.67% | 1/6 | multiply by 7/6 or 5/6 |
| 20% | 1/5 | multiply by 6/5 or 4/5 |
| 25% | 1/4 | multiply by 5/4 or 3/4 |
| 33.33% | 1/3 | multiply by 4/3 or 2/3 |
| 50% | 1/2 | multiply by 3/2 or 1/2 |

Example: +20% then −25% gives \( \frac{6}{5} \times \frac{3}{4} = \frac{9}{10} \), so the net change is **−10%**.

**Trick 2: Memorise common results.**

| Successive changes | Net change |
|---|---|
| +10%, +10% | +21% |
| +20%, +20% | +44% |
| +10%, +20% | +32% |
| +20%, −20% | −4% |
| +25%, −20% | 0% |
| +10%, −10% | −1% |
| −10%, −10% | −19% |
| −20%, −20% | −36% |
| −10%, −20% | −28% |
| +50%, −50% | −25% |

**Trick 3: Dimension-change shortcut.**
- Area of a rectangle: length and breadth change by \( a\% \) and \( b\% \), so net change in area is \( a + b + \frac{ab}{100} \).
- Square or circle: a single \( a\% \) change in side or radius gives area change \( 2a + \frac{a^2}{100} \).
- Cube or sphere: a single \( a\% \) change in edge or radius gives volume change \( 3a + \frac{3a^2}{100} + \frac{a^3}{10000} \).

**Trick 4: Price vs consumption (constant expenditure).**

$$
\text{Expenditure} = \text{Price} \times \text{Consumption}
$$

If price rises by \( a\% \), the consumption must fall by:

$$
\boxed{\frac{a}{100 + a} \times 100\ \%}
$$

If price falls by \( a\% \), the consumption must rise by:

$$
\frac{a}{100 - a} \times 100\ \%
$$

---

## 5. Important Concepts for SSC

- **Mensuration link:** side/radius/edge changes always lead to successive-change calculations. Area is two-dimensional (apply the change twice) and volume is three-dimensional (apply it three times).
- **Population and depreciation:** these are repeated successive changes, so use multipliers.
- **Salary hike or cut:** the question may ask for the final salary or the single equivalent change.
- **Discount chains:** two or three successive discounts, combined with marked price and profit, appear in Tier 2.
- **Required change to restore the original:** the percentage is calculated on the **new** base, so it is not equal to the original change.
- **Percentage point vs percent:** a rise from 20% to 25% is a **5 percentage point** increase but a **25% relative** increase.

---

## 6. PYQ-Pattern Questions with Solutions

*These are pattern-based questions that reflect SSC style; they are not claimed to be actual PYQs.*

**Q1.** The price of an article is increased by 20% and then by 30%. What is the net percentage increase?

**Ans: 56%**

$$
20 + 30 + \frac{20 \times 30}{100} = 56
$$

---

**Q2.** A number is first increased by 25% and then decreased by 20%. What is the net change?

**Ans: 0% (no change)**

Fraction method: \( \frac{5}{4} \times \frac{4}{5} = 1 \).

---

**Q3.** The side of a square is increased by 20%. By what percentage does its area increase?

**Ans: 44%**

$$
2(20) + \frac{20^2}{100} = 40 + 4 = 44
$$

---

**Q4.** The length of a rectangle is increased by 20% and its breadth is decreased by 10%. Find the net change in area.

**Ans: 8% increase**

$$
20 - 10 + \frac{20 \times (-10)}{100} = 10 - 2 = 8
$$

---

**Q5.** The population of a town is 20,000. It increases by 10% in the first year and by 20% in the second year. What is the population after two years?

**Ans: 26,400**

$$
20000 \times \frac{11}{10} \times \frac{6}{5} = 26400
$$

---

**Q6.** The price of sugar increases by 25%. By what percentage must a family reduce its consumption so that expenditure remains unchanged?

**Ans: 20%**

$$
\frac{25}{100 + 25} \times 100 = 20\%
$$

---

**Q7.** A number is increased by 20% and then decreased by 20%. If the final result is 960, find the original number.

**Ans: 1000**

Net effect: \( 1.2 \times 0.8 = 0.96 \), so \( 0.96x = 960 \) and \( x = 1000 \).

---

**Q8.** Find the single discount equivalent to successive discounts of 20% and 10%.

**Ans: 28%**

$$
20 + 10 - \frac{20 \times 10}{100} = 28
$$

---

**Q9.** A person's salary is increased by 20% and then decreased by 25%. Find the net change.

**Ans: 10% decrease**

Fraction method: \( \frac{6}{5} \times \frac{3}{4} = \frac{9}{10} \).

---

**Q10.** The radius of a circle is increased by 10%. By what percentage does its area increase?

**Ans: 21%**

$$
2(10) + \frac{10^2}{100} = 21
$$

---

**Q11.** Three successive increases of 10%, 20% and 25% are applied to a price. Find the net increase.

**Ans: 65%**

Multiplier: \( 1.1 \times 1.2 \times 1.25 = 1.65 \), so the increase is 65%.

---

**Q12.** Two successive discounts of 20% and \( x\% \) are equivalent to a single discount of 28%. Find \( x \).

**Ans: 10%**

$$
20 + x - \frac{20x}{100} = 28 \implies 0.8x = 8 \implies x = 10
$$

---

## 7. Practice Questions

**Q1.** A price is reduced by 10% and then by 20%. Find the net percentage decrease.

**Ans: 28%**

Fraction method: \( \frac{9}{10} \times \frac{4}{5} = \frac{18}{25} \), which is 72% of the original, so the decrease is 28%.

---

**Q2.** A quantity is increased by 50% and then decreased by 50%. What is the net change?

**Ans: 25% decrease**

$$
50 - 50 - \frac{50 \times 50}{100} = -25
$$

---

**Q3.** The radius of a sphere is increased by 10%. By what percentage does its volume increase?

**Ans: 33.1%**

$$
3(10) + \frac{3(10)^2}{100} + \frac{10^3}{10000} = 30 + 3 + 0.1 = 33.1
$$

---

**Q4.** The length of a rectangle is increased by 25% and its breadth is decreased by 20%. What happens to the area?

**Ans: No change**

$$
25 - 20 + \frac{25 \times (-20)}{100} = 5 - 5 = 0
$$

---

**Q5.** The price of rice rises by 20%. By what percentage should a family cut consumption to keep monthly expenditure the same?

**Ans: \( 16\frac{2}{3}\% \)**

$$
\frac{20}{120} \times 100 = 16\frac{2}{3}\%
$$

---

**Q6.** A town has a population of 50,000. It decreases by 10% in one year and then increases by 20% the next year. What is the population after two years?

**Ans: 54,000**

$$
50000 \times \frac{9}{10} \times \frac{6}{5} = 54000
$$

---

**Q7.** A salary is increased by 20% and then reduced by \( x\% \), so that the net change is an 8% increase. Find \( x \).

**Ans: 10%**

$$
1.2 \times \left(1 - \frac{x}{100}\right) = 1.08 \implies 1 - \frac{x}{100} = 0.9 \implies x = 10
$$

---

**Q8.** A shopkeeper marks an article 40% above cost price and allows two successive discounts of 10% each. Find the profit percentage.

**Ans: 13.4%**

$$
1.4 \times 0.9 \times 0.9 = 1.134
$$

So the selling price is 113.4% of the cost price, a profit of 13.4%.

---

**Q9.** The side of a square is increased by \( x\% \), and its area increases by 69%. Find \( x \).

**Ans: 30%**

New area factor is 1.69, so the side factor is \( \sqrt{1.69} = 1.3 \), an increase of 30%.

---

**Q10.** Three successive discounts of 10%, 20% and 30% are given on an article. Find the single equivalent discount.

**Ans: 49.6%**

$$
0.9 \times 0.8 \times 0.7 = 0.504
$$

So the final price is 50.4% of the original, a discount of 49.6%.

---

## 8. Common Exam Traps

- **Adding percentages directly.** +20% and +30% is **not** +50%; it is +56%.
- **Wrong sign in the cross term.** For one increase and one decrease, \( ab \) is negative.
- **Using the wrong base.** Percentage change is always on the base **before** that change.
- **Assuming "+x% then −x%" returns the original.** It gives a net decrease of \( \frac{x^2}{100}\% \).
- **Reverse change is not equal.** Restoring a 20% increase needs a **16.67%** decrease, not 20%.
- **Area or volume answered as a single change.** Side +10% does not mean area +10%.
- **Successive discount treated as additive.** 20% + 10% discounts equal 28%, not 30%.
- **Confusing percentage points with percent.**
- **Wrong multiplier for a decrease.** A 15% decrease uses 0.85, not 1.15.

---

## 9. Last-Minute Revision Table

| Concept | Key point |
|---|---|
| Two changes (a, b) | a + b + ab/100 |
| Three changes (a, b, c) | a + b + c + (ab + bc + ca)/100 + abc/10000 |
| Same change twice | 2a + a²/100 |
| +x% then −x% | Net decrease of x²/100 % |
| Area, side change a% | 2a + a²/100 |
| Volume, edge change a% | 3a + 3a²/100 + a³/10000 |
| Rectangle area (length a%, breadth b%) | a + b + ab/100 |
| Price rise a%, constant expenditure | Cut consumption by a/(100 + a) × 100 % |
| Price fall a%, constant expenditure | Raise consumption by a/(100 − a) × 100 % |
| Successive discounts d1, d2 | d1 + d2 − d1·d2/100 |
| Order of changes | Does not matter |
| Best method | Fraction/multiplier method for speed |