"""
Design Patterns Used : 
1) Singleton : File Handler Class
2) Factory : User Class
3) Model View Controller
"""
import json
import pprint
from abc import ABC
import sys
import logging


roles = json.loads(open('/home/keertankrishnan/Downloads/roles.json').read())
logging.basicConfig(filename='exec_log.log',level=logging.DEBUG)

class RoleError(Exception):
    def __init__(self, message):
        self.message = message
        


def check_privelege(operation,queryrole):
    """Function that takes the operation, and the role trying to attempt the operation 
    as parameters and checks whether the operation is allowed. Permission Error is raised,
    if the operation is not allowed, and 1 is returned if the operation is allowed."""
    logging.info('Checking privelege for %s by %s',operation,queryrole)
    if(queryrole=='admin'):
        logging.info('Operation approved (admin)')
        return 1
    if(operation in roles['role_priviledges'][queryrole]['allowed']):
        logging.info('Operation %s approved (%s)',operation,queryrole)
        return 1
    else:
        logging.error('%s was not allowed by %s',operation,queryrole)
        raise PermissionError('Operation not allowed')


class File_Handler:
    """This class uses the singleton design pattern"""
    __instance = None
    #Do we need new file handler objects for each function?
    def __init__(self):
        if(File_Handler.__instance!=None):
            logging.error('Exception: %d attempted to create multiple file handlers',self)
            raise Exception('Multiple file handlers being used!')
        else:
            
            File_Handler.__instance = self
            logging.info('File Handler Singleton object created: %s',File_Handler.__instance)
    
    @staticmethod
    def get_file_handler():
        
        if(File_Handler.__instance == None):
            File_Handler()
        return File_Handler.__instance
    
    def get_user_obj(self,u_id):
        """"File handler function to read and return a single object. Takes 
        calling object and ID of the object to be read as parameters, and 
        returns it. Returns -1 if object not found"""
        f = open('/home/keertankrishnan/Downloads/userdata.json','r')
        #Optimize
        user_list = json.loads(f.read())
        logging.info('File finished reading by %s (executing File_Handler.%s)',self,File_Handler.get_user_obj.__name__)
        flag = 0
        for i in user_list:
            if(i['id']==u_id):
                logging.info('File Handler Object %s found object with ID %s (executing File_Handler.%s)',self,u_id,File_Handler.get_user_obj.__name__)
                flag = 1
                user_obj = User(i['desc'],i['id'],i['name'],i['pass'],i['role'])
                f.close()
                return user_obj
        if(flag==0):
            logging.warning('File Handler Object %s was unable to find object with ID %s (executing File_Handler.%s)',self,u_id,File_Handler.get_user_obj.__name__)
            return -1
        f.close()

    
    def get_num_users(self):
        """File handling function to read the number of users."""
        f = open('/home/keertankrishnan/Downloads/userdata.json','r')
        #Optimize
        count =  len(json.loads(f.read()))
        logging.info('File finished reading by %s (executing File_Handler.%s)',self,File_Handler.get_num_users.__name__)
        f.close()
        return count

    def get_num_users_role(self, role_name):
        """File handling function to read the number of users from file based on role"""
        f = open('/home/keertankrishnan/Downloads/userdata.json','r')
        count = 0
        logging.info('File finished reading by %s (executing File_Handler.%s)',self,File_Handler.get_num_users_role.__name__)
        #Optimize
        user_list = json.loads(f.read())
        for i in user_list:
            if(i['role']==role_name):
                count += 1
        f.close()
        return count

    def write_new_obj(self,new_obj):
        #Write only single object, not whole file
        #Know it's a list, so remove last ], and then add obj, and add on ]
        """File handling function to write a new object to the file. Takes the calling 
        object and the new object as parameters. If ID is already present, a KeyError is 
        raised and 0 is returned. Else 1 is returned."""
        f = open('/home/keertankrishnan/Downloads/userdata.json','r+')
        logging.info('File finished reading by %s (executing File_Handler.%s)',self,File_Handler.write_new_obj.__name__)
        #Optimize
        user_list = json.loads(f.read())
        for i in user_list:
            if(i['id']==new_obj.id):
                logging.warning('Key %s already found in file (executing File_Handler.%s)',new_obj.id,File_Handler.write_new_obj.__name__)
                raise KeyError('ID already present!')
                return 0
        f.close()
        f = open('/home/keertankrishnan/Downloads/userdata.json','w')
        logging.info('File opened by file handler obj %s for writing (executing File_Handler.%s)',self,File_Handler.write_new_obj.__name__)
        new_dict = {'id':new_obj.id,'name':new_obj.name,'pass':new_obj.passwo,'role':new_obj.role,'desc':new_obj.desc}
        user_list.append(new_dict)
        if(f.write(json.dumps(user_list, indent = 4))):
            logging.info('File successfully written by %s (executing File_Handler.%s)',self,File_Handler.write_new_obj.__name__)
            f.close()
            return 1
    
    def del_obj(self,del_id):
        """File handling function for deleting an object. Takes the calling object and the 
        ID of the object obe deleted as parameters. Returns 1 if object is found and return 
        -1 if not found."""
        f = open('/home/keertankrishnan/Downloads/userdata.json','r+')
        logging.info('File finished reading by %s (executing File_Handler.%s)',self,File_Handler.del_obj.__name__)
        #Optimize
        found = -1
        user_list = json.loads(f.read())
        for i in range(len(user_list)):
            #print(user_list[i])
            if(user_list[i]['id']==del_id):
                found = 1
                f.close()
                logging.info('File handler %s found object with ID %s (executing File_Handler.%s)',self,del_id,File_Handler.del_obj.__name__)
                user_list.pop(i)
                break
        if(found==-1):
            logging.warning('File handler %s finished reading, but was unable object with ID %s (executing File_Handler.%s)',self,del_id,File_Handler.del_obj.__name__)
        if(found==1):      
            f = open('/home/keertankrishnan/Downloads/userdata.json','w')
            f.write(json.dumps(user_list,indent = 4))
            logging.info('File Handler %s finished writing file (executing File_Handler.%s)',self,File_Handler.del_obj.__name__)
        f.close()
        return found

    def overwrite(self,obj):
        """File handling function for overwriting an object in the file. Takes the
        calling object, and the object to be written as parameters. Pops the item out of the 
        list, and then adds the new object, and then writes the whole file again. 1 is returned
        if successful."""
        f = open('/home/keertankrishnan/Downloads/userdata.json','r+')
        #Optimize
        found = -1
        user_list = json.loads(f.read())
        logging.info('File Handler %s finished reading file (executing File_Handler.%s)',self,File_Handler.overwrite.__name__)
        for i in range(len(user_list)):
            #print(user_list[i])
            if(user_list[i]['id']==obj.id):
                found = 1
                logging.info('File Handler %s found object with matching ID %s (executing File_Handler.%s)',self,obj.id,File_Handler.overwrite.__name__)
                f.close()
                user_list.pop(i)
                f = open('/home/keertankrishnan/Downloads/userdata.json','w')
                new_dict = {'id':obj.id,'name':obj.name,'pass':obj.passwo,'role':obj.role,'desc':obj.desc}
                user_list.insert(i,new_dict)
                if(f.write(json.dumps(user_list, indent = 4))):
                    f.close()
                    logging.info('File Handler %s finished writing %s to file (executing File_Handler.%s)',self,obj,File_Handler.overwrite.__name__)
                    return 1
                break
        if(found==-1):
            logging.warning('File Handler %s could not find object with ID %s (executing File_Handler.%s)',self,obj.id,File_Handler.overwrite.__name__)
            return -1
            

    



