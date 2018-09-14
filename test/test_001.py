import unittest
import sys
import keyring
import json
from subprocess import run
src_path = "src/"
sys.path.insert(0, src_path)
from sira import build_parser, extract_values, preprocess_args, process, initUser
from config import read_from_config 

#########################################

# sira.exe CLI Test Cases

## Valid Inputs:

class Test_0(unittest.TestCase):
    def setUp(self):
        self.parser = build_parser()

    def test_0(self):
        args = "".split(" ")
        preprocess_args(args)
        namespace = self.parser.parse_args(args)
        verbose = getattr(namespace, "verbose")
        extract_values(namespace, verbose)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
           "action": None,
           "help": False,
           "verbose": None
        }, kwargs)
        with self.assertRaises(SystemExit) as se:
            process(namespace, self.parser, verbose)
        self.assertEqual(0, se.exception.code)

    def test_1(self):
        args = "-h".split(" ")
        preprocess_args(args)
        namespace = self.parser.parse_args(args)
        verbose = getattr(namespace, "verbose")
        extract_values(namespace, verbose)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
           "action": None,
           "help": True,
           "verbose": None
        }, kwargs)
        with self.assertRaises(SystemExit) as se:
            process(namespace, self.parser, verbose)
        self.assertEqual(0, se.exception.code)

    def test_2(self):
        args = "--help".split(" ")
        preprocess_args(args)
        namespace = self.parser.parse_args(args)
        verbose = getattr(namespace, "verbose")
        extract_values(namespace, verbose)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
           "action": None,
           "help": True,
           "verbose": None
        }, kwargs)
        with self.assertRaises(SystemExit) as se:
            process(namespace, self.parser, verbose)
        self.assertEqual(0, se.exception.code)

class Test_1(unittest.TestCase):
    def setUp(self):
        self.parser = build_parser()

    def test_3(self):
        args = "-q type=project mode=all".split(" ")
        preprocess_args(args)
        namespace = self.parser.parse_args(args)
        verbose = getattr(namespace, "verbose")
        extract_values(namespace, verbose)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "project",
            "mode": "all",
            "verbose": None
        }, kwargs)
        command = process(namespace, self.parser, verbose)
        self.assertEqual("sira-query project -f", command)

    def test_4(self):
        args = "-v -q type=project mode=all".split(" ")
        preprocess_args(args)
        namespace = self.parser.parse_args(args)
        verbose = getattr(namespace, "verbose")
        extract_values(namespace, verbose)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "project",
            "mode": "all",
            "verbose": True
        }, kwargs)
        command = process(namespace, self.parser, verbose)
        self.assertEqual("sira-query project -v -f", command)

    def test_5(self):
        args = "-vq type=project mode=all".split(" ")
        preprocess_args(args)
        namespace = self.parser.parse_args(args)
        verbose = getattr(namespace, "verbose")
        extract_values(namespace, verbose)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "project",
            "mode": "all",
            "verbose": True
        }, kwargs)
        command = process(namespace, self.parser, verbose)
        self.assertEqual("sira-query project -v -f", command)

    def test_6(self):
        args = "-qv type=project mode=all".split(" ")
        preprocess_args(args)
        namespace = self.parser.parse_args(args)
        verbose = getattr(namespace, "verbose")
        extract_values(namespace, verbose)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "project",
            "mode": "all",
            "verbose": True
        }, kwargs)
        command = process(namespace, self.parser, verbose)
        self.assertEqual("sira-query project -v -f", command)

    def test_7(self):
        args = "-q -v type=project mode=all".split(" ")
        preprocess_args(args)
        namespace = self.parser.parse_args(args)
        verbose = getattr(namespace, "verbose")
        extract_values(namespace, verbose)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "project",
            "mode": "all",
            "verbose": True
        }, kwargs)
        command = process(namespace, self.parser, verbose)
        self.assertEqual("sira-query project -v -f", command)

    def test_8(self):
        args = "-q type=project -v mode=all".split(" ")
        preprocess_args(args)
        namespace = self.parser.parse_args(args)
        verbose = getattr(namespace, "verbose")
        extract_values(namespace, verbose)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "project",
            "mode": "all",
            "verbose": True
        }, kwargs)
        command = process(namespace, self.parser, verbose)
        self.assertEqual("sira-query project -v -f", command)

    def test_9(self):
        args = "-q type=project mode=all -v".split(" ")
        preprocess_args(args)
        namespace = self.parser.parse_args(args)
        verbose = getattr(namespace, "verbose")
        extract_values(namespace, verbose)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "project",
            "mode": "all",
            "verbose": True
        }, kwargs)
        command = process(namespace, self.parser, verbose)
        self.assertEqual("sira-query project -v -f", command)

class Test_2(unittest.TestCase):
    def setUp(self):
        self.parser = build_parser()

    def test_10(self):
        args = "-q type=project mode=current".split(" ")
        preprocess_args(args)
        namespace = self.parser.parse_args(args)
        verbose = getattr(namespace, "verbose")
        extract_values(namespace, verbose)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "project",
            "mode": "current",
            "verbose": None
        }, kwargs)
        command = process(namespace, self.parser, verbose)
        self.assertEqual("sira-query project -l 1 -f", command)

    def test_11(self):
        args = "--query type=project mode=current".split(" ")
        preprocess_args(args)
        namespace = self.parser.parse_args(args)
        verbose = getattr(namespace, "verbose")
        extract_values(namespace, verbose)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "project",
            "mode": "current",
            "verbose": None
        }, kwargs)
        command = process(namespace, self.parser, verbose)
        self.assertEqual("sira-query project -l 1 -f", command)

    def test_12(self):
        args = "-v --query type=project mode=current".split(" ")
        preprocess_args(args)
        namespace = self.parser.parse_args(args)
        verbose = getattr(namespace, "verbose")
        extract_values(namespace, verbose)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "project",
            "mode": "current",
            "verbose": True
        }, kwargs)
        command = process(namespace, self.parser, verbose)
        self.assertEqual("sira-query project -l 1 -v -f", command)

    def test_13(self):
        args = "--query -v type=project mode=current".split(" ")
        preprocess_args(args)
        namespace = self.parser.parse_args(args)
        verbose = getattr(namespace, "verbose")
        extract_values(namespace, verbose)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "project",
            "mode": "current",
            "verbose": True
        }, kwargs)
        command = process(namespace, self.parser, verbose)
        self.assertEqual("sira-query project -l 1 -v -f", command)

    def test_14(self):
        args = "--query type=project -v mode=current".split(" ")
        preprocess_args(args)
        namespace = self.parser.parse_args(args)
        verbose = getattr(namespace, "verbose")
        extract_values(namespace, verbose)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "project",
            "mode": "current",
            "verbose": True
        }, kwargs)
        command = process(namespace, self.parser, verbose)
        self.assertEqual("sira-query project -l 1 -v -f", command)

    def test_15(self):
        args = "--query type=project mode=current -v".split(" ")
        preprocess_args(args)
        namespace = self.parser.parse_args(args)
        verbose = getattr(namespace, "verbose")
        extract_values(namespace, verbose)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "project",
            "mode": "current",
            "verbose": True
        }, kwargs)
        command = process(namespace, self.parser, verbose)
        self.assertEqual("sira-query project -l 1 -v -f", command)

