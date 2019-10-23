#include <assert.h>
#include <string.h>
#include <stdio.h>
#include "py/obj.h"
#include "py/runtime.h"
#include "py/builtin.h"

/************************** hello fun **************************/

STATIC mp_obj_t uhello_hello(mp_uint_t n_args, const mp_obj_t *args){
    if(n_args == 0){
        mp_raise_ValueError("Not enough arguments");
        return mp_const_none;
    }
    for(int i=0; i<n_args; i++){
        int v = mp_obj_get_int(args[i]);
        printf("%d\n", v);
    }
    return mp_const_none;
}

STATIC MP_DEFINE_CONST_FUN_OBJ_VAR(uhello_hello_obj, 0, uhello_hello);


typedef struct _mp_obj_hi_t {
    mp_obj_base_t base;
    int v;
} mp_obj_hi_t;

STATIC mp_obj_t uhello_hi_make_new(const mp_obj_type_t *type, size_t n_args, size_t n_kw, const mp_obj_t *args) {
    mp_arg_check_num(n_args, n_kw, 0, 1, false);
    mp_obj_hi_t *o = m_new_obj(mp_obj_hi_t);//, char, sizeof(SHA1_CTX));
    o->base.type = type;
    // sha1_Init((SHA1_CTX*)o->state);
    o->v = 0;
    if (n_args == 1) {
        o->v = mp_obj_get_int(args[0]);
        // hashlib_sha1_update(MP_OBJ_FROM_PTR(o), args[0]);
    }
    printf("assigned number %d to self\n", o->v);
    return MP_OBJ_FROM_PTR(o);
}

STATIC mp_obj_t uhello_hi_print(mp_uint_t n_args, const mp_obj_t *args) {
    mp_obj_hi_t *self = MP_OBJ_TO_PTR(args[0]);//, char, sizeof(SHA1_CTX));
    printf("Our number: %d\n", self->v);
    uhello_hello(n_args-1, args+1);
    return mp_const_none;
}

STATIC MP_DEFINE_CONST_FUN_OBJ_VAR(uhello_hi_print_obj, 1, uhello_hi_print);

STATIC const mp_rom_map_elem_t uhello_hi_locals_dict_table[] = {
    { MP_ROM_QSTR(MP_QSTR_print), MP_ROM_PTR(&uhello_hi_print_obj) },
};

STATIC MP_DEFINE_CONST_DICT(uhello_hi_locals_dict, uhello_hi_locals_dict_table);

STATIC const mp_obj_type_t uhello_hi_type = {
    { &mp_type_type },
    .name = MP_QSTR_hi,
    .make_new = uhello_hi_make_new,
    .locals_dict = (void*)&uhello_hi_locals_dict,
};


/****************************** MODULE ******************************/

STATIC const mp_rom_map_elem_t uhello_module_globals_table[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_uhello) },
    { MP_ROM_QSTR(MP_QSTR_hi), MP_ROM_PTR(&uhello_hi_type) },
    { MP_ROM_QSTR(MP_QSTR_hello), MP_ROM_PTR(&uhello_hello_obj) },
};

STATIC MP_DEFINE_CONST_DICT(uhello_module_globals, uhello_module_globals_table);

const mp_obj_module_t uhello_user_cmodule = {
    .base = { &mp_type_module },
    .globals = (mp_obj_dict_t*)&uhello_module_globals,
};

MP_REGISTER_MODULE(MP_QSTR_uhello, uhello_user_cmodule, MODULE_UHELLO_ENABLED);
