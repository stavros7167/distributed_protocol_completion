

mtype = { send, mytimeout, deliver, p0, p1, p0p, p1p, a0, a1, a0p, a1p };

// mtype_env2sender = { mysend, mytimeout };
// mtype_receiver2env = { deliver };
// mtype_sender2forwchannel = { p0, p1 };
// mtype_forwchannel2receiver = { p0p, p1p };
// mtype_receiver2backchannel = { a0, a1 };
// mtype_backchannel2sender = { a0p, a1p };

chan env2sender = [0] of { mtype};
chan receiver2env = [0] of { mtype};
chan sender2forwchannel = [0] of { mtype};
chan forwchannel2receiver = [0] of { mtype};
chan receiver2backchannel = [0] of { mtype};
chan backchannel2sender = [0] of { mtype};

chan env2safetymon = [0] of { mtype };

#include "env.pml"

#include "forward_channel.pml"
#include "backward_channel.pml"

#include "sender1.pml"
#include "receiver1.pml"

#include "safety_monitor.pml"

#include "liveness1.pml" // defines "deliver_follows_send" LTL formula
// the property below does not hold on its own, because channels might always
// lose messages
ltl liveness_property { deliver_follows_send }

