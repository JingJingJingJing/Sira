import unittest
import sys
from subprocess import run

src_path = "src/"
sys.path.insert(0, src_path)
from sira import build_parser, extract_values, preprocess_args
#########################################

# sira.exe CLI Test Cases

## Valid Inputs:

class Test_0(unittest.TestCase):
    def setUp(self):
        self.parser = build_parser()

    def test_0(self):
        namespace = self.parser.parse_args("".split(" "))
        extract_values(namespace)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
           "action": None,
           "help": False,
           "verbose": None
        }, kwargs)

    def test_1(self):
        namespace = self.parser.parse_args("-h".split(" "))
        extract_values(namespace)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
           "action": None,
           "help": True,
           "verbose": None
        }, kwargs)

    def test_2(self):
        namespace = self.parser.parse_args("--help".split(" "))
        extract_values(namespace)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
           "action": None,
           "help": True,
           "verbose": None
        }, kwargs)

class Test_1(unittest.TestCase):
    def setUp(self):
        self.parser = build_parser()

    def test_3(self):
        namespace = self.parser.parse_args("-q type=project mode=all".split(" "))
        extract_values(namespace)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "project",
            "mode": "all",
            "verbose": None
        }, kwargs)

    def test_4(self):
        namespace = self.parser.parse_args("-v -q type=project mode=all".split(" "))
        extract_values(namespace)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "project",
            "mode": "all",
            "verbose": True
        }, kwargs)

    def test_5(self):
        namespace = self.parser.parse_args("-vq type=project mode=all".split(" "))
        extract_values(namespace)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "project",
            "mode": "all",
            "verbose": True
        }, kwargs)

    def test_6(self):
        namespace = self.parser.parse_args("-qv type=project mode=all".split(" "))
        extract_values(namespace)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "project",
            "mode": "all",
            "verbose": True
        }, kwargs)

    def test_7(self):
        namespace = self.parser.parse_args("-q -v type=project mode=all".split(" "))
        extract_values(namespace)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "project",
            "mode": "all",
            "verbose": True
        }, kwargs)

    def test_8(self):
        namespace = self.parser.parse_args("-q type=project -v mode=all".split(" "))
        extract_values(namespace)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "project",
            "mode": "all",
            "verbose": True
        }, kwargs)

    def test_9(self):
        namespace = self.parser.parse_args("-q type=project mode=all -v".split(" "))
        extract_values(namespace)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "project",
            "mode": "all",
            "verbose": True
        }, kwargs)

class Test_2(unittest.TestCase):
    def setUp(self):
        self.parser = build_parser()

    def test_10(self):
        namespace = self.parser.parse_args("-q type=project mode=current".split(" "))
        extract_values(namespace)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "project",
            "mode": "current",
            "verbose": None
        }, kwargs)

    def test_11(self):
        namespace = self.parser.parse_args("--query type=project mode=current".split(" "))
        extract_values(namespace)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "project",
            "mode": "current",
            "verbose": None
        }, kwargs)

    def test_12(self):
        namespace = self.parser.parse_args("-v --query type=project mode=current".split(" "))
        extract_values(namespace)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "project",
            "mode": "current",
            "verbose": True
        }, kwargs)

    def test_13(self):
        namespace = self.parser.parse_args("--query -v type=project mode=current".split(" "))
        extract_values(namespace)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "project",
            "mode": "current",
            "verbose": True
        }, kwargs)

    def test_14(self):
        namespace = self.parser.parse_args("--query type=project -v mode=current".split(" "))
        extract_values(namespace)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "project",
            "mode": "current",
            "verbose": True
        }, kwargs)

    def test_15(self):
        namespace = self.parser.parse_args("--query type=project mode=current -v".split(" "))
        extract_values(namespace)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "project",
            "mode": "current",
            "verbose": True
        }, kwargs)

