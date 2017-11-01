#slope_friction_walls.py: A slope failure simulation using quarter

#import the appropriate ESyS-Particle modules:
from esys.lsm import *
from esys.lsm.util import *
from esys.lsm.geometry import *

normalK = 1e-6;


#instantiate a simulation object and
#initialise the neighbour search algorithm:
sim = LsmMpi (numWorkerProcesses = 1, mpiDimList = [1,1,1])
sim.initNeighbourSearch (
particleType = "NRotSphere",
gridSpacing = 9.0000,
verletDist = 0.1000
)

#specify the number of timesteps and the timestep increment:
sim.setNumTimeSteps (10000)
sim.setTimeStepSize (1)

#specify the spatial domain for the simulation:
domain = BoundingBox(Vec3(0,0,0), Vec3(64,240,64))
sim.setSpatialDomain(domain)

#construct a block of particles with radii in range [0.2,0.5]:
geoRandomBlock = RandomBoxPacker(
	minRadius = 4.0000,
	maxRadius = 15.0000,
	cubicPackRadius = 11.0000,
	maxInsertFails = 1000,
	bBox = BoundingBox(
	Vec3(9.0000, 2.0000, 9.0000),
	Vec3(51.0000, 60.0000, 51.0000)
	),
	circDimList = [False, False, False],
	tolerance = 1.0000e-05
	)

geoRandomBlock.generate()
geoRandomBlock_particles = geoRandomBlock.getSimpleSphereCollection()

#add the particles to the simulation object:
sim.createParticles(geoRandomBlock_particles)

#add a wall as a floor for the model:
sim.readMesh(
	fileName = "os_test1.msh",
	meshName = "floor_mesh_wall"
	)

#specify that particles undergo frictional interactions:
sim.createInteractionGroup (
	NRotFrictionPrms (
		name = "friction",
		normalK = normalK,
		dynamicMu = 0.6,
		shearK = normalK/10.0,
		scaling = True
		)
	)

#specify that particles undergo elastic repulsion
#with the floor mesh wall:
sim.createInteractionGroup (
	NRotElasticTriMeshPrms (
		name = "floorWall_repell",
		meshName = "floor_mesh_wall",
		normalK = normalK
		)
	)

#specify the direction and magnitude of gravity:
sim.createInteractionGroup (
	GravityPrms (
		name = "gravity",
		acceleration = Vec3(0.0000, 1e-9, 0.0000)
		)
	)

#add viscosity to damp particle oscillations:
sim.createInteractionGroup (
	LinDampingPrms (
		name = "viscosity",
		viscosity = 0.000001,
		maxIterations = 100
		)
	)

#add a CheckPointer to store simulation data:
sim.createCheckPointer (
	CheckPointPrms (
		fileNamePrefix = "flow_data",
		beginTimeStep = 0,
		endTimeStep = 10000,
		timeStepIncr = 100
		)
	)

#execute the simulation:
sim.run()