class Test_3(unittest.TestCase):
    def setUp(self):
        self.parser = build_parser()

    def test_16(self):
        args = "-q type=project mode=recent".split(" ")
        preprocess_args(args)
        namespace = self.parser.parse_args(args)
        verbose = getattr(namespace, "verbose")
        extract_values(namespace, verbose)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "project",
            "mode": "recent",
            "verbose": None
        }, kwargs)
        command = process(namespace, self.parser, verbose)
        self.assertEqual("sira-query project -o recent -f", command)

    def test_17(self):
        args = "--silent -q type=project mode=recent".split(" ")
        preprocess_args(args)
        namespace = self.parser.parse_args(args)
        verbose = getattr(namespace, "verbose")
        extract_values(namespace, verbose)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "project",
            "mode": "recent",
            "verbose": False
        }, kwargs)
        command = process(namespace, self.parser, verbose)
        self.assertEqual("sira-query project -o recent -s -f", command)

    def test_18(self):
        args = "-q --silent type=project mode=recent".split(" ")
        preprocess_args(args)
        namespace = self.parser.parse_args(args)
        verbose = getattr(namespace, "verbose")
        extract_values(namespace, verbose)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "project",
            "mode": "recent",
            "verbose": False
        }, kwargs)
        command = process(namespace, self.parser, verbose)
        self.assertEqual("sira-query project -o recent -s -f", command)

    def test_19(self):
        args = "-q type=project --silent mode=recent".split(" ")
        preprocess_args(args)
        namespace = self.parser.parse_args(args)
        verbose = getattr(namespace, "verbose")
        extract_values(namespace, verbose)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "project",
            "mode": "recent",
            "verbose": False
        }, kwargs)
        command = process(namespace, self.parser, verbose)
        self.assertEqual("sira-query project -o recent -s -f", command)

    def test_20(self):
        args = "-q type=project mode=recent --silent".split(" ")
        preprocess_args(args)
        namespace = self.parser.parse_args(args)
        verbose = getattr(namespace, "verbose")
        extract_values(namespace, verbose)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "project",
            "mode": "recent",
            "verbose": False
        }, kwargs)
        command = process(namespace, self.parser, verbose)
        self.assertEqual("sira-query project -o recent -s -f", command)

class Test_4(unittest.TestCase):
    def setUp(self):
        self.parser = build_parser()

    def test_21(self):
        args = "-q type=issue mode=mine".split(" ")
        preprocess_args(args)
        namespace = self.parser.parse_args(args)
        verbose = getattr(namespace, "verbose")
        extract_values(namespace, verbose)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "issue",
            "mode": "mine",
            "verbose": None
        }, kwargs)
        command = process(namespace, self.parser, verbose)
        self.assertEqual("sira-query issue -a mine -f", command)

    def test_22(self):
        args = "--query type=issue mode=mine".split(" ")
        preprocess_args(args)
        namespace = self.parser.parse_args(args)
        verbose = getattr(namespace, "verbose")
        extract_values(namespace, verbose)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "issue",
            "mode": "mine",
            "verbose": None
        }, kwargs)
        command = process(namespace, self.parser, verbose)
        self.assertEqual("sira-query issue -a mine -f", command)

    def test_23(self):
        args = "--silent --query type=issue mode=mine".split(" ")
        preprocess_args(args)
        namespace = self.parser.parse_args(args)
        verbose = getattr(namespace, "verbose")
        extract_values(namespace, verbose)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "issue",
            "mode": "mine",
            "verbose": False
        }, kwargs)
        command = process(namespace, self.parser, verbose)
        self.assertEqual("sira-query issue -a mine -s -f", command)

    def test_24(self):
        args = "--query --silent type=issue mode=mine".split(" ")
        preprocess_args(args)
        namespace = self.parser.parse_args(args)
        verbose = getattr(namespace, "verbose")
        extract_values(namespace, verbose)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "issue",
            "mode": "mine",
            "verbose": False
        }, kwargs)
        command = process(namespace, self.parser, verbose)
        self.assertEqual("sira-query issue -a mine -s -f", command)

    def test_25(self):
        args = "--query type=issue --silent mode=mine".split(" ")
        preprocess_args(args)
        namespace = self.parser.parse_args(args)
        verbose = getattr(namespace, "verbose")
        extract_values(namespace, verbose)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "issue",
            "mode": "mine",
            "verbose": False
        }, kwargs)
        command = process(namespace, self.parser, verbose)
        self.assertEqual("sira-query issue -a mine -s -f", command)

    def test_26(self):
        args = "--query type=issue mode=mine --silent".split(" ")
        preprocess_args(args)
        namespace = self.parser.parse_args(args)
        verbose = getattr(namespace, "verbose")
        extract_values(namespace, verbose)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "issue",
            "mode": "mine",
            "verbose": False
        }, kwargs)
        command = process(namespace, self.parser, verbose)
        self.assertEqual("sira-query issue -a mine -s -f", command)

