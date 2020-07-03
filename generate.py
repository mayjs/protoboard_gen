from KicadModTree import *
import itertools
from argparse import ArgumentParser

def generate(name, width, height, spacing=2.54, rails=False):
    drill = 1
    size = 2
    mod = Footprint(name)
    mod.setDescription(f"A {width}x{height} pad prototyping area footprint with {spacing}mm spacing")
    mod.setTags("Prototyping")

    for x in range(width):
        for y in range(height):
            number = ""
            if x == 0 and (y == 0 or rails):
                number = 1
            elif x == width - 1 and (y == 0 or rails):
                number = 2

            pad = Pad(number=number,
                      type=Pad.TYPE_THT,
                      layers=Pad.LAYERS_THT,
                      at=Vector2D(x*spacing, y*spacing),
                      drill=drill,
                      size=size,
                      shape=Pad.SHAPE_CIRCLE
                  )
            mod.append(pad)
    if rails:
        for x in [0, (width-1)*spacing]:
            for layer in ["F.Cu", "B.Cu"]:
                l = Line(start=[x, 0], end=[x, (height-1)*spacing], layer=layer, width=(size-drill))
                mod.append(l)
    return mod



def main():
    parser = ArgumentParser(description="Generate a prototyping area with to pins and rails")
    parser.add_argument("--width", "-w", type=int, help="Number of pads on the x axis", required=True)
    parser.add_argument("--height", "-H", type=int, help="Number of pads on the y axis", required=True)
    parser.add_argument("--rails", "-r", action="store_true", default=False, help="Add rails on the left and right edge")
    parser.add_argument("--name", "-n", help="The module name", required=True)

    args = parser.parse_args()

    mod = generate(args.name, args.width, args.height, rails=args.rails)
    file_handler = KicadFileHandler(mod)
    file_handler.writeFile(f"{args.name}.kicad_mod")

if __name__ == "__main__":
    main()
