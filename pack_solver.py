from dataclasses import dataclass
from typing import List
from enum import Enum
import requests
import json



class Rotation(Enum): 
    ORIGINAL = 1
    SIDEWAYS = 2
    FRONT = 3


@dataclass
class Dimension:
    l: float
    w: float
    h: float


@dataclass
class Position:
    x: float
    y: float
    z: float
    rotation: Rotation

@dataclass
class Container:
    name: str
    dimensions: Dimension

@dataclass
class Box:
    name: str
    dimensions: Dimension
    copies: int

@dataclass
class SolvedBox:
    name: str
    dimensions: Dimension
    position: Position

@dataclass
class SolvedContainer:
    name: str
    percentage_fill: int
    solved_boxes: List[SolvedBox]

class Packer:
    containers: List[Container] = []
    boxes: List[Box] = []
    solved_containers: List[SolvedContainer] = []

    def add_container(self, container: Container):
        self.containers.append(container)

    def add_boxes(self, box: Box):
        self.boxes.append(box)

    def pack(self):
        url = "https://xserver2-dashboard.cloud.ptvgroup.com/services/rs/XLoad/experimental/packBins"
        items_payload = []
        bins_payload = []
        for box in self.boxes:
            items_payload.append({
                "id": box.name,
                "numberOfItems": box.copies,
                "dimensions": {
                    "x": box.dimensions.l,
                    "y": box.dimensions.w,
                    "z": box.dimensions.h
                },
                "weight": 1
            })
        
        for container in self.containers:
            bins_payload.append({
                "id": container.name,
                "numberOfBins": 1,
                "dimensions": {
                    "x": int(container.dimensions.l),
                    "y": int(container.dimensions.w),
                    "z": int(container.dimensions.h)
                },
                "maximumWeightCapacity": 79999
            })

        payload = json.dumps({
            "bins": bins_payload,
            "items": items_payload,
            "options": {
                "focus": "REDUCE_LOADING_METERS",
                "unloadingSequence": [],
                "stackingOptions": {
                    "stackingRestrictions": []
                }
            }
        })
        headers = {
            'Referer': 'https://xserver2-dashboard.cloud.ptvgroup.com/dashboard/Content/Resources/showcases/LoadingOptimization/InteractiveVisualization/index.html',
            'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        
        decoded_resp = response.json()

        for packed_bin in decoded_resp["packedBins"]:
            solved_boxes = []

            for item in packed_bin["packedItems"]:
                orientation = Rotation.ORIGINAL
                if item["orientation"] == "X":
                    orientation = Rotation.SIDEWAYS
                elif item["orientation"] == "XY":
                    orientation = Rotation.FRONT
                solved_box = SolvedBox(item["itemTypeId"], 
                Dimension(item["dimensions"]["x"], item["dimensions"]["y"], item["dimensions"]["z"]), 
                Position(item["position"]["x"], item["position"]["y"], item["position"]["z"], orientation ))

                solved_boxes.append(solved_box)

            solved_container = SolvedContainer(
                packed_bin["binTypeId"], packed_bin["usedVolumeCapacity"], solved_boxes)
            
            self.solved_containers.append(solved_container)

        return self.solved_containers



