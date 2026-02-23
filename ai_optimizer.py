import numpy as np
from scipy.optimize import differential_evolution
import copy

class TrussOptimizer:
    def __init__(self, base_truss, density=7850, yield_stress=250e6, max_deflection=0.05):
        """
        AI Optimizer for 3D Space Trusses.
        density: Material density in kg/m^3 (Default: Steel = 7850)
        yield_stress: Allowable stress in N/m^2 (Default: 250 MPa)
        max_deflection: Maximum allowable nodal displacement in meters (Default: 50mm)
        """
        # We make a deep copy so the AI can play around without destroying the original UI model
        self.ts = copy.deepcopy(base_truss) 
        self.density = density
        self.yield_stress = yield_stress
        self.max_deflection = max_deflection
        
        # To calculate weight, we need the lengths
        self.lengths = np.array([m.L for m in self.ts.members])

    def objective_function(self, areas):
        """
        The AI's Evaluation Loop: 
        1. Apply the AI's guessed areas.
        2. Solve the truss.
        3. Calculate Weight.
        4. Add massive penalties if stress or deflection fails.
        """
        # 1. Update the truss with the AI's current "genes" (Areas)
        for i, m in enumerate(self.ts.members):
            m.A = areas[i]
            # Must update local stiffness matrix since Area changed
            m.k_global_matrix = (m.E * m.A / m.L) * np.outer(m.T_vector, m.T_vector)
            
        # 2. Solve the system
        try:
            self.ts.solve() # Using the linear solver for speed during 1000s of iterations
        except Exception:
            # If the matrix becomes singular/unstable, return a massive penalty
            return 1e12 
            
        # 3. Calculate Objective (Total Weight of the structure in kg)
        # Weight = Sum(Area * Length * Density)
        weight = np.sum(areas * self.lengths * self.density)
        
        # 4. Constraints & Penalties
        penalty = 0.0
        
        # Check Maximum Deflection Constraint
        if self.ts.U_global is not None:
            max_disp = np.max(np.abs(self.ts.U_global))
            if max_disp > self.max_deflection:
                # Add heavy penalty proportional to how badly it failed
                penalty += 1e9 * (max_disp / self.max_deflection)
                
        # Check Yield Stress Constraint (Stress = Force / Area)
        for i, m in enumerate(self.ts.members):
            stress = abs(m.internal_force) / areas[i]
            if stress > self.yield_stress:
                penalty += 1e9 * (stress / self.yield_stress)
                
        # The AI's final score for this specific design (Lower is better)
        return weight + penalty

    def optimize(self, min_area=0.0001, max_area=0.05, pop_size=15, max_gen=100):
        """
        Runs the Differential Evolution (Genetic Algorithm) to find the optimal areas.
        min_area, max_area: The bounds for the cross-sectional areas in m^2
        """
        num_members = len(self.ts.members)
        
        # Define the lower and upper bounds for each member's area
        bounds = [(min_area, max_area) for _ in range(num_members)]
        
        # Run the SciPy AI Optimizer
        result = differential_evolution(
            self.objective_function, 
            bounds, 
            strategy='best1bin', 
            popsize=pop_size, 
            maxiter=max_gen, 
            tol=0.01, 
            mutation=(0.5, 1.0), 
            recombination=0.7,
            disp=False # Set to True if you want to see console logs
        )
        
        optimized_areas = result.x
        final_weight = np.sum(optimized_areas * self.lengths * self.density)
        
        return optimized_areas, final_weight, result.success
