# Triggers_Top_100
SELECT 
  g.name "主机群组",
  h.name "主机",
  t.description "触发器",
  COUNT(DISTINCT e.eventid) AS "cnt_event 状态改变次数" 
FROM
  zabbix.events e,
  zabbix.triggers t,
  zabbix.functions f,
  zabbix.items i,
  zabbix.hosts_groups hgg,
  zabbix.hosts h,
  zabbix.groups g 
WHERE t.triggerid = e.objectid 
  AND e.clock >= UNIX_TIMESTAMP('2017-05-01 00:00:00') 
  AND e.clock <  UNIX_TIMESTAMP('2017-06-01 00:00:00') 
  AND e.source = 0 # 0 - event created by a trigger; 
  AND e.object = 0 # 0 - trigger; 
  AND t.triggerid = f.triggerid 
  AND f.itemid = i.itemid 
  AND i.hostid = hgg.hostid 
  AND h.hostid = hgg.hostid 
  AND g.groupid = hgg.groupid 
  AND g.name LIKE '%ka%' 
  AND h.name LIKE '%app%' 
GROUP BY g.name,h.name,t.description 
ORDER BY g.name,h.name,t.description ;
