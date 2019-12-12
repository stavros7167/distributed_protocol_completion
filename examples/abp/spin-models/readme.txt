
First generate the spin analyzer:

	spin -a abp1.pml

Then compile it:

	gcc -DNOREDUCE -DNFAIR=3 -o pan pan.c

Then run it:

	./pan -a -f

If you find a counterexample, play it back with:

	spin -p -t abp1.pml


For more info, see:

	http://spinroot.com/spin/Man/Manual.html

	http://spinroot.com/spin/Man/Roadmap.html 

etc.