class User:
    """User Class. Encapsulates all attributes and functions of the user objects. Does NOT
    deal with file I/O operations. If file I/O is required, suitable calls are issued to 
    the file handling class."""
    def __init__(self,desc,idi,name,passwo,role):
        """Initialize instances of users"""
        self.desc = desc
        self.id = idi
        self.name = name
        self.passwo = passwo
        self.role = role
        logging.info('User Object %s created with ID %s',self,idi)
    
    def get_user_info(self,idi):
        """Takes the object calling, and the ID of the object whose details are being 
        requested, as parameters. If the object cannot be found, an IndexError is raised.
        If it is found, a call is issued to the file handler function, get_user_obj"""
        logging.info('User Object %s and ID %s executing User.%s',self,self.id,User.get_user_info.__name__)
        queryrole = self.role
        q_obj = File_Handler.get_file_handler().get_user_obj(idi)
        if(q_obj==-1):
            #print('server')
            logging.error('User Object with ID %s not found (executing User.%s)')
            raise IndexError('ID not found',self,idi)
            
        return q_obj
    
    def user_count(self):
        """Takes the calling object as parameter.Finds the total number of users 
        which have been registered using the file handler function, get_num_users and 
        returns it."""
        logging.info('User Object %s and ID %s executing User.%s',self,self.id,User.user_count.__name__)
        queryrole = self.role
        return File_Handler.get_file_handler().get_num_users()

    def role_based_user_count(self,query_role):
        """Takes the calling object and the role being queried for as parameters. 
        Finds the total number of users who work in that role, by using the file
        handling function, get_num_users_role and returns it. If role is not present, Value
        Error is raised."""
        logging.info('User Object %s and ID %s executing User.%s',self,self.id,User.role_based_user_count.__name__)
        queryrole = self.role
        
        role_names = list(roles['role_priviledges'].keys())
        if(query_role not in role_names):
            logging.error('User Object %s and ID %s tried to find role %s, that does not exist (executing User.%s)',self,self.id,query_role,User.role_based_user_count.__name__)
            raise RoleError('Role Not Present')
        else:
            logging.info('User Object %s and ID %s found role %s, that exists (executing User.%s)',self,self.id,query_role,User.role_based_user_count.__name__)
            return File_Handler.get_file_handler().get_num_users_role(query_role)

    def get_user_role(self,idi):
        """Takes the calling object and the ID of the object whose role is being requested
        as parameters. Reads the object using the file handling function, get_user_obj,
        and returns role, if ID is valid. If ID is not valid, guest is returned."""
        logging.info('User Object %s and ID %s executing User.%s',self,self.id,User.get_user_role.__name__)
        queryrole = self.role
        role = 'guest'
        q_obj = File_Handler.get_file_handler().get_user_obj(idi)
        if(q_obj==-1):
            logging.warning('ID %s does not exist, hence guest role being returned (executing User.%s)',idi,User.get_user_role.__name__)
            return role
        else:
            logging.info('ID %s found in file (executing User.%s)',idi,User.get_user_role.__name__)
            return q_obj.role
    @staticmethod
    def verify(uname,upass):
        """Verify the user based on user name and password. 
        Creates User object and returns it.
        Return codes : -1 : password wrong -2 : user name wrong
        Design Pattern Used : Factory"""
        logging.info('Executing User.%s',User.verify.__name__)
        f = open('/home/keertankrishnan/Downloads/userdata.json','r+')
        #Optimize
        user_list = json.loads(f.read())
        ufound = 0
        uver = 0
        for i in user_list:
            if(i['name']==uname):
                logging.info('User with Username %s found in file (executing User.%s)',uname,User.verify.__name__)
                ufound = 1
                if(i['pass'] == upass):
                    uver = 1
                    logging.info('User with Username %s authenticated (executing User.%s)',uname,User.verify.__name__)
                    return User(i['desc'],i['id'],i['name'],i['pass'],i['role'])
                else:
                    logging.error('User with Username %s not authenicated. Wrong Password. (executing User.%s)',uname,User.verify.__name__)
                    return -1
        if(ufound==0):
            logging.error('User with Username %s not found.(executing User.%s)',uname,User.verify.__name__)
            return -2
    def create_user(self,desc,idi,name,passwo,role):
        """Takes user details and returns the created object. Meant to be used as an 
        interface for creation
        Design Pattern : Factory"""
        logging.info('Executing User.%s',User.create_user.__name__)
        new_obj = User(desc,idi,name,passwo,role)
        logging.info('User object %s with ID %s created by %s (executing User.%s)',self,str(self.id),new_obj,User.create_user.__name__)
        return new_obj