class Test_5(unittest.TestCase):
    def setUp(self):
        self.parser = build_parser()

    def test_27(self):
        args = "-q type=issue mode=reported".split(" ")
        preprocess_args(args)
        namespace = self.parser.parse_args(args)
        verbose = getattr(namespace, "verbose")
        extract_values(namespace, verbose)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "issue",
            "mode": "reported",
            "verbose": None
        }, kwargs)
        command = process(namespace, self.parser, verbose)
        self.assertEqual("sira-query issue -r mine -f", command)

    def test_28(self):
        args = "-q mode=reported type=issue".split(" ")
        preprocess_args(args)
        namespace = self.parser.parse_args(args)
        verbose = getattr(namespace, "verbose")
        extract_values(namespace, verbose)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "issue",
            "mode": "reported",
            "verbose": None
        }, kwargs)
        command = process(namespace, self.parser, verbose)
        self.assertEqual("sira-query issue -r mine -f", command)

    def test_29(self):
        args = "-q type=issue mode=reported limit=0".split(" ")
        preprocess_args(args)
        namespace = self.parser.parse_args(args)
        verbose = getattr(namespace, "verbose")
        extract_values(namespace, verbose)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "issue",
            "mode": "reported",
            "verbose": None,
            "limit": 0
        }, kwargs)
        command = process(namespace, self.parser, verbose)
        self.assertEqual("sira-query issue -r mine -l 0 -f", command)

    def test_30(self):
        args = "-q type=issue mode=reported limit=1".split(" ")
        preprocess_args(args)
        namespace = self.parser.parse_args(args)
        verbose = getattr(namespace, "verbose")
        extract_values(namespace, verbose)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "issue",
            "mode": "reported",
            "verbose": None,
            "limit": 1
        }, kwargs)
        command = process(namespace, self.parser, verbose)
        self.assertEqual("sira-query issue -r mine -l 1 -f", command)

    def test_31(self):
        args = "-q type=issue mode=reported limit=10".split(" ")
        preprocess_args(args)
        namespace = self.parser.parse_args(args)
        verbose = getattr(namespace, "verbose")
        extract_values(namespace, verbose)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "issue",
            "mode": "reported",
            "verbose": None,
            "limit": 10
        }, kwargs)
        command = process(namespace, self.parser, verbose)
        self.assertEqual("sira-query issue -r mine -l 10 -f", command)

    def test_32(self):
        args = "-q type=issue mode=reported limit=100".split(" ")
        preprocess_args(args)
        namespace = self.parser.parse_args(args)
        verbose = getattr(namespace, "verbose")
        extract_values(namespace, verbose)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "issue",
            "mode": "reported",
            "verbose": None,
            "limit": 100
        }, kwargs)
        command = process(namespace, self.parser, verbose)
        self.assertEqual("sira-query issue -r mine -l 100 -f", command)

    def test_33(self):
        args = "-q type=issue mode=reported limit=-2147483649".split(" ")
        preprocess_args(args)
        namespace = self.parser.parse_args(args)
        verbose = getattr(namespace, "verbose")
        extract_values(namespace, verbose)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "issue",
            "mode": "reported",
            "verbose": None,
            "limit": -2147483649
        }, kwargs)
        command = process(namespace, self.parser, verbose)
        self.assertEqual("sira-query issue -r mine -l -2147483649 -f", command)

    def test_34(self):
        args = "-q type=issue mode=reported limit=2147483648".split(" ")
        preprocess_args(args)
        namespace = self.parser.parse_args(args)
        verbose = getattr(namespace, "verbose")
        extract_values(namespace, verbose)
        kwargs = vars(namespace)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "issue",
            "mode": "reported",
            "verbose": None,
            "limit": 2147483648
        }, kwargs)
        command = process(namespace, self.parser, verbose)
        self.assertEqual("sira-query issue -r mine -l 2147483648 -f", command)

    def test_35(self):
        args = "-q type=issue mode=reported order=desc".split(" ")
        preprocess_args(args)
        namespace = self.parser.parse_args(args)
        verbose = getattr(namespace, "verbose")
        extract_values(namespace, verbose)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "issue",
            "mode": "reported",
            "verbose": None,
            "order": "desc"
        }, kwargs)
        command = process(namespace, self.parser, verbose)
        self.assertEqual("sira-query issue -r mine -o desc -f", command)


    def test_36(self):
        args = "-q type=issue mode=reported order=asc".split(" ")
        preprocess_args(args)
        namespace = self.parser.parse_args(args)
        verbose = getattr(namespace, "verbose")
        extract_values(namespace, verbose)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "issue",
            "mode": "reported",
            "verbose": None,
            "order": "asc"
        }, kwargs)
        command = process(namespace, self.parser, verbose)
        self.assertEqual("sira-query issue -r mine -o asc -f", command)

    def test_37(self):
        args = "-q type=issue mode=reported limit=10 order=desc".split(" ")
        preprocess_args(args)
        namespace = self.parser.parse_args(args)
        verbose = getattr(namespace, "verbose")
        extract_values(namespace, verbose)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "issue",
            "mode": "reported",
            "verbose": None,
            "limit": 10,
            "order": "desc"
        }, kwargs)
        command = process(namespace, self.parser, verbose)
        self.assertEqual("sira-query issue -r mine -l 10 -o desc -f", command)

    def test_38(self):
        args = "-q type=issue mode=reported limit=10 order=asc".split(" ")
        preprocess_args(args)
        namespace = self.parser.parse_args(args)
        verbose = getattr(namespace, "verbose")
        extract_values(namespace, verbose)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "issue",
            "mode": "reported",
            "verbose": None,
            "order": "asc"
        }, kwargs)
        command = process(namespace, self.parser, verbose)
        self.assertEqual("sira-query issue -r mine -l 10 -o asc -f", command)

