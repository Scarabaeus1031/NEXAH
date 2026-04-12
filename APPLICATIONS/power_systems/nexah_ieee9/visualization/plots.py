import matplotlib.pyplot as plt

def plot_all(lambdas, Vmin, c, dc, d2c, fragmentation,
             distance, residual, states):
    
    fig, axs = plt.subplots(4, 1, figsize=(10, 14))
    
    # --- Panel 1 ---
    axs[0].plot(lambdas, Vmin)
    axs[0].set_title("Voltage Collapse (Baseline)")
    
    # --- Panel 2 ---
    axs[1].plot(lambdas, c, label="c")
    axs[1].plot(lambdas, d2c, label="d2c")
    axs[1].plot(lambdas, fragmentation, label="frag")
    axs[1].legend()
    
    # --- Panel 3 ---
    axs[2].scatter(distance, residual, c=lambdas)
    axs[2].set_title("Residual vs Distance")
    
    # --- Panel 4 ---
    colors = {"SAFE":"green","WARNING":"orange","CRITICAL":"red","TRANSIENT":"gray"}
    
    for i in range(len(lambdas)):
        axs[3].scatter(lambdas[i], 0, color=colors[states[i]])
    
    axs[3].set_title("NEXAH Decision Timeline")
    
    plt.tight_layout()
    plt.show()
