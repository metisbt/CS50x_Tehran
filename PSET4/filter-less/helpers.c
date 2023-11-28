#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < width; i++)
    {
        for (int j = 0; j < height; j++)
        {
            int red = image[j][i].rgbtRed;
            int blue = image[j][i].rgbtBlue;
            int green = image[j][i].rgbtGreen;

            float gray = round((red + blue + green) / 3.0);

            image[j][i].rgbtRed = gray;
            image[j][i].rgbtBlue = gray;
            image[j][i].rgbtGreen = gray;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < width; i++)
    {
        for (int j = 0; j < height; j++)
        {
            int red = image[j][i].rgbtRed;
            int blue = image[j][i].rgbtBlue;
            int green = image[j][i].rgbtGreen;

            float sepiaR = round(0.393 * red + 0.769 * green + 0.189 * blue);
            float sepiaG = round(0.349 * red + 0.686 * green + 0.168 * blue);
            float sepiaB = round(0.272 * red + 0.534 * green + 0.131 * blue);

            if (sepiaR > 255)
            {
                sepiaR = 255;
            }
            if (sepiaB > 255)
            {
                sepiaB = 255;
            }
            if (sepiaG > 255)
            {
                sepiaG = 255;
            }

            image[j][i].rgbtRed = sepiaR;
            image[j][i].rgbtBlue = sepiaB;
            image[j][i].rgbtGreen = sepiaG;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < (width / 2); j++)
        {
            int tempR = image[i][j].rgbtRed;
            int tempG = image[i][j].rgbtGreen;
            int tempB = image[i][j].rgbtBlue;

            image[i][j].rgbtRed = image[i][width - j - 1].rgbtRed;
            image[i][j].rgbtGreen = image[i][width - j - 1].rgbtGreen;
            image[i][j].rgbtBlue = image[i][width - j - 1].rgbtBlue;

            image[i][width - j - 1].rgbtRed = tempR;
            image[i][width - j - 1].rgbtGreen = tempG;
            image[i][width - j - 1].rgbtBlue = tempB;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE copyimg[height][width];

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            copyimg[i][j] = image[i][j];
        }
    }

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int count = 0;
            float sumR = 0;
            float sumG = 0;
            float sumB = 0;

            for (int m = -1; m < 2; m++)
            {
                for (int n = -1; n < 2; n++)
                {
                    if (!((i + m < 0) || (i + m >= height) || (j + n < 0) || (j + n >= width)))
                    {
                        count++;
                        sumR += copyimg[i + m][j + n].rgbtRed;
                        sumG += copyimg[i + m][j + n].rgbtGreen;
                        sumB += copyimg[i + m][j + n].rgbtBlue;
                    }
                    else
                    {
                        continue;
                    }
                }
            }

            image[i][j].rgbtRed = (int) round(sumR / count);
            image[i][j].rgbtGreen = (int) round(sumG / count);
            image[i][j].rgbtBlue = (int) round(sumB / count);
        }
    }
    return;
}
