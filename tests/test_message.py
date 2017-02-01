import os

# This is a hack for now until directory structure is sorted
# When this is removed remember to un-ignore E402 in flake8
import sys
TEST_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.abspath(os.path.join(TEST_DIR, os.pardir))
sys.path.insert(0, PROJECT_DIR)

from message import TemplateMessage


def test_template():
    """Test whether template messages are filled in correctly"""
    
    # Keywords and values to be filled into the template
    items = {'item_1': 'First', 'long_keyword_item_2': 'Second',
             'space_3': 'Third Third Third ', 'item_4': 'Fourth',
             'item_5': None}
 
    sender = 'dummy@moc.org'
    receiver = 'dummy@moc.org'
    result = 'First Second\nThird Third Third  Fourth\n'
     
    # TEST_DIR = os.path.dirname(os.path.abspath(__file__))
    template = os.path.abspath(os.path.join(TEST_DIR, 'test_template.txt'))

    msg = TemplateMessage(sender=sender, email=receiver, template=template,
                          **items)
    assert msg.body == result
