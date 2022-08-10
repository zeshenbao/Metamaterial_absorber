


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

    
