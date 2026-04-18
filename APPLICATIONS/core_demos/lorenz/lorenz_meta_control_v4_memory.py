# state-specific mode preference
state_mode_scores = {
    s: {m: 1.0 for m in modes}
    for s in range(N_STATES)
}

# recent reward memory per mode
recent_rewards = {m: [] for m in modes}
recent_window = 25

learning_rate_global = 0.01
learning_rate_state = 0.03

# temporal inertia
last_mode = "none"
stickiness_bonus = 0.10

prev_risk = None


# ==================================================
# 5. MAIN LOOP
# ==================================================

for t in range(steps):

    dx = lorenz(x)
    dx = safe_clip(dx, 50)

    state = compute_symbolic_state(x)
    confidence = compute_confidence(x)

    probs = np.random.dirichlet(np.ones(N_STATES))
    entropy = compute_entropy(probs)

    risk = compute_risk(dx)

    # ==================================================
    # COMBINED MODE SCORE (MEMORY CORE)
    # ==================================================

    combined_scores = {}

    for m in modes:

        # recent reward
        if len(recent_rewards[m]) > 0:
            recent_avg = float(np.mean(recent_rewards[m]))
        else:
            recent_avg = 0.0

        combined = (
            0.35 * global_mode_scores[m]
            + 0.50 * state_mode_scores[state][m]
            + 0.15 * recent_avg
        )

        # temporal stickiness
        if m == last_mode:
            combined += stickiness_bonus

        # context bias (important!)
        if m == "entropy" and entropy > 1.2:
            combined += 0.4

        if m == "uncertainty" and confidence < 0.45:
            combined += 0.4

        if m == "predictive" and abs(x[0]) > 12:
            combined += 0.25

        if m == "stabilize" and 8 < risk < 30:
            combined += 0.25

        if m == "none" and risk < 12 and confidence > 0.75:
            combined += 0.35

        combined_scores[m] = combined

    # ==================================================
    # MODE SELECTION
    # ==================================================

    mode_keys, mode_probs = softmax(combined_scores, temperature=0.5)
    chosen_mode = np.random.choice(mode_keys, p=mode_probs)

    # ==================================================
    # CONTROL LAW
    # ==================================================

    if chosen_mode == "entropy":
        control = -0.60 * dx

    elif chosen_mode == "uncertainty":
        control = -0.40 * dx

    elif chosen_mode == "predictive":
        control = -0.30 * dx

    elif chosen_mode == "stabilize":
        control = -0.20 * dx

    else:
        control = np.zeros(3)

    control = safe_clip(control, 20)

    # ==================================================
    # UPDATE SYSTEM
    # ==================================================

    step_update = (dx + control) * dt
    step_update = safe_clip(step_update, 5)

    x = x + step_update

    # ==================================================
    # LEARNING STEP (KEY)
    # ==================================================

    if prev_risk is not None:

        reward = prev_risk - risk  # positive = improvement

        # global learning
        global_mode_scores[chosen_mode] += learning_rate_global * reward

        # state-aware learning
        state_mode_scores[state][chosen_mode] += learning_rate_state * reward

        # clamp scores
        for m in modes:
            global_mode_scores[m] = float(np.clip(global_mode_scores[m], -2.0, 5.0))
            state_mode_scores[state][m] = float(
                np.clip(state_mode_scores[state][m], -2.0, 5.0)
            )

        # recent memory
        recent_rewards[chosen_mode].append(reward)
        if len(recent_rewards[chosen_mode]) > recent_window:
            recent_rewards[chosen_mode].pop(0)

    prev_risk = risk
    last_mode = chosen_mode

    # ==================================================
    # LOGGING
    # ==================================================

    trajectory.append(x.copy())
    risk_list.append(risk)
    mode_list.append(chosen_mode)
    state_list.append(state)
    confidence_list.append(confidence)
    entropy_list.append(entropy)
    global_score_history.append(global_mode_scores.copy())
    state_score_history.append({s: state_mode_scores[s].copy() for s in range(N_STATES)})


trajectory = np.array(trajectory)


# ==================================================
# 6. PLOTTING
# ==================================================

fig = plt.figure(figsize=(14, 10))

# 3D trajectory
ax1 = fig.add_subplot(221, projection='3d')
ax1.plot(trajectory[:, 0], trajectory[:, 1], trajectory[:, 2], color="cyan")
ax1.set_title("Meta-Control v4 (Memory)")

# XY path
ax2 = fig.add_subplot(222)
ax2.plot(trajectory[:, 0], trajectory[:, 1], color="cyan")
ax2.set_title("XY Path")

# Risk
ax3 = fig.add_subplot(223)
ax3.plot(risk_list, color="red")
ax3.set_title("Risk over Time")

# Mode scores
ax4 = fig.add_subplot(224)
for m in modes:
    ax4.plot([h[m] for h in global_score_history], label=m)

ax4.legend()
ax4.set_title("Global Mode Scores")

plt.tight_layout()
plt.savefig("APPLICATIONS/outputs/lorenz_meta_control_v4_memory.png")
plt.show()


# ==================================================
# 7. STATE MEMORY VISUAL
# ==================================================

fig2, axes = plt.subplots(2, 3, figsize=(14, 8))
axes = axes.flatten()

for s in range(N_STATES):
    ax = axes[s]
    for m in modes:
        ax.plot([h[s][m] for h in state_score_history], label=m)
    ax.set_title(f"State S{s}")
    if s == 0:
        ax.legend(fontsize=8)

plt.tight_layout()
plt.savefig("APPLICATIONS/outputs/lorenz_meta_control_v4_state_memory.png")
plt.show()


# ==================================================
# 8. OUTPUT
# ==================================================

print("\n--- META CONTROL v4 (MEMORY) ---")
print("Mean risk:", np.mean(risk_list))
print("Max risk:", np.max(risk_list))
print("Modes used:", set(mode_list))

print("\nFinal global mode scores:")
for m, s in global_mode_scores.items():
    print(f"{m} → {round(s, 3)}")

print("\nState-specific best modes:")
for s in range(N_STATES):
    best = max(state_mode_scores[s], key=state_mode_scores[s].get)
    print(f"S{s} → {best}")
