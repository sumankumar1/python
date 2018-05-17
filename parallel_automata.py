import time
from multiprocessing import Process, Pipe,Queue
import matplotlib.pyplot as plot

def rule_110(a, b, c):
	return (not c and b) or (c and not (a and b))

def simple(arr,iterations):
	#t3=time.time()
	time1=[]
	for _ in range(iterations):
		t1=time.time()
        	# First element
        	leftmost = arr[0]
        	a, b, c = arr[-1], leftmost, arr[1]
        	arr[0] = rule_110(a, b, c)

        	# Middle element
        	for i in range(1, len(arr)-1):
            		a, b, c = b, c, arr[i+1]
            		arr[i] = rule_110(a, b, c)

        	# Last element
        	a, b, c = b, c, leftmost
        	arr[-1] = rule_110(a, b, c)

		t2=time.time()
		time1.append(t2-t1)
	#t4=time.time()
	return arr,time1#,t4-t3
	



def process_section(left_conn, right_conn, queue, row_section, iters, num):
    left_conn.send(row_section[0])
    right_conn.send(row_section[-1])
    time1=[]
    for _ in range(iters):
	t3=time.time()
        # First col
        a, b, c = left_conn.recv(), row_section[0], row_section[1]
        row_section[0] = rule_110(a, b, c)
        left_conn.send(row_section[0])

        # Middle cols
        for i in range(1, len(row_section)-1):
            a, b, c = b, c, row_section[i+1]
            row_section[i] = rule_110(a, b, c)

        # Last col
        a, b, c = b, c, right_conn.recv()
        row_section[-1] = rule_110(a, b, c)
        right_conn.send(row_section[-1])
	t4=time.time()
	time1.append(t4-t3)
    # Push final result into the queue so that it can be collated
    queue.put((num, row_section,time1))
    return


def fixed(row, iters, splits=20):
    # Queue for processes to send final results
    q = Queue(maxsize=splits)

    # Pipes for each process to communicate with the processes to its immediate
    # left and right
    pipes = [Pipe() for _ in range(splits)]

    # Create processes and divide up into sections
    processes = []
    for i in range(splits):
        # connect pipes
        if i == splits - 1:
            left, right = pipes[i][0], pipes[0][1]
            start, end = len(row)/splits * i, len(row)
        else:
            left, right = pipes[i][0], pipes[i+1][1]
            start, end = len(row)/splits * i, len(row)/splits * (i+1)

        # Create process for this section
        p = Process(target=process_section,
                    args=(left, right, q, row[start:end], iters, i))
        processes.append(p)

    for p in processes:
        p.start()

    for p in processes:
        p.join()

        proc_id, result,time3 = q.get()
	
        for i, v in enumerate(result):
            row[len(row)/splits * proc_id + i] = v
    return row,time3
	

def main():
	iterations = 2000
	initial_state = lambda: [False]*2000+ [True, False]
	arr=initial_state()
	#print inital_state()
	t0=time.time()
	std_result,time2 = simple(initial_state(), iterations)
	total=time.time()-t0
	t1=time.time()
	arr3,time3=fixed(arr,iterations,4)#4 processor so running 4 process on my computer
	t2=time.time()
	total1=t2-t1
	p=(total-(total1-sum(time3)))/total
	s=sum(time2)/sum(time3)
	slat=1/(1-p+p/s);
	improvement= 100*(1-1/slat)
	print "single process:",total,"Multiple process:",total1,"latency:",slat,"improvement:",improvement
	plot.plot(time3,'-r',time2,'-b')
	plot.text(x=1000,y=0.0005,s='S(lat):'+str(slat)+'\n'+'improvement(%):'+str(improvement), bbox=dict(facecolor='blue', alpha=0.18))
	plot.show()

main()


