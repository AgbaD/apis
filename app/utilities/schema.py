#!/usr/bin/python3
# Author:   @AgbaD | @Agba_dr3

from jsonschema import validate
from jsonschema.exceptions import ValidationError, SchemaError

userRegSchema = {
    "type": "object",
    "properties": {
        "email": {
            "type": "string",
            "format": "email",
            "minLength": 8
        },
        "firstname": {
            "type": "string",
            "maxLength": 23,
            "minLength": 3
        },
        "lastname": {
            "type": "string",
            "maxLength": 23,
            "minLength": 3
        },
        "password": {
            "type": "string",
            "minLength": 8
        },
        "phone": {
            "type": "string",
            "maxLength": 14,
            "minLength": 11
        },
        "address": {
            "type": "string"
        },
    },
    "required": ["firstname", "lastname", "email", "password", "phone"],
    "additionalProperties": False
}

userLoginSchema = {
    "type": "object",
    "properties": {
        "email": {
            "type": "string",
            "format": "email"
        },
        "password": {
            "type": "string"
        },
    },
    "required": ["email", "password"],
    "additionalProperties": False
}


def validate_reg(user):
    try:
        validate(user, userRegSchema)
        return {"msg": "success"}
    except SchemaError as e:
        return {"msg": "error", "error": e.message}
    except ValidationError as e:
        p = list(e.schema_path)
        print(p)
        print(len(p))
        if len(p) > 1:
            if p[1] == 'password' and p[2] == 'minLength':
                error_message = "Password too short, minimum length of 8 characters"
                return {"msg": "error", "error": error_message}
            if p[1] == 'phone':
                error_message = "Phone number is invalid, please check!"
                return {"msg": "error", "error": error_message}
            if p[1] == 'firstname':
                if p[2] == 'minLength':
                    error_message = "Firstname too short, minimum of 3 characters"
                    return {"msg": "error", "error": error_message}
                if p[2] == 'maxLength':
                    error_message = "Firstname too long, maximum of 23 characters"
                    return {"msg": "error", "error": error_message}
            if p[1] == 'lastname':
                if p[2] == 'minLength':
                    error_message = "Lastname too short, minimum of 3 characters"
                    return {"msg": "error", "error": error_message}
                if p[2] == 'maxLength':
                    error_message = "Lastname too long, maximum of 23 characters"
                    return {"msg": "error", "error": error_message}
        return {"msg": "error", "error": e.message}


def validate_login(user):
    try:
        validate(user, userLoginSchema)
        return {"msg": "success"}
    except SchemaError as e:
        return {"msg": "error", "error": e.message}
    except ValidationError as e:
        return {"msg": "error", "error": e.message}
