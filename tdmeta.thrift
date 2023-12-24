struct mapOptions { 
  1: double zoomScale
  2: i32 ifReverse
}

service userService {
    list<double> test1(1:bool typ)
    string getMapData(1:mapOptions opt)
    string drawSmiles(1:string txt)
}