
active proctype Env()
{
  do
  :: env2sender!send; env_after_send: env2safetymon!send
  :: env2sender!mytimeout 
  :: receiver2env?deliver; env_after_deliver: env2safetymon!deliver
  od
}


