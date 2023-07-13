#!/usr/bin/python3
"""Entry point of command interpreter"""

import cmd
from models.base_model import BaseModel
import models
import re
import math


class HBNBCommand(cmd.Cmd):
    """Console class"""

    class_mapping = {'BaseModel': BaseModel}

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
        if not arg:
            print("** class name missing **")
        else:
            if arg in self.class_mapping:
                obj = self.class_mapping[arg]()
                obj.save()
                print(obj.id)
            else:
                print("** class doesn't exist **")

    def do_show(self, arg):
        """Prints string representation of an instance"""
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
            if class_name in self.class_mapping:
                key = f"{class_name}.{obj_id}"
                all_objs = models.storage.all()
                if key in all_objs:
                    print(all_objs[key])
                else:
                    print("** no instance found **")
            else:
                print("** class doesn't exist **")

    def do_destroy(self, arg):
        """Deletes an instance based on the class name and id"""
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
        elif len(args) == 1:
            if args[0] not in self.class_mapping:
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

    def do_all(self, arg):
        """ Show All instance """
        model_name = arg
        if arg and model_name not in self.class_mapping:
            print("** class doesn't exist **")
            return

        list_objs = []
        all_objs = models.storage.all().items()
        if arg:
            for key, value in all_objs:
                if type(value) == self.class_mapping[model_name]:
                    list_objs.append(str(value))
            return print(list_objs)

        for key, value in all_objs:
            list_objs.append(str(value))
        print(list_objs)

    def do_update(self, args):
        args_list = args.split()
        args_len = len(args_list)
        conversion_dict = {
            "str": str,
            "int": lambda x: int(math.trunc(float(x))),
            "float": float
        }
        # handle missing args
        if args_len == 0:
            print("** class name missing **")
            return
        if args_len == 1:
            print("** instance id missing **")
            return
        if args_len == 2:
            print("** attribute name missing **")
            return
        if args_len == 3:
            print("** value missing **")
            return

        class_name, id, name, *value = args_list
        if class_name not in self.class_mapping:
            print("** class doesn't exist **")
            return
        # check if obj exist
        obj = self.get_by_id(class_name, id)
        if obj == False:
            print("** no instance found **")
            return
        # check if attribuet already exist then cast
        if hasattr(obj, name):
            attr = getattr(obj, name)
            attr_type = attr.__class__.__name__
            new_val = " ".join(value)
            result = self.handle_type(new_val)
            val_to_insert = conversion_dict[attr_type](result['val'])
            setattr(obj, name, val_to_insert)
            obj.save()
            return
        # for string in double qoutes
        new_val = " ".join(value)
        result = self.handle_type(new_val)
        val_to_insert = conversion_dict[result['type']](result['val'])
        setattr(obj, name, val_to_insert)
        obj.save()

    def is_float(self, num):
        try:
            int(num)
            return False
        except ValueError:
            return True

    def get_str(self, string):
        if string[0] == '"':
            return re.search('"[^"]*"', string).group()[1:-1]
        if string[0].isalpha():
            return string.split()[0]

    def handle_type(self, string):
        result = {}
        if string[0] == '"' or string[0].isalpha():
            result["val"] = self.get_str(string)
            result["type"] = "str"
            return result
        value = string.split()[0]
        result["val"] = value
        if self.is_float(value) == True:
            result["type"] = "float"
        else:
            result["type"] = "int"
        return result

    def get_by_id(self, class_name, id):
        """ return obj if exist in storage otherwise return False"""
        key = f"{class_name}.{id}"
        if key in models.storage.all():
            return models.storage.all()[key]
        return False


if __name__ == '__main__':
    HBNBCommand().cmdloop()
