
active proctype Sender()
{
  s0: do
	:: env2sender?send -> break
	:: backchannel2sender?a0p
	:: backchannel2sender?a1p
	:: env2sender?mytimeout
      od;

  s1: sender2forwchannel!p0;

  s2: do
        // :: env2sender?send // sanity check for safety monitor
	:: backchannel2sender?a0p -> break
	:: backchannel2sender?a1p
	:: env2sender?mytimeout -> goto s1
      od;

  s3: do
	:: env2sender?send -> break
	:: backchannel2sender?a0p
	:: backchannel2sender?a1p
	:: env2sender?mytimeout 
      od;

  s4: sender2forwchannel!p1;

  s5: do
	:: backchannel2sender?a1p -> goto s0
	:: backchannel2sender?a0p 
	:: env2sender?mytimeout -> goto s4
      od;

}

