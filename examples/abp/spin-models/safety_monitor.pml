
active proctype SafetyMonitor()
{
  sm0: if
	:: env2safetymon?send
	:: env2safetymon?deliver -> assert(0)
       fi;

  sm1: if
	:: env2safetymon?deliver -> goto sm0
	:: env2safetymon?send -> assert(0)
       fi;

  // atomic { !p -> assert(p) } 
}

