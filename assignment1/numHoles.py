def isXonRight(pixels, location, x):
    (row, col) = location
    if x == -1:
        return col + 1 == len(pixels[0])
    if col + 1 == len(pixels[0]):
        return False
    else:
        return pixels[row][col + 1] == x

def isXonLeft(pixels, location, x):
    (row, col) = location
    if x == -1:
        return col == 0
    if col == 0:
        return False
    else:
        return pixels[row][col - 1] == x

def isXonTop(pixels, location, x):
    (row, col) = location
    if x == -1:
        return row + 1 == len(pixels)
    if row + 1 == len(pixels):
        return False
    else:
        return pixels[row + 1][col] == x

def isXonBottom(pixels, location, x):
    (row, col) = location
    if x == -1:
        return row == 0
    if row == 0:
        return False
    else:
        return pixels[row - 1][col] == x

def isNextTo(pixels, location, x):
    return isXonBottom(pixels, location, x) or isXonTop(pixels, location, x) or isXonRight(pixels, location, x) or isXonLeft(pixels, location, x)

def printarr(pixels):
    for i in pixels:
        print i
    print "--------------------"

def replaceAll(pixels, num, withNum):
    for row in xrange(len(pixels)):
        for col in xrange(len(pixels[0])):
            if pixels[row][col] == num:
                pixels[row][col] = withNum
    return pixels

def findFirst(pixels, num, after):
    (arow, acol) = after
    for row in xrange(len(pixels)):
        for col in xrange(len(pixels[0])):
            if pixels[row][col] == num:
                if row > arow:
                    return (row, col)
                elif col > acol:
                    return (row, col)
    return (-1,-1)

def aKindaFloodFill(pixels, orig, wall, enc):
    (frow, fcol) = findFirst(pixels, orig, (-1, -1))
    while frow != -1:
        first = (frow, fcol)
        setTo = -1

        if isNextTo(pixels, first, -1) or isNextTo(pixels, first, wall):
            setTo = wall
        elif isNextTo(pixels, first, 1) or isNextTo(pixels, first, enc):
            setTo = enc

        pixels[frow][fcol] = setTo
        if frow + 1 < len(pixels):
            if isXonTop(pixels, first, orig):
                pixels[frow + 1][fcol] = setTo
        if fcol + 1 < len(pixels[0]):
            if isXonRight(pixels, first, orig):
                pixels[frow][fcol + 1] = setTo

        (frow, fcol) = findFirst(pixels, orig, first)

def vertFlipArr(arr):
    newArr = []
    for i in xrange(len(arr)):
        newArr.append(arr[len(arr) - i - 1])
    return newArr

def horFlipArr(arr):
    newArr = []
    for i in xrange(len(arr)):
        row = []
        for h in xrange(len(arr[0])):
            row.append(arr[i][len(arr[0]) - h - 1])
        newArr.append(row)
    return newArr

def numberOfHoles(pixels):
    aKindaFloodFill(pixels, 0, 2, 3)
    printarr(pixels)
    flipped = horFlipArr(vertFlipArr(pixels))
    printarr(flipped)
    aKindaFloodFill(flipped, 3, 2, 4)
    printarr(flipped)
    replaceAll(flipped, 4, 0)
    replaceAll(flipped, 2, 1)
    printarr(flipped)

if __name__ == '__main__':
    import openpbm
    import getbounding
    import extractNumber

    fstruct = 'pbms/digit/*N_*F.pbm'
    for n in xrange(1):
        sum = 0
        print "For number: " + str(n)
        for f in xrange(1):
            file = openpbm.fileNameFrom(fstruct, n, f)
            pixels = openpbm.read_pbm(file)
            extracted = extractNumber.extract(pixels, getbounding.getBoundingBox(pixels))
            #printarr(extracted)
            numh = numberOfHoles(extracted)
            print numh
            sum += numh

        print sum / 100.0