class Test_3(unittest.TestCase):
    def setUp(self):
        self.parser = build_parser()

    def test_16(self):
        namespace = self.parser.parse_args("-q type=project mode=recent".split(" "))
        extract_values(namespace)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "project",
            "mode": "recent",
            "verbose": None
        }, kwargs)

    def test_17(self):
        namespace = self.parser.parse_args("--silent -q type=project mode=recent".split(" "))
        extract_values(namespace)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "project",
            "mode": "recent",
            "verbose": False
        }, kwargs)

    def test_18(self):
        namespace = self.parser.parse_args("-q --silent type=project mode=recent".split(" "))
        extract_values(namespace)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "project",
            "mode": "recent",
            "verbose": False
        }, kwargs)

    def test_19(self):
        namespace = self.parser.parse_args("-q type=project --silent mode=recent".split(" "))
        extract_values(namespace)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "project",
            "mode": "recent",
            "verbose": False
        }, kwargs)

    def test_20(self):
        namespace = self.parser.parse_args("-q type=project mode=recent --silent".split(" "))
        extract_values(namespace)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "project",
            "mode": "recent",
            "verbose": False
        }, kwargs)

class Test_4(unittest.TestCase):
    def setUp(self):
        self.parser = build_parser()

    def test_21(self):
        namespace = self.parser.parse_args("-q type=issue mode=mine".split(" "))
        extract_values(namespace)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "issue",
            "mode": "mine",
            "verbose": None
        }, kwargs)

    def test_22(self):
        namespace = self.parser.parse_args("--query type=issue mode=mine".split(" "))
        extract_values(namespace)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "issue",
            "mode": "mine",
            "verbose": None
        }, kwargs)

    def test_23(self):
        namespace = self.parser.parse_args("--silent --query type=issue mode=mine".split(" "))
        extract_values(namespace)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "issue",
            "mode": "mine",
            "verbose": False
        }, kwargs)

    def test_24(self):
        namespace = self.parser.parse_args("--query --silent type=issue mode=mine".split(" "))
        extract_values(namespace)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "issue",
            "mode": "mine",
            "verbose": False
        }, kwargs)

    def test_25(self):
        namespace = self.parser.parse_args("--query type=issue --silent mode=mine".split(" "))
        extract_values(namespace)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "issue",
            "mode": "mine",
            "verbose": False
        }, kwargs)

    def test_26(self):
        namespace = self.parser.parse_args("--query type=issue mode=mine --silent".split(" "))
        extract_values(namespace)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "issue",
            "mode": "mine",
            "verbose": False
        }, kwargs)

class Test_5(unittest.TestCase):
    def setUp(self):
        self.parser = build_parser()

    def test_27(self):
        namespace = self.parser.parse_args("-q type=issue mode=reported".split(" "))
        extract_values(namespace)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "issue",
            "mode": "reported",
            "verbose": None
        }, kwargs)

    def test_28(self):
        namespace = self.parser.parse_args("-q mode=reported type=issue".split(" "))
        extract_values(namespace)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "issue",
            "mode": "reported",
            "verbose": None
        }, kwargs)

    def test_29(self):
        namespace = self.parser.parse_args("-q type=issue mode=reported limit=0".split(" "))
        extract_values(namespace)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "issue",
            "mode": "reported",
            "verbose": None,
            "limit": 0
        }, kwargs)

    def test_30(self):
        namespace = self.parser.parse_args("-q type=issue mode=reported limit=1".split(" "))
        extract_values(namespace)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "issue",
            "mode": "reported",
            "verbose": None,
            "limit": 1
        }, kwargs)

    def test_31(self):
        namespace = self.parser.parse_args("-q type=issue mode=reported limit=10".split(" "))
        extract_values(namespace)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "issue",
            "mode": "reported",
            "verbose": None,
            "limit": 10
        }, kwargs)

    def test_32(self):
        namespace = self.parser.parse_args("-q type=issue mode=reported limit=100".split(" "))
        extract_values(namespace)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "issue",
            "mode": "reported",
            "verbose": None,
            "limit": 100
        }, kwargs)

    def test_33(self):
        namespace = self.parser.parse_args("-q type=issue mode=reported limit=-2147483649".split(" "))
        extract_values(namespace)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "issue",
            "mode": "reported",
            "verbose": None,
            "limit": -2147483649
        }, kwargs)

    def test_34(self):
        namespace = self.parser.parse_args("-q type=issue mode=reported limit=2147483648".split(" "))
        extract_values(namespace)
        kwargs = vars(namespace)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "issue",
            "mode": "reported",
            "verbose": None,
            "limit": 2147483648
        }, kwargs)

    def test_35(self):
        namespace = self.parser.parse_args("-q type=issue mode=reported order=desc".split(" "))
        extract_values(namespace)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "issue",
            "mode": "reported",
            "verbose": None,
            "order": "desc"
        }, kwargs)


    def test_36(self):
        namespace = self.parser.parse_args("-q type=issue mode=reported order=asc".split(" "))
        extract_values(namespace)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "issue",
            "mode": "reported",
            "verbose": None,
            "order": "asc"
        }, kwargs)

    def test_37(self):
        namespace = self.parser.parse_args("-q type=issue mode=reported limit=10 order=desc".split(" "))
        extract_values(namespace)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "issue",
            "mode": "reported",
            "verbose": None,
            "limit": 10,
            "order": "desc"
        }, kwargs)

    def test_38(self):
        namespace = self.parser.parse_args("-q type=issue mode=reported limit=10 order=asc".split(" "))
        extract_values(namespace)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "issue",
            "mode": "reported",
            "verbose": None,
            "order": "asc"
        }, kwargs)

