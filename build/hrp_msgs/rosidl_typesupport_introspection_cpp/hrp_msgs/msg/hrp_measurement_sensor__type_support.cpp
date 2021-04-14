// generated from rosidl_typesupport_introspection_cpp/resource/idl__type_support.cpp.em
// with input from hrp_msgs:msg/HrpMeasurementSensor.idl
// generated code does not contain a copyright notice

#include "array"
#include "cstddef"
#include "string"
#include "vector"
#include "rosidl_generator_c/message_type_support_struct.h"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_interface/macros.h"
#include "hrp_msgs/msg/hrp_measurement_sensor__struct.hpp"
#include "rosidl_typesupport_introspection_cpp/field_types.hpp"
#include "rosidl_typesupport_introspection_cpp/identifier.hpp"
#include "rosidl_typesupport_introspection_cpp/message_introspection.hpp"
#include "rosidl_typesupport_introspection_cpp/message_type_support_decl.hpp"
#include "rosidl_typesupport_introspection_cpp/visibility_control.h"

namespace hrp_msgs
{

namespace msg
{

namespace rosidl_typesupport_introspection_cpp
{

void HrpMeasurementSensor_init_function(
  void * message_memory, rosidl_generator_cpp::MessageInitialization _init)
{
  new (message_memory) hrp_msgs::msg::HrpMeasurementSensor(_init);
}

void HrpMeasurementSensor_fini_function(void * message_memory)
{
  auto typed_message = static_cast<hrp_msgs::msg::HrpMeasurementSensor *>(message_memory);
  typed_message->~HrpMeasurementSensor();
}

static const ::rosidl_typesupport_introspection_cpp::MessageMember HrpMeasurementSensor_message_member_array[3] = {
  {
    "f",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_INT16,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(hrp_msgs::msg::HrpMeasurementSensor, f),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "l",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_INT16,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(hrp_msgs::msg::HrpMeasurementSensor, l),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "r",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_INT16,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(hrp_msgs::msg::HrpMeasurementSensor, r),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr  // resize(index) function pointer
  }
};

static const ::rosidl_typesupport_introspection_cpp::MessageMembers HrpMeasurementSensor_message_members = {
  "hrp_msgs::msg",  // message namespace
  "HrpMeasurementSensor",  // message name
  3,  // number of fields
  sizeof(hrp_msgs::msg::HrpMeasurementSensor),
  HrpMeasurementSensor_message_member_array,  // message members
  HrpMeasurementSensor_init_function,  // function to initialize message memory (memory has to be allocated)
  HrpMeasurementSensor_fini_function  // function to terminate message instance (will not free memory)
};

static const rosidl_message_type_support_t HrpMeasurementSensor_message_type_support_handle = {
  ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  &HrpMeasurementSensor_message_members,
  get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_introspection_cpp

}  // namespace msg

}  // namespace hrp_msgs


namespace rosidl_typesupport_introspection_cpp
{

template<>
ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<hrp_msgs::msg::HrpMeasurementSensor>()
{
  return &::hrp_msgs::msg::rosidl_typesupport_introspection_cpp::HrpMeasurementSensor_message_type_support_handle;
}

}  // namespace rosidl_typesupport_introspection_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, hrp_msgs, msg, HrpMeasurementSensor)() {
  return &::hrp_msgs::msg::rosidl_typesupport_introspection_cpp::HrpMeasurementSensor_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif
