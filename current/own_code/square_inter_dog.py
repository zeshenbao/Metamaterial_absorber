
import cadquery as cq
from cadquery import exporters
from math import *



class Wall():
    """Implements different wall tiles such as sides
    and corner with different cross sections."""

    def __init__(self, tile_len=1.0, tile_wid=1.0, tile_height=2, foundation_thickness=4, scale=2):
        """Creates a wall object.
        :param tile_len: length of tile
        :param tile_wid: width of tile
        :param tile_height: height of tile
        :param foundation_thickness: thickness of the tile foundation under the cross section.
        """
        self.scale = scale
        self.tile_len = tile_len * self.scale
        self.tile_wid = tile_wid * self.scale
        self.tile_height = tile_height * self.scale
        self.foundation_thickness = foundation_thickness *self.scale

        self.sides = None
        self.corners = None

    def get_scale(self):
        return self.scale

    def make_dog_components(self):
        """Make a triangular corner"""
         #carefull with rotation and see if they are at same position


        def copy_cross_section():
            foundation_thickness = self.foundation_thickness
            tile_len = self.tile_len
            tile_height = self.tile_height
            angle = (pi/6)/2
            
            h = self.tile_height/2
            w = h*tan(angle)
            
            k = 1/tan(2*angle)
            k_w = 1/(1-tan(angle)**2) # koefficient front of w at lowest point
            a = tile_len - 2*w#((1.5-k_w)*w-(-0.5*w-k_w)*w)
            s = a*cos(2*angle)

            dx = s*cos(2*angle)
            dy = s*sin(2*angle)


            xs_1 = (s+dy)/(2*k)
            xs_2 = (s+dy)/(2*k)+dx
            ys_1 = (s+dy)/2
            ys_2 = (s-dy)/2

            xs = (xs_1+xs_2)/2
            ys = (ys_1+ys_2)/2

            xa = xs
            c1 = xa
            c2 = a - c1

            area_left_pts = [(0,0),
                    (xa,0),
                    (xs,ys),
                    (xs_1, ys_1)]


            area_right_pts = [(xa,0),
                    (a,0),
                    (xs_2,ys_2),
                    (xs,ys)]
            

            pts = [(0,0),
                   (1.5*w, -1.5*h),
                   ((1.5-k_w)*w, -2*h),
                   ((-0.5-k_w)*w, -2*h),
                   (-0.5*w, -1.5*h),
                   (-w, -h)]


            max_wid = 2*(abs((-0.5-k_w)*w-c2))#2*(abs(max(1.5*w,(-0.5-k_w)*w-c2))) #((1.5-k_w)*w, -2*h)+c1 might be max
            ##max always take the lowest because of neg large

            self.max_wid = max_wid
            
            geo_xz = cq.Workplane("XZ").center(0,0).polyline(pts).close().extrude(max_wid/2).mirror(mirrorPlane="XZ", union=True)

            
            geo_xy = cq.Workplane("XY").add(geo_xz).translate((0,0,tile_height))

            
            dog_side = geo_xy.add(cq.Workplane("XY").center(0,0).rect(max_wid, max_wid).extrude(-foundation_thickness))

            area_right_side = cq.Workplane("XZ").center((1.5-k_w)*w,0).polyline(area_left_pts).close().extrude(max_wid/2).mirror(mirrorPlane="XZ", union=True)
            area_left_side = cq.Workplane("XZ").center((-0.5-k_w)*w-a,0).polyline(area_right_pts).close().extrude(max_wid/2).mirror(mirrorPlane="XZ", union=True)


            circle_right_side = cq.Workplane("XZ").center((1.5-k_w)*w+c1,s/2).circle(s/2).extrude(max_wid/2).mirror(mirrorPlane="XZ", union=True)

            circle_left_side = cq.Workplane("XZ").center((-0.5-k_w)*w-c2,s/2).circle(s/2).extrude(max_wid/2).mirror(mirrorPlane="XZ", union=True)

            dog_side = dog_side.add(area_left_side).add(area_right_side)
            dog_side = dog_side.cut(circle_right_side).cut(circle_left_side)
            


            return dog_side
            

        def copy_components():
            comp = {}
            comp["ver"] = copy_cross_section()
            comp["hor"] = copy_cross_section().rotate((0,0,0), (0,0,1), 90) #((vek_svans),(vek_huvud),(grader))
            comp["inter"] = comp["ver"].intersect(comp["hor"]) ### the start workplane must always be new but add could be reused
            return comp

        def copy_sides(comp):
            sides = {}
            
            sides["ver_half_left"] = comp["hor"].faces(">X").workplane(-self.max_wid/2).split(keepBottom=True)
            sides["ver_half_right"] = comp["hor"].faces(">X").workplane(-self.max_wid/2).split(keepTop=True)

            sides["hor_half_down"] = comp["ver"].faces(">Y").workplane(-self.max_wid/2).split(keepBottom=True)
            sides["hor_half_up"] = comp["ver"].faces(">Y").workplane(-self.max_wid/2).split(keepTop=True)
            

            return sides
        
        inter = copy_components()["inter"]
        
        return inter


    


def main():
    """Operates functions and classes to export a finished stl file."""

    x = 10
    y = 10
    result = cq.Workplane("XY")
    dogleg_wall = Wall(foundation_thickness=1, tile_height=3)
    inter = dogleg_wall.make_dog_components()
    scale = dogleg_wall.get_scale()

    for i in range(x):
        for j in range(y):
            result.add(inter.translate((i*scale,j*scale,0)))
            
    exporters.export(result, "square_dog.stl")
    print("done")


#if __name__ == "main":
main()