class Test_6(unittest.TestCase):
    def setUp(self):
        self.parser = build_parser()

    def test_39(self):
        namespace = self.parser.parse_args("-q type=issue".split(" "))
        extract_values(namespace)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "issue",
            "verbose": None
        }, kwargs)

    def test_40(self):
        namespace = self.parser.parse_args("-q type=issue limit=10".split(" "))
        extract_values(namespace)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "issue",
            "limit": 10,
            "verbose": None
        }, kwargs)

    def test_41(self):
        namespace = self.parser.parse_args("-q type=issue order=desc".split(" "))
        extract_values(namespace)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "issue",
            "order": "desc",
            "verbose": None
        }, kwargs)

    def test_42(self):
        namespace = self.parser.parse_args("-q type=issue limit=10 order=desc".split(" "))
        extract_values(namespace)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "issue",
            "limit": 10,
            "order": "desc",
            "verbose": None
        }, kwargs)

class Test_7(unittest.TestCase):
    def setUp(self):
        self.parser = build_parser()

    def test_43(self):
        namespace = self.parser.parse_args("-q type=issue mode=recent".split(" "))
        extract_values(namespace)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "issue",
            "mode": "recent",
            "verbose": None
        }, kwargs)

    def test_44(self):
        namespace = self.parser.parse_args("-q type=issue mode=recent limit=10 order=asc".split(" "))
        extract_values(namespace)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "issue",
            "mode": "recent",
            "limit": 10,
            "order": "asc",
            "verbose": None
        }, kwargs)

    def test_45(self):
        namespace = self.parser.parse_args("-q type=issue mode=recent order=asc limit=10".split(" "))
        extract_values(namespace)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "issue",
            "mode": "recent",
            "limit": 10,
            "order": "asc",
            "verbose": None
        }, kwargs)

    def test_46(self):
        namespace = self.parser.parse_args("-q type=issue limit=10 mode=recent order=asc".split(" "))
        extract_values(namespace)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "issue",
            "mode": "recent",
            "limit": 10,
            "order": "asc",
            "verbose": None
        }, kwargs)

    def test_47(self):
        namespace = self.parser.parse_args("-q type=issue limit=10 order=asc mode=recent".split(" "))
        extract_values(namespace)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "issue",
            "mode": "recent",
            "limit": 10,
            "order": "asc",
            "verbose": None
        }, kwargs)

    def test_48(self):
        namespace = self.parser.parse_args("-q type=issue order=asc mode=recent limit=10".split(" "))
        extract_values(namespace)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "issue",
            "mode": "recent",
            "limit": 10,
            "order": "asc",
            "verbose": None
        }, kwargs)

    def test_49(self):
        namespace = self.parser.parse_args("-q type=issue order=asc limit=10 mode=recent".split(" "))
        extract_values(namespace)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "issue",
            "mode": "recent",
            "limit": 10,
            "order": "asc",
            "verbose": None
        }, kwargs)

    def test_50(self):
        namespace = self.parser.parse_args("-q mode=recent type=issue limit=10 order=asc".split(" "))
        extract_values(namespace)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "issue",
            "mode": "recent",
            "limit": 10,
            "order": "asc",
            "verbose": None
        }, kwargs)

    def test_51(self):
        namespace = self.parser.parse_args("-q limit=10 type=issue mode=recent order=asc".split(" "))
        extract_values(namespace)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "issue",
            "mode": "recent",
            "limit": 10,
            "order": "asc",
            "verbose": None
        }, kwargs)

    def test_52(self):
        namespace = self.parser.parse_args("-q order=asc type=issue mode=recent limit=10".split(" "))
        extract_values(namespace)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "issue",
            "mode": "recent",
            "limit": 10,
            "order": "asc",
            "verbose": None
        }, kwargs)

    def test_53(self):
        namespace = self.parser.parse_args("-q mode=recent limit=10 order=asc type=issue".split(" "))
        extract_values(namespace)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "issue",
            "mode": "recent",
            "limit": 10,
            "order": "asc",
            "verbose": None
        }, kwargs)

    def test_54(self):
        namespace = self.parser.parse_args("-q limit=10 mode=recent order=asc type=issue".split(" "))
        extract_values(namespace)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "issue",
            "mode": "recent",
            "limit": 10,
            "order": "asc",
            "verbose": None
        }, kwargs)

    def test_55(self):
        namespace = self.parser.parse_args("-q order=asc mode=recent limit=10 type=issue".split(" "))
        extract_values(namespace)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "issue",
            "mode": "recent",
            "limit": 10,
            "order": "asc",
            "verbose": None
        }, kwargs)

