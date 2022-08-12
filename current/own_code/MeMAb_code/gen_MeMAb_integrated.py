"""
gen_MeMAb v1.0.0

Before you run the code, make sure to do the followig to ensure that the code works:

- Update to the newest version of miniconda: Will otherwise cause OCP errors.
- Uses Cadquery 2.1/master: see if it works with the newest version of cadquery.

Zeshen Bao
"""



import cadquery as cq
from cadquery import exporters
from math import *
from copy import copy
import numpy as np
from os.path import exists


class Absorber():
    """Implements a absorber with patterns and different wall segments 
    and saved as a stl file.
    """

    def __init__(self, wall, pattern):
        """Creates an absorber object with input wall corners, wall sides and system.
         _____ _____    ___________
        |     |     |  |           |    
        |  2  |  3  |  |           |   
        |-----+-----|  |     +-----|    
        |  1  |  0  |  |     |  0  |
        |_____|_____|, |_____|_____|     
      
        
        :param corners: A dictionary that stores wall corner in 4 different directions as seen in the figure above.
        You can see how the zeroth list element looks like.

        :param sides: A dictionary of two wall sides, the zeroth vertically and first horisontal.

        :param result: The generated absorber as a cq.Workplane object.

        """
    
        self.pattern = pattern
        self.wall = wall
        self.result = cq.Workplane("XY")
        

    def build(self): 
        """Builds the absorber with pattern blueprint."""

        for part in self.pattern.blue_print:
            #self.result = self.result.add(self.sides["hor"].translate((-1*self.scale,0,0)))
            #print(type(tuple(part.coord)))
            #print(part.tile)

            if part.group == "sides":
                self.result = self.result.add(self.wall.sides[part.tile].translate(tuple(part.coord)))

            elif part.group == "corners":
                self.result = self.result.add(self.wall.corners[part.tile].translate(tuple(part.coord)))

            elif part.group == "other":
                self.result = self.result.add(self.wall.other[part.tile].translate(tuple(part.coord)))


            else:
                print("No such group")
            
            
        

    def export(self):
        """Export created self.result to a stl file
        with file name specified with iterations (if there are iterations)."""
        
        itera = self.pattern.iterations
        exporters.export(self.result, self.wall.cs_choice +"_" +self.pattern.name +("_iter" + str(itera)  if itera != None else "") +".stl")
        print("exported")




