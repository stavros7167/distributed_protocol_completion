
active proctype ForwardChannel()
{
  fc0: do
        :: sender2forwchannel?p0 -> goto fc1
        :: sender2forwchannel?p0 // non-deterministically lose p0
        :: sender2forwchannel?p1 -> goto fc2
        :: sender2forwchannel?p1 // non-deterministically lose p1
       od;

  fc1: do
        :: forwchannel2receiver!p0p -> goto fc0
        :: forwchannel2receiver!p0p // non-deterministically duplicate p0
        :: sender2forwchannel?p0 // ignore p0
        :: sender2forwchannel?p1 // ignore p1
       od;

  fc2: do
        :: forwchannel2receiver!p1p -> goto fc0
        :: forwchannel2receiver!p1p // non-deterministically duplicate p1
        :: sender2forwchannel?p0 // ignore p0
        :: sender2forwchannel?p1 // ignore p1
       od;
}

