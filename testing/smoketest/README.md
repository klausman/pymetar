# Smoke Test for pymetar

`runtest.sh` handles all the dirty work for you, except unpacking the reports
(see below)

This is just a smoke test, i.e. run the parser against a large set of reports,
all `getXYZ()` functions are called. The data is *not validated.*

Note that the reports to be used need to be unpacked first. Just run 
`tar xzf reports.tgz` in this directory  and it should unpack into the right
spot. 

