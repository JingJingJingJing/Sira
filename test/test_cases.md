# sira.exe CLI Test Cases

## Valid Inputs:

`sira.exe`

`sira.exe -h`

`sira.exe --help`

-----------------------------------------------------------

`sira.exe -q type=project mode=all`

`sira.exe -v -q type=project mode=all`

`sira.exe -vq type=project mode=all`

`sira.exe -qv type=project mode=all`

`sira.exe -q -v type=project mode=all`

`sira.exe -q type=project -v mode=all`

`sira.exe -q type=project mode=all -v`

-----------------------------------------------------------

`sira.exe -q type=project mode=current`

`sira.exe --query type=project mode=current`

`sira.exe -v --query type=project mode=current`

`sira.exe --query -v type=project mode=current`

`sira.exe --query type=project -v mode=current`

`sira.exe --query type=project mode=current -v`

-----------------------------------------------------------

`sira.exe -q type=project mode=recent`

`sira.exe --silent -q type=project mode=recent`

`sira.exe -q --silent type=project mode=recent`

`sira.exe -q type=project --silent mode=recent`

`sira.exe -q type=project mode=recent --silent`

-----------------------------------------------------------

`sira.exe -q type=issue mode=mine`

`sira.exe --query type=issue mode=mine`

`sira.exe --silent --query type=issue mode=mine`

`sira.exe --query --silent type=issue mode=mine`

`sira.exe --query type=issue --silent mode=mine`

`sira.exe --query type=issue mode=mine --silent`

-----------------------------------------------------------

`sira.exe -q type=issue mode=reported`

`sira.exe -q mode=reported type=issue`

`sira.exe -q type=issue mode=reported limit=0`

`sira.exe -q type=issue mode=reported limit=1`

`sira.exe -q type=issue mode=reported limit=10`

`sira.exe -q type=issue mode=reported limit=100`

`sira.exe -q type=issue mode=reported limit=2147483647`

`sira.exe -q type=issue mode=reported limit=2147483648`

`sira.exe -q type=issue mode=reported order=desc`

`sira.exe -q type=issue mode=reported order=asc`

`sira.exe -q type=issue mode=reported limit=10 order=desc`

`sira.exe -q type=issue mode=reported limit=10 order=asc`

-----------------------------------------------------------

`sira.exe -q type=issue`

`sira.exe -q type=issue limit=10`

`sira.exe -q type=issue order=desc`

`sira.exe -q type=issue limit=10 order=desc`

-----------------------------------------------------------

`sira.exe -q type=issue mode=recent`

`sira.exe -q type=issue mode=recent limit=10 order=asc`

`sira.exe -q type=issue mode=recent order=asc limit=10`

`sira.exe -q type=issue limit=10 mode=recent order=asc`

`sira.exe -q type=issue limit=10 order=asc mode=recent`

`sira.exe -q type=issue order=asc mode=recent limit=10`

`sira.exe -q type=issue order=asc limit=10 mode=recent`

`sira.exe -q mode=recent type=issue limit=10 order=asc`

`sira.exe -q limit=10 type=issue mode=recent order=asc`

`sira.exe -q order=asc type=issue mode=recent limit=10`

`sira.exe -q mode=recent limit=10 order=asc type=issue`

`sira.exe -q limit=10 mode=recent order=asc type=issue`

`sira.exe -q order=asc mode=recent limit=10 type=issue`

-----------------------------------------------------------

`sira.exe -q type=issue mode=board key=2`

`sira.exe -q type=issue mode=board limit=10 order=asc key=2`

`sira.exe -qv type=issue -s mode=board limit=10 order=asc key=2`

`sira.exe -qvsvs type=issue mode=board limit=10 order=asc key=2`

`sira.exe -qv type=issue mode=board limit=10 order=asc -s key=2`

`sira.exe -qv type=issue -v mode=board -v limit=10 -v order=asc -s key=2`

`sira.exe -sq type=issue --verbose mode=board limit=10 order=asc key=2`

`sira.exe -sq --verbose --silent --verbose type=issue mode=board limit=10 order=asc key=2`

`sira.exe -sq type=issue mode=board limit=10 order=asc --verbose key=2`

`sira.exe -sq type=issue --silent mode=board --silent limit=10 --silent order=asc --verbose key=2`

`sira.exe -q type=issue mode=mine mode=board limit=10 order=asc key=2`

`sira.exe -q type=issue mode=mine limit=10 order=asc mode=board key=2`

`sira.exe -q type=issue mode=board limit=1 limit=10 order=asc key=2`

`sira.exe -q type=issue mode=board limit=10 order=desc order=asc key=2`

`sira.exe -q type=issue mode=reported limit=100 order=desc mode=board limit=10 order=asc key=2`

`sira.exe -q type=issue -q type=issue mode=board limit=10 order=asc key=2`

-----------------------------------------------------------

`sira.exe -q type=board`

`sira.exe -q type=board key=52`

`sira.exe -q type=board limit=12 key=52`

`sira.exe -q order=desc type=board limit=12 key=52`

`sira.exe limit=12 -q type=board`

`sira.exe ccc=yyy --query mode=all type=board -v -q type=board key=52`

`sira.exe xxx=yyy --silent -q --verbose --query type=key type=issue key=23`

## Ambiguous Inputs:

### help manual
`sira.exe -v`

### verbose help
`sira.exe -vh`

### verbose help
`sira.exe -hv`

### help manual
`sira.exe -s`

### help manual
`sira.exe -vs[...]`

### floot
`sira.exe -q type=issue mode=reported limit=1.0`

### discard invalid keys
`sira.exe -q xxx=yyy type=issue yyy=xxx`

## Invalid Inputs:

-----------------------------------------------------------

`sira.exe -x`

`sira.exe -qx`

`sira.exe --xxx`

`sira.exe xxx`

-----------------------------------------------------------

`sira.exe -v -q type=xxx`

`sira.exe -v -q type=project`

`sira.exe -v -q type=project mode=xxx`

`sira.exe -v -q type=project mode=current limit=xxx`

`sira.exe -v -q type=project mode=current order=xxx`

-----------------------------------------------------------

`sira.exe -v -q type=issue mode=all`

`sira.exe -v mode=all -q type=project`

`sira.exe -v -q type=project mode=board`

`sira.exe -v -q type=project mode=board key=xxx`

-----------------------------------------------------------

`sira.exe -v -q type=board key=xxx`

-----------------------------------------------------------
`sira.exe -i/-init`