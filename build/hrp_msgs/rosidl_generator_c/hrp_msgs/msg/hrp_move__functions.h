// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from hrp_msgs:msg/HrpMove.idl
// generated code does not contain a copyright notice

#ifndef HRP_MSGS__MSG__HRP_MOVE__FUNCTIONS_H_
#define HRP_MSGS__MSG__HRP_MOVE__FUNCTIONS_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stdlib.h>

#include "rosidl_generator_c/visibility_control.h"
#include "hrp_msgs/msg/rosidl_generator_c__visibility_control.h"

#include "hrp_msgs/msg/hrp_move__struct.h"

/// Initialize msg/HrpMove message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * hrp_msgs__msg__HrpMove
 * )) before or use
 * hrp_msgs__msg__HrpMove__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_hrp_msgs
bool
hrp_msgs__msg__HrpMove__init(hrp_msgs__msg__HrpMove * msg);

/// Finalize msg/HrpMove message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_hrp_msgs
void
hrp_msgs__msg__HrpMove__fini(hrp_msgs__msg__HrpMove * msg);

/// Create msg/HrpMove message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * hrp_msgs__msg__HrpMove__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_hrp_msgs
hrp_msgs__msg__HrpMove *
hrp_msgs__msg__HrpMove__create();

/// Destroy msg/HrpMove message.
/**
 * It calls
 * hrp_msgs__msg__HrpMove__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_hrp_msgs
void
hrp_msgs__msg__HrpMove__destroy(hrp_msgs__msg__HrpMove * msg);


/// Initialize array of msg/HrpMove messages.
/**
 * It allocates the memory for the number of elements and calls
 * hrp_msgs__msg__HrpMove__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_hrp_msgs
bool
hrp_msgs__msg__HrpMove__Sequence__init(hrp_msgs__msg__HrpMove__Sequence * array, size_t size);

/// Finalize array of msg/HrpMove messages.
/**
 * It calls
 * hrp_msgs__msg__HrpMove__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_hrp_msgs
void
hrp_msgs__msg__HrpMove__Sequence__fini(hrp_msgs__msg__HrpMove__Sequence * array);

/// Create array of msg/HrpMove messages.
/**
 * It allocates the memory for the array and calls
 * hrp_msgs__msg__HrpMove__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_hrp_msgs
hrp_msgs__msg__HrpMove__Sequence *
hrp_msgs__msg__HrpMove__Sequence__create(size_t size);

/// Destroy array of msg/HrpMove messages.
/**
 * It calls
 * hrp_msgs__msg__HrpMove__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_hrp_msgs
void
hrp_msgs__msg__HrpMove__Sequence__destroy(hrp_msgs__msg__HrpMove__Sequence * array);

#ifdef __cplusplus
}
#endif

#endif  // HRP_MSGS__MSG__HRP_MOVE__FUNCTIONS_H_
