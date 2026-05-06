from __future__ import annotations

import argparse
import xml.etree.ElementTree as ET
from pathlib import Path

BODY_LENGTH = 0.42
BODY_WIDTH = 0.30
BODY_HEIGHT = 0.10
BODY_MASS = 4.0

UPPER_LENGTH = 0.16
UPPER_RADIUS = 0.025
UPPER_MASS = 0.18

LOWER_LENGTH = 0.18
LOWER_RADIUS = 0.020
LOWER_MASS = 0.14

FOOT_RADIUS = 0.028
FOOT_MASS = 0.05

HIP_LIMITS = (-0.9, 0.9)
KNEE_LIMITS = (-1.6, 0.0)
JOINT_EFFORT = 45.0
JOINT_VELOCITY = 10.0

LEG_X = (0.15, 0.00, -0.15)
LEG_Y = (-0.12, 0.00, 0.12)
LEG_Z = -BODY_HEIGHT / 2.0

DEFAULT_OUTPUT = (
    Path(__file__).resolve().parents[1]
    / "source"
    / "nonapod_lab"
    / "nonapod_lab"
    / "assets"
    / "robots"
    / "nonapod"
    / "nonapod.urdf"
)


def box_inertia(mass: float, x: float, y: float, z: float) -> tuple[float, float, float]:
    return (
        mass * (y * y + z * z) / 12.0,
        mass * (x * x + z * z) / 12.0,
        mass * (x * x + y * y) / 12.0,
    )


def cylinder_inertia(mass: float, radius: float, length: float) -> tuple[float, float, float]:
    i_xy = mass * (3.0 * radius * radius + length * length) / 12.0
    i_z = 0.5 * mass * radius * radius
    return (i_xy, i_xy, i_z)


def sphere_inertia(mass: float, radius: float) -> tuple[float, float, float]:
    value = 0.4 * mass * radius * radius
    return (value, value, value)


def add_inertial(
    parent: ET.Element,
    mass: float,
    inertia: tuple[float, float, float],
    xyz: tuple[float, float, float] = (0.0, 0.0, 0.0),
    rpy: tuple[float, float, float] = (0.0, 0.0, 0.0),
) -> None:
    inertial = ET.SubElement(parent, "inertial")
    ET.SubElement(inertial, "origin", xyz=fmt_xyz(xyz), rpy=fmt_xyz(rpy))
    ET.SubElement(inertial, "mass", value=f"{mass:.6f}")
    ET.SubElement(
        inertial,
        "inertia",
        ixx=f"{inertia[0]:.8f}",
        ixy="0.0",
        ixz="0.0",
        iyy=f"{inertia[1]:.8f}",
        iyz="0.0",
        izz=f"{inertia[2]:.8f}",
    )


def add_materials(robot: ET.Element) -> None:
    materials = {
        "body_green": "0.12 0.62 0.42 1.0",
        "leg_gray": "0.70 0.70 0.72 1.0",
        "foot_black": "0.12 0.12 0.12 1.0",
    }
    for name, rgba in materials.items():
        material = ET.SubElement(robot, "material", name=name)
        ET.SubElement(material, "color", rgba=rgba)


def add_box_link(
    robot: ET.Element,
    name: str,
    size: tuple[float, float, float],
    mass: float,
    material_name: str,
) -> None:
    link = ET.SubElement(robot, "link", name=name)
    add_inertial(link, mass, box_inertia(mass, *size))

    visual = ET.SubElement(link, "visual")
    ET.SubElement(visual, "origin", xyz="0 0 0", rpy="0 0 0")
    geometry = ET.SubElement(visual, "geometry")
    ET.SubElement(geometry, "box", size=fmt_xyz(size))
    ET.SubElement(visual, "material", name=material_name)

    collision = ET.SubElement(link, "collision")
    ET.SubElement(collision, "origin", xyz="0 0 0", rpy="0 0 0")
    geometry = ET.SubElement(collision, "geometry")
    ET.SubElement(geometry, "box", size=fmt_xyz(size))


def add_cylinder_link(
    robot: ET.Element,
    name: str,
    length: float,
    radius: float,
    mass: float,
    material_name: str,
) -> None:
    link = ET.SubElement(robot, "link", name=name)
    offset = (0.0, 0.0, -length / 2.0)
    add_inertial(link, mass, cylinder_inertia(mass, radius, length), xyz=offset)

    visual = ET.SubElement(link, "visual")
    ET.SubElement(visual, "origin", xyz=fmt_xyz(offset), rpy="0 0 0")
    geometry = ET.SubElement(visual, "geometry")
    ET.SubElement(geometry, "cylinder", radius=f"{radius:.6f}", length=f"{length:.6f}")
    ET.SubElement(visual, "material", name=material_name)

    collision = ET.SubElement(link, "collision")
    ET.SubElement(collision, "origin", xyz=fmt_xyz(offset), rpy="0 0 0")
    geometry = ET.SubElement(collision, "geometry")
    ET.SubElement(geometry, "cylinder", radius=f"{radius:.6f}", length=f"{length:.6f}")


