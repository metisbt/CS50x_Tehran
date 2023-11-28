#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // get number from user
    int height;
    do
    {
        height = get_int("Height: ");
    }
    while (height < 1 || height > 8);

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < height - (i + 1); j++)
        {
            printf(" ");
        }

        for (int k = 0; k <= i; k++)
        {
            printf("#");
        }
        printf("  ");
        for (int m = 0; m <= i; m++)
        {
            printf("#");
        }
        printf("\n");
    }
}