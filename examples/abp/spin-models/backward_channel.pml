
active proctype BackwardChannel()
{
  bc0: do
        :: receiver2backchannel?a0 -> goto bc1
        :: receiver2backchannel?a0 // non-deterministically lose a0
        :: receiver2backchannel?a1 -> goto bc2
        :: receiver2backchannel?a1 // non-deterministically lose a1
       od;

  bc1: do
        :: backchannel2sender!a0p -> goto bc0
        :: backchannel2sender!a0p // non-deterministically duplicate a0
        :: receiver2backchannel?a0 // ignore a0
        :: receiver2backchannel?a1 // ignore a1
       od;

  bc2: do
        :: backchannel2sender!a1p -> goto bc0
        :: backchannel2sender!a1p // non-deterministically duplicate a1
        :: receiver2backchannel?a0 // ignore a0
        :: receiver2backchannel?a1 // ignore a1
       od;
}

