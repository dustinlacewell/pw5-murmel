#include "shapes.inc"
#include "colors.inc"
             
             
             
             
global_settings { ambient_light rgb<1, 1, 1>*4 }  
background { color Black }


camera{    
        orthographic 
        location <0, 0, -20>
        look_at <0, 0, 0>    
        right 3*x
        up 1.5*y 
}
                           
#declare ball = sphere {         
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
};
     
light_source {
        <-2, 10, -5>
        color <1,1,1>  
        spotlight
        radius 7
        falloff 9
        //tightness 5
        point_at <0, 0, 0>
} 
             
             





// UNIT OBJECT OBTIONS
#declare explode_object = object{ball}; // object to explode
#declare object_centre =<0,0,0> ; // exact centre of the explode object, best used for spherical or cylindrical obj
#declare object_size = <2*.495,2*.495,2*.495>;  // x,y,z dimensions of obj
//#declare object_corner1 = ; // lower-left hand corner
//#declare object_corner2 = ; // upper-right hand corner
//#declare object_orientation = ; // rotation about centre of object
#declare object_hollow = false; // true->surface model only, false->solid
// PARTICLE OPTIONS
#declare particle_res = <5,5,5>; //<10,10,10>;//<3,3,3>; // <7, 3, 5> ->7 particles in x, 3 in y 5 in z  TOTAL: 7*3*5 = 105
//#declare particle_object = ; // shape of particles, unit-sized and origin centered, DEFAULT: box{<-0.5,-0.5,-0.5> <0.5,0.5,0.5>}
#declare particle_texture = texture{pigment{rgb<1,1,1>}}; // only if object_hollow=false
#declare disintegration = 0;  // with explode_life shrink particles over time
// EXPLOSION OPTIONS
#declare explosion_location = <0,-5,0>; // vector location of the explosion
#declare exp_strength = 1; // force of explosion, actually velocity given to each particle
#declare exp_falloff = 7; // units away from exp_location to recaive 25% of force specified by exp_strength
#declare exp_gravity = 15; // strength of force of gravity (not a vector)
//#declare exp_sky = ; // direction vector that points in the up direction, DEFAULT: <0,1,0>
#declare exp_spin = 0.2 ; // <0.5,1,0>==180° about x, 360° about y per time unit
// GROUND PLANE OPTIONS
#declare ground_plane = true ; // true->ground plane present, otherwise absent
#declare ground_dist = -0.497; // distance from origin, plane normal is allway the same as exp_sky, DEFAULT: 0
#declare ground_reflection = 0.2; // amaount of energy a particle retains after hitting ground, DFAULT: 0
#declare max_bounces = 2; // maximum number a particle will rebound of plane, DEFAULT: 1
// TURBULENCE OPTIONS
#declare exp_turb = 0.5; // overall amount of tubulence added to the explosion, DEFAULT: 0
#declare scale_turb = 0.2; // only if exp_turb!=0 example 0.5 will give particles scaled up to 50% larger or smaller
#declare rotate_turb = 0.5; // only if exp_turb!=0 fraction of 360° amount of turbulence added to rotation of the particles
#declare vel_turb = 0.1; // only if exp_turb!=0 fraction amount of particles velocity more or less
#declare dir_turb = 0.1; // only if exp_turb!=0 fracton of 360° amount moves particles away from normal
#declare spin_turb = 0.2; // only if exp_spin!=0 factor total spin amount more or less than normal
#declare exp_seed = 123548; // random number seed used whenn adding turbulence DEFAULT: 0
// GENERATING THE EXPLOSION
//#declare explode_clock = ; // normally no need of this, current time value of the explosion, like POV-Ray's internal clock variable
//#declare explode_start = ; // time value wehn to start explosion, normally no need for explode_clock
#declare explode_life = 0.9; // lifetime of particles, DEFAULT: disintegration is enabled
#declare time_scale = 1; // speed of explosion DEFAULT: 1
// CREATE EXPLODING OBJECT
#include "Explode.inc"























// Tennisball    
/*
    pigment{
        image_map{ 
            jpeg "NewTennisBallColor.jpg"
//            jpeg "TennisBallColorMap.jpg"
            map_type 1
        }
        scale<20,20,20>
//        rgb <1,1,0>
        }
    normal{
//        crackle form <1,0,0>
        bump_map{
            jpeg "TennisBallBump.jpg"  
            map_type 1
            }
        scale <20,20,20>
        } 
    rotate <clock*360,clock*360,0>
    }

*/