class Actions(ABC):
    """Class created only for moderator and admin activities. No file I/o operations are 
    handled by this class. If file I/O operations are required, then file handler operaitons
    are called."""
    @staticmethod
    def add_user(user_obj,add_obj):
        """Function to add a user. The object calling the operation and the new object are 
        taken as parameters. If the role is not valid, a ValueError is raised. If role is 
        valid, call is issued to the file handler operation, write_new_obj. """
        logging.info('%s executing Actions.%s',user_obj,Actions.add_user.__name__)
        status = 0
        queryrole = user_obj.role
        role_names = list(roles['role_priviledges'].keys())
        if(add_obj.role not in role_names):
            logging.error('Role %s not valid (executing Actions.%s)',add_obj.role,Actions.add_user.__name__)
            raise RoleError('Role Not Present')
        else:
            logging.info('Role %s found and valid. (executing Actions.%s)',add_obj.role,Actions.add_user.__name__)
            status = File_Handler.get_file_handler().write_new_obj(add_obj)
            logging.warning('User %s with ID %s has been added. (executing Actions.%s)',add_obj,add_obj.id,Actions.add_user.__name__)
        return status

    @staticmethod
    def delete_user(x,del_id):
        """Function to delete a user. The calling object and the ID of the object to be deleted 
        are taken as parameters. A call is issued to the file handling function to delete an object.
        If the ID is not found, an IndexError is raised. """
        logging.info('%s executing Actions.%s',x,Actions.delete_user.__name__)
        status = 0
        queryrole = x.role
        
        status = File_Handler.get_file_handler().del_obj(del_id)
        if(status==-1):
            logging.error('Execution Error: ID not found (executing Actions.%s)',)
            raise IndexError('ID not found')
        logging.warning('User with ID %s has been deleted by %s and ID %s (executing Actions.%s)',del_id,x,x.id,Actions.delete_user.__name__)
        return status

    @staticmethod
    def set_user_role(x,idi,setrole):
        """Function to set user roles. The calling object, ID of the object whose role 
        is to be changed, and the role to be set to, are taken as parameters. A valueError 
        is raised in case the role is not valid, or a RuntimeError, or an IndexError."""
        logging.info('%s executing Actions.%s',x,Actions.set_user_role.__name__)
        status = 0 
        queryrole = x.role
        role_names = list(roles['role_priviledges'].keys())
        if(setrole not in role_names):
            logging.error('Execution Error: Role %s not present (executing Actions.%s)',setrole,Actions.set_user_role.__name__)
            raise RoleError('Role not present')
        #check_privelege('set_user_role',queryrole)
        if(queryrole=='moderator' and setrole == 'admin'):
            logging.error('Execution Error: Moderator %s trying to change user with ID %s to admin OR attempting to change admin privileges(executing Actions.%s)',x,str(idi),Actions.set_user_role.__name__)
            raise RuntimeError('Moderator trying to change someone to admin OR trying to change admin priveleges')
        flag =0
        q_obj = File_Handler.get_file_handler().get_user_obj(idi)
        if(queryrole=='moderator' and q_obj.role=='admin'):
            logging.error('Execution Error: Moderator %s trying to change user with ID %s to admin OR attempting to change admin privileges(executing Actions.%s)',x,str(idi),Actions.set_user_role.__name__)
            raise RuntimeError('Moderator trying to change someone to admin OR trying to change admin priveleges')
        if(q_obj!=-1):
            flag = 1
            status = 1
            logging.warning('Role of user with ID %s has been changed to %s by %s (executing Actions.%s)',idi,setrole,x, Actions.set_user_role.__name__)
            q_obj.role = setrole
            File_Handler.get_file_handler().overwrite(q_obj)
        if(flag==0):
            logging.error('User with ID %s not found (executing Actions.%s)',idi,Actions.set_user_role.__name__)
            raise IndexError("ID not found")
        return status
    @staticmethod
    def edit_user(x,idi,desc='',name=''):
        """Function to edit a user description and name. Takes the calling object, and
        the ID of the object whose details are to changed, along with the details as
        parameters. After changing, the object is overwritten through the file handling
        overwrite function. """
        logging.info('%s executing Actions.%s',x,Actions.edit_user.__name__)
        status = 0
        queryrole = x.role
        check_privelege('edit_user',queryrole)
        q_obj = File_Handler.get_file_handler().get_user_obj(idi)
        if(queryrole=='moderator' and q_obj.role=='admin'):
            logging.error('User Object %s with ID %s attempting to edit details of admin (id %s)(executing Actions.%s)',x,x.id,idi,Actions.edit_user.__name__)
            raise RuntimeError('Moderator attempting to edit details of admin')
            
        if(q_obj!=-1):
            logging.info('User object with ID %s found(executing Actions.%s)',idi,Actions.edit_user.__name__)
            status = 1
            if(desc!=''):
                q_obj.desc = desc
            if(name!=''):
                q_obj.name = name
            logging.warning('User object with ID %s changed to Name: %s Description %s by object %s and ID %s (executing Actions.%s)',idi,name,desc,x,x.id,Actions.edit_user.__name__)
        if(status==0):
            logging.error('User Object with ID %s not found(executing Actions.%s)',idi,Actions.edit_user.__name__)
            raise IndexError('ID not found')
        File_Handler.get_file_handler().overwrite(q_obj)
        
        return status