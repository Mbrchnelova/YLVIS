Welcome to YLVIS (pYthon-based consoLe finite-Volume meshIng Software), my meshing library! This library was developed mainly for:
- hypersonic computational fluid dynamics (CFD) simulations
- CFD simulations of the solar chromosphere and solar corona but it can be used by whoever for whatever. Note: this code is an intellectual property of KU Leuven, CmPA.

This is a simple pyton-based meshing program capable of generating GAMBIT neutral mesh files for your CFD simulations for:
- simple, blocked 2D/3D quad-based/ hexa-based domains
- 3D spherical domains, where the surface mesh is provided in the ply format (e.g. from Blender)

For 2D and 3D modelling, in the main_mesher.py, the parameters of the mesh can be regulated under the section ### MAIN PROGRAM GOES HERE. Some basic stretching functions are provided (uniform, hyptng, doubhyptng, get_doubhypsin, get_hypsin), but the user can make their own if they define the appropriate function.

Unless you need blocks specifically, do not use them. The algorithm is still a bit stupid and to connect the blocks, it goes through a double for loop through the elements and nodes to find the nodes intersecting and adjusting the connectivity respectively.

The python file produces an own-formatted file, here with the extension .brch, which is done as an intermediate step since GAMBIT neutral files should be written by fortran, not python. That file can be read by the "write" fortran script provided (also the executable is available), which needs first the following argument

- "2d" or "2D" if the domain is 2D
- "3d" or "3D" if the domain is 3D
- "pr" or "Pr" or "PR" for prisms (discussed later)

and afterwards the path to the own formatted .brch file. The code has been used a lot for 2D domains but not so much for 3D, so if there are bugs, let me know on michaela.brchnelova@kuleuven.be. Also let me know if anything else about the usage is unclear.

To generate a 3D sherical mesh (in the spherical extension folder) for solar coronal modelling, a ply formatted surface file is required, such as the sub_1.ply file shown. This file is linked in the icosphere_pure.py script along with the output directory under the names "name" and "path" respectively. This surface mesh will be used for each layer of the mesh (the layers are stacked one on the top of another radially outwards) with the radial stretching function defined in "Return Spacing". In "n_layer", you should define the number of layers to be stacked. The output file name is set in "file1". This once again creates an intermediate .brch file, to be translated by a fortran write executble - in this case requiring the "pr" argument.

Again, if anything is unclear, let me know.

Also, the code is just a couple of thousands of lines, so going through it might actually be a fast way to get acquinted.

In addition, the code is basically still in development as the applications are growing, so if you want to use it and there are weird messages/ print statements popping up, just contact me and we can figure it out together.

For now, ignore the other files in the repository unless you know what they are for.
