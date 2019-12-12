
active proctype ForwardChannel()
{
  fc0: do
        :: sender2forwchannel?p0 -> 
	fc00:
	if
	:: goto progress_fc1
	:: skip // non-deterministically lose p0
	fi
        :: sender2forwchannel?p1 -> 
	fc01:
	if
	:: goto progress_fc2
        :: skip // non-deterministically lose p1
	fi
       od;

  progress_fc1: do
        :: forwchannel2receiver!p0p -> goto fc0
        :: forwchannel2receiver!p0p // non-deterministically duplicate p0
        :: sender2forwchannel?p0 // ignore p0
        :: sender2forwchannel?p1 // ignore p1
       od;

  progress_fc2: do
        :: forwchannel2receiver!p1p -> goto fc0
        :: forwchannel2receiver!p1p // non-deterministically duplicate p1
        :: sender2forwchannel?p0 // ignore p0
        :: sender2forwchannel?p1 // ignore p1
       od;
}

