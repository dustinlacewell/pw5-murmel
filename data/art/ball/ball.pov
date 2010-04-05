//+w150 +h150 +ua +fn -KC +kff20 -J
//+w150 +h150 +ua  -KC +kff20 -J +fn

#include "colors.inc"
//#include "stones.inc"

                       
//#include "textures.inc"
//#include "shapes.inc"                       
//#include "glass.inc"
//#include "metals.ind"
//#include "woods.inc"
  
global_settings { ambient_light rgb<1, 1, 1>*4 }  
background { color Black }


camera{    
        orthographic 
        location <0, 0, -20>
        look_at <0, 0, 0>    
        right 1*x
        up 1*y 
}
                           
sphere {         
    /*
        #declare p = 1.2;
        #declare tt = clock*p;
        #declare r = 0.3;
        
        <0,p*p+r-tt*tt,0>, r
      */
        <0,0,0>, .495
        texture{
                pigment{ color <1, 1, 1> 
                }
                finish {phong 0.1
                }
        }
}   
     
light_source {
        <-2, 10, -5>
        color <1,1-clock,1-clock>  
        spotlight
        radius 7
        falloff 9
        //tightness 5
        point_at <0, 0, 0>
} 
