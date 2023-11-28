#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./recover IMAGE\n");
        return 1;
    }

    FILE *imgmemory = fopen(argv[1], "r");

    unsigned char *picfind = malloc(512);

    if (picfind == NULL)
    {
        return 1;
    }

    char *picname = malloc(3 * sizeof(int));

    if (picname == NULL)
    {
        return 1;
    }

    int image_found = 0;
    while (fread(picfind, sizeof(unsigned char), 512, imgmemory))
    {
        if (picfind[0] == 0xff && picfind[1] == 0xd8 && picfind[2] == 0xff && (picfind[3] & 0xf0) == 0xe0)
        {
            sprintf(picname, "%03i.jpg", image_found);
            FILE *imgfile = fopen(picname, "w");
            fwrite(picfind, 1, 512, imgfile);
            fclose(imgfile);
            image_found++;
        }
        else if (image_found != 0)
        {
            FILE *imgfile = fopen(picname, "a");
            fwrite(picfind, 1, 512, imgfile);
            fclose(imgfile);
        }
    }
    free(picfind);
    free(picname);
    fclose(imgmemory);
}