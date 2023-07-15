#!/usr/bin/python3
"""Entry point of command interpreter"""

import cmd
from models.base_model import BaseModel
import models
import re
import shlex
from models.user import User
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.amenity import Amenity


class HBNBCommand(cmd.Cmd):
    """Console class"""

    class_mapping = {
        'BaseModel': BaseModel, 'User': User, 'State': State, 'City': City,
        'Amenity': Amenity, 'Place': Place, 'Review': Review
    }

    prompt = "(hbnb) "

    def do_quit(self, arg):
        """ Quit command to exit the program"""
        return True

    def do_EOF(self, arg):
        """Exit the program when it's called"""
        print()
        return True

    def emptyline(self):
        """Override emptyline method to do nothing"""
        pass

    def do_create(self, arg):
        """Creates a new instance of BaseModel"""
        arg_list = shlex.split(arg)
        if len(arg_list) == 0:
            print("** class name missing **")
        elif arg_list[0] not in self.class_mapping:
            print("** class doesn't exist **")
        else:
            obj = self.class_mapping[arg_list[0]]()
            print(obj.id)
            obj.save()

    def do_show(self, arg):
        """Prints string representation of an instance"""
        args = shlex.split(arg)
        if len(args) == 0:
            print("** class name missing **")
        elif len(args) == 1:
            if args[0] in self.class_mapping:
                print("** instance id missing **")
            else:
                print("** class doesn't exist **")
        else:
            class_name = args[0]
            obj_id = args[1]
            key = f"{class_name}.{obj_id}"
            all_objs = models.storage.all()

            if class_name not in self.class_mapping:
                print("** class doesn't exist **")
            elif key not in all_objs:
                print("** no instance found **")
            else:
                print(all_objs[key])

    def do_destroy(self, arg):
        """Deletes an instance based on the class name and id"""
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
        elif len(args) == 1:
            if args[0] in self.class_mapping:
                print("** instance id missing **")
            else:
                print("** class doesn't exist **")
        else:
            class_name = args[0]
            obj_id = args[1]
            all_objs = models.storage.all()
            key = f"{class_name}.{obj_id}"
            if key in all_objs:
                del all_objs[key]
                models.storage.save()
            else:
                print("** no instance found **")

    def do_all(self, args):
        """ Show All instance """
        arg = shlex.split(args)
        if arg and arg[0] not in self.class_mapping:
            print("** class doesn't exist **")
            return

        list_objs = []
        all_objs = models.storage.all().items()
        if len(arg) > 0:
            for key, value in all_objs:
                if value["__class__"] in self.class_mapping:
                    list_objs.append(str(value))
        else:
            for key, value in all_objs:
                list_objs.append(str(value))
        if len(list_objs) > 0:
            print(list_objs)

    def do_update(self, args):
        """update"""
        tokens = shlex.split(args)
        args_len = len(tokens)

        if args_len == 0:
            print("** class name missing **")
            return
        class_name = tokens[0]
        if args_len == 1:
            if class_name not in self.class_mapping:
                print("** class doesn't exist **")
            else:
                print("** instance id missing **")
            return
        id = tokens[1]
        instance = self.get_by_id(class_name, id)
        if args_len == 2:
            if instance == False:
                print("** no instance found **")
            else:
                print("** attribute name missing **")
            return

        if args_len == 3:
            print("** value missing **")
            return

        attribute_name = tokens[2]
        attribute_value = tokens[3]

        if attribute_name not in ["id", "created_at", "updated_at"]:
            if hasattr(instance, attribute_name):
                attr_type = type(getattr(instance, attribute_name))
                setattr(instance, attribute_name, attr_type(attribute_value))
            else:
                setattr(instance, attribute_name, attribute_value)
            instance.save()

    def get_by_id(self, class_name, id):
        """ return obj if exist in storage otherwise return False"""
        key = f"{class_name}.{id}"
        if key in models.storage.all():
            return models.storage.all()[key]
        return False


if __name__ == '__main__':
    HBNBCommand().cmdloop()
