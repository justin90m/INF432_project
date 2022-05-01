def grid_from_file(file_name):
    f=open(file_name)
    grid=[]
    grid=f.readlines()
    #lignes = [[8]; [0010--10]; [0000000] ... ]
    # n = lignes[0]
    n=grid[0];
    # test if n = length of list - 1
    if int(n) != (len(grid)-1) :
        print("erreur d'entree, BYE")
        return None
    grid.pop(0)
    #boucle pour chaque elem de liste (indice >= 1)
    for i in range(len(grid)):
    #create list l
        l = []
        ligne = grid[i];
    #if elem type is char add each char to l
        for j in range(len(ligne)):
            case = ligne[j]
            # if '0' add 0
            # if '1' add 1
            # else add None
            if case == '0':
                l.append(0)
            elif case == '1':
                l.append(1)
            elif case == '-':
                l.append(None)                
        #and then lignes[indice] = l
        grid[i] = l;
    f.close()   
    return grid

grid = grid_from_file("fichier_test.txt")
for i in range(len(grid)):
    for j in range(len(grid[i])):
        print(grid[i][j], end=' ')
    print()
print(grid)
