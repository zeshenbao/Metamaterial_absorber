from turtle import *


def L_system(iterations):
        axiom = "A"
        A = "+BF-AFA-FB+"
        B = "-AF+BFB+FA-"

        system = axiom

        for i in range(iterations):
            system = system.replace("A", "a").replace("B", "b") #a, b are temporary variables because we wnt to replace A and B at the same time

            system = system.replace("a", A).replace("b", B)

        system = system.replace("A", "").replace("B", "")
        
        while "+-" in system:
            system = system.replace("+-", "")
            
        while "-+" in system:
            system = system.replace("-+", "")

        return system


system=L_system(2)
print(system)
speed(1)
for letter in system:
    if letter == "F":
        forward(10)
    elif letter == "+":
        right(90)
    elif letter == "-":
        left(90)
    else:
        print("error")
