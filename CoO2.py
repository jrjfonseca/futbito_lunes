from mp_api.client import MPRester

#### COO2 CALCULATIONS #####
with MPRester(api_key="sorNeGqPKtHSyd4u8o9ODl9Em96eJDJT") as mpr:
    tasks_doc = mpr.materials.tasks.search(
            ["mp-2049438"],           # task_id of this calculation
            fields=["task_id", "orig_inputs", "calcs_reversed", "output", "last_updated"]
        )
    
    # Extract data from the first (and only) task document
    if tasks_doc:
        task = tasks_doc[0]
        
        # Get the final energy from the output
        final_energy = task.output.energy
        
        # Get the number of atoms from the structure
        structure = task.output.structure
        num_atoms = len(structure)
        
        # Calculate energy per atom
        energy_per_atom = final_energy / num_atoms
        
        # Store CoO2 energy and number of atoms
        CoO2_energy = final_energy
        CoO2_num_atoms = num_atoms
        
        # Display the results
        print("=== CoO2 Results ===")
        print(f"Task ID: {task.task_id}")
        print(f"Final Energy: {final_energy:.6f} eV")
        print(f"Number of Atoms: {num_atoms}")
        print(f"Energy per Atom: {energy_per_atom:.6f} eV/atom")
        print()
    else:
        print("No task found for CoO2")
        CoO2_energy = None
        CoO2_num_atoms = None

##### CO CALCULATIONS #####

with MPRester(api_key="sorNeGqPKtHSyd4u8o9ODl9Em96eJDJT") as mpr:
    tasks_doc = mpr.materials.tasks.search(
            ["mp-2019009"],           # task_id of this calculation
            fields=["task_id", "orig_inputs", "calcs_reversed", "output", "last_updated"]
        )
    
    # Extract data from the first (and only) task document
    if tasks_doc:
        task = tasks_doc[0]
        
        # Get the final energy from the output
        final_energy = task.output.energy
        
        # Get the number of atoms from the structure
        structure = task.output.structure
        num_atoms = len(structure)
        
        # Calculate energy per atom
        energy_per_atom = final_energy / num_atoms
        
        # Store Co energy and number of atoms
        Co_energy = final_energy
        Co_num_atoms = num_atoms
        
        # Display the results
        print("=== Co Results ===")
        print(f"Task ID: {task.task_id}")
        print(f"Final Energy: {final_energy:.6f} eV")
        print(f"Number of Atoms: {num_atoms}")
        print(f"Energy per Atom: {energy_per_atom:.6f} eV/atom")
        print()
    else:
        print("No task found for Co")
        Co_energy = None
        Co_num_atoms = None

##### O2 CALCULATIONS #####

with MPRester(api_key="sorNeGqPKtHSyd4u8o9ODl9Em96eJDJT") as mpr:
    tasks_doc = mpr.materials.tasks.search(
            ["mp-1933400"],           # task_id of this calculation
            fields=["task_id", "orig_inputs", "calcs_reversed", "output", "last_updated"]
        )
    
    # Extract data from the first (and only) task document
    if tasks_doc:
        task = tasks_doc[0]
        
        # Get the final energy from the output
        final_energy = task.output.energy
        
        # Get the number of atoms from the structure
        structure = task.output.structure
        num_atoms = len(structure)
        
        # Calculate energy per atom
        energy_per_atom = final_energy / num_atoms
        
        # Store O2 energy and number of atoms
        O2_energy = final_energy
        O2_num_atoms = num_atoms
        
        # Display the results
        print("=== O2 Results ===")
        print(f"Task ID: {task.task_id}")
        print(f"Final Energy: {final_energy:.6f} eV")
        print(f"Number of Atoms: {num_atoms}")
        print(f"Energy per Atom: {energy_per_atom:.6f} eV/atom")
        print()
    else:
        print("No task found for O2")
        O2_energy = None
        O2_num_atoms = None

##### FORMATION ENERGY CALCULATION #####

if (CoO2_energy is not None and Co_energy is not None and O2_energy is not None and 
    CoO2_num_atoms is not None and Co_num_atoms is not None and O2_num_atoms is not None):
    # Get number of atoms in each structure to determine normalization
    # We need to get the number of atoms from each calculation
    
    # For proper formation energy calculation per atom of CoO2:
    # CoO2 has 12 atoms total: 4 Co + 8 O
    # Stoichiometry: Co + O2 → CoO2 (1 Co + 2 O → 1 CoO2 formula unit)
    
    # Normalize energies per atom based on stoichiometry in CoO2
    n_Co_in_CoO2 = 4  # 4 Co atoms in 12-atom CoO2 cell
    n_O_in_CoO2 = 8   # 8 O atoms in 12-atom CoO2 cell
    total_atoms_CoO2 = 12
    
    # CoO2 energy per atom
    CoO2_energy_per_atom = CoO2_energy / CoO2_num_atoms
    
    # Calculate energy per atom for each constituent
    Co_energy_per_atom = Co_energy / Co_num_atoms
    O2_energy_per_atom = O2_energy / O2_num_atoms
    
    # Co contribution: energy per atom × fraction of Co atoms in CoO2
    Co_contribution = Co_energy_per_atom * (n_Co_in_CoO2 / total_atoms_CoO2)
    
    # O2 contribution: energy per atom × fraction of O atoms in CoO2  
    O2_contribution = O2_energy_per_atom * (n_O_in_CoO2 / total_atoms_CoO2)
    
    # Formation energy per atom of CoO2
    formation_energy_per_atom = CoO2_energy_per_atom - Co_contribution - O2_contribution
    
    print("=== Formation Energy Calculation ===")
    print("Reaction: Co + O2 → CoO2")
    print(f"CoO2 unit cell: {total_atoms_CoO2} atoms ({n_Co_in_CoO2} Co + {n_O_in_CoO2} O)")
    print()
    print("Energies:")
    print(f"E(CoO2) total = {CoO2_energy:.6f} eV ({CoO2_num_atoms} atoms)")
    print(f"E(CoO2) per atom = {CoO2_energy_per_atom:.6f} eV/atom")
    print(f"E(Co) total = {Co_energy:.6f} eV ({Co_num_atoms} atoms)")
    print(f"E(Co) per atom = {Co_energy_per_atom:.6f} eV/atom")
    print(f"E(O2) total = {O2_energy:.6f} eV ({O2_num_atoms} atoms)")
    print(f"E(O2) per atom = {O2_energy_per_atom:.6f} eV/atom")
    print()
    print("Normalized contributions:")
    print(f"Co contribution = {Co_energy_per_atom:.6f} eV/atom × ({n_Co_in_CoO2}/{total_atoms_CoO2}) = {Co_contribution:.6f} eV/atom")
    print(f"O2 contribution = {O2_energy_per_atom:.6f} eV/atom × ({n_O_in_CoO2}/{total_atoms_CoO2}) = {O2_contribution:.6f} eV/atom")
    print()
    print("Formation energy per atom of CoO2:")
    print(f"ΔH_f = E(CoO2)/atom - E(Co)/atom×({n_Co_in_CoO2}/{total_atoms_CoO2}) - E(O2)/atom×({n_O_in_CoO2}/{total_atoms_CoO2})")
    print(f"ΔH_f = {CoO2_energy_per_atom:.6f} - {Co_contribution:.6f} - {O2_contribution:.6f}")
    print(f"ΔH_f = {formation_energy_per_atom:.6f} eV/atom")
    print(f"ΔH_f = {formation_energy_per_atom * 1000:.2f} meV/atom")
else:
    print("Cannot calculate formation energy - missing energy data for one or more compounds")