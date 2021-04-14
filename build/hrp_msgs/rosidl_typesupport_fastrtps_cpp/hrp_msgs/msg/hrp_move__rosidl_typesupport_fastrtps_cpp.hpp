// generated from rosidl_typesupport_fastrtps_cpp/resource/idl__rosidl_typesupport_fastrtps_cpp.hpp.em
// with input from hrp_msgs:msg/HrpMove.idl
// generated code does not contain a copyright notice

#ifndef HRP_MSGS__MSG__HRP_MOVE__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_
#define HRP_MSGS__MSG__HRP_MOVE__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_

#include "rosidl_generator_c/message_type_support_struct.h"
#include "rosidl_typesupport_interface/macros.h"
#include "hrp_msgs/msg/rosidl_typesupport_fastrtps_cpp__visibility_control.h"
#include "hrp_msgs/msg/hrp_move__struct.hpp"

#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-parameter"
# ifdef __clang__
#  pragma clang diagnostic ignored "-Wdeprecated-register"
#  pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
# endif
#endif
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif

#include "fastcdr/Cdr.h"

namespace hrp_msgs
{

namespace msg
{

namespace typesupport_fastrtps_cpp
{

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_hrp_msgs
cdr_serialize(
  const hrp_msgs::msg::HrpMove & ros_message,
  eprosima::fastcdr::Cdr & cdr);

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_hrp_msgs
cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  hrp_msgs::msg::HrpMove & ros_message);

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_hrp_msgs
get_serialized_size(
  const hrp_msgs::msg::HrpMove & ros_message,
  size_t current_alignment);

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_hrp_msgs
max_serialized_size_HrpMove(
  bool & full_bounded,
  size_t current_alignment);

}  // namespace typesupport_fastrtps_cpp

}  // namespace msg

}  // namespace hrp_msgs

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_hrp_msgs
const rosidl_message_type_support_t *
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, hrp_msgs, msg, HrpMove)();

#ifdef __cplusplus
}
#endif

#endif  // HRP_MSGS__MSG__HRP_MOVE__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_