def add_sphere_link(robot: ET.Element, name: str, radius: float, mass: float, material_name: str) -> None:
    link = ET.SubElement(robot, "link", name=name)
    add_inertial(link, mass, sphere_inertia(mass, radius))

    visual = ET.SubElement(link, "visual")
    ET.SubElement(visual, "origin", xyz="0 0 0", rpy="0 0 0")
    geometry = ET.SubElement(visual, "geometry")
    ET.SubElement(geometry, "sphere", radius=f"{radius:.6f}")
    ET.SubElement(visual, "material", name=material_name)

    collision = ET.SubElement(link, "collision")
    ET.SubElement(collision, "origin", xyz="0 0 0", rpy="0 0 0")
    geometry = ET.SubElement(collision, "geometry")
    ET.SubElement(geometry, "sphere", radius=f"{radius:.6f}")


def add_revolute_joint(
    robot: ET.Element,
    name: str,
    parent_link: str,
    child_link: str,
    origin_xyz: tuple[float, float, float],
    axis_xyz: tuple[float, float, float],
    limits: tuple[float, float],
) -> None:
    joint = ET.SubElement(robot, "joint", name=name, type="revolute")
    ET.SubElement(joint, "parent", link=parent_link)
    ET.SubElement(joint, "child", link=child_link)
    ET.SubElement(joint, "origin", xyz=fmt_xyz(origin_xyz), rpy="0 0 0")
    ET.SubElement(joint, "axis", xyz=fmt_xyz(axis_xyz))
    ET.SubElement(
        joint,
        "limit",
        lower=f"{limits[0]:.6f}",
        upper=f"{limits[1]:.6f}",
        effort=f"{JOINT_EFFORT:.6f}",
        velocity=f"{JOINT_VELOCITY:.6f}",
    )
    ET.SubElement(joint, "dynamics", damping="0.1", friction="0.01")


def add_fixed_joint(
    robot: ET.Element,
    name: str,
    parent_link: str,
    child_link: str,
    origin_xyz: tuple[float, float, float],
) -> None:
    joint = ET.SubElement(robot, "joint", name=name, type="fixed")
    ET.SubElement(joint, "parent", link=parent_link)
    ET.SubElement(joint, "child", link=child_link)
    ET.SubElement(joint, "origin", xyz=fmt_xyz(origin_xyz), rpy="0 0 0")


def fmt_xyz(values: tuple[float, float, float]) -> str:
    return " ".join(f"{value:.6f}" for value in values)


def build_nonapod() -> ET.ElementTree:
    robot = ET.Element("robot", name="nonapod")
    add_materials(robot)
    add_box_link(robot, "base_link", (BODY_LENGTH, BODY_WIDTH, BODY_HEIGHT), BODY_MASS, "body_green")

    leg_index = 0
    for x in LEG_X:
        for y in LEG_Y:
            upper_link = f"leg_{leg_index}_upper"
            lower_link = f"leg_{leg_index}_lower"
            foot_link = f"leg_{leg_index}_foot"

            add_cylinder_link(robot, upper_link, UPPER_LENGTH, UPPER_RADIUS, UPPER_MASS, "leg_gray")
            add_cylinder_link(robot, lower_link, LOWER_LENGTH, LOWER_RADIUS, LOWER_MASS, "leg_gray")
            add_sphere_link(robot, foot_link, FOOT_RADIUS, FOOT_MASS, "foot_black")

            add_revolute_joint(
                robot=robot,
                name=f"leg_{leg_index}_hip_joint",
                parent_link="base_link",
                child_link=upper_link,
                origin_xyz=(x, y, LEG_Z),
                axis_xyz=(0.0, 1.0, 0.0),
                limits=HIP_LIMITS,
            )
            add_revolute_joint(
                robot=robot,
                name=f"leg_{leg_index}_knee_joint",
                parent_link=upper_link,
                child_link=lower_link,
                origin_xyz=(0.0, 0.0, -UPPER_LENGTH),
                axis_xyz=(0.0, 1.0, 0.0),
                limits=KNEE_LIMITS,
            )
            add_fixed_joint(
                robot=robot,
                name=f"leg_{leg_index}_foot_joint",
                parent_link=lower_link,
                child_link=foot_link,
                origin_xyz=(0.0, 0.0, -LOWER_LENGTH),
            )
            leg_index += 1

    tree = ET.ElementTree(robot)
    ET.indent(tree, space="  ")
    return tree


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate the nonapod URDF.")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="Path to the generated URDF file.")
    args = parser.parse_args()

    args.output.parent.mkdir(parents=True, exist_ok=True)
    tree = build_nonapod()
    tree.write(args.output, encoding="utf-8", xml_declaration=True)
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
