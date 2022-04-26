"""Runs an XFOIL analysis for a given airfoil and flow conditions"""
import os
import subprocess
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

# %% Inputs

airfoil_name = "NACA6409"
alpha_start = 0
alpha_end = 15
alpha_step = 0.5
Re = 10**5
n_iter = 100

# %% XFOIL input file writer 
def run_xfoil(airfoil_name, alpha_start, alpha_end, alpha_step = 1, Re = 10**5, n_iter = 100):
    if os.path.exists("polar_file.txt"):
        os.remove("polar_file.txt")
        
    if os.path.exists("input_file.in"):
        os.remove("input_file.in")
    
    input_file = open("input_file.in", 'w')
    input_file.write("LOAD {0}.dat\n".format(airfoil_name))
    input_file.write(airfoil_name + '\n')
    input_file.write("PANE\n")
    input_file.write("OPER\n")
    input_file.write("Visc {0}\n".format(Re))
    input_file.write("PACC\n")
    input_file.write("polar_file.txt\n\n")
    input_file.write("ITER {0}\n".format(n_iter))
    input_file.write("ASeq {0} {1} {2}\n".format(alpha_start, alpha_end,
                                                 alpha_step))
    input_file.write("\n\n")
    input_file.write("quit\n")
    input_file.close()
    
    print("Executing xfoil ...")
    subprocess.call("xfoil.exe < input_file.in", shell=True)
                    #cwd = os.path.dirname(os.path.abspath(r"./xfoil.exe")))
    #subprocess.Popen("xfoil.exe < input_file.in", 
     #               cwd = os.path.dirname(os.path.abspath(r"./xfoil.exe")), 
      #              shell = False)
    
    print("Calculation ended.")
    
    polar_data = np.loadtxt("polar_file.txt", skiprows=12)
    polar_df = pd.DataFrame(data = polar_data, 
                            columns = ["alpha", "C_l", "C_d", "C_dp", "C_m", "Top_Xtr", "Bot_Xtr"])
    
    polar_df.insert(loc = polar_df.columns.to_list().index("C_d") + 1, column = "C_l/C_d", value = polar_df["C_l"]/polar_df["C_d"])
    return polar_df

def plot_airfoil_performance(airfoil_name, airfoil_data):
    fig, axes = plt.subplots(nrows = 2, ncols = 1, sharex = True, figsize = (17/2.54, 12/2.54))
    plt.suptitle("{} airfoil - performance coefficients".format(airfoil_name))
    axes[0].plot(airfoil_data["alpha"], airfoil_data["C_l"], linestyle = "-.", marker = "^", color = "blue")
    axes[0].plot(airfoil_data["alpha"], airfoil_data["C_d"], linestyle = "--", marker = "v", color = "orange")
    axes[0].legend(["C_l", "C_d"])
    axes[0].grid(which = "major")
    
    axes[1].plot(airfoil_data["alpha"], airfoil_data["C_l"]/airfoil_data["C_d"], linestyle = "-", marker = "d", color = "red")
    axes[1].legend(["glide ratio (C_l/C_d)"])
    axes[1].set_xlabel("attack angle alpha (deg)")
    axes[1].grid(which = "major")
    plt.tight_layout()
    
    return fig

airfoil_data = run_xfoil(airfoil_name, alpha_start, alpha_end, alpha_step = 1)

#f = plot_airfoil_performance(airfoil_name, airfoil_data)

#subprocess.run([command, "xfoil.exe < input_file.in"], shell = True)


