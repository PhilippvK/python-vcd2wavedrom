import nose
import json
from vcd2wavedrom import *

# TODO

test_input = """$date today $end
$timescale 1 ns $end
$scope module top $end
$var reg 1 0 A $end
$var reg 1 1 B $end
$var reg 1 2 sel $end
$var reg 1 3 seln $end
$var reg 1 4 S1 $end
$var reg 1 5 S2 $end
$var reg 1 6 Q $end
$upscope $end
$enddefinitions $end
#0
b0 0
b0 1
b1 2
b0 3
b1 4
b1 5
b0 6
#10
b1 1
#12
b0 5
#14
b1 6
#20
b1 0
#30
b0 2
#32
b1 3
b1 5
#34
b0 4
b0 6
#36
b1 6
"""

custom_title = "TESTtitleTEST"

def test_title():
    result = VCD2Wavedrom(test_input, title=custom_title).convert()
    assert custom_title in result

def test_json():
    try:
        json.loads(VCD2Wavedrom(test_input).convert())
    except ValueError as err:
        assert False
    assert True

if __name__ == '__main__':
    nose.run()