class Test_6(unittest.TestCase):
    def setUp(self):
        self.parser = build_parser()

    def test_39(self):
        args = "-q type=issue".split(" ")
        preprocess_args(args)
        namespace = self.parser.parse_args(args)
        verbose = getattr(namespace, "verbose")
        extract_values(namespace, verbose)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "issue",
            "verbose": None
        }, kwargs)
        command = process(namespace, self.parser, verbose)
        self.assertEqual("sira-query issue -a mine -f", command)

    def test_40(self):
        args = "-q type=issue limit=10".split(" ")
        preprocess_args(args)
        namespace = self.parser.parse_args(args)
        verbose = getattr(namespace, "verbose")
        extract_values(namespace, verbose)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "issue",
            "limit": 10,
            "verbose": None
        }, kwargs)
        command = process(namespace, self.parser, verbose)
        self.assertEqual("sira-query issue -a mine -l 10 -f", command)

    def test_41(self):
        args = "-q type=issue order=desc".split(" ")
        preprocess_args(args)
        namespace = self.parser.parse_args(args)
        verbose = getattr(namespace, "verbose")
        extract_values(namespace, verbose)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "issue",
            "order": "desc",
            "verbose": None
        }, kwargs)
        command = process(namespace, self.parser, verbose)
        self.assertEqual("sira-query issue -a mine -o desc -f", command)

    def test_42(self):
        args = "-q type=issue limit=10 order=desc".split(" ")
        preprocess_args(args)
        namespace = self.parser.parse_args(args)
        verbose = getattr(namespace, "verbose")
        extract_values(namespace, verbose)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "issue",
            "limit": 10,
            "order": "desc",
            "verbose": None
        }, kwargs)
        command = process(namespace, self.parser, verbose)
        self.assertEqual("sira-query issue -a mine -l 10 -o desc -f", command)

class Test_7(unittest.TestCase):
    def setUp(self):
        self.parser = build_parser()

    def test_43(self):
        args = "-q type=issue mode=recent".split(" ")
        preprocess_args(args)
        namespace = self.parser.parse_args(args)
        verbose = getattr(namespace, "verbose")
        extract_values(namespace, verbose)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "issue",
            "mode": "recent",
            "verbose": None
        }, kwargs)
        command = process(namespace, self.parser, verbose)
        self.assertEqual("sira-query issue -o recent -f", command)

    def test_44(self):
        args = "-q type=issue mode=recent limit=10 order=asc".split(" ")
        preprocess_args(args)
        namespace = self.parser.parse_args(args)
        verbose = getattr(namespace, "verbose")
        extract_values(namespace, verbose)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "issue",
            "mode": "recent",
            "limit": 10,
            "order": "asc",
            "verbose": None
        }, kwargs)
        command = process(namespace, self.parser, verbose)
        self.assertEqual("sira-query issue -o recent -l 10 -f", command)

    def test_45(self):
        args = "-q type=issue mode=recent order=asc limit=10".split(" ")
        preprocess_args(args)
        namespace = self.parser.parse_args(args)
        verbose = getattr(namespace, "verbose")
        extract_values(namespace, verbose)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "issue",
            "mode": "recent",
            "limit": 10,
            "order": "asc",
            "verbose": None
        }, kwargs)
        command = process(namespace, self.parser, verbose)
        self.assertEqual("sira-query issue -o recent -l 10 -f", command)

    def test_46(self):
        args = "-q type=issue limit=10 mode=recent order=asc".split(" ")
        preprocess_args(args)
        namespace = self.parser.parse_args(args)
        verbose = getattr(namespace, "verbose")
        extract_values(namespace, verbose)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "issue",
            "mode": "recent",
            "limit": 10,
            "order": "asc",
            "verbose": None
        }, kwargs)
        command = process(namespace, self.parser, verbose)
        self.assertEqual("sira-query issue -o recent -l 10 -f", command)

    def test_47(self):
        args = "-q type=issue limit=10 order=asc mode=recent".split(" ")
        preprocess_args(args)
        namespace = self.parser.parse_args(args)
        verbose = getattr(namespace, "verbose")
        extract_values(namespace, verbose)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "issue",
            "mode": "recent",
            "limit": 10,
            "order": "asc",
            "verbose": None
        }, kwargs)
        command = process(namespace, self.parser, verbose)
        self.assertEqual("sira-query issue -o recent -l 10 -f", command)

    def test_48(self):
        args = "-q type=issue order=asc mode=recent limit=10".split(" ")
        preprocess_args(args)
        namespace = self.parser.parse_args(args)
        verbose = getattr(namespace, "verbose")
        extract_values(namespace, verbose)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "issue",
            "mode": "recent",
            "limit": 10,
            "order": "asc",
            "verbose": None
        }, kwargs)
        command = process(namespace, self.parser, verbose)
        self.assertEqual("sira-query issue -o recent -l 10 -f", command)

    def test_49(self):
        args = "-q type=issue order=asc limit=10 mode=recent".split(" ")
        preprocess_args(args)
        namespace = self.parser.parse_args(args)
        verbose = getattr(namespace, "verbose")
        extract_values(namespace, verbose)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "issue",
            "mode": "recent",
            "limit": 10,
            "order": "asc",
            "verbose": None
        }, kwargs)
        command = process(namespace, self.parser, verbose)
        self.assertEqual("sira-query issue -o recent -l 10 -f", command)

    def test_50(self):
        args = "-q mode=recent type=issue limit=10 order=asc".split(" ")
        preprocess_args(args)
        namespace = self.parser.parse_args(args)
        verbose = getattr(namespace, "verbose")
        extract_values(namespace, verbose)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "issue",
            "mode": "recent",
            "limit": 10,
            "order": "asc",
            "verbose": None
        }, kwargs)
        command = process(namespace, self.parser, verbose)
        self.assertEqual("sira-query issue -o recent -l 10 -f", command)

    def test_51(self):
        args = "-q limit=10 type=issue mode=recent order=asc".split(" ")
        preprocess_args(args)
        namespace = self.parser.parse_args(args)
        verbose = getattr(namespace, "verbose")
        extract_values(namespace, verbose)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "issue",
            "mode": "recent",
            "limit": 10,
            "order": "asc",
            "verbose": None
        }, kwargs)
        command = process(namespace, self.parser, verbose)
        self.assertEqual("sira-query issue -o recent -l 10 -f", command)

    def test_52(self):
        args = "-q order=asc type=issue mode=recent limit=10".split(" ")
        preprocess_args(args)
        namespace = self.parser.parse_args(args)
        verbose = getattr(namespace, "verbose")
        extract_values(namespace, verbose)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "issue",
            "mode": "recent",
            "limit": 10,
            "order": "asc",
            "verbose": None
        }, kwargs)
        command = process(namespace, self.parser, verbose)
        self.assertEqual("sira-query issue -o recent -l 10 -f", command)

    def test_53(self):
        args = "-q mode=recent limit=10 order=asc type=issue".split(" ")
        preprocess_args(args)
        namespace = self.parser.parse_args(args)
        verbose = getattr(namespace, "verbose")
        extract_values(namespace, verbose)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "issue",
            "mode": "recent",
            "limit": 10,
            "order": "asc",
            "verbose": None
        }, kwargs)
        command = process(namespace, self.parser, verbose)
        self.assertEqual("sira-query issue -o recent -l 10 -f", command)

    def test_54(self):
        args = "-q limit=10 mode=recent order=asc type=issue".split(" ")
        preprocess_args(args)
        namespace = self.parser.parse_args(args)
        verbose = getattr(namespace, "verbose")
        extract_values(namespace, verbose)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "issue",
            "mode": "recent",
            "limit": 10,
            "order": "asc",
            "verbose": None
        }, kwargs)
        command = process(namespace, self.parser, verbose)
        self.assertEqual("sira-query issue -o recent -l 10 -f", command)

    def test_55(self):
        args = "-q order=asc mode=recent limit=10 type=issue".split(" ")
        preprocess_args(args)
        namespace = self.parser.parse_args(args)
        verbose = getattr(namespace, "verbose")
        extract_values(namespace, verbose)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "issue",
            "mode": "recent",
            "limit": 10,
            "order": "asc",
            "verbose": None
        }, kwargs)
        command = process(namespace, self.parser, verbose)
        self.assertEqual("sira-query issue -o recent -l 10 -f", command)

