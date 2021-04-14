// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from hrp_msgs:msg/HrpMeasurementSensor.idl
// generated code does not contain a copyright notice

#ifndef HRP_MSGS__MSG__HRP_MEASUREMENT_SENSOR__FUNCTIONS_H_
#define HRP_MSGS__MSG__HRP_MEASUREMENT_SENSOR__FUNCTIONS_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stdlib.h>

#include "rosidl_generator_c/visibility_control.h"
#include "hrp_msgs/msg/rosidl_generator_c__visibility_control.h"

#include "hrp_msgs/msg/hrp_measurement_sensor__struct.h"

/// Initialize msg/HrpMeasurementSensor message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * hrp_msgs__msg__HrpMeasurementSensor
 * )) before or use
 * hrp_msgs__msg__HrpMeasurementSensor__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_hrp_msgs
bool
hrp_msgs__msg__HrpMeasurementSensor__init(hrp_msgs__msg__HrpMeasurementSensor * msg);

/// Finalize msg/HrpMeasurementSensor message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_hrp_msgs
void
hrp_msgs__msg__HrpMeasurementSensor__fini(hrp_msgs__msg__HrpMeasurementSensor * msg);

/// Create msg/HrpMeasurementSensor message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * hrp_msgs__msg__HrpMeasurementSensor__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_hrp_msgs
hrp_msgs__msg__HrpMeasurementSensor *
hrp_msgs__msg__HrpMeasurementSensor__create();

/// Destroy msg/HrpMeasurementSensor message.
/**
 * It calls
 * hrp_msgs__msg__HrpMeasurementSensor__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_hrp_msgs
void
hrp_msgs__msg__HrpMeasurementSensor__destroy(hrp_msgs__msg__HrpMeasurementSensor * msg);


/// Initialize array of msg/HrpMeasurementSensor messages.
/**
 * It allocates the memory for the number of elements and calls
 * hrp_msgs__msg__HrpMeasurementSensor__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_hrp_msgs
bool
hrp_msgs__msg__HrpMeasurementSensor__Sequence__init(hrp_msgs__msg__HrpMeasurementSensor__Sequence * array, size_t size);

/// Finalize array of msg/HrpMeasurementSensor messages.
/**
 * It calls
 * hrp_msgs__msg__HrpMeasurementSensor__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_hrp_msgs
void
hrp_msgs__msg__HrpMeasurementSensor__Sequence__fini(hrp_msgs__msg__HrpMeasurementSensor__Sequence * array);

/// Create array of msg/HrpMeasurementSensor messages.
/**
 * It allocates the memory for the array and calls
 * hrp_msgs__msg__HrpMeasurementSensor__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_hrp_msgs
hrp_msgs__msg__HrpMeasurementSensor__Sequence *
hrp_msgs__msg__HrpMeasurementSensor__Sequence__create(size_t size);

/// Destroy array of msg/HrpMeasurementSensor messages.
/**
 * It calls
 * hrp_msgs__msg__HrpMeasurementSensor__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_hrp_msgs
void
hrp_msgs__msg__HrpMeasurementSensor__Sequence__destroy(hrp_msgs__msg__HrpMeasurementSensor__Sequence * array);

#ifdef __cplusplus
}
#endif

#endif  // HRP_MSGS__MSG__HRP_MEASUREMENT_SENSOR__FUNCTIONS_H_
