# Contributing

If you have any issues or ideas for improvement you can send me an email to _thl-cmk[at]outlook[dot]com_.

For some fixes/improvements I migth need a _snmpwalk_ from the device in question.
This must contain

- .1.3.6.1.2.1.1.1 sysDescr 
- .1.3.6.1.2.1.1.2 sysObjectID

and all the SNMP OIDs used in the plugin.

If you run the _snmpwalk_ command, please uses these options _**-ObentU**_ in addition to your snmp options like community, version etc.
For example:
```
snmpwalk -v2c -c public -ObentU 10.10.10.10 .1.3.6.1.2.1.1.1 > hostname.snmpwalk
snmpwalk -v2c -c public -ObentU 10.10.10.10 .1.3.6.1.2.1.1.2 >> hostname.snmpwalk
snmpwalk -v2c -c public -ObentU 10.10.10.10 .1.3.6.1.2.1.197 >> hostname.snmpwalk
```