class Test_8(unittest.TestCase):
    def setUp(self):
        self.parser = build_parser()

    def test_56(self):
        args = "-q type=issue mode=board key=2".split(" ")
        preprocess_args(args)
        namespace = self.parser.parse_args(args)
        verbose = getattr(namespace, "verbose")
        extract_values(namespace, verbose)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "issue",
            "mode": "board",
            "key": 2,
            "verbose": None
        }, kwargs)
        command = process(namespace, self.parser, verbose)
        self.assertEqual("sira-query issue -b 2 -f", command)

    def test_57(self):
        args = "-q type=issue mode=board limit=10 order=asc key=2".split(" ")
        preprocess_args(args)
        namespace = self.parser.parse_args(args)
        verbose = getattr(namespace, "verbose")
        extract_values(namespace, verbose)
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
        command = process(namespace, self.parser, verbose)
        self.assertEqual("sira-query issue -b 2 -l 10 -o asc -f", command)

    def test_58(self):
        args = "-qv type=issue -s mode=board limit=10 order=asc key=2".split(" ")
        preprocess_args(args)
        namespace = self.parser.parse_args(args)
        verbose = getattr(namespace, "verbose")
        extract_values(namespace, verbose)
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
        command = process(namespace, self.parser, verbose)
        self.assertEqual("sira-query issue -b 2 -l 10 -o asc -s -f", command)

    def test_59(self):
        args = "-qvsvs type=issue mode=board limit=10 order=asc key=2".split(" ")
        preprocess_args(args)
        namespace = self.parser.parse_args(args)
        verbose = getattr(namespace, "verbose")
        extract_values(namespace, verbose)
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
        command = process(namespace, self.parser, verbose)
        self.assertEqual("sira-query issue -b 2 -l 10 -o asc -s -f", command)

    def test_60(self):
        args = "-qv type=issue mode=board limit=10 order=asc -s key=2".split(" ")
        preprocess_args(args)
        namespace = self.parser.parse_args(args)
        verbose = getattr(namespace, "verbose")
        extract_values(namespace, verbose)
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
        command = process(namespace, self.parser, verbose)
        self.assertEqual("sira-query issue -b 2 -l 10 -o asc -s -f", command)

    def test_61(self):
        args = "-qv type=issue -v mode=board -v limit=10 -v order=asc -s key=2".split(" ")
        preprocess_args(args)
        namespace = self.parser.parse_args(args)
        verbose = getattr(namespace, "verbose")
        extract_values(namespace, verbose)
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
        command = process(namespace, self.parser, verbose)
        self.assertEqual("sira-query issue -b 2 -l 10 -o asc -s -f", command)

    def test_62(self):
        args = "-sq type=issue --verbose mode=board limit=10 order=asc key=2".split(" ")
        preprocess_args(args)
        namespace = self.parser.parse_args(args)
        verbose = getattr(namespace, "verbose")
        extract_values(namespace, verbose)
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
        command = process(namespace, self.parser, verbose)
        self.assertEqual("sira-query issue -b 2 -l 10 -o asc -v -f", command)

    def test_63(self):
        args = "-sq --verbose --silent --verbose type=issue mode=board limit=10 order=asc key=2".split(" ")
        preprocess_args(args)
        namespace = self.parser.parse_args(args)
        verbose = getattr(namespace, "verbose")
        extract_values(namespace, verbose)
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
        command = process(namespace, self.parser, verbose)
        self.assertEqual("sira-query issue -b 2 -l 10 -o asc -v -f", command)

    def test_64(self):
        args = "-sq type=issue mode=board limit=10 order=asc --verbose key=2".split(" ")
        preprocess_args(args)
        namespace = self.parser.parse_args(args)
        verbose = getattr(namespace, "verbose")
        extract_values(namespace, verbose)
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
        command = process(namespace, self.parser, verbose)
        self.assertEqual("sira-query issue -b 2 -l 10 -o asc -v -f", command)

    def test_65(self):
        args = "-sq type=issue --silent mode=board --silent limit=10 --silent order=asc --verbose key=2".split(" ")
        preprocess_args(args)
        namespace = self.parser.parse_args(args)
        verbose = getattr(namespace, "verbose")
        extract_values(namespace, verbose)
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
        command = process(namespace, self.parser, verbose)
        self.assertEqual("sira-query issue -b 2 -l 10 -o asc -v -f", command)

    def test_66(self):
        args = "-q type=issue mode=mine mode=board limit=10 order=asc key=2".split(" ")
        preprocess_args(args)
        namespace = self.parser.parse_args(args)
        verbose = getattr(namespace, "verbose")
        extract_values(namespace, verbose)
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
        command = process(namespace, self.parser, verbose)
        self.assertEqual("sira-query issue -b 2 -l 10 -o asc -f", command)

    def test_67(self):
        args = "-q type=issue mode=mine limit=10 order=asc mode=board key=2".split(" ")
        preprocess_args(args)
        namespace = self.parser.parse_args(args)
        verbose = getattr(namespace, "verbose")
        extract_values(namespace, verbose)
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
        command = process(namespace, self.parser, verbose)
        self.assertEqual("sira-query issue -b 2 -l 10 -o asc -f", command)

    def test_68(self):
        args = "-q type=issue mode=board limit=1 limit=10 order=asc key=2".split(" ")
        preprocess_args(args)
        namespace = self.parser.parse_args(args)
        verbose = getattr(namespace, "verbose")
        extract_values(namespace, verbose)
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
        command = process(namespace, self.parser, verbose)
        self.assertEqual("sira-query issue -b 2 -l 10 -o asc -f", command)

    def test_69(self):
        args = "-q type=issue mode=board limit=10 order=desc order=asc key=2".split(" ")
        preprocess_args(args)
        namespace = self.parser.parse_args(args)
        verbose = getattr(namespace, "verbose")
        extract_values(namespace, verbose)
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
        command = process(namespace, self.parser, verbose)
        self.assertEqual("sira-query issue -b 2 -l 10 -o asc -f", command)

    def test_70(self):
        args = "-q type=issue mode=reported limit=100 order=desc mode=board limit=10 order=asc key=2".split(" ")
        preprocess_args(args)
        namespace = self.parser.parse_args(args)
        verbose = getattr(namespace, "verbose")
        extract_values(namespace, verbose)
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
        command = process(namespace, self.parser, verbose)
        self.assertEqual("sira-query issue -b 2 -l 10 -o asc -f", command)

    def test_71(self):
        args = "-q type=issue -q type=issue mode=board limit=10 order=asc key=2".split(" ")
        preprocess_args(args)
        namespace = self.parser.parse_args(args)
        verbose = getattr(namespace, "verbose")
        extract_values(namespace, verbose)
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
        command = process(namespace, self.parser, verbose)
        self.assertEqual("sira-query issue -b 2 -l 10 -o asc -f", command)

