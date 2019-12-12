
active proctype Receiver()
{
  r0: do
	// :: receiver2env!deliver // sanity check for safety monitor
        :: forwchannel2receiver?p0p -> break
        :: forwchannel2receiver?p1p -> goto progress_r5
      od;

  r1: receiver2env!deliver;

  r2: receiver2backchannel!a0;

  r3: do
        :: forwchannel2receiver?p1p -> break
        :: forwchannel2receiver?p0p -> goto r2
      od;

  r4: receiver2env!deliver;

  progress_r5: receiver2backchannel!a1 -> goto r0
}