class Wall():
    """Implements different wall tiles such as sides
    and corner with different cross sections."""


    def __init__(self, cross_section="dogleg", tile_len=1.0, tile_wid=1.0, tile_height=2, foundation_thickness=4, scale=1, export = True):
        """Creates a wall object.
        :param cross_section: str on type of cross section
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
        self.cs_choice = cross_section
        self.export = export
        
        self.cross_section = None
        self.comps = None
        self.sides = None
        self.corners = None
        self.other = None

        #init runned functions
        self.set_cross_section()
        self.make_wall_components()

    def set_cross_section(self, choice=None):

        if choice == None:
            choice = self.cs_choice

        cross_sections = {"dogleg":self._make_dogleg_basic, "triangle":self._make_triangle_basic, "block":self._make_block_basic}

        if cross_sections[str(choice)]() != None:
            self.cross_section = cross_sections[str(choice)]()
    
        else:
            print("Choice error, check typos in cross_section choice.")

    
    def get_scale(self):
        return self.scale

    

    def export_parts(self):
            
            bundle = {"comps":self.comps, "sides":self.sides, "corners":self.corners}

            for item in bundle:
                #print(bundle[item])
                for key in bundle[item]:
                    exporters.export(bundle[item][key], str(item[:-1]) + "_" +key +".stl")


    def _make_block_basic(self):
        
        self.max_wid = self.tile_wid

        geo_xz = (cq.Workplane("XZ")
                  .rect(self.tile_wid/2,  self.tile_height).extrude(self.max_wid/2)
                      .mirror(mirrorPlane="XZ", union=True)) #make wall


        geo_xy = (cq.Workplane("XY").union(geo_xz)) #change plane


        block_side = (geo_xy.faces("<Z")
                     .rect(self.tile_len, self.tile_wid).extrude(-self.foundation_thickness)) #add foundation

        
        return block_side


    def _make_triangle_basic(self):
        """Make a triangular wall side facing y (upp/down or vertical) direction."""
        pts = [(-self.tile_len/2,0),
               (self.tile_len/2, 0),
               (0, self.tile_height)] #Note that pts are centered at 0!
 
        self.max_wid = self.tile_wid
        
        geo_xz = (cq.Workplane("XZ")
                  .polyline(pts).close().extrude(self.tile_wid/2)
                      .mirror(mirrorPlane="XZ", union=True)) #make wall


        geo_xy = (cq.Workplane("XY").union(geo_xz)) #change plane


        tria_side = (geo_xy.faces("<Z")
                     .rect(self.tile_len, self.tile_wid).extrude(-self.foundation_thickness)) #add foundation

        """
        #center at (0,0) if you want to make sure the foundation is on center to see if your prism or extruded triangle is in (x,y)=(0,0)

        tria_side = (geo_xy.union(cq.Workplane("XY")
                                  .center(0,0).rect(self.max_wid, self.max_wid).extrude(-self.foundation_thickness))) #add foundation
        """ 
        
        

        return tria_side
    

    def _make_dogleg_basic(self):
            """Helper fuction to generate dogleg cross section and with that make a vertical wall tile.
            The vertical wall tile then gets returned."""
            
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
            
            geo_xz = (cq.Workplane("XZ")
                      .center(0,0).polyline(pts).close().extrude(max_wid/2)
                      .mirror(mirrorPlane="XZ", union=True))


            geo_xy = (cq.Workplane("XY")
                      .union(geo_xz).translate((0,0,tile_height)))

            
            dog_side = (geo_xy.union(cq.Workplane("XY")
                                   .center(0,0).rect(max_wid, max_wid).extrude(-foundation_thickness)))


            area_right_side = (cq.Workplane("XZ")
                               .center((1.5-k_w)*w,0).polyline(area_left_pts).close().extrude(max_wid/2)
                               .mirror(mirrorPlane="XZ", union=True))


            area_left_side = (cq.Workplane("XZ")
                              .center((-0.5-k_w)*w-a,0).polyline(area_right_pts).close()
                              .extrude(max_wid/2).mirror(mirrorPlane="XZ", union=True))


            circle_right_side = (cq.Workplane("XZ")
                                 .center((1.5-k_w)*w+c1,s/2).circle(s/2).extrude(max_wid/2)
                                 .mirror(mirrorPlane="XZ", union=True))

            circle_left_side = (cq.Workplane("XZ")
                                .center((-0.5-k_w)*w-c2,s/2).circle(s/2).extrude(max_wid/2)
                                .mirror(mirrorPlane="XZ", union=True))


            dog_side = (dog_side.union(area_left_side)
                        .union(area_right_side))
            
            dog_side = (dog_side.cut(circle_right_side)
                        .cut(circle_left_side))
            
            return dog_side


    def _make_new_basic(self):
        pass
            

    def make_wall_components(self):
        """Make different wall tiles and return them as a pair of dictionaries.
        The first dict contains wall side tiles + wall intersection tile and the second dict contains wall corner tiles."""
         #carefull with rotation and see if they are at same position
            

        def make_components():
            """Helper function to make and return the side wall tiles and intersection wall tile.
            Could write ver, hor and inter as seperate helper function to speed up in case of frequent copy usage."""
            
            comps = {}
            comps["ver"] = (self.cross_section)
            comps["hor"] = (comps["ver"].rotate((0,0,0), (0,0,1), 90)) #((vek_svans),(vek_huvud),(grader))
            comps["inter"] = (comps["ver"].intersect(comps["hor"])) ### the start workplane must always be new but add could be reused
            comps["union"] = (comps["ver"].union(comps["hor"])) #When adding object2 to object1 then object1 will include object2 so don't use usable parts as object1 to add on. But object2 which adds to other stuff can be reused.

            self.comps = comps
            self.other = {}
            self.other["inter"] = comps["inter"]
            self.other["union"] = comps["union"]

        def make_sides():
            """Helper function to make and return the corner wall tiles. """
            
            sides = {"ver":self.comps["ver"], "hor":self.comps["hor"], "ver_half_down":None, "ver_half_up":None, "hor_half_left":None, "hor_half_right":None}

            for key in sides:

                if key == "ver" or key == "hor":
                    continue
                
                if key[:3] == "hor":
                    comp_key, face_key = "hor", ">X"

                elif key[:3] == "ver":
                    comp_key, face_key = "ver", ">Y"

                else:
                    print("Key error1")

                if key[9:] == "left" or key[9:] == "down":
                    sides[key] = (self.comps[comp_key].faces(face_key)
                                  .workplane(-self.max_wid/2).split(keepBottom=True))

                elif key[9:] == "right" or key[9:] == "up":
                    sides[key] = (self.comps[comp_key].faces(face_key)
                                  .workplane(-self.max_wid/2).split(keepTop=True))
                    
                else:
                    print("Key error2")

            self.sides = sides



        def make_corners():
            corners = {"left_down":None, "left_up":None, "right_down":None, "right_up":None}
            
            for key in corners:
                corners[key] = (self.comps["inter"].union(self.sides["hor_half_" +key.split("_")[0]])
                                .union(self.sides["ver_half_" +key.split("_")[1]]))

            self.corners = corners


        make_components()
        make_sides()
        make_corners()

        if self.export == True:
            self.export_parts()

        
        


class Tile():

    def __init__(self, group, tile, coord = None):
        """:param tile: a wall object
           :param coord: a np array, if it is [x, y] vector or list object, then it will be comverted to np array.
        """
        
        self.coord = np.array(coord)
        self.group = group
        self.tile = tile
        self.repr = str(group) +"_" +str(tile)

    def __repr__(self):
        return self.repr

        
    def goto(self, coord):
        self.coord = np.array(coord)


    def translate(self, d_coord):
        self.coord += np.array(d_coord)
    
        


class Pattern(): 
    """
    #Used to generate different patterns. By exporting a list of Tile objects.

    :param system: str
    System instructions to generate the walls.
    
    #:param pattern_choice: str
    #Choose between different patterns.
    
    :param iterations: int
    Optional, used for fractals

    :param pattern_len: int
    Optional, used for non-fractals

    :param pattern_wid: int
    Optional, used for non-fractals
    """
    #pattern_len=10, pattern_wid=10
    
    def __init__(self):
        """Creates a pattern object with an empty system."""
        self.blue_print = []
        self.iterations = None
        self.name = None

    def _gen_hilbert_sys(self):
        """Generates and returns a hilbert curve system 
        where the iterations depends on the parameter iterations. 

        :param iterations: iterations of hilbert system.
        """
        
        axiom = "A"
        A = "+BF-AFA-FB+"
        B = "-AF+BFB+FA-"

        system = axiom

        for i in range(self.iterations):
            system = system.replace("A", "a").replace("B", "b") #a, b are temporary variables because we wnt to replace A and B at the same time

            system = system.replace("a", A).replace("b", B)

        system = system.replace("A", "").replace("B", "")
        
        while "+-" in system:
            system = system.replace("+-", "")
            
        while "-+" in system:
            system = system.replace("-+", "")

        system = system.replace("F+", "+").replace("F-", "-")

        #self.system = system
        #print(system)

        return system


    def create_hilbert_blueprint(self, iterations=2, scale = 1): 
        """Make instructions on how to build hilbert absorber by making a list of tiles with tile types with their respective coordinates."""
        
        """Code variable reminders:
           :var pos: position of current tile
           :var angle: current direction of movement of the tile.
           :var count: current tile number.
        """
        self.name = "hilbert"
        self.iterations = iterations
        self.scale = scale
        
        system = self._gen_hilbert_sys()
        
        
        
        position = [0,0,0]
        angle = 0    #0 degrees == right
        count = 0

        
        if self.iterations % 2 == 0:
            self.blue_print.append(Tile("sides", "hor", [-1*self.scale,0,0]))
            
        
        for letter in system:
            print(count/len(system))
            #print(position[0], position[1], angle)
            
            if letter == "F":
                #exporters.export(self.sides["ver"], "sides_hor.stl")
                #exporters.export(self.sides["ver"], "sides_hor.stl")
                #return
                
                if angle == 0:
                    self.blue_print.append(Tile("sides", "hor", position))
                    position[0] +=1*self.scale

                elif angle == 180:
                    self.blue_print.append(Tile("sides", "hor", position))
                    position[0] -=1*self.scale
                    
                elif angle == 90:
                    self.blue_print.append(Tile("sides", "ver", position))
                    position[1] -=1*self.scale

                elif angle == 270:
                    self.blue_print.append(Tile("sides", "ver", position))
                    position[1] +=1*self.scale

                else:
                    print("error")

                
            elif letter == "+": #clockwise angle, + equals turn to the right or add 90 degrees
                if angle == 0:
                    #print(self.corners["left_down"])
                    self.blue_print.append(Tile("corners", "left_down", position))
                    position[1] -=1*self.scale

                elif angle == 180:
                    self.blue_print.append(Tile("corners", "right_up", position))
                    position[1] +=1*self.scale
                    
                elif angle == 90:
                    self.blue_print.append(Tile("corners", "left_up", position))
                    position[0] -=1*self.scale

                elif angle == 270:
                    self.blue_print.append(Tile("corners", "right_down", position))
                    position[0] +=1*self.scale

                else:
                    print("error")

                angle += 90
                angle %= 360
                
                
            elif letter == "-":
                if angle == 0:
                    self.blue_print.append(Tile("corners", "left_up", position))
                    position[1] +=1*self.scale

                elif angle == 180:
                    self.blue_print.append(Tile("corners", "right_down", position))
                    position[1] -=1*self.scale
                    
                elif angle == 90:
                    self.blue_print.append(Tile("corners", "right_up", position))
                    position[0] +=1*self.scale

                elif angle == 270:
                    self.blue_print.append(Tile("corners", "left_down", position))
                    position[0] -=1*self.scale

                else:
                    print("error")

                angle -= 90
                angle %= 360
                
            count += 1


    def create_ver_rows_blueprint(self, pattern_len=5, pattern_wid=5, scale = 1):
        self.name = "ver_rows"
        
        for i in range(int(pattern_len)):
            for j in range(int(pattern_wid)):
                self.blue_print.append(Tile("sides", "ver", [i*scale, j*scale, 0]))

    
    def create_dots_blueprint(self, pattern_len=10, pattern_wid=10, scale = 1):
        self.name = "dots"
        
        for i in range(int(pattern_len)):
            for j in range(int(pattern_len)):
                self.blue_print.append(Tile("other", "inter", [i*scale, j*scale, 0]))
                    
             

def main():
    """Operates functions and classes to export a finished stl file."""

    ###Example builds


    #default wall(hilbert) setup with rows pattern
    """
    hilbert = Wall() #define wall
    
    rows = Pattern() #define pattern
    rows.create_ver_rows_blueprint() #choose pattern to vertical rows and generate blueprint
    
    dogleg_rows = Absorber(hilbert, rows) #define absorber with wall1 and rows parameters
    dogleg_rows.build() #builds the cadquery object of absorber
    print("Build complete, exporting to stl file") #Confirming building
    dogleg_rows.export() #exports the absorber cadquery object
    """


    #hilbert rows with other len and wid
    """
    hilbert = Wall(cross_section = "dogleg") #will be same as default
    
    rows = Pattern() #same
    rows.create_ver_rows_blueprint(pattern_len=8, pattern_wid=4) #same as before but with other parameters for length and width of pattern
    
    dogleg_rows = Absorber(hilbert, rows) #same
    dogleg_rows.build() #same
    print("Build complete, exporting to stl file") #same
    dogleg_rows.export() #same
    """

    
    #triangle cross section with dots pattern
    """
    triangle = Wall(cross_section = "triangle") #changing cross section to triangle
    
    dots = Pattern() #same
    dots.create_dots_blueprint(pattern_len=5, pattern_wid=5) #same as before but with other parameters for length and width of pattern
    
    triangle_dots = Absorber(triangle, dots) #same
    triangle_dots.build() #same
    print("Build complete, exporting to stl file") #same
    triangle_dots.export() #same
    """

    
    #hilbert block iter 4
    """
    block = Wall(cross_section = "block") #changing cross section to block
    
    dots = Pattern() #same
    dots.create_hilbert_blueprint(iterations =4) #setting iterations to 4 for hilbert curve
    
    block_hilbert = Absorber(block, dots) #same
    block_hilbert.build() #same
    print("Build complete, exporting to stl file") #same
    block_hilbert.export() #same
    """




#if __name__ == "main":
main()








