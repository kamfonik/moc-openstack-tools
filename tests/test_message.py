import os
import mock

# This is a hack for now until directory structure is sorted
# When this is removed remember to un-ignore E402 in flake8
import sys
TEST_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.abspath(os.path.join(TEST_DIR, os.pardir))
sys.path.insert(0, PROJECT_DIR)

from message import Message, TemplateMessage

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

@mock.patch('message.smtplib.SMTP')
def test_send(mock_smtp):
    """Test the function that sends emails"""
    
    msg_values = { 'sender': 'dummy@moc.org',
                 'receiver': 'newuser1@moc.org',
                 'subject': 'Test Message Subject',
                 'body': 'This is a Test.'
               }

    msg = Message(**msg_values)
   
    # What we expect to be passed to smtplib.SMTP.sendmail() 
    expected_string =("Content-Type: text/plain; charset=\"us-ascii\"\n"
                      "MIME-Version: 1.0\n"
                      "Content-Transfer-Encoding: 7bit\n"
                      "Subject: {subject}\n"
                      "From: {sender}\n"
                      "To: {receiver}\n\n"
                      "{body}").format(**msg_values)

    msg.send() 

    mock_smtp.assert_called_with('127.0.0.1', '25')
    
    mock_smtp_rval = mock_smtp.return_value 
    assert mock_smtp_rval.starttls.call_count == 1
    assert mock_smtp_rval.ehlo.call_count == 1
    mock_smtp_rval.sendmail.assert_called_with(msg_values['sender'], [msg_values['receiver']], expected_string) 


@mock.patch('message.open', new_callable=mock.mock_open, create=True)  
def _file_dump(m_op):
    msg_values = { 'sender': 'dummy@moc.org',
                   'receiver': 'newuser1@moc.org',
                   'subject': 'Test Message Subject',
                   'body': 'This is a Test.'
                 }
    
    expected_file_name = '/tmp/newuser1_Test Message Subject.txt'
 
    msg = Message(**msg_values)
    
    msg_path = msg.dump_to_file()
 
    m_op.assert_called_with(expected_file_name, 'w')

    mock_file_handle = m_op()

    assert mock_file_handle.write.call_count == 1
    mock_file_handle.write.assert_called_with(msg_values['body'])
    



def test_file_dump():
#    _file_dump(tmpdir)
     _file_dump()
    #_file_dump(tmpdir, subject="foo")

    #_file_dump(tmpdir, label="bar")

    #_file_dump(tmpdir, subject="foo", label="bar")
   

