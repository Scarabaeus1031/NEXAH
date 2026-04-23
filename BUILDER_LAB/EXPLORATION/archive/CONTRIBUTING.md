# 🤝 CONTRIBUTING — NEXAH

Welcome.

If you're here, you probably felt it already:

👉 there is structure here  
👉 and it’s not random  

You don’t need to understand everything to contribute.

---

## 🧠 How to start (5 minutes)

```bash
cd ENGINE/research/experiments/prime_modular_resonance/analysis
python run_all_visuals.py
```

Look at the output.

That’s it.

---

## 👀 What you're working with

You are exploring:

- discrete systems (e.g. primes mod n)
- transition structures
- flow fields
- loops, basins, and topology

👉 Your job is simple:

**change something → observe structure**

---

## 🔧 Ways to contribute

### 1. Change the system

Try:

- mod 7 → mod 11 / 13 / 17  
- primes → random numbers  
- primes → filtered primes (e.g. twin primes)  

👉 Question:

Does the structure survive?

---

### 2. Add a new experiment

Create a new script:

```
scripts/your_experiment.py
```

Examples:

- new modular system
- new embedding (3D, spiral, torus)
- new signal (gap sequence, binary indicator)

---

### 3. Build new visuals

Ideas:

- better flow maps  
- basin detection improvements  
- cycle detection overlays  
- spectral plots (FFT, autocorrelation)  

Save into:

```
analysis/output/plots/
```

---

### 4. Compare against controls

This is critical.

Always test against:

- random integers  
- random odd numbers  
- shuffled primes  

👉 We care about **structure vs baseline**

---

### 5. Detect something new

If you find:

- repeating cycles  
- stable regions  
- unusual clustering  
- spectral peaks  

👉 document it.

Create:

```
RESULT_SUMMARY_*.md
```

---

## 🧪 Rules (important)

- no claims without comparison  
- no interpretation without data  
- no “magic” — only structure  

This is:

- computational  
- reproducible  
- exploratory  

---

## 🧭 Philosophy (optional, but useful)

We are not trying to prove a theory.

We are trying to answer:

> What kind of structure emerges from simple rules?

---

## 🧠 What matters most

Not code quality.  
Not math complexity.

👉 **Observation quality**

Good contributions:

- isolate one variable  
- show before vs after  
- visualize clearly  
- compare to control  

---

## 🚀 Contribution workflow

1. Fork repo  
2. Create branch  
3. Add experiment / visual / result  
4. Open pull request  

Explain:

- what you changed  
- what you observed  
- how it compares to control  

---

## 🔥 Minimal contribution examples

- change mod 7 → mod 11 and post visuals  
- compare primes vs random  
- detect strongest cycle length  
- visualize transition matrix differently  

---

## ❌ What NOT to do

- don’t overinterpret  
- don’t jump to physics claims  
- don’t skip controls  

---

## 🔮 Why this is interesting

We start with:

```
0,1,2,3,4,5,6
```

And get:

- flow  
- cycles  
- basins  
- structure  

👉 That’s the whole game.

---

## 🧠 One sentence

We don’t invent structure —  
we reveal it.

---

Scarabæus1033 · NEXAH
