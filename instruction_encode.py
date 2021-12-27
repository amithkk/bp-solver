from pack_solver import *
from itertools import groupby

def rot_instruction(box: SolvedBox):
    rot = box.position.rotation
    if rot == Rotation.ORIGINAL:
        return 'Place'
    else:
        return 'Rotate sideways and place'


def row_reset(x1, y1, z1, x2, y2, z2):
    st = 'on the next row'
    if y2 > y1:
        st = f'{st} on top'
    elif z2 > z1:
        st = f'{st} in front'
    return st


def rel_placement(x1, y1, z1, x2, y2, z2):
    end = 'the previous box'
    if x2 == 0 and x1 != x2:
        return row_reset(x1, y1, z1, x2, y2, z2)
    if x2 > x1:
        return f'to the right of {end}'
    elif x2 < x1:
        return f'to the left of {end}'
    elif y2 > y1:
        return f'above {end}'
    elif y2 < y1:
        return f'below {end}'
    elif z2 < z1:
        return f'in front of {end}'
    elif z2 > z1:
        return f'behind {end}'

def simplify_instructions(instructions: List):
    simplified_instructions = []
    for k, g in groupby(instructions):
        repeat_c = len(list(g))
        if repeat_c == 1:
            simplified_instructions.append(f'{k[0]} {k[1]}')
        else:
            simplified_instructions.append(f'{k[0]} {repeat_c} of {k[1]}')
    return simplified_instructions


def make_instructions(solved_container: SolvedContainer):
    instructions_expanded = []
    for i, box in enumerate(solved_container.solved_boxes): 
        if i == 0:
            instructions_expanded.append(
            [f'To start stacking, {rot_instruction(box)}', f'{box.name} at left-back of container'])
            continue
        prev = solved_container.solved_boxes[i-1]
        px, py, pz = prev.position.x, prev.position.y, prev.position.z
        x, y, z = box.position.x, box.position.y, box.position.z
        instructions_expanded.append(
        [rot_instruction(box), f'{box.name} {rel_placement(px,py,pz,x,y,z)}'])
    return simplify_instructions(instructions_expanded)