class Test_8(unittest.TestCase):
    def setUp(self):
        self.parser = build_parser()

    def test_56(self):
        namespace = self.parser.parse_args("-q type=issue mode=board key=2".split(" "))
        extract_values(namespace)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "issue",
            "mode": "board",
            "key": 2,
            "verbose": None
        }, kwargs)

    def test_57(self):
        namespace = self.parser.parse_args("-q type=issue mode=board limit=10 order=asc key=2".split(" "))
        extract_values(namespace)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "issue",
            "mode": "board",
            "limit": 10,
            "order": "asc",
            "key": 2,
            "verbose": None
        }, kwargs)

    def test_58(self):
        namespace = self.parser.parse_args("-qv type=issue -s mode=board limit=10 order=asc key=2".split(" "))
        extract_values(namespace)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "issue",
            "mode": "board",
            "limit": 10,
            "order": "asc",
            "key": 2,
            "verbose": False
        }, kwargs)

    def test_59(self):
        namespace = self.parser.parse_args("-qvsvs type=issue mode=board limit=10 order=asc key=2".split(" "))
        extract_values(namespace)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "issue",
            "mode": "board",
            "limit": 10,
            "order": "asc",
            "key": 2,
            "verbose": False
        }, kwargs)

    def test_60(self):
        namespace = self.parser.parse_args("-qv type=issue mode=board limit=10 order=asc -s key=2".split(" "))
        extract_values(namespace)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "issue",
            "mode": "board",
            "limit": 10,
            "order": "asc",
            "key": 2,
            "verbose": False
        }, kwargs)

    def test_61(self):
        namespace = self.parser.parse_args("-qv type=issue -v mode=board -v limit=10 -v order=asc -s key=2".split(" "))
        extract_values(namespace)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "issue",
            "mode": "board",
            "limit": 10,
            "order": "asc",
            "key": 2,
            "verbose": False
        }, kwargs)

    def test_62(self):
        namespace = self.parser.parse_args("-sq type=issue --verbose mode=board limit=10 order=asc key=2".split(" "))
        extract_values(namespace)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "issue",
            "mode": "board",
            "limit": 10,
            "order": "asc",
            "key": 2,
            "verbose": True
        }, kwargs)

    def test_63(self):
        namespace = self.parser.parse_args("-sq --verbose --silent --verbose type=issue mode=board limit=10 order=asc key=2".split(" "))
        extract_values(namespace)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "issue",
            "mode": "board",
            "limit": 10,
            "order": "asc",
            "key": 2,
            "verbose": True
        }, kwargs)

    def test_64(self):
        namespace = self.parser.parse_args("-sq type=issue mode=board limit=10 order=asc --verbose key=2".split(" "))
        extract_values(namespace)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "issue",
            "mode": "board",
            "limit": 10,
            "order": "asc",
            "key": 2,
            "verbose": True
        }, kwargs)

    def test_65(self):
        namespace = self.parser.parse_args("-sq type=issue --silent mode=board --silent limit=10 --silent order=asc --verbose key=2".split(" "))
        extract_values(namespace)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "issue",
            "mode": "board",
            "limit": 10,
            "order": "asc",
            "key": 2,
            "verbose": True
        }, kwargs)

    def test_66(self):
        namespace = self.parser.parse_args("-q type=issue mode=mine mode=board limit=10 order=asc key=2".split(" "))
        extract_values(namespace)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "issue",
            "mode": "board",
            "limit": 10,
            "order": "asc",
            "key": 2,
            "verbose": None
        }, kwargs)

    def test_67(self):
        namespace = self.parser.parse_args("-q type=issue mode=mine limit=10 order=asc mode=board key=2".split(" "))
        extract_values(namespace)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "issue",
            "mode": "board",
            "limit": 10,
            "order": "asc",
            "key": 2,
            "verbose": None
        }, kwargs)

    def test_68(self):
        namespace = self.parser.parse_args("-q type=issue mode=board limit=1 limit=10 order=asc key=2".split(" "))
        extract_values(namespace)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "issue",
            "mode": "board",
            "limit": 10,
            "order": "asc",
            "key": 2,
            "verbose": None
        }, kwargs)

    def test_69(self):
        namespace = self.parser.parse_args("-q type=issue mode=board limit=10 order=desc order=asc key=2".split(" "))
        extract_values(namespace)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "issue",
            "mode": "board",
            "limit": 10,
            "order": "asc",
            "key": 2,
            "verbose": None
        }, kwargs)

    def test_70(self):
        namespace = self.parser.parse_args("-q type=issue mode=reported limit=100 order=desc mode=board limit=10 order=asc key=2".split(" "))
        extract_values(namespace)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "issue",
            "mode": "board",
            "limit": 10,
            "order": "asc",
            "key": 2,
            "verbose": None
        }, kwargs)

    def test_71(self):
        namespace = self.parser.parse_args("-q type=issue -q type=issue mode=board limit=10 order=asc key=2".split(" "))
        extract_values(namespace)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "issue",
            "mode": "board",
            "limit": 10,
            "order": "asc",
            "key": 2,
            "verbose": None
        }, kwargs)

