import io
import random

s = "testfile_"
v = 200
f = 20

def write_files(fn_base,values,files):

    for y in range(0,files):

        ## create files and open them for writing
        fn = "in/" + fn_base + str(y)
        f = open(fn,"w")
        
        for x in range(0,values):
            random.seed()
            f.write( str(random.randint(0, 1000000)/100) + "\n" )
        
        f.close()
    
    return
    

if __name__ == "__main__":
    write_files(s,v,f)


