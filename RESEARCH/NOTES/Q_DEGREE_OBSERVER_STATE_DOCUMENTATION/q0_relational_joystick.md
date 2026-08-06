# Q° — The Relational Joystick

## Purpose

This note separates three ideas that had begun to overlap:

1. the quaternion \(q\), which represents an orientation state;
2. the relational operator \(\mathcal Q^\circ\), which selects, weights, or changes orientation;
3. the normalized control coordinate \(\xi_Q\), which describes a position between declared bounds.

The distinction prevents \(Q^\circ\) from being misread as a fifth quaternion component.

---

## 1. Quaternion — The Orientation State

A quaternion is written:

\[
\boxed{
q=a+bi+cj+dk
}
\]

with:

\[
i^2=j^2=k^2=ijk=-1.
\]

The four real components are associated with the basis:

\[
\{1,i,j,k\}.
\]

- \(1\) is the scalar or identity basis element;
- \(i,j,k\) are the three imaginary basis elements;
- the signs \(\pm\) indicate direction or sign along those basis components.

Therefore:

\[
\pm1,\;\pm i,\;\pm j,\;\pm k
\]

do not introduce eight new dimensions. They are signed directions associated with the four basis elements.

### Status

This is established quaternion algebra.

---

## 2. Q° — The Relational Control Operator

To distinguish the NEXAH operator from the quaternion state, use:

\[
\boxed{
\mathcal Q^\circ
}
\]

for the relational control operator.

A general state update may be written:

\[
\boxed{
q_{t+1}
=
\mathcal Q^\circ
\left(
q_t;\,
M,S,T,R,\mathrm{Obs}
\right)
}
\]

where:

- \(q_t\): current orientation state;
- \(M\): maps or representations;
- \(S\): scale;
- \(T\): time or observation window;
- \(R\): regime;
- \(\mathrm{Obs}\): observer or reference system.

This equation does not yet specify a unique physical update law. It states the role of the operator:

\[
\mathcal Q^\circ:
\text{reference configuration}
\longrightarrow
\text{orientation update}.
\]

### Core distinction

\[
\boxed{
q=\text{orientation state}
}
\]

\[
\boxed{
\mathcal Q^\circ=\text{relational joystick}
}
\]

\[
\boxed{
\mathcal Q^\circ\neq\text{fifth quaternion component}
}
\]

### Status

\(\mathcal Q^\circ\) is a NEXAH working operator. A concrete application must define its inputs, output space, transformation rule, and empirical interpretation.

---

## 3. The Five-Leaf View

The visual five-leaf grammar may be written:

\[
\boxed{
\{1,i,j,k\}+\mathcal Q^\circ
}
\]

This is not a five-dimensional quaternion.

It is a diagrammatic architecture:

- four quaternion basis elements;
- one relational controller positioned between them.

The central element does not add another spatial direction. It determines how the available orientation components are read, coupled, weighted, or changed.

> Four basis possibilities. One relational control.

### Status

The quaternion basis is established mathematics. The five-leaf arrangement is a NEXAH visual and operational interpretation.

---

## 4. The Three-Lift Model

Let:

- \(L(t)\): left or lower bound;
- \(R(t)\): right or upper bound;
- \(x(t)\): current belt or control position;
- \(S(t)\): width of the available range.

Assume:

\[
L(t)<R(t)
\]

and:

\[
x(t)\in[L(t),R(t)].
\]

The width or scale is:

\[
\boxed{
S(t)=R(t)-L(t)
}
\]

The position normalized to \([0,1]\) is:

\[
u(t)
=
\frac{x(t)-L(t)}{R(t)-L(t)}.
\]

The centered joystick coordinate is:

\[
\boxed{
\xi_Q(t)
=
2\frac{x(t)-L(t)}{R(t)-L(t)}-1
\in[-1,+1]
}
\]

Thus:

- \(\xi_Q=-1\): one rail or bound;
- \(\xi_Q=0\): the relational midpoint;
- \(\xi_Q=+1\): the opposite rail or bound.

