// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from hrp_msgs:msg/HrpMove.idl
// generated code does not contain a copyright notice
#include "hrp_msgs/msg/hrp_move__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>


bool
hrp_msgs__msg__HrpMove__init(hrp_msgs__msg__HrpMove * msg)
{
  if (!msg) {
    return false;
  }
  // x
  // y
  // angle
  return true;
}

void
hrp_msgs__msg__HrpMove__fini(hrp_msgs__msg__HrpMove * msg)
{
  if (!msg) {
    return;
  }
  // x
  // y
  // angle
}

hrp_msgs__msg__HrpMove *
hrp_msgs__msg__HrpMove__create()
{
  hrp_msgs__msg__HrpMove * msg = (hrp_msgs__msg__HrpMove *)malloc(sizeof(hrp_msgs__msg__HrpMove));
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(hrp_msgs__msg__HrpMove));
  bool success = hrp_msgs__msg__HrpMove__init(msg);
  if (!success) {
    free(msg);
    return NULL;
  }
  return msg;
}

void
hrp_msgs__msg__HrpMove__destroy(hrp_msgs__msg__HrpMove * msg)
{
  if (msg) {
    hrp_msgs__msg__HrpMove__fini(msg);
  }
  free(msg);
}


bool
hrp_msgs__msg__HrpMove__Sequence__init(hrp_msgs__msg__HrpMove__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  hrp_msgs__msg__HrpMove * data = NULL;
  if (size) {
    data = (hrp_msgs__msg__HrpMove *)calloc(size, sizeof(hrp_msgs__msg__HrpMove));
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = hrp_msgs__msg__HrpMove__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        hrp_msgs__msg__HrpMove__fini(&data[i - 1]);
      }
      free(data);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
hrp_msgs__msg__HrpMove__Sequence__fini(hrp_msgs__msg__HrpMove__Sequence * array)
{
  if (!array) {
    return;
  }
  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      hrp_msgs__msg__HrpMove__fini(&array->data[i]);
    }
    free(array->data);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

hrp_msgs__msg__HrpMove__Sequence *
hrp_msgs__msg__HrpMove__Sequence__create(size_t size)
{
  hrp_msgs__msg__HrpMove__Sequence * array = (hrp_msgs__msg__HrpMove__Sequence *)malloc(sizeof(hrp_msgs__msg__HrpMove__Sequence));
  if (!array) {
    return NULL;
  }
  bool success = hrp_msgs__msg__HrpMove__Sequence__init(array, size);
  if (!success) {
    free(array);
    return NULL;
  }
  return array;
}

void
hrp_msgs__msg__HrpMove__Sequence__destroy(hrp_msgs__msg__HrpMove__Sequence * array)
{
  if (array) {
    hrp_msgs__msg__HrpMove__Sequence__fini(array);
  }
  free(array);
}
