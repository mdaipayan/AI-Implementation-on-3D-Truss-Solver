import os
import subprocess
import tempfile
import datetime
import pandas as pd

def generate_pdf_report(ts_solved, opt_data=None, fig_base=None, fig_res=None, scale_factor=1000.0, unit_label="kN"):
    """
    Generates a professional PDF report via pdflatex.
    opt_data: dictionary containing 'sections', 'orig_weight', 'final_weight'
    """
    temp_dir = tempfile.mkdtemp()
    tex_path = os.path.join(temp_dir, "report.tex")
    pdf_path = os.path.join(temp_dir, "report.pdf")
    
    # 1. Export Plotly Figures to PNG using Kaleido
    base_img_path = os.path.join(temp_dir, "geometry.png")
    res_img_path = os.path.join(temp_dir, "results.png")
    
    if fig_base:
        fig_base.write_image(base_img_path, engine="kaleido", width=1000, height=700, scale=2)
    if fig_res:
        fig_res.write_image(res_img_path, engine="kaleido", width=1000, height=700, scale=2)

    # 2. Begin LaTeX Document Construction
    tex = r"""\documentclass[11pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage{geometry}
\geometry{margin=1in}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{longtable}
\usepackage{xcolor}
\usepackage{float}
\usepackage{hyperref}

\title{\textbf{Professional 3D Space Truss Analysis \\ \& AI Optimization Report}}
\author{\textbf{Mr. D Mandal} \\ \textit{Assistant Professor, Department of Civil Engineering} \\ \textit{KITS Ramtek}}
\date{""" + datetime.date.today().strftime("%B %d, %Y") + r"""}

\begin{document}
\maketitle

\section{Structural Visualization}
"""
    # Insert Geometry Image
    if fig_base:
        tex += r"""
\begin{figure}[H]
    \centering
    \includegraphics[width=0.85\textwidth]{geometry.png}
    \caption{Undeformed 3D Truss Geometry}
\end{figure}
"""
    # Insert Results Image
    if fig_res:
        tex += r"""
\begin{figure}[H]
    \centering
    \includegraphics[width=0.85\textwidth]{results.png}
    \caption{Structural Forces and Reactions Diagram}
\end{figure}
"""

    # 3. Static Results Section
    tex += r"""
\section{Linear Static Analysis Results}
\subsection{Nodal Displacements}
\begin{longtable}{cccc}
\toprule
\textbf{Node ID} & \textbf{Ux (m)} & \textbf{Uy (m)} & \textbf{Uz (m)} \\
\midrule
\endhead
"""
    for node in ts_solved.nodes:
        ux = ts_solved.U_global[node.dofs[0]] if ts_solved.U_global is not None else 0
        uy = ts_solved.U_global[node.dofs[1]] if ts_solved.U_global is not None else 0
        uz = ts_solved.U_global[node.dofs[2]] if ts_solved.U_global is not None else 0
        tex += f"{node.id} & {ux:.6e} & {uy:.6e} & {uz:.6e} \\\\\n"
    
    tex += r"""\bottomrule
\end{longtable}

\subsection{Internal Axial Forces}
\begin{longtable}{cccc}
\toprule
\textbf{Member} & \textbf{Nodes} & \textbf{Axial Force (""" + unit_label + r""")} & \textbf{Nature} \\
\midrule
\endhead
"""
    for m in ts_solved.members:
        force = m.internal_force / scale_factor
        nature = "Tension" if force > 1e-6 else ("Compression" if force < -1e-6 else "Zero Force")
        color = r"\textcolor{blue}" if force > 1e-6 else (r"\textcolor{red}" if force < -1e-6 else r"\textcolor{gray}")
        tex += f"M{m.id} & {m.node_i.id} - {m.node_j.id} & {color}{{{abs(force):.2f}}} & {color}{{{nature}}} \\\\\n"
    
    tex += r"""\bottomrule
\end{longtable}
"""

    # 4. AI Optimization Section (If Data Exists)
    if opt_data and 'sections' in opt_data:
        orig_wt = opt_data.get('orig_weight', 0)
        final_wt = opt_data.get('final_weight', 0)
        saved = orig_wt - final_wt
        pct = (saved / orig_wt * 100) if orig_wt > 0 else 0
        
        tex += r"""
\section{IS 800 Discrete AI Optimization}
\subsection{Optimization Metrics}
\begin{itemize}
    \item \textbf{Original Steel Weight:} """ + f"{orig_wt:.2f} kg" + r"""
    \item \textbf{Optimized Steel Weight:} """ + f"{final_wt:.2f} kg" + r"""
    \item \textbf{Material Saved:} """ + f"{saved:.2f} kg ({pct:.1f}\%)" + r"""
\end{itemize}

\subsection{Final IS 800 Assigned Sections}
\begin{longtable}{cc}
\toprule
\textbf{Member ID} & \textbf{Optimized Section (SP 6)} \\
\midrule
\endhead
"""
        for m_id, sec in opt_data['sections'].items():
            tex += f"M{m_id} & {sec} \\\\\n"
            
        tex += r"""\bottomrule
\end{longtable}
"""

    tex += r"\end{document}"

    # 5. Write to .tex file
    # Replace backslashes in Windows paths if necessary, but writing raw text is safe
    with open(tex_path, 'w', encoding='utf-8') as f:
        f.write(tex)

    # 6. Compile using pdflatex
    # -interaction=nonstopmode ensures it doesn't freeze waiting for user input on minor warnings
    try:
        subprocess.run(['pdflatex', '-interaction=nonstopmode', 'report.tex'], cwd=temp_dir, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        # Run twice for proper table alignment and referencing
        subprocess.run(['pdflatex', '-interaction=nonstopmode', 'report.tex'], cwd=temp_dir, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        raise RuntimeError("pdflatex compilation failed. Ensure TeX Live / MiKTeX is installed and in your system PATH.")

    # 7. Read the generated PDF into memory
    with open(pdf_path, 'rb') as f:
        pdf_data = f.read()

    return pdf_data
