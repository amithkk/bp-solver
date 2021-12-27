from pack_solver import Container, SolvedContainer, Rotation

def make_visuals(container: Container, solution: SolvedContainer):
    itm_arr = []
    for i, box in enumerate(solution.solved_boxes):
        itm_arr.append({
            "i": i,
            "w": int(box.dimensions.l),
            "h": int(box.dimensions.w),
            "d": int(box.dimensions.h),
            "x": int(box.position.x),
            "y": int(box.position.y),
            "z": int(box.position.z),
            "r": 1 if box.position.rotation == Rotation.SIDEWAYS else 0
        })
    json_o = {
        "box": [
            {
                "w": container.dimensions.l,
                "h": container.dimensions.w,
                "d": container.dimensions.h,
                "tl": 100 - solution.percentage_fill,
                "f": 1,
                "items": itm_arr
            }
        ]
    }

    return json_o
