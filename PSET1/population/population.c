#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // TODO: Prompt for start size
    int first_num;
    do
    {
        first_num = get_int("enter start number of lama: ");
    }
    while (first_num < 9);
    // TODO: Prompt for end size
    int end_num;
    do
    {
        end_num = get_int("enter end number of lama: ");
    }
    while (end_num < first_num);
    // TODO: Calculate number of years until we reach threshold
    int year = 0;

    while (first_num < end_num)
    {
        first_num = first_num + (first_num / 3) - (first_num / 4);
        year += 1;
    }
    // TODO: Print number of years
    printf("Years: %i\n", year);
}