class Test_9(unittest.TestCase):
    def setUp(self):
        self.parser = build_parser()

    def test_72(self):
        args = "-q type=board".split(" ")
        preprocess_args(args)
        namespace = self.parser.parse_args(args)
        verbose = getattr(namespace, "verbose")
        extract_values(namespace, verbose)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "board",
            "verbose": None
        }, kwargs)
        command = process(namespace, self.parser, verbose)
        self.assertEqual("sira-query board -o recent -f", command)


    def test_73(self):
        args = "-q type=board key=52".split(" ")
        preprocess_args(args)
        namespace = self.parser.parse_args(args)
        verbose = getattr(namespace, "verbose")
        extract_values(namespace, verbose)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "board",
            "verbose": None,
            "key": 52
        }, kwargs)
        command = process(namespace, self.parser, verbose)
        self.assertEqual("sira-query board -k 52 -f", command)

    def test_74(self):
        args = "-q type=board limit=12 key=52".split(" ")
        preprocess_args(args)
        namespace = self.parser.parse_args(args)
        verbose = getattr(namespace, "verbose")
        extract_values(namespace, verbose)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "board",
            "verbose": None,
            "key": 52,
            "limit": 12
        }, kwargs)
        command = process(namespace, self.parser, verbose)
        self.assertEqual("sira-query board -k 52 -l 12 -f", command)

    def test_75(self):
        args = "-q order=desc type=board limit=12 key=52".split(" ")
        preprocess_args(args)
        namespace = self.parser.parse_args(args)
        verbose = getattr(namespace, "verbose")
        extract_values(namespace, verbose)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "board",
            "verbose": None,
            "key": 52,
            "limit": 12
        }, kwargs)
        command = process(namespace, self.parser, verbose)
        self.assertEqual("sira-query board -k 52 -l 12 -o desc -f", command)

    def test_76(self):
        args = "limit=12 -q type=board".split(" ")
        preprocess_args(args)
        namespace = self.parser.parse_args(args)
        verbose = getattr(namespace, "verbose")
        extract_values(namespace, verbose)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "board",
            "verbose": None
        }, kwargs)
        command = process(namespace, self.parser, verbose)
        self.assertEqual("sira-query board -o recent -f", command)

    def test_77(self):
        args = "ccc=yyy --query mode=all type=board -v -q type=board key=52".split(" ")
        preprocess_args(args)
        namespace = self.parser.parse_args(args)
        verbose = getattr(namespace, "verbose")
        extract_values(namespace, verbose)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "board",
            "verbose": True,
            "key": 52
        }, kwargs)
        command = process(namespace, self.parser, verbose)
        self.assertEqual("sira-query board -k 52 -v -f", command)

    def test_78(self):
        args = "xxx=yyy --silent -q --verbose --query type=key type=board key=23".split(" ")
        preprocess_args(args)
        namespace = self.parser.parse_args(args)
        verbose = getattr(namespace, "verbose")
        extract_values(namespace, verbose)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "board",
            "verbose": True,
            "key": 23
        }, kwargs)
        command = process(namespace, self.parser, verbose)
        self.assertEqual("sira-query board -k 23 -v -f", command)

## Ambiguous Inputs:

class Test_10(unittest.TestCase):
    def setUp(self):
        self.parser = build_parser()

### help manual

class Test_11(unittest.TestCase):
    def setUp(self):
        self.parser = build_parser()

    def test_79(self):
        args = "-v".split(" ")
        preprocess_args(args)
        namespace = self.parser.parse_args(args)
        verbose = getattr(namespace, "verbose")
        extract_values(namespace, verbose)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": None,
            "help": False,
            "verbose": True
        }, kwargs)
        with self.assertRaises(SystemExit) as se:
            process(namespace, self.parser, verbose)
        self.assertEqual(0, se.exception.code)

### verbose help

class Test_12(unittest.TestCase):
    def setUp(self):
        self.parser = build_parser()

    def test_80(self):
        args = "-vh".split(" ")
        preprocess_args(args)
        namespace = self.parser.parse_args(args)
        verbose = getattr(namespace, "verbose")
        extract_values(namespace, verbose)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": None,
            "help": True,
            "verbose": True
        }, kwargs)
        with self.assertRaises(SystemExit) as se:
            process(namespace, self.parser, verbose)
        self.assertEqual(0, se.exception.code)

### verbose help

class Test_13(unittest.TestCase):
    def setUp(self):
        self.parser = build_parser()

    def test_81(self):
        args = "-hv".split(" ")
        preprocess_args(args)
        namespace = self.parser.parse_args(args)
        verbose = getattr(namespace, "verbose")
        extract_values(namespace, verbose)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": None,
            "help": True,
            "verbose": True
        }, kwargs)
        with self.assertRaises(SystemExit) as se:
            process(namespace, self.parser, verbose)
        self.assertEqual(0, se.exception.code)
### help manual

class Test_14(unittest.TestCase):
    def setUp(self):
        self.parser = build_parser()

    def test_82(self):
        args = "-s".split(" ")
        preprocess_args(args)
        namespace = self.parser.parse_args(args)
        verbose = getattr(namespace, "verbose")
        extract_values(namespace, verbose)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": None,
            "help": False,
            "verbose": False
        }, kwargs)
        with self.assertRaises(SystemExit) as se:
            process(namespace, self.parser, verbose)
        self.assertEqual(0, se.exception.code)

### help manual

class Test_15(unittest.TestCase):
    def setUp(self):
        self.parser = build_parser()

    def test_83(self):
        args = "-vsvsvss".split(" ")
        preprocess_args(args)
        namespace = self.parser.parse_args(args)
        verbose = getattr(namespace, "verbose")
        extract_values(namespace, verbose)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": None,
            "help": False,
            "verbose": False
        }, kwargs)
        with self.assertRaises(SystemExit) as se:
            process(namespace, self.parser, verbose)
        self.assertEqual(0, se.exception.code)

### floot

class Test_16(unittest.TestCase):
    def setUp(self):
        self.parser = build_parser()

    def test_84(self):
        args = "-q type=issue mode=reported limit=1.0".split(" ")
        preprocess_args(args)
        namespace = self.parser.parse_args(args)
        verbose = getattr(namespace, "verbose")
        extract_values(namespace, verbose)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "issue",
            "mode": "reported",
            "limit": 1,
            "verbose": None
        }, kwargs)
        command = process(namespace, self.parser, verbose)
        self.assertEqual("sira-query issue -r mine -l 1 -f", command)

### discard invalid keys

class Test_17(unittest.TestCase):
    def setUp(self):
        self.parser = build_parser()

    def test_85(self):
        args = "-q xxx=yyy type=issue yyy=xxx".split(" ")
        preprocess_args(args)
        namespace = self.parser.parse_args(args)
        verbose = getattr(namespace, "verbose")
        extract_values(namespace, verbose)
        kwargs = vars(namespace)
        self.assertDictContainsSubset({
            "action": "query",
            "type": "issue",
            "verbose": None
        }, kwargs)
        command = process(namespace, self.parser, verbose)
        self.assertEqual("sira-query issue -a mine -f", command)

## Invalid Inputs:

class Test_18(unittest.TestCase):
    def setUp(self):
        self.parser = build_parser()

class Test_19(unittest.TestCase):
    def setUp(self):
        self.parser = build_parser()

    def test_86(self):
        with self.assertRaises(SystemExit) as se:
            args = "-x".split(" ")
            preprocess_args(args)
            namespace = self.parser.parse_args(args)
        self.assertEqual(2, se.exception.code)
            

    def test_87(self):
        with self.assertRaises(SystemExit) as se:
            args = "-qx".split(" ")
            preprocess_args(args)
            namespace = self.parser.parse_args(args)
        self.assertEqual(2, se.exception.code)

    def test_88(self):
        with self.assertRaises(SystemExit) as se:
            args = "--xxx".split(" ")
            preprocess_args(args)
            namespace = self.parser.parse_args(args)
        self.assertEqual(2, se.exception.code)
        
    # valid but print help

    def test_89(self):
        args = "xxx".split(" ")
        preprocess_args(args)
        namespace = self.parser.parse_args(args)
        verbose = getattr(namespace, "verbose")
        extract_values(namespace, verbose)
        kwargs = vars(namespace)

