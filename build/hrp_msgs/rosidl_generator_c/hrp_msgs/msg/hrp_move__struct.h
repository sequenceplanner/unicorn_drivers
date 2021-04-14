// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from hrp_msgs:msg/HrpMove.idl
// generated code does not contain a copyright notice

#ifndef HRP_MSGS__MSG__HRP_MOVE__STRUCT_H_
#define HRP_MSGS__MSG__HRP_MOVE__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Struct defined in msg/HrpMove in the package hrp_msgs.
typedef struct hrp_msgs__msg__HrpMove
{
  float x;
  float y;
  float angle;
} hrp_msgs__msg__HrpMove;

// Struct for a sequence of hrp_msgs__msg__HrpMove.
typedef struct hrp_msgs__msg__HrpMove__Sequence
{
  hrp_msgs__msg__HrpMove * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} hrp_msgs__msg__HrpMove__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // HRP_MSGS__MSG__HRP_MOVE__STRUCT_H_
