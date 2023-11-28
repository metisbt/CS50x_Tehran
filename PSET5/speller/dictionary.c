// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

int dict_count = 0;

const unsigned int N = 10000000;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    int hash_value = hash(word);
    node *n = table[hash_value];

    while (n != NULL)
    {
        if (strcasecmp(word, n->word) == 0)
        {
            return true;
        }
        n = n->next;
    }
    return false;
}

// Hashes word to a number
// I got help from ( https://www.digitalocean.com/community/tutorials/hash-table-in-c-plus-plus ) to get ideas for hash function.
unsigned int hash(const char *word)
{
    long sum = 0;
    for (int i = 0; i < strlen(word); i++)
    {
        sum = tolower(word[i]);
    }

    return sum % N;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    FILE *dict_flag = fopen(dictionary, "r");
    if (dictionary == NULL)
    {
        printf("Can't open file %s\n", dictionary);
        return false;
    }
    char nword[LENGTH + 1];
    while (fscanf(dict_flag, "%s", nword) != EOF)
    {
        node *n = malloc(sizeof(node));
        if (n == NULL)
        {
            return false;
        }
        strcpy(n->word, nword);
        int hash_value = hash(nword);

        n->next = table[hash_value];
        table[hash_value] = n;
        dict_count++;
    }
    fclose(dict_flag);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    return dict_count;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        node *n = table[i];
        while (n != NULL)
        {
            node *temp = n;
            n = n->next;
            free(temp);
        }
        if (n == NULL && i == N - 1)
        {
            return true;
        }
    }
    return false;
}
