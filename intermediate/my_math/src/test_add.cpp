#include <gtest/gtest.h>
#include "my_math/add.hpp"

TEST(AddTest, PositiveNumbers)
{
    EXPECT_EQ(my_math::add_two_ints(2, 3), 5);
    EXPECT_EQ(my_math::add_two_ints(10, 20), 30);
}

TEST(AddTest, NegativeNumbers)
{
    EXPECT_EQ(my_math::add_two_ints(-1, -5), -6);
}

TEST(AddTest, Zero)
{
    EXPECT_EQ(my_math::add_two_ints(0, 0), 0);
    EXPECT_EQ(my_math::add_two_ints(0, 42), 42);
}

int main(int argc, char **argv)
{
    testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}