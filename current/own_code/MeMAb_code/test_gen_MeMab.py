


def test_deep_copy():
    """Careful of add method for deep copy."""
    
    #Testing add method for Workplanes
    comps = copy_components()

    #scenario 1(best): adding an existing obj to a new obj
    union = (copy_components()["ver"].add(comps["hor"])) # works fine

    #scenario 2: adding to a existing obj
    union = (comps["ver"].add(comps["hor"])) # comps["ver"] becomes union in the process and can't be used as ver.

    #scenario 3: adding two existing objs to a new obj
    union = (copy_components()["ver"].add(comps["hor"])
             .add(comps["ver"])) # works fine, both add is to obj1 (obj3 is not added to obj2).

    #scenario 4:
    union = (copy_components()["ver"].add(copy_components()["hor"])) # works but slower and unefficient.

    #scenario 5:
    union = (cq.Workplane().copyWorkplane(comps["ver"]) # copyWorkplane() makes temp copy of a obj
             .add(comps["hor"])) #start with new Workplane and make a temporary copy of comps["ver"]. Problem is that comp["ver"] then dissapears from union

    #scenario 6:
    union = (comps["ver"].add(cq.Workplane().copyWorkplane(comps["hor"]))) #comps["hor"] is only temp and get removed from union.
    

    #Testing rotate method for Workplanes
    comp["hor"] = (comp["ver"].rotate((0,0,0), (0,0,1), 90)) #don't affect obj1, comp["ver"] still the same

    #Testing intersect method for Workplanes
    comp["inter"] = (comp["ver"].intersect(comp["hor"])) #don't affect obj1


    #Test translate - don't affect
    #translated_comp = (comp["ver"].translate((1,1,1))) #comp["ver"] will be in the same coordinates.
    #test by making comp["ver"] and then translate it, if two then correct, if one object then error.

    
    #Test cut 
    comp["union"] = (comp["ver"].cut(comp["hor"])) #unlike add, comp["ver"] stays the same but comp["union"] will be ver cut by hor.

    
    #use union instead of add normally. union does not change the object but add will. use add only in build or assembly. union is for parts, add is for assembly kind of









def test_Tile():
    wall1 = Wall(cross_section="block")
    tile1 = Tile(wall1.sides["ver"], "ver", [0,0,1])

    #test self.coord
    assert (tile1.coord == np.array([0,0,1])).all()
    
    #test repr
    assert repr(tile1) == "ver"

    #test goto()
    tile1.goto([1,2,3])
    assert (tile1.coord == np.array([1,2,3])).all()

    #test translate()
    tile1.translate([2,1,1])
    assert (tile1.coord == np.array([3,3,4])).all()

def test_Wall_export():
    """Make sure to not have any stl files already when testing this."""

    #don't export parts automatically after build
    wall1 = Wall(cross_section="block", export = False)
    assert exists("comp_ver.stl") == False
    
    #export with default
    wall1 = Wall(cross_section="block")
    assert exists("comp_ver.stl") == True
    
    #export
    wall1 = Wall(cross_section="block", export = True)
    assert exists("comp_ver.stl") == True

    

def test_Pattern():


    """
    wall1 = Wall(cross_section="dogleg")
    hilbert = Pattern()
    hilbert.create_hilbert_blueprint(iterations = 3)
    #print(pattern1.pattern)
    block_hilbert = Absorber(wall1, hilbert)
    block_hilbert.build()
    block_hilbert.export()
    """
    wall1 = Wall(cross_section="dogleg", scale = 0.1)
    rows = Pattern()
    rows.create_dots_blueprint(pattern_len=50, pattern_wid=50, scale = 0.1)
    #print(rows.blue_print)
    dogleg_rows = Absorber(wall1, rows)
    dogleg_rows.build()
    print("Build complete, exporting to stl file")
    dogleg_rows.export()
    
def unittest():
    """The tests are made manually and visually to check that the program exports the right wall tiles, absorber, etc..
    almost all of the functions and methods are tested."""

    #test_Tile()
    #test_Wall_export()
    test_Pattern()







