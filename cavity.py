# Generic imports
import math
import progress.bar

# Custom imports
from lattice_utils import *

###############################################
### LBM lid-driven cavity
###############################################

### Free parameters
Re_lbm      = 100.0
u_lbm       = 0.03
L_lbm       = 200
t_max       = 20.0

# Deduce other parameters
Cs          = 1.0/math.sqrt(3.0)
nx          = L_lbm
nu_lbm      = u_lbm*L_lbm/Re_lbm
tau_lbm     = 0.5 + nu_lbm/(Cs**2)
rho_lbm     = 1.0
dt          = Re_lbm*nu_lbm/L_lbm**2
it_max      = math.floor(t_max/dt)

# Other parameters
output_freq = 500
dpi         = 200

# Initialize lattice
lattice = Lattice(nx      = nx,
                  dx      = 1.0/nx,
                  dt      = dt,
                  tau_lbm = tau_lbm,
                  Re_lbm  = Re_lbm,
                  u_lbm   = u_lbm,
                  L_lbm   = L_lbm,
                  nu_lbm  = nu_lbm,
                  rho_lbm = rho_lbm,
                  dpi     = dpi)

# Initialize fields
lattice.set_cavity(u_lbm)
lattice.rho *= rho_lbm

# Set initial distributions
lattice.equilibrium()
lattice.g = lattice.g_eq.copy()

# Solve
bar = progress.bar.Bar('Solving...', max=it_max)
for it in range(it_max+1):

    # Compute macroscopic fields
    lattice.macro()

    # Output field
    lattice.output_fields(it,
                          output_freq,
                          u_norm   = True,
                          u_stream = False)

    # Compute equilibrium state
    lattice.equilibrium()

    # Collisions
    lattice.trt_collisions()

    # Streaming
    lattice.stream()

    # Boundary conditions
    lattice.zou_he_bottom_wall_velocity()
    lattice.zou_he_left_wall_velocity()
    lattice.zou_he_right_wall_velocity()
    lattice.zou_he_top_wall_velocity()
    lattice.zou_he_bottom_left_corner()
    lattice.zou_he_top_left_corner()
    lattice.zou_he_top_right_corner()
    lattice.zou_he_bottom_right_corner()

    lx = lattice.lx
    ly = lattice.ly

    if(any(lattice.g[1, 0,  :] == -1.0)): print('stop')
    if(any(lattice.g[2, lx, :]  == -1.0)): print('stop')
    if(any(lattice.g[3, :,  0]  == -1.0)): print('stop')
    if(any(lattice.g[4, :,  ly] == -1.0)): print('stop')
    if(any(lattice.g[5, 0,  :]  == -1.0)): print('stop')
    if(any(lattice.g[5, :,  0]  == -1.0)): print('stop')
    if(any(lattice.g[6, lx, :]  == -1.0)): print('stop')
    if(any(lattice.g[6, :,  ly] == -1.0)): print('stop')
    if(any(lattice.g[7, lx, :]  == -1.0)): print('stop')
    if(any(lattice.g[7, :,  0]  == -1.0)): print('stop')
    if(any(lattice.g[8, 0,  :]  == -1.0)): print('stop')
    if(any(lattice.g[8, :,  ly] == -1.0)): print('stop')

    # Increment bar
    bar.next()

# End bar
bar.finish()

# Output error with exact solution
lattice.cavity_error(u_lbm)

# Output streamlines
lattice.output_fields(1, 1,
                      u_norm   = False,
                      u_stream = True)