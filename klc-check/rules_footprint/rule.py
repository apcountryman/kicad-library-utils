import math
import os
import sys
from typing import Any, Dict

common = os.path.abspath(
    os.path.join(os.path.dirname(__file__), os.path.pardir, "common")
)

if common not in sys.path:
    sys.path.insert(0, common)

from kicad_mod import KicadMod
from rulebase import KLCRuleBase


def mapToGrid(dimension: float, grid: float) -> float:
    return round(dimension / grid) * grid


# Convert mm to microns
def mmToNanoMeter(mm: float) -> float:
    return round(mm * 1e6)


def getStartPoint(graph: Dict[str, Any]):
    if "center" in graph:
        return graph["end"]
    elif "angle" in graph:
        # do some magic to find the actual start point
        # fetch values
        x_c = graph["start"]["x"]
        y_c = graph["start"]["y"]
        x_e = graph["end"]["x"]
        y_e = graph["end"]["y"]
        a_arc = graph["angle"]
        # calculate radius
        dx = x_c - x_e
        dy = y_c - y_e
        r = math.hypot(dx, dy)
        # calculate vector of length 1 of the end point
        dx_s = dx / r
        dy_s = dy / r
        # now get the angle of the end point
        a = math.degrees(math.atan2(dy_s, dx_s))
        a_s = math.radians(a + a_arc)
        x_s = x_c - math.cos(a_s) * r
        y_s = y_c - math.sin(a_s) * r
        return {"x": x_s, "y": y_s}
    elif "start" in graph:
        return graph["start"]
    else:
        return None


def getEndPoint(graph: Dict[str, Any]):
    if "end" in graph:
        return graph["end"]
    else:
        return None


# Display string for a graph item
# Line / Arc / Circle
def graphItemString(
    graph: Dict[str, Any], layer: bool = False, width: bool = False
) -> str:

    layerText = ""
    shapeText = ""
    widthText = ""

    try:
        if layer:
            layerText = " on layer '{layer}'".format(layer=graph["layer"])

        if width:
            widthText = " has width '{width}'".format(width=graph["width"])
    except KeyError:
        pass

    # Line or Arc
    if "start" in graph and "end" in graph:
        # Arc item
        if "angle" in graph:
            shape = "Arc"
        else:
            shape = "Line"
        shapeText = "{shape} ({x1},{y1}) -> ({x2},{y2})".format(
            shape=shape,
            x1=graph["start"]["x"],
            y1=graph["start"]["y"],
            x2=graph["end"]["x"],
            y2=graph["end"]["y"],
        )

    # Circle
    elif "center" in graph and "end" in graph:
        shapeText = "Circle @ ({x},{y})".format(
            x=graph["center"]["x"], y=graph["center"]["y"]
        )

    # Unknown shape
    else:
        shapeText = "Graphical item"

    return shapeText + layerText + widthText


class KLCRule(KLCRuleBase):
    """
    A base class to represent a KLC rule
    """

    def __init__(self, module: KicadMod, args):

        super().__init__()

        self.module: KicadMod = module
        self.args = args
        self.needsFixMore: bool = False

        # Illegal chars
        self.illegal_chars = ["*", "?", ":", "/", "\\", "[", "]", ";", "|", "=", ","]

    def fix(self) -> None:
        self.info("fix not supported")

    def fixmore(self) -> None:
        if self.needsFixMore:
            self.info("fixmore not supported")
