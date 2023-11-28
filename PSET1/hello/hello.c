#include <cs50.h>
#include <stdio.h>

int main(void)
{
    ///get name from user
    string user_name = get_string("What is your name?\n");

    ///print hello whit user name
    printf("hello, %s\n", user_name);
}