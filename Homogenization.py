# This code aims to calculate homogenized property of wire mesh shieldings. 

def Homogenization(permittivity_wire, permeability_wire):

    # Define the properties of the wire and air
    permittivity_air = 1.0 # F/m
    permeability_air = 1.0 # H/m
    
    # permittivity_wire = 1e-10 # F/m (very small value for a perfect conductor)
    # permeability_wire = 1e-10 # H/m (very small value for a perfect conductor)

    # Define the volume fraction of the wire in the wire mesh shield
    f = 0.1 # 10% wire, 90% air

    # Calculate the effective permittivity and permeability of the wire mesh shield
    permittivity_eff = permittivity_air*(1-f) + permittivity_wire*f
    permeability_eff = permeability_air*(1-f) + permeability_wire*f

    #print out the result
    print("Effective permittivity:", permittivity_eff, "F/m")
    print("Effective permeability:", permeability_eff, "H/m")

    return permeability_eff, permittivity_eff

permeability_eff, permittivity_eff = Homogenization(1e-10, 1e-10)