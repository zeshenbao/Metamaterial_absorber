
# L-system definition
axiom = "A"
A = "-BF+AFA+FB-"
B = "+AF-BFB-FA+"


# Prepare L-system
lsystem = axiom
for _ in range(5):
    lsystem = (
        lsystem.replace("A", "a").replace("B", "b").replace("a", A).replace("b", B)
    )
lsystem = lsystem.replace("A", "").replace("B", "")
while "+-" in lsystem:
    lsystem = lsystem.replace("+-", "")
while "-+" in lsystem:
    lsystem = lsystem.replace("-+", "")
lsystem = lsystem.strip("+-")


print(lsystem)
