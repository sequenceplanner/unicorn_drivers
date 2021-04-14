// generated from rosidl_typesupport_fastrtps_cpp/resource/idl__type_support.cpp.em
// with input from hrp_msgs:msg/HrpMeasurementSensor.idl
// generated code does not contain a copyright notice
#include "hrp_msgs/msg/hrp_measurement_sensor__rosidl_typesupport_fastrtps_cpp.hpp"
#include "hrp_msgs/msg/hrp_measurement_sensor__struct.hpp"

#include <limits>
#include <stdexcept>
#include <string>
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_fastrtps_cpp/identifier.hpp"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support_decl.hpp"
#include "rosidl_typesupport_fastrtps_cpp/wstring_conversion.hpp"
#include "fastcdr/Cdr.h"


// forward declaration of message dependencies and their conversion functions

namespace hrp_msgs
{

namespace msg
{

namespace typesupport_fastrtps_cpp
{

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_hrp_msgs
cdr_serialize(
  const hrp_msgs::msg::HrpMeasurementSensor & ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  // Member: f
  cdr << ros_message.f;
  // Member: l
  cdr << ros_message.l;
  // Member: r
  cdr << ros_message.r;
  return true;
}

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_hrp_msgs
cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  hrp_msgs::msg::HrpMeasurementSensor & ros_message)
{
  // Member: f
  cdr >> ros_message.f;

  // Member: l
  cdr >> ros_message.l;

  // Member: r
  cdr >> ros_message.r;

  return true;
}

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_hrp_msgs
get_serialized_size(
  const hrp_msgs::msg::HrpMeasurementSensor & ros_message,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // Member: f
  {
    size_t item_size = sizeof(ros_message.f);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: l
  {
    size_t item_size = sizeof(ros_message.l);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: r
  {
    size_t item_size = sizeof(ros_message.r);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  return current_alignment - initial_alignment;
}

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_hrp_msgs
max_serialized_size_HrpMeasurementSensor(
  bool & full_bounded,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;
  (void)full_bounded;


  // Member: f
  {
    size_t array_size = 1;

    current_alignment += array_size * sizeof(uint16_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint16_t));
  }

  // Member: l
  {
    size_t array_size = 1;

    current_alignment += array_size * sizeof(uint16_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint16_t));
  }

  // Member: r
  {
    size_t array_size = 1;

    current_alignment += array_size * sizeof(uint16_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint16_t));
  }

  return current_alignment - initial_alignment;
}

static bool _HrpMeasurementSensor__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  auto typed_message =
    static_cast<const hrp_msgs::msg::HrpMeasurementSensor *>(
    untyped_ros_message);
  return cdr_serialize(*typed_message, cdr);
}

static bool _HrpMeasurementSensor__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  auto typed_message =
    static_cast<hrp_msgs::msg::HrpMeasurementSensor *>(
    untyped_ros_message);
  return cdr_deserialize(cdr, *typed_message);
}

static uint32_t _HrpMeasurementSensor__get_serialized_size(
  const void * untyped_ros_message)
{
  auto typed_message =
    static_cast<const hrp_msgs::msg::HrpMeasurementSensor *>(
    untyped_ros_message);
  return static_cast<uint32_t>(get_serialized_size(*typed_message, 0));
}

static size_t _HrpMeasurementSensor__max_serialized_size(bool & full_bounded)
{
  return max_serialized_size_HrpMeasurementSensor(full_bounded, 0);
}

static message_type_support_callbacks_t _HrpMeasurementSensor__callbacks = {
  "hrp_msgs::msg",
  "HrpMeasurementSensor",
  _HrpMeasurementSensor__cdr_serialize,
  _HrpMeasurementSensor__cdr_deserialize,
  _HrpMeasurementSensor__get_serialized_size,
  _HrpMeasurementSensor__max_serialized_size
};

static rosidl_message_type_support_t _HrpMeasurementSensor__handle = {
  rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
  &_HrpMeasurementSensor__callbacks,
  get_message_typesupport_handle_function,
};

}  // namespace typesupport_fastrtps_cpp

}  // namespace msg

}  // namespace hrp_msgs

namespace rosidl_typesupport_fastrtps_cpp
{

template<>
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_EXPORT_hrp_msgs
const rosidl_message_type_support_t *
get_message_type_support_handle<hrp_msgs::msg::HrpMeasurementSensor>()
{
  return &hrp_msgs::msg::typesupport_fastrtps_cpp::_HrpMeasurementSensor__handle;
}

}  // namespace rosidl_typesupport_fastrtps_cpp

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, hrp_msgs, msg, HrpMeasurementSensor)() {
  return &hrp_msgs::msg::typesupport_fastrtps_cpp::_HrpMeasurementSensor__handle;
}

#ifdef __cplusplus
}
#endif
