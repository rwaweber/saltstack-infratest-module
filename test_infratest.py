import infratest
import os.path
import pwd
import grp

def standup_test_file_user(path):
    if not os.path.isfile(path):
        file(path,"w+")
    os.chown(path, pwd.getpwnam().pw_uid, os.getgid())

def cleanup_test_file_user(path):
    try:
        os.remove(path)
    except Exception as e:
        return e

def test_file_user():
    test_file_path = "./test/file_user"
    standup_test_file_user(test_file_path)
    assert infratest.file_user(test_file_path, "testuser")['Passed']
    cleanup_test_file_user(test_file_path)
