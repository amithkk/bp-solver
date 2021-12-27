import json
from pack_solver import *
from instruction_encode import make_instructions
from pint import UnitRegistry
from visualize import make_visuals

ureg = UnitRegistry()
Q_ = ureg.Quantity

problem_input = None
with open("input.json", "r") as infile:
    problem_input = json.load(infile)


def to_inch(x: str):
    return round(Q_(x).to("inch").to_tuple()[0], 2)


container_dimensions = Dimension(to_inch(problem_input["container"]["l"]),
                                 to_inch(problem_input["container"]["w"]),
                                 to_inch(problem_input["container"]["h"]))

carton_small_dimensions = Dimension(to_inch(problem_input["carton_small"]["l"]),
                                    to_inch(
                                        problem_input["carton_small"]["w"]),
                                    to_inch(problem_input["carton_small"]["h"]))

carton_big_dimensions = Dimension(to_inch(problem_input["carton_big"]["l"]),
                                  to_inch(problem_input["carton_big"]["w"]),
                                  to_inch(problem_input["carton_big"]["h"]))


packer = Packer()
packer.add_container(Container("Container", container_dimensions))
packer.add_boxes(Box("carton_small", carton_small_dimensions,
                 problem_input["carton_small"]["count"]))
packer.add_boxes(Box("carton_big", carton_big_dimensions,
                 problem_input["carton_big"]["count"]))
packing_results = packer.pack()

container = packing_results[0]
boxes = container.solved_boxes

carton_small_count = len(
    list(filter(lambda x: x.name == "carton_small", boxes)))
carton_big_count = len(list(filter(lambda x: x.name == "carton_big", boxes)))
instructions = make_instructions(packing_results[0])
out_payload = {
    "carton_small": carton_small_count,
    "carton_big": carton_big_count,
    "instructions": instructions
}

with open("output.json", "w") as outfile:
    outfile.write(json.dumps(out_payload, indent=4))

with open("viz.json", "w") as outfile:
    outfile.write(json.dumps(make_visuals(packer.containers[0], container), indent=4))

print(
    f"Completed solving with {container.percentage_fill:.2f}% fill. ({100-container.percentage_fill:.2f}% trim loss)")
print(f"Generated {len(instructions)} instructions after simplification.")
print("Find results in output.json")
print("Visualization output created as viz.json")
