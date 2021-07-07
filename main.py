
from multiprocessing import shared_memory,Pool,Process,Queue
import time

memory_size = 20
Q = Queue()
in_size = 200
process_count = 2

#
# Reads data and timestamp from the element in shared memory
# and marks it as read
#
#
def ReadElement(index,sliste,slistt,slistd):

    if(index > memory_size):
        return(0,0)
    
    data = sliste[index]
    timestamp = slistt[index]
    slistd[index] = True
    return (data,timestamp)

#
# Writes a new element to shared memory using data and timestamp
#
#
#
def WriteElement(data,timestamp,sliste,slistt,slistd):
    
    index = 0
    for dirty in slistd:
        if dirty == True:
            sliste[index] = data
            slistt[index] = timestamp
            slistd[index] = False
            return True
        else:
            index = index + 1
        
        if index > memory_size:
            index = 0

    return False

#
# takes data from a file and inputs into slist with timestamp
#
#
#
def InputData(sliste, slistt, slistd, dfile):

    print("entering ImportData")
    ## get all the lines in the file
    with open(dfile) as f:
        lines = f.read().splitlines()
    f.close()
    
    count = 0

    for line in lines:
        #try to write the element to the list until successful
        while True:
            if WriteElement(float(line),time.time(),sliste,slistt,slistd) == True:
                count += 1
               # print("printing")
                break

        Q.put(False)

        
    Q.put(True)
    print("closing ImportData: " + str(count))
    return True

#
# takes data from slist and inserts into a file
#
#
#
def ExportData(sliste,slistt,slistd,dfile):

    time.sleep(1)
    count = 0


    ## create output file
    f = open(dfile,"w")


    print("entering ExportData")
    while True:
        index = 0
        while index < memory_size:
           # print("exporting")
            index += 1
            if slistd[index] == False:
                count = count + 1
                (data,timestamp) = ReadElement(index,sliste,slistt,slistd)
                out = str(data) + " " + str(timestamp) + "\n"
                f.write(out)
                break

        res = Q.get()
        #print(res)
        if res == True:
            break

    f.close()
    
    print("closing ExportData: " + str(count))
    return True


def main():
    
    # create shared memory lists
    elements   = shared_memory.ShareableList(range(memory_size), name="elements")
    timestamps = shared_memory.ShareableList(range(memory_size), name="timestamps")
    dirty      = shared_memory.ShareableList(memory_size * [True], name="dirty")

    e = shared_memory.ShareableList(name=elements.shm.name)
    t = shared_memory.ShareableList(name=timestamps.shm.name)
    d = shared_memory.ShareableList(name=dirty.shm.name)

    with Pool(processes=3) as pool:
        i1 = pool.apply_async(InputData, args = (e,t,d,"in/testfile_0"))
        i2 = pool.apply_async(InputData, args = (e       ,t         ,d    ,"in/testfile_1"))
        o  = pool.apply_async(ExportData,args = (e       ,t         ,d    ,"out/testfile_out"))
   
        i1.get()
        i2.get()
        o.get()

    elements.shm.close()
    timestamps.shm.close()
    dirty.shm.close()
    e.shm.close()
    t.shm.close()
    d.shm.close()
    e.shm.unlink()
    t.shm.unlink()
    d.shm.unlink()
    print("done")

    return


if __name__ == "__main__":
    main()