class Test_20(unittest.TestCase):
    def setUp(self):
        self.parser = build_parser()

    def test_90(self):
        args = "-v -q type=xxx".split(" ")
        preprocess_args(args)
        namespace = self.parser.parse_args(args)
        verbose = getattr(namespace, "verbose")
        extract_values(namespace, verbose)
        kwargs = vars(namespace)

    def test_91(self):
        args = "-v -q type=project".split(" ")
        preprocess_args(args)
        namespace = self.parser.parse_args(args)
        verbose = getattr(namespace, "verbose")
        extract_values(namespace, verbose)
        kwargs = vars(namespace)

    def test_92(self):
        args = "-v -q type=project mode=xxx".split(" ")
        preprocess_args(args)
        namespace = self.parser.parse_args(args)
        verbose = getattr(namespace, "verbose")
        extract_values(namespace, verbose)
        kwargs = vars(namespace)

    def test_93(self):
        args = "-v -q type=project mode=current limit=xxx".split(" ")
        preprocess_args(args)
        namespace = self.parser.parse_args(args)
        verbose = getattr(namespace, "verbose")
        extract_values(namespace, verbose)
        kwargs = vars(namespace)

    def test_94(self):
        args = "-v -q type=project mode=current order=xxx".split(" ")
        preprocess_args(args)
        namespace = self.parser.parse_args(args)
        verbose = getattr(namespace, "verbose")
        extract_values(namespace, verbose)
        kwargs = vars(namespace)

class Test_21(unittest.TestCase):
    def setUp(self):
        self.parser = build_parser()

    def test_95(self):
        args = "-v -q type=issue mode=all".split(" ")
        preprocess_args(args)
        namespace = self.parser.parse_args(args)
        verbose = getattr(namespace, "verbose")
        extract_values(namespace, verbose)
        kwargs = vars(namespace)

    def test_96(self):
        args = "-v mode=all -q type=project".split(" ")
        preprocess_args(args)
        namespace = self.parser.parse_args(args)
        verbose = getattr(namespace, "verbose")
        extract_values(namespace, verbose)
        kwargs = vars(namespace)

    def test_97(self):
        args = "-v -q type=project mode=board".split(" ")
        preprocess_args(args)
        namespace = self.parser.parse_args(args)
        verbose = getattr(namespace, "verbose")
        extract_values(namespace, verbose)
        kwargs = vars(namespace)

    def test_98(self):
        args = "-v -q type=project mode=board key=xxx".split(" ")
        preprocess_args(args)
        namespace = self.parser.parse_args(args)
        verbose = getattr(namespace, "verbose")
        extract_values(namespace, verbose)
        kwargs = vars(namespace)

class Test_22(unittest.TestCase):
    def setUp(self):
        self.parser = build_parser()

    def test_99(self):
        args = "-v -q type=board key=xxx".split(" ")
        preprocess_args(args)
        namespace = self.parser.parse_args(args)
        verbose = getattr(namespace, "verbose")
        extract_values(namespace, verbose)
        kwargs = vars(namespace)

class Test_23(unittest.TestCase):
    def setUp(self):
        self.parser = build_parser()
    def test_100(self):
        args = ['-i']
        preprocess_args(args)
        namespace = self.parser.parse_args(args)
        userName='mayh11'
        passWord='Ma940871651='
        jiraUrl='https://lnvusconf.lenovonet.lenovo.local'
        initUser(userName,passWord,jiraUrl)
        UserName =read_from_config().get("credential").get("username")
        PassWord=keyring.get_password("sira",userName)
        JiraUrl = read_from_config().get("credential").get("domain")
        self.assertMultiLineEqual(userName,UserName)
        self.assertMultiLineEqual(passWord,PassWord)
        self.assertMultiLineEqual(jiraUrl,JiraUrl)

class Test_24(unittest.TestCase):
    def setUp(self):
        self.parser = build_parser()
    def test_101(self):
        args = ['-q', 'type=jql', "query=assignee='kidd liu' and issuetype=bug"]
        preprocess_args(args)
        namespace = self.parser.parse_args(args)
        verbose = getattr(namespace, "verbose")
        extract_values(namespace, verbose)
        kwargs = vars(namespace)
        command = process(namespace, self.parser, verbose)
        self.assertEqual("sira-query jql -q \"assignee='kidd liu' and issuetype=bug\" -f", command)

    def test_102(self):
        args = ['-q', 'type=jql', "query=assignee='kidd liu'"]
        preprocess_args(args)
        namespace = self.parser.parse_args(args)
        verbose = getattr(namespace, "verbose")
        extract_values(namespace, verbose)
        kwargs = vars(namespace)
        command = process(namespace, self.parser, verbose)
        self.assertEqual("sira-query jql -q \"assignee='kidd liu'\" -f", command)

    def test_103(self):
        args = ['-q', 'type=jql', "query=assignee='kidd liu'",'limit=10', 'order=asc']
        preprocess_args(args)
        namespace = self.parser.parse_args(args)
        verbose = getattr(namespace, "verbose")
        extract_values(namespace, verbose)
        kwargs = vars(namespace)
        command = process(namespace, self.parser, verbose)
        self.assertEqual("sira-query jql -q \"assignee='kidd liu'\" -l 10 -o asc -f", command)

class Test_25(unittest.TestCase):
    def setUp(self):
        self.parser = build_parser()
    def test_104(self):
        args = ['-q', 'type=jql', "query=assignee='kidd liu'",'limit=10', 'order=asc','-c', 'mayh11:Ma940871651=']
        preprocess_args(args)
        namespace = self.parser.parse_args(args)
        verbose = getattr(namespace, "verbose")
        extract_values(namespace, verbose)
        kwargs = vars(namespace)
        command = process(namespace, self.parser, verbose)
        self.assertEqual("sira-query jql -q \"assignee='kidd liu'\" -u mayh11:Ma940871651= -l 10 -o asc -f", command)
    
    def test_105(self):
        args = ['-q','-c', 'mayh11:Ma940871651=', 'type=jql', "query=assignee='kidd liu'"]
        preprocess_args(args)
        namespace = self.parser.parse_args(args)
        verbose = getattr(namespace, "verbose")
        extract_values(namespace, verbose)
        kwargs = vars(namespace)
        command = process(namespace, self.parser, verbose)
        self.assertEqual("sira-query jql -q \"assignee='kidd liu'\" -u mayh11:Ma940871651= -f", command)


def main():
    unittest.main()

if __name__ == '__main__':
    main()
