import assign
from assign import RoleError
import sys
import logging



def login():
    global u_obj
    logged_in = 0
    while(logged_in==0):
        print('Please enter your login credentials:\nUser Name:')
        uname = input()
        print('\nPassword:')
        upass = input()
        u_obj = assign.User.verify(uname,upass)
        if(u_obj==-1):
            logging.error('Wrong Password entered.(executing %s)',login.__name__)
            print('\nPassword Wrong')
        elif(u_obj ==-2):
            logging.error('Wrong User Name entered.(executing %s)',login.__name__)
            print('\nUser not found')
        else:
            logged_in=1
            logging.info('User with username %s logged in.(executing %s)',uname,login.__name__)
            print('Logged in succesfully')

def client_get_user_info():
    logging.info('Executing %s',client_get_user_info.__name__)
    print('Enter the user ID for retrieval of details')
    q_id = int(input())
    try:
        assign.check_privelege('get_user_info',u_obj.role)
        q_obj = assign.User.get_user_info(u_obj,q_id)
        print('Name:'+ q_obj.name,'\nDesc:'+q_obj.desc,'\nRole:'+q_obj.role)
        logging.info('Successful execution of %s',client_get_user_info.__name__)
    except IndexError as ie:
        print('ID not found')
        logging.error('ID not found')
        logging.error(ie.args)
        logging.error(sys.exc_info())
    except PermissionError as pe:
        print('Operation not allowed')
        logging.error('Operation not allowed')
        logging.error('%s (Role: %s) attempting to perform %s',u_obj,u_obj.role,assign.User.get_user_info.__name__)
        logging.error(pe.args)
        logging.error(sys.exc_info())
    except:
        print('Unexpected error')
        logging.error('Unexpected error:')
        logging.error(sys.exc_info())

def client_count_users():
    logging.info('Executing %s',client_count_users.__name__)
    try:
        assign.check_privelege('user_count',u_obj.role)
        count = assign.User.user_count(u_obj)
        print('Total Number of users:',count)
        logging.info('Successful execution of %s',client_count_users.__name__)
    except PermissionError as pe:
        print('Operation not allowed')
        logging.error('Operation not allowed')
        logging.error('%s (Role: %s) attempting to perform %s',u_obj,u_obj.role,assign.User.user_count.__name__)
        logging.error(pe.args)
        logging.error(sys.exc_info())
    except:
        print('Unexpected error')
        logging.error('Unexpected error:')
        logging.error(sys.exc_info())

def client_role_based_user_count():
    logging.info('Executing %s',client_role_based_user_count.__name__)
    try:
        assign.check_privelege('role_based_user_count',u_obj.role)
        print('Enter Role you would like to search for:')
        query_role = input()
        count = assign.User.role_based_user_count(u_obj,query_role)
        print('Count of users performing '+query_role+' is '+str(count))
        logging.info('Successful execution of %s',client_role_based_user_count.__name__)
    except RoleError as ve:
        print('Role Not Present')
        logging.error('Role Not Present')
        logging.error(ve.args)
        logging.error(sys.exc_info())
    except PermissionError as pe:
        print('Operation not allowed')
        logging.error('Operation not allowed')
        logging.error('%s (Role: %s) attempting to perform %s',u_obj,u_obj.role,assign.User.role_based_user_count.__name__)
        logging.error(pe.args)
        logging.error(sys.exc_info())
    except:
        print('Unexpected error:')
        logging.error('Unexpected error:')
        logging.error(sys.exc_info())

def client_get_user_role():
    logging.info('Executing %s',client_get_user_role.__name__)
    try:
        assign.check_privelege('get_user_role',u_obj.role)
        print('Enter the user ID for retrieval of role')
        q_id = int(input())
        q_role = assign.User.get_user_role(u_obj,q_id)
        print('User Role: '+q_role)
        logging.info('Successful Execution of %s',client_get_user_role.__name__)
    except PermissionError as pe:
        print('Operation not allowed')
        logging.error('Operation not allowed')
        logging.error('%s (Role: %s) attempting to perform %s',u_obj,u_obj.role,assign.User.get_user_role.__name__)
        logging.error(pe.args)
        logging.error(sys.exc_info())
    except:
        print('Unexpected error:')
        logging.error('Unexpected error:')
        logging.error(sys.exc_info())

