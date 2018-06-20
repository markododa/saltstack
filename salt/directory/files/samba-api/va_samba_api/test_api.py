from . import *
import pytest
import subprocess


@pytest.mark.incremental
class TestUserList:
    def test_user_list_1(self):
        purge_cache()  # Delete cache
        users = list_users()  # will build cache, shouldnt be empty
        assert len(users) > 0
        for user in users:
            assert 'name' in user.keys()
            assert 'username' in user.keys()
            assert len(user['username']) > 0

    def test_user_list_2(self):
        purge_cache()  # Delete cache
        # Lists users from cache, should be empty because we don't have cache
        users = list_users(auto_build_cache=False)
        assert len(users) == 0


@pytest.mark.incremental
class TestUserOps:
    def test_user_add_1(self):
        assert (not get_user('mytestuser'))
        add_user(username='mytestuser', password='som38w4c09LnzLllznxi',
                 name='Test', surname='Testovsky', vpn=False)
        assert get_user('mytestuser')  # First test with cache

    def test_user_add_2(self):
        purge_cache()
        user = get_user('mytestuser')
        assert user
        assert user['name'] == 'Test Testovsky'

    def test_user_change_name(self):
        change_name('mytestuser', 'John Doe')
        user = get_user('mytestuser')
        assert user['name'] == 'John Doe'
        purge_cache()
        user = get_user('mytestuser')
        assert user['name'] == 'John Doe'

    def test_user_lock_1(self):
        set_user_status('mytestuser', lock=True)
        assert get_user('mytestuser')['is_locked']
        set_user_status('mytestuser', lock=False)
        assert not get_user('mytestuser')['is_locked']

    def test_delete_1(self):
        result = delete_user('mytestuser')
        assert (not get_user('mytestuser'))

    def test_delete_2(self):
        purge_cache()
        assert (not get_user('mytestuser'))

    def test_delete_3(self):
        assert not get_user('somenonexistentuser')
        with pytest.raises(Exception) as exc_info:
            delete_user('somenonexistentuser')


def test_group_list():
    groups = list_groups()
    assert 'Administrators' in groups


def get_user(username):
    filtered_users = [x for x in list_users() if x['username'] == username]
    return filtered_users[0] if len(filtered_users) == 1 else None