### Interpretation

| Element | Mathematical role |
|---|---|
| Two rails \(L,R\) | Declared bounds |
| Central belt \(x(t)\) | Active channel or transport path |
| Width \(S=R-L\) | Scale or aperture |
| \(\xi_Q\) | Normalized control coordinate |
| \(\mathcal Q^\circ\) | Operator acting from the current relational configuration |

The midpoint is not automatically an objective center. It is the midpoint of the chosen bounds.

### Status

Interval normalization is established mathematics. Its Lift/rail/belt interpretation is a NEXAH model.

---

## 5. Pressure, Weight, and Influence

Pressures or contributions can be represented by weights:

\[
w_i(t)\geq0.
\]

Normalized weights are:

\[
\boxed{
\lambda_i(t)
=
\frac{w_i(t)}
{\sum_jw_j(t)}
}
\]

and:

\[
\sum_i\lambda_i(t)=1.
\]

These weights may modify the relational control without creating new geometric dimensions.

A small contact can therefore have high orientational influence if its weight changes the selected relation. This captures the structural intuition behind the pinky or smallest contact point without claiming that it supplies the largest mechanical force.

### Status

Normalized weighting is established mathematics. Any interpretation as pressure, confidence, grip influence, or force requires a declared measurement model.

---

## 6. Orientation Change

The operator produces or selects an orientation change:

\[
\boxed{
\Delta q_t
=
\mathcal Q^\circ
\left(
q_t;\,
\xi_Q(t),\,
\mathbf w(t),\,
\mathcal C(t)
\right)
}
\]

where \(\mathcal C(t)\) contains the relevant contextual constraints.

A generic update may be expressed:

\[
q_{t+1}
=
\operatorname{Normalize}
\left(
q_t\otimes\Delta q_t
\right),
\]

where \(\otimes\) denotes quaternion multiplication.

This is only a structural template. A concrete rotation update should define whether \(\Delta q_t\) is a finite rotation quaternion, an incremental quaternion, or the exponential of an angular-velocity element.

---

## 7. Lyra — The Tensioned Geometry

Lyra is retained as a visual analogy:

- outer strings or rails define a span;
- a middle channel carries movement;
- tension or pressure changes the effective weighting;
- width defines scale;
- motion modulates the relation.

Lyra is not introduced as an additional mathematical object. It is a readable image for the interaction of bounds, scale, tension, and relational control.

---

## 8. Compact Notation

The full distinction can be frozen in five lines:

\[
\boxed{
q=a+bi+cj+dk
}
\]

\[
\boxed{
\mathcal Q^\circ\neq\text{fifth quaternion component}
}
\]

\[
\boxed{
\mathcal Q^\circ=\text{relational control operator}
}
\]

\[
\boxed{
\xi_Q
=
2\frac{x-L}{R-L}-1
\in[-1,+1]
}
\]

\[
\boxed{
q_{t+1}
=
\operatorname{Normalize}
\left(
q_t\otimes\Delta q_t
\right)
}
\]

---

## 9. Epistemic Status

| Statement | Status |
|---|---|
| \(q=a+bi+cj+dk\) | Established quaternion algebra |
| \(i^2=j^2=k^2=ijk=-1\) | Established quaternion algebra |
| Interval normalization to \([-1,+1]\) | Established mathematics |
| Normalized weighting | Established mathematics |
| Quaternion multiplication for rotation composition | Established mathematics |
| \(\mathcal Q^\circ\) as relational joystick | NEXAH working interpretation |
| Five-leaf arrangement | NEXAH visual grammar |
| Three-Lift model | NEXAH explanatory model |
| Pinky/contact influence | Requires biomechanical measurement |
| Lyra | Visual analogy, not a mathematical claim |

The resulting architecture is:

**Quaternion = state**  
**Four leaves = basis**  
**\(\mathcal Q^\circ\) = joystick**  
**Rails = bounds**  
**Belt = channel**  
**Width = scale**  
**Weights = pressures or contributions**  
**\(\Delta q\) = orientation change**

