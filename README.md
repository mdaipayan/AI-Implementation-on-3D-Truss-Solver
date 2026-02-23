Here is a comprehensive and professionally structured `README.md` file. It highlights the rigorous mathematical foundation, the advanced AI optimization capabilities, and the pedagogical focus of the application.

You can save this directly as `README.md` in your project folder.

---

```markdown
# 🏗️ Professional Space Truss Analysis (3D)

A state-of-the-art, web-based 3D structural analysis and optimization suite built with Python and Streamlit. This application features a robust Direct Stiffness Method (DSM) solver, geometric non-linear capabilities, and a discrete Evolutionary AI sizing optimizer based on the Indian Standard (IS 800:2007) steel catalog.

Developed by **Daipayan Mandal**, Assistant Professor at KITS Ramtek, this tool is designed for both rigorous engineering design and pedagogical exploration of structural optimization using AI.

---

## ✨ Key Features

* **Advanced 3D Matrix Solver:** Implements the Direct Stiffness Method for 3D space trusses with 3 DOFs per node.
* **Geometric Non-Linearity (P-Δ):** Features an Incremental Newton-Raphson solver utilizing a true-stretch kinematic formulation and updated Lagrangian matrices for large-deflection analysis.
* **Discrete AI Sizing Optimization:** Integrates SciPy's Differential Evolution algorithm to automatically select optimal Indian Standard Equal Angles (ISA) from the SP(6) catalog while minimizing weight and strictly satisfying IS 800 buckling and yield constraints.
* **Educational "Glass-Box" Mode:** Exposes the intermediate mathematical steps of the DSM, displaying local kinematics, global coordinate transformations, stiffness matrix assembly, and degree-of-freedom partitioning in real-time.
* **Interactive 3D Visualizations:** Renders undeformed geometry, load application, and post-analysis free body diagrams (FBD) with color-coded axial forces using Plotly.
* **Professional PDF Reporting:** Compiles formal analysis documentation, including high-resolution 3D plots, nodal displacements, member forces, and AI optimization metrics.

---

## 🧮 Mathematical Foundation

### 1. Linear Elastic Direct Stiffness Method (DSM)
The core linear solver evaluates the equilibrium equation:
$$F = K \cdot U$$
Where the 6x6 global element stiffness matrix for a 3D truss member is defined by its direction cosines ($l, m, n$):
$$k_{global} = \frac{EA}{L} \begin{bmatrix} l^2 & lm & ln & -l^2 & -lm & -ln \\ lm & m^2 & mn & -lm & -m^2 & -mn \\ ln & mn & n^2 & -ln & -mn & -n^2 \\ -l^2 & -lm & -ln & l^2 & lm & ln \\ -lm & -m^2 & -mn & lm & m^2 & mn \\ -ln & -mn & -n^2 & ln & mn & n^2 \end{bmatrix}$$


### 2. Geometric Non-Linearity & Instability
To capture large displacements, the tangent stiffness matrix is iteratively updated across incremental load steps:
$$K_T = K_E + K_G$$
The geometric stiffness matrix ($K_G$) modifies the structural stiffness based on current internal axial forces, effectively modeling tension-stiffening and compression-softening (P-Delta effects).

### 3. AI Sizing Optimization
The AI engine utilizes a metaheuristic evolutionary algorithm (Differential Evolution) to solve the discrete constrained optimization problem:
$$\text{Minimize: } W = \sum_{i=1}^{m} \rho \cdot A_i \cdot L_i + P_v$$
Where $P_v$ is a quadratic penalty function applied when a candidate structure violates IS 800 allowable compressive buckling stresses, tensile yield limits, or user-defined maximum nodal deflections.

---

## 🚀 Installation & Setup

Ensure you have Python 3.9+ installed.

**1. Clone the repository (or download the source files):**
```bash
git clone [https://github.com/yourusername/professional-truss-suite.git](https://github.com/yourusername/professional-truss-suite.git)
cd professional-truss-suite

```

**2. Install the required dependencies:**
Use the provided `requirements.txt` file to install the necessary libraries.

```bash
pip install -r requirements.txt

```

**3. Launch the Application:**
Start the Streamlit web server.

```bash
streamlit run app.py

```

*(Note: If your main file is named differently, replace `app.py` with your file name).*

---

## 📂 Project Structure

* **`app.py`**: The main Streamlit web interface and application logic.
* **`core_solver.py`**: The object-oriented physics engine (`Node`, `Member`, `TrussSystem`). Handles DSM matrix assembly, partitioning, boundary conditions, and Newton-Raphson iterations.
* **`ai_optimizer.py`**: Contains the `TrussOptimizer` class, managing the genetic algorithm, fitness evaluations, IS 800 constraint checks, and penalty scaling.
* **`is_catalog.py`**: An optimized, cached local database of standard Indian Standard Equal Angles (ISA) from the SP(6) handbook.
* **`visualizer.py`**: Helper functions leveraging Plotly to render the interactive 3D geometries and force diagrams.
* **`report_gen.py`**: The document compiler utilizing `fpdf2` to dynamically build and export professional PDF engineering reports.

---

## 📜 License & Credit

This software was developed for academic and professional engineering use.
**Author:** Daipayan Mandal

```

***

Now that the documentation is completely mapped out, would you like me to help draft a `.gitignore` file so you don't accidentally push large PDF reports or Python cache folders (`__pycache__`) to your GitHub repository?

```
