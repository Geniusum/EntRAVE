# Documentation

![EntRAVE Banner](assets/banner.png)

> For the last version : [**v3**](entrave/v3.py)

## Make a board

To make a board, you must instance the class `Board()`.
There is the arguments to pass in the builder function :
- `entity:Entity` : The main entity instance.
- `thickness:int=10` : The visual articulations thickness in pixels.
- `width:int=40` : The visual members width in pixels.
- `height:int=40` : The visual members height in pixels.
- `width_mul:bool=False` : Decide if members will be affected by `mul_divid`.
- `mul_divid:float=1.5` : The size multiplicator for the number of articulation linked to the member.
- `min_speed:int=1` : The minimum of number of pixel of a member to move in one frame (only in `move` process).
- `max_speed:int=10` : The maximum of number of pixel of a member to move in one frame (only in `move` process).
- `interval_delay:float=1` : The interval delay between every frame (only in `move` process).
- `sync:bool=1` : When a member moves, the others members recursively linked to it will be affected by it movement in factor of the recursive distance.

### Run a simulation

To run a simulation, execute the method `Board().run(process:str="move")` with the argument `process` who will define the process to follow to simulate the entity.
Here is a list of all process you can use :
- `move` : _Default_, For do move the members.
- `static` : For let the members static.
- `edit` : For edit the members positions.
- `editmove` : For edit the members positions at the same time of the members moves.
- `create` : _Not available for now_, For create members and link articulations.
- `fluxes` / `movefluxes` / `editfluxes` / `editmovefluxes` : For activate the informations fluxes in entity.

### Example code

Here is example code with default values.

```py
from entrave.v3 import *

ins = Board(Entity())
ins.run()
```

## Make an entity

To make an entity, you must instance the class `Entity()`.
There is the arguments to pass in the builder function :
- `members:int=6` : The number of members who will be generated.
- `choice:bool=False` : Dicide if the articulations between members will be randomly present or not.
- `only_members:bool=False` : Will don't generates articulations.
- `informations:int=10` : Set the numbers of given informations.
- `inf_evolution:bool=True` : Decide if the informations will be changed randomly when it cross an members.

## Change constants

To change constants, got to the module file, and at begin will be present the constants list, here is the default values :

```py
MAX_WIDTH = 1200 # The width of the board, and the visualizer window
MAX_HEIGHT = 900 # The height of the board, and the visualizer window
MARGE = 40 # The marge of spawn area
MIN_WEIGHT = 0.1
MAX_WEIGHT = 0.9
```