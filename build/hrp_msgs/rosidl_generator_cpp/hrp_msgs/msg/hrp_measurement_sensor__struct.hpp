// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from hrp_msgs:msg/HrpMeasurementSensor.idl
// generated code does not contain a copyright notice

#ifndef HRP_MSGS__MSG__HRP_MEASUREMENT_SENSOR__STRUCT_HPP_
#define HRP_MSGS__MSG__HRP_MEASUREMENT_SENSOR__STRUCT_HPP_

#include <rosidl_generator_cpp/bounded_vector.hpp>
#include <rosidl_generator_cpp/message_initialization.hpp>
#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>


#ifndef _WIN32
# define DEPRECATED__hrp_msgs__msg__HrpMeasurementSensor __attribute__((deprecated))
#else
# define DEPRECATED__hrp_msgs__msg__HrpMeasurementSensor __declspec(deprecated)
#endif

namespace hrp_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct HrpMeasurementSensor_
{
  using Type = HrpMeasurementSensor_<ContainerAllocator>;

  explicit HrpMeasurementSensor_(rosidl_generator_cpp::MessageInitialization _init = rosidl_generator_cpp::MessageInitialization::ALL)
  {
    if (rosidl_generator_cpp::MessageInitialization::ALL == _init ||
      rosidl_generator_cpp::MessageInitialization::ZERO == _init)
    {
      this->f = 0;
      this->l = 0;
      this->r = 0;
    }
  }

  explicit HrpMeasurementSensor_(const ContainerAllocator & _alloc, rosidl_generator_cpp::MessageInitialization _init = rosidl_generator_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_generator_cpp::MessageInitialization::ALL == _init ||
      rosidl_generator_cpp::MessageInitialization::ZERO == _init)
    {
      this->f = 0;
      this->l = 0;
      this->r = 0;
    }
  }

  // field types and members
  using _f_type =
    int16_t;
  _f_type f;
  using _l_type =
    int16_t;
  _l_type l;
  using _r_type =
    int16_t;
  _r_type r;

  // setters for named parameter idiom
  Type & set__f(
    const int16_t & _arg)
  {
    this->f = _arg;
    return *this;
  }
  Type & set__l(
    const int16_t & _arg)
  {
    this->l = _arg;
    return *this;
  }
  Type & set__r(
    const int16_t & _arg)
  {
    this->r = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    hrp_msgs::msg::HrpMeasurementSensor_<ContainerAllocator> *;
  using ConstRawPtr =
    const hrp_msgs::msg::HrpMeasurementSensor_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<hrp_msgs::msg::HrpMeasurementSensor_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<hrp_msgs::msg::HrpMeasurementSensor_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      hrp_msgs::msg::HrpMeasurementSensor_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<hrp_msgs::msg::HrpMeasurementSensor_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      hrp_msgs::msg::HrpMeasurementSensor_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<hrp_msgs::msg::HrpMeasurementSensor_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<hrp_msgs::msg::HrpMeasurementSensor_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<hrp_msgs::msg::HrpMeasurementSensor_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__hrp_msgs__msg__HrpMeasurementSensor
    std::shared_ptr<hrp_msgs::msg::HrpMeasurementSensor_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__hrp_msgs__msg__HrpMeasurementSensor
    std::shared_ptr<hrp_msgs::msg::HrpMeasurementSensor_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const HrpMeasurementSensor_ & other) const
  {
    if (this->f != other.f) {
      return false;
    }
    if (this->l != other.l) {
      return false;
    }
    if (this->r != other.r) {
      return false;
    }
    return true;
  }
  bool operator!=(const HrpMeasurementSensor_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct HrpMeasurementSensor_

// alias to use template instance with default allocator
using HrpMeasurementSensor =
  hrp_msgs::msg::HrpMeasurementSensor_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace hrp_msgs

#endif  // HRP_MSGS__MSG__HRP_MEASUREMENT_SENSOR__STRUCT_HPP_
