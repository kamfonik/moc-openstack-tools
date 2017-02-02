import os

# This is a hack for now until directory structure is sorted
# When this is removed remember to un-ignore E402 in flake8
import sys
TEST_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.abspath(os.path.join(TEST_DIR, os.pardir))
sys.path.insert(0, PROJECT_DIR)

from message import TemplateMessage, Message


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
   
def _file_dump(tmpdir, subject=None, label=None):
    addr = 'dummy.email@moc.org'
    body = 'Body of the email'

    if label is not None:
        tag = label
    elif subject is not None:
        tag = subject
    else:
        tag = None

    expected_file_name = 'dummy.email_{0}.txt'.format(tag)

    msg = Message(sender=addr, receiver=addr, body=body, subject=subject)
 
    msg_path = msg.dump_to_file(target_path='{}'.format(tmpdir), label=label)

    assert os.path.isfile(msg_path)

    assert os.path.basename(msg_path) == expected_file_name

    with open(msg_path, 'r') as f:
        assert f.read() == body
 
    # clean up
    os.remove(msg_path)

def test_file_dump(tmpdir):
    _file_dump(tmpdir)

    _file_dump(tmpdir, subject="foo")

    _file_dump(tmpdir, label="bar")
    
    _file_dump(tmpdir, subject="foo", label="bar")
