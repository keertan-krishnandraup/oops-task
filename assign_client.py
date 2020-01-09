"""finally"""
"""switch case"""
"""log exceptions and warnings
levels of log
log critical points
logging as part of file handlers"""
#rotating file handler
#read about python packages
#underscore vs underscore underscore
"""Custom error"""
#Decorator for checking permissions
"""Design Patterns"""
import assign
import client_fn
import sys


def menu(choice):
    return option_list[choice]


option_list = {
    1:client_fn.client_get_user_info,
    2:client_fn.client_count_users,
    3:client_fn.client_role_based_user_count,
    4:client_fn.client_get_user_role,
    5:client_fn.client_add_user,
    6:client_fn.client_delete_user,
    7:client_fn.client_set_user_role,
    8:client_fn.client_edit_user}

client_fn.login()
while(True):
    print('\nWhat would you like to do?')
    print('\n1.Get User Info\n2.Count Users\n3.Role Based User Count\n4.Get User Role\n5.Add User\n6.Delete User\n7.Set User Role\n8.Edit user\n9.Exit')
    uch = int(input())
    if(uch==9):
        break
    menu(uch)()
    if(uch not in range(1,10)):
        continue