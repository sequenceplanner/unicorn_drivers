// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from hrp_msgs:msg/HrpMove.idl
// generated code does not contain a copyright notice

#ifndef HRP_MSGS__MSG__HRP_MOVE__STRUCT_HPP_
#define HRP_MSGS__MSG__HRP_MOVE__STRUCT_HPP_

#include <rosidl_generator_cpp/bounded_vector.hpp>
#include <rosidl_generator_cpp/message_initialization.hpp>
#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>


#ifndef _WIN32
# define DEPRECATED__hrp_msgs__msg__HrpMove __attribute__((deprecated))
#else
# define DEPRECATED__hrp_msgs__msg__HrpMove __declspec(deprecated)
#endif

namespace hrp_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct HrpMove_
{
  using Type = HrpMove_<ContainerAllocator>;

  explicit HrpMove_(rosidl_generator_cpp::MessageInitialization _init = rosidl_generator_cpp::MessageInitialization::ALL)
  {
    if (rosidl_generator_cpp::MessageInitialization::ALL == _init ||
      rosidl_generator_cpp::MessageInitialization::ZERO == _init)
    {
      this->x = 0.0f;
      this->y = 0.0f;
      this->angle = 0.0f;
    }
  }

  explicit HrpMove_(const ContainerAllocator & _alloc, rosidl_generator_cpp::MessageInitialization _init = rosidl_generator_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_generator_cpp::MessageInitialization::ALL == _init ||
      rosidl_generator_cpp::MessageInitialization::ZERO == _init)
    {
      this->x = 0.0f;
      this->y = 0.0f;
      this->angle = 0.0f;
    }
  }

  // field types and members
  using _x_type =
    float;
  _x_type x;
  using _y_type =
    float;
  _y_type y;
  using _angle_type =
    float;
  _angle_type angle;

  // setters for named parameter idiom
  Type & set__x(
    const float & _arg)
  {
    this->x = _arg;
    return *this;
  }
  Type & set__y(
    const float & _arg)
  {
    this->y = _arg;
    return *this;
  }
  Type & set__angle(
    const float & _arg)
  {
    this->angle = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    hrp_msgs::msg::HrpMove_<ContainerAllocator> *;
  using ConstRawPtr =
    const hrp_msgs::msg::HrpMove_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<hrp_msgs::msg::HrpMove_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<hrp_msgs::msg::HrpMove_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      hrp_msgs::msg::HrpMove_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<hrp_msgs::msg::HrpMove_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      hrp_msgs::msg::HrpMove_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<hrp_msgs::msg::HrpMove_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<hrp_msgs::msg::HrpMove_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<hrp_msgs::msg::HrpMove_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__hrp_msgs__msg__HrpMove
    std::shared_ptr<hrp_msgs::msg::HrpMove_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__hrp_msgs__msg__HrpMove
    std::shared_ptr<hrp_msgs::msg::HrpMove_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const HrpMove_ & other) const
  {
    if (this->x != other.x) {
      return false;
    }
    if (this->y != other.y) {
      return false;
    }
    if (this->angle != other.angle) {
      return false;
    }
    return true;
  }
  bool operator!=(const HrpMove_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct HrpMove_

// alias to use template instance with default allocator
using HrpMove =
  hrp_msgs::msg::HrpMove_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace hrp_msgs

#endif  // HRP_MSGS__MSG__HRP_MOVE__STRUCT_HPP_
