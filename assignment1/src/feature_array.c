//
// Created by Jordan Lewis on 28/4/17.
//

#include "captcha.h"

void get_image_features(int height, int width, int pixels[height][width], double features[NUM_FEATURES]) {

    int startRow, startCol, boxHeight, boxWidth;
    get_bounding_box(height, width, pixels, &startRow, &startCol, &boxHeight, &boxWidth);

    int extracted[boxHeight][boxWidth];
    copy_pixels(height, width, pixels, startRow, startCol, boxHeight, boxWidth, extracted);

    int area = (boxHeight * boxWidth);
    double hBalance = get_horizontal_balance(boxHeight, boxWidth, extracted);
    double vBalance = get_vertical_balance(boxHeight, boxWidth, extracted);
    int numHoles = numberOfHoles(boxHeight, boxWidth, extracted);
    double hHoleBalance = get_horizontal_hole_balance(boxHeight, boxWidth, extracted);
    double vHoleBalance = get_vertical_hole_balance(boxHeight, boxWidth, extracted);
    double blackDensity = get_density(boxHeight, boxWidth, extracted);
    double holeDensity = get_hole_fraction(boxHeight, boxWidth, extracted);

    features[0] = (double)boxHeight;
    features[1] = (double)boxWidth;
    features[2] = hBalance;
    features[3] = vBalance;
    features[4] = blackDensity;
    features[5] = holeDensity;
    features[6] = (double)numHoles;
    features[7] = (double)area;
    features[8] = hHoleBalance;
    features[9] = vHoleBalance;
}