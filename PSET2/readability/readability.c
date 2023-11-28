#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

float letter(string text);
float word(string text);
float sentence(string text);

int main(void)
{
    string text = get_string("Text :");

    float letter_len = letter(text);
    float word_len = word(text);
    float sentence_len = sentence(text);

    float L = 100 * (letter_len / word_len);
    float S = 100 * (sentence_len / word_len);

    int index = round(0.0588 * L - 0.296 * S - 15.8);

    if (index >= 16)
    {
        printf("Grade 16+\n");
    }
    else if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else
    {
        printf("Grade %i\n", index);
    }
}

float letter(string text)
{
    int count = 0;
    int len = strlen(text);
    for (int i = 0; i < len; i++)
    {
        if (isalpha(text[i]) != 0)
        {
            count++;
        }
    }
    return count;
}

float word(string text)
{
    int count = 1;
    int len = strlen(text);
    for (int i = 0; i < len; i++)
    {
        if (text[i] == ' ')
        {
            count++;
        }
    }
    return count;
}

float sentence(string text)
{
    int count = 0;
    int len = strlen(text);
    for (int i = 0; i < len; i++)
    {
        if (text[i] == '.' || text[i] == '!' || text[i] == '?')
        {
            count++;
        }
    }
    return count;
}