class Test_9(unittest.TestCase):
    def setUp(self):
        self.parser = build_parser()

    def test_72(self):
        namespace = self.parser.parse_args("-q type=board".split(" "))
        extract_values(namespace)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "board",
            "verbose": None
        }, kwargs)

    def test_73(self):
        namespace = self.parser.parse_args("-q type=board key=52".split(" "))
        extract_values(namespace)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "board",
            "verbose": None,
            "key": 52
        }, kwargs)

    def test_74(self):
        namespace = self.parser.parse_args("-q type=board limit=12 key=52".split(" "))
        extract_values(namespace)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "board",
            "verbose": None,
            "key": 52,
            "limit": 12
        }, kwargs)

    def test_75(self):
        namespace = self.parser.parse_args("-q order=desc type=board limit=12 key=52".split(" "))
        extract_values(namespace)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "board",
            "verbose": None,
            "key": 52,
            "limit": 12
        }, kwargs)

    def test_76(self):
        namespace = self.parser.parse_args("limit=12 -q type=board".split(" "))
        extract_values(namespace)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "board",
            "verbose": None
        }, kwargs)

    def test_77(self):
        namespace = self.parser.parse_args("ccc=yyy --query mode=all type=board -v -q type=board key=52".split(" "))
        extract_values(namespace)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "board",
            "verbose": True,
            "key": 52
        }, kwargs)

    def test_78(self):
        namespace = self.parser.parse_args("xxx=yyy --silent -q --verbose --query type=key type=issue key=23".split(" "))
        extract_values(namespace)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "issue",
            "verbose": True,
            "key": 23
        }, kwargs)

## Ambiguous Inputs:

class Test_10(unittest.TestCase):
    def setUp(self):
        self.parser = build_parser()

### help manual

class Test_11(unittest.TestCase):
    def setUp(self):
        self.parser = build_parser()

    def test_79(self):
        namespace = self.parser.parse_args("-v".split(" "))
        extract_values(namespace)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": None,
            "help": False,
            "verbose": True
        }, kwargs)

### verbose help

class Test_12(unittest.TestCase):
    def setUp(self):
        self.parser = build_parser()

    def test_80(self):
        namespace = self.parser.parse_args("-vh".split(" "))
        extract_values(namespace)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": None,
            "help": True,
            "verbose": True
        }, kwargs)

### verbose help

class Test_13(unittest.TestCase):
    def setUp(self):
        self.parser = build_parser()

    def test_81(self):
        namespace = self.parser.parse_args("-hv".split(" "))
        extract_values(namespace)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": None,
            "help": True,
            "verbose": True
        }, kwargs)
### help manual

class Test_14(unittest.TestCase):
    def setUp(self):
        self.parser = build_parser()

    def test_82(self):
        namespace = self.parser.parse_args("-s".split(" "))
        extract_values(namespace)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": None,
            "help": False,
            "verbose": True
        }, kwargs)

### help manual

class Test_15(unittest.TestCase):
    def setUp(self):
        self.parser = build_parser()

    def test_83(self):
        namespace = self.parser.parse_args("-vsvsvss".split(" "))
        extract_values(namespace)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": None,
            "help": False,
            "verbose": False
        }, kwargs)

### floot

class Test_16(unittest.TestCase):
    def setUp(self):
        self.parser = build_parser()

    def test_84(self):
        namespace = self.parser.parse_args("-q type=issue mode=reported limit=1.0".split(" "))
        extract_values(namespace)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "issue",
            "mode": "reported",
            "limit": 1,
            "verbose": None
        }, kwargs)

### discard invalid keys

class Test_17(unittest.TestCase):
    def setUp(self):
        self.parser = build_parser()

    def test_85(self):
        namespace = self.parser.parse_args("-q xxx=yyy type=issue yyy=xxx".split(" "))
        extract_values(namespace)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "issue",
            "verbose": None
        }, kwargs)

## Invalid Inputs:

class Test_18(unittest.TestCase):
    def setUp(self):
        self.parser = build_parser()

class Test_19(unittest.TestCase):
    def setUp(self):
        self.parser = build_parser()

    def test_86(self):
        with self.assertRaises(SystemExit) as se:
            namespace = self.parser.parse_args("-x".split(" "))
            extract_values(namespace)
            kwargs = vars(namespace)
        self.assertEqual(2, se.exception.code)
            

    def test_87(self):
        with self.assertRaises(SystemExit) as se:
            namespace = self.parser.parse_args("-qx".split(" "))
            extract_values(namespace)
            kwargs = vars(namespace)
        self.assertEqual(2, se.exception.code)

    def test_88(self):
        with self.assertRaises(SystemExit) as se:
            namespace = self.parser.parse_args("--xxx".split(" "))
            extract_values(namespace)
            kwargs = vars(namespace)
        self.assertEqual(2, se.exception.code)
        
    # valid but print help

    def test_89(self):
        namespace = self.parser.parse_args("xxx".split(" "))
        extract_values(namespace)
        kwargs = vars(namespace)

class Test_20(unittest.TestCase):
    def setUp(self):
        self.parser = build_parser()

    def test_90(self):
        namespace = self.parser.parse_args("-v -q type=xxx".split(" "))
        extract_values(namespace)
        kwargs = vars(namespace)

    def test_91(self):
        namespace = self.parser.parse_args("-v -q type=project".split(" "))
        extract_values(namespace)
        kwargs = vars(namespace)

    def test_92(self):
        namespace = self.parser.parse_args("-v -q type=project mode=xxx".split(" "))
        extract_values(namespace)
        kwargs = vars(namespace)

    def test_93(self):
        namespace = self.parser.parse_args("-v -q type=project mode=current limit=xxx".split(" "))
        extract_values(namespace)
        kwargs = vars(namespace)

    def test_94(self):
        namespace = self.parser.parse_args("-v -q type=project mode=current order=xxx".split(" "))
        extract_values(namespace)
        kwargs = vars(namespace)

class Test_21(unittest.TestCase):
    def setUp(self):
        self.parser = build_parser()

    def test_95(self):
        namespace = self.parser.parse_args("-v -q type=issue mode=all".split(" "))
        extract_values(namespace)
        kwargs = vars(namespace)

    def test_96(self):
        namespace = self.parser.parse_args("-v mode=all -q type=project".split(" "))
        extract_values(namespace)
        kwargs = vars(namespace)

    def test_97(self):
        namespace = self.parser.parse_args("-v -q type=project mode=board".split(" "))
        extract_values(namespace)
        kwargs = vars(namespace)

    def test_98(self):
        namespace = self.parser.parse_args("-v -q type=project mode=board key=xxx".split(" "))
        extract_values(namespace)
        kwargs = vars(namespace)

class Test_22(unittest.TestCase):
    def setUp(self):
        self.parser = build_parser()

    def test_99(self):
        namespace = self.parser.parse_args("-v -q type=board key=xxx".split(" "))
        extract_values(namespace)
        kwargs = vars(namespace)


def main():
    unittest.main()

if __name__ == '__main__':
    main()