def client_add_user():
    logging.info('Executing %s',client_add_user.__name__)
    try:
        assign.check_privelege('add_user',u_obj.role)
        print('Enter the user details')
        print('Enter the User Name')
        nu_name = input()
        print('Enter the password')
        nu_pass = input()
        print('Enter the ID')
        nu_id = int(input())
        print('Enter the desc')
        nu_desc = input()
        print('Enter the role')
        nu_role = input()
        nu_obj = assign.User.create_user(u_obj,nu_desc,nu_id,nu_name,nu_pass,nu_role)
        status = assign.Actions.add_user(u_obj,nu_obj)
        if(status==1):
            logging.info('Successful Execution of %s',client_add_user.__name__)
    except KeyError as ke:
        print('ID already present')
        logging.error('ID already present')
        logging.error(ke.args)
        logging.error(sys.exc_info())
    except RoleError as ve:
        print('Role not Present')
        logging.error('Role not Present')
        logging.error(ve.args)
        logging.error(sys.exc_info())
    except PermissionError as pe:
        print('Operation not allowed')
        logging.error('Operation not allowed')
        logging.error('%s (Role: %s) attempting to perform %s',u_obj,u_obj.role,assign.Actions.add_user.__name__)
        logging.error(pe.args)
        logging.error(sys.exc_info())
    except:
        print('Unexpected error:')
        logging.error('Unexpected error:')
        logging.error(sys.exc_info())
    
def client_delete_user():
    logging.info('Executing %s',client_delete_user.__name__)
    try:
        assign.check_privelege('delete_user',u_obj.role)
        print('Enter the user ID for deletion')
        q_id = int(input())
        status = assign.Actions.delete_user(u_obj,q_id)
        if(status==1):
            logging.info('Successful Execution of %s',client_add_user.__name__)
    except IndexError as ie:
        print('ID not found')
        logging.error('ID not found')
        logging.error(ie.args)
        logging.error(sys.exc_info())
    except PermissionError as pe:
        print('Operation not allowed')
        logging.error('Operation not allowed')
        logging.error('%s (Role: %s) attempting to perform %s',u_obj,u_obj.role,assign.Actions.delete_user.__name__)
        logging.error(pe.args)
        logging.error(sys.exc_info())
    except:
        print('Unexpected error:')
        logging.error('Unexpected error:')
        logging.error(sys.exc_info())

def client_set_user_role():
    logging.info('Executing %s',client_set_user_role.__name__)
    try:
        assign.check_privelege('set_user_role',u_obj.role)
        print('Enter the user ID for updation')
        q_id = int(input())
        print('Enter the role')
        q_role = input()
        status = assign.Actions.set_user_role(u_obj,q_id,q_role)
        if(status == -1):
            raise IndexError('ID not present')
        if(status == 1):
            logging.info('Successful Execution of %s',client_set_user_role.__name__)
    except IndexError as ie:
        print('ID not present')
        logging.error('ID not found')
        logging.error(ie.args)
        logging.error(sys.exc_info())
    except RoleError as ve:
        print('Role not present')
        logging.error('Role not Present')
        logging.error(ve.args)
        logging.error(sys.exc_info())
    except RuntimeError as re:
        print('Moderator trying to change someone to admin OR trying to change admin priveleges')
        logging.error(re.args)
        logging.error(sys.exc_info())
    except PermissionError as pe:
        print('Operation not allowed')
        logging.error('Operation not allowed')
        logging.error('%s (Role: %s) attempting to perform %s',u_obj,u_obj.role,assign.Actions.delete_user.__name__)
        logging.error(pe.args)
        logging.error(sys.exc_info())
    except:
        print('Unexpected error:')
        logging.error('Unexpected error:')
        logging.error(sys.exc_info())

def client_edit_user():
    logging.info('Executing %s',client_edit_user.__name__)
    try:
        assign.check_privelege('edit_user',u_obj.role)
        print('Enter the details you wish to change')
        print('Enter Name:(optional)')
        uname = input()
        print('Enter Description:(optional)')
        udesc = input()
        print('Enter ID:')
        uid = int(input())
        status = assign.Actions.edit_user(u_obj,uid,udesc,uname)
        if(status == 1):
            logging.info('Successful Execution of %s',client_edit_user.__name__)
    except RuntimeError as re:
        print('Moderator trying to change priveleges of admin')
        logging.error('Moderator trying to change priveleges of admin')
        logging.error(re.args)
        logging.error(sys.exc_info())
    except ValueError as ve:
        print('ID not found')
        logging.error('ID not found')
        logging.error(ie.args)
        logging.error(sys.exc_info())
    except PermissionError as pe:
        print('Operation not allowed')
        logging.error('Operation not allowed')
        logging.error('%s (Role: %s) attempting to perform %s',u_obj,u_obj.role,assign.Actions.delete_user.__name__)
        logging.error(pe.args)
        logging.error(sys.exc_info())
    except:
        print('Unexpected error:')
        logging.error('Unexpected error:')
        logging.error(sys.exc_info())