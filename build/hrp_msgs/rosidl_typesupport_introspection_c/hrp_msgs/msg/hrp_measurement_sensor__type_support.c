// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from hrp_msgs:msg/HrpMeasurementSensor.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "hrp_msgs/msg/hrp_measurement_sensor__rosidl_typesupport_introspection_c.h"
#include "hrp_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "hrp_msgs/msg/hrp_measurement_sensor__functions.h"
#include "hrp_msgs/msg/hrp_measurement_sensor__struct.h"


#ifdef __cplusplus
extern "C"
{
#endif

void HrpMeasurementSensor__rosidl_typesupport_introspection_c__HrpMeasurementSensor_init_function(
  void * message_memory, enum rosidl_runtime_c_message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  hrp_msgs__msg__HrpMeasurementSensor__init(message_memory);
}

void HrpMeasurementSensor__rosidl_typesupport_introspection_c__HrpMeasurementSensor_fini_function(void * message_memory)
{
  hrp_msgs__msg__HrpMeasurementSensor__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember HrpMeasurementSensor__rosidl_typesupport_introspection_c__HrpMeasurementSensor_message_member_array[3] = {
  {
    "f",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT16,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(hrp_msgs__msg__HrpMeasurementSensor, f),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "l",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT16,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(hrp_msgs__msg__HrpMeasurementSensor, l),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "r",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT16,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(hrp_msgs__msg__HrpMeasurementSensor, r),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers HrpMeasurementSensor__rosidl_typesupport_introspection_c__HrpMeasurementSensor_message_members = {
  "hrp_msgs__msg",  // message namespace
  "HrpMeasurementSensor",  // message name
  3,  // number of fields
  sizeof(hrp_msgs__msg__HrpMeasurementSensor),
  HrpMeasurementSensor__rosidl_typesupport_introspection_c__HrpMeasurementSensor_message_member_array,  // message members
  HrpMeasurementSensor__rosidl_typesupport_introspection_c__HrpMeasurementSensor_init_function,  // function to initialize message memory (memory has to be allocated)
  HrpMeasurementSensor__rosidl_typesupport_introspection_c__HrpMeasurementSensor_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t HrpMeasurementSensor__rosidl_typesupport_introspection_c__HrpMeasurementSensor_message_type_support_handle = {
  0,
  &HrpMeasurementSensor__rosidl_typesupport_introspection_c__HrpMeasurementSensor_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_hrp_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, hrp_msgs, msg, HrpMeasurementSensor)() {
  if (!HrpMeasurementSensor__rosidl_typesupport_introspection_c__HrpMeasurementSensor_message_type_support_handle.typesupport_identifier) {
    HrpMeasurementSensor__rosidl_typesupport_introspection_c__HrpMeasurementSensor_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &HrpMeasurementSensor__rosidl_typesupport_introspection_c__HrpMeasurementSensor_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
