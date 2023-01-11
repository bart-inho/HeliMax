# This code aims to calculate homogenized property of wire mesh shieldings. 

def Homogenization(permittivity_wire, permeability_wire):

    epsilon_0 = 8.8541878128e-12
    mu_0 = 1.25663706212e-6
    # Define the properties of the wire and air
    permittivity_air = 1.0 # F/m
    permeability_air = 1.0 # H/m
    
    # permittivity_wire = 1e-10 # F/m (very small value for a perfect conductor)
    # permeability_wire = 1e-10 # H/m (very small value for a perfect conductor)

    # Define the volume fraction of the wire in the wire mesh shield
    f = 0.2 # 10% wire, 90% air

    # Calculate the effective permittivity and permeability of the wire mesh shield
    permittivity_eff = permittivity_air*(1-f) + permittivity_wire*f
    permeability_eff = permeability_air*(1-f) + permeability_wire*f

    #print out the result
    print("Effective permittivity:", permittivity_eff, "F/m")
    print("Effective permeability:", permeability_eff, "H/m")

    wire_permittivity = permittivity_eff/epsilon_0
    wire_permeability = permeability_eff/mu_0

    print('Relative permittivity:', wire_permittivity, 'F/m')
    print('Relative permeability:', wire_permeability, 'H/m')

    return wire_permittivity, wire_permeability