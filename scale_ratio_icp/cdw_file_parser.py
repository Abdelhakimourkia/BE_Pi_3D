import numpy  as np 

def parse_file(filename) :
    with open(filename , mode="r") as f :
        lines =  f.readlines()
    mat = []
    for l in lines :
        line_nb = l.split("\t")[:-1]
        mat.append(np.asarray(line_nb , dtype=np.float32))
    ContributionRate = np.asarray(mat)
    return ContributionRate

def main() :
    filename = "bunny_0.ply.cdw"
    parse_file(filename)

if __name__ == "__main__" :
    main()
