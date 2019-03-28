# -*- coding: utf-8 -*-

th = {}

th['gov'] = """ The partial differential equation (PDE) governing one-dimensional fluid flow in a porous medium is given by
$$
\\frac{\partial u}{\partial t} - c_v \\frac{\partial^2 u}{\partial z^2} = 0
$$
where \( u \) is the pore fluid pressure, \( t \)  stands for time, \( z \) represents depth and \( c_v \) is the coefficient of consolidation which can be expressed as
$$
c_v = \\frac{k}{m_v \gamma}
$$
with \( k \) being the hydraulic conductivity, \( m_v \) the coefficient of volumetric compressibility and \( \gamma \) the unit weight of the fluid. From known elastic parameters of the porous medium, \( m_v \) can be calculated as
$$
m_v = \\frac{(1+\\nu) (1-2\\nu)}{E (1-\\nu)}
$$
where \( E \) is the Young's modulus and \( \\nu \) is the Poisson's ratio of the porous medium. Thus, the coefficient of consolidation can be calculated for a known hydraulic conductivity and elastic parameters."""

th['ana'] = """
The analytical solution of the PDE is
$$ 
\\frac{u(t,z)}{u_o} = \\frac{4}{\pi} \sum_{i=1}^\infty
\\frac{{(-1)}^{i-1}}{2i-1} \exp{\left[ -{(2i-1)}^2 \\frac{\pi^2 T}{4} \\right]}
\cos{\left[ (2i-1) \\frac{\pi z}{2h} \\right]} 
$$
where \( u_o \) is the initial excess pore pressure, \( h \) is the drainage height and \( T \) is the dimensionless time defined in terms of the coefficient of consolidation and the real time as
$$
T = \\frac{c_v t}{h^2}
$$
If both boundaries are drained, \( h=0.5H \) and if only one boundary is drained, \( h=H \), where \( H \) is the height of the model.
"""

th['deg'] = """
The degree of consolidation \( U \), expressed in percentage, indicates the level of consolidation achieved at a given time with respect to what is achievable for a given stress condition. The analytical solution for \( U \) is given by
$$
U = 1 - \\frac{8}{\pi^2} \sum_{i=1}^\infty \\frac{1}{(2i-1)^2}  \exp{\left[ -{(2i-1)}^2 \\frac{\pi^2 T}{4} \\right]} 
$$
"""