def enumerate2d(rows):
    "Generates a 2d indexed series:  (0,0,coll[0])[0], (0,1,coll[0][1]) , (1,0,coll[1][0])..."
    for y, row in enumerate(rows):
        for x, val in enumerate(row):
            yield x, y, val
