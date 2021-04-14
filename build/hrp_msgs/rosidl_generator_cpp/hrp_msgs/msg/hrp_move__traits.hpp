// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from hrp_msgs:msg/HrpMove.idl
// generated code does not contain a copyright notice

#ifndef HRP_MSGS__MSG__HRP_MOVE__TRAITS_HPP_
#define HRP_MSGS__MSG__HRP_MOVE__TRAITS_HPP_

#include "hrp_msgs/msg/hrp_move__struct.hpp"
#include <rosidl_generator_cpp/traits.hpp>
#include <stdint.h>
#include <type_traits>

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<hrp_msgs::msg::HrpMove>()
{
  return "hrp_msgs::msg::HrpMove";
}

template<>
struct has_fixed_size<hrp_msgs::msg::HrpMove>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<hrp_msgs::msg::HrpMove>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<hrp_msgs::msg::HrpMove>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // HRP_MSGS__MSG__HRP_MOVE__TRAITS_HPP_
