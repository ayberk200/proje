import cv
#cv.NamedWindow("h_plane", 1)
cv.NamedWindow("s_plane", 1)
#cv.NamedWindow("v_plane", 1)
capture = cv.CaptureFromCAM(0)
frame1=cv.QueryFrame(capture)
#cv.WaitKey(1) 
print cv.GetSize(frame1)
hsv=cv.CreateImage(cv.GetSize(frame1), 8, 3)
h_plane=cv.CreateImage(cv.GetSize(frame1), 8, 1)
h_plane2=cv.CreateImage(cv.GetSize(frame1), 8, 1)
h_plane3=cv.CreateImage(cv.GetSize(frame1), 8, 1)
s_plane=cv.CreateImage(cv.GetSize(frame1), 8, 1)
while True:
    frame1=cv.QueryFrame(capture)
    cv.Flip(frame1, None, 1)
    image_size = cv.GetSize(frame1)
    cv.CvtColor(frame1, hsv, cv.CV_BGR2YCrCb )
    cv.Split(hsv, h_plane, s_plane, None, None)
    cv.Threshold(h_plane, h_plane,180, 255, cv.CV_THRESH_BINARY)
    #cv.AbsDiff(h_plane3,h_plane2, h_plane)
    h_plane2=cv.CloneImage(h_plane3)
    cv.Dilate(h_plane, h_plane, None,10)
    cv.Erode(h_plane, h_plane, None, 1)

    storage = cv.CreateMemStorage(0)
    contour = cv.FindContours(h_plane, storage, cv.CV_RETR_CCOMP, cv.CV_CHAIN_APPROX_SIMPLE)
    points = []

    while contour:
        bound_rect = cv.BoundingRect(list(contour))
        contour = contour.h_next()

        pt1 = (bound_rect[0], bound_rect[1])
        pt2 = (bound_rect[0] + bound_rect[2], bound_rect[1] + bound_rect[3])
        points.append(pt1)
        points.append(pt2)
        print '{0:4d} {1:4d} '.format(bound_rect[0] + bound_rect[2]/2, bound_rect[1] + bound_rect[3]/2)
        cv.Circle(s_plane, (bound_rect[0] + bound_rect[2]/2,bound_rect[1] + bound_rect[3]/2), 20, cv.CV_RGB(255, 255, 255), 1)
        print '{0:4d} {1:4d} '.format(bound_rect[0] + bound_rect[2]/2,bound_rect[1] + bound_rect[3]/2)
        #cv.Rectangle(s_plane, pt1, pt2, cv.CV_RGB(255,0,0), 3)
        #if len(points):
           # center_point = reduce(lambda a, b: ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2), points)
            #cv.Circle(s_plane, center_point, 20, cv.CV_RGB(255, 255, 255), 1)
            #cv.Circle(s_plane, center_point, 25, cv.CV_RGB(255, 0,0), 1)
    
    #cv.ShowImage("h_plane", h_plane)
    cv.ShowImage("s_plane", s_plane)
    
    #cv.ShowImage("v_plane", frame1)
    #cv.EqualizeHist(grayscale,grayscale)
    #cv.Threshold(grayscale,grayscale, 253,255,cv.CV_THRESH_BINARY)
    #cv.ShowImage("camera", grayscale)
    if cv.WaitKey(10) == 27:
        break
cv.DestroyWindow("camera")
