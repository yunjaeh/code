/***********************************************************************
	UDF for initializing flow field variables
************************************************************************/
#include "udf.h"
#include "math.h"


/***********************************************************************
	House dimensions	
************************************************************************/
#define x_dim 3.14
#define y_dim 2.33 
#define z_dim 2.3


/***********************************************************************
	Thermal boundary conditions	
************************************************************************/
#define Temp_in 300
#define Temp_out 290



/***********************************************************************
	internal load inside the house

  x, y, z dim	: house dimensions
  vol 		: total air volume of the house
  heat_gen 	: total heat generation

************************************************************************/


DEFINE_SOURCE(internal_load,c,t,dS,eqn)       /* define source  */
{

  real xc[ND_ND];
  real vol;
  real heat_gen;
  real source;

  heat_gen = 400.0;
  vol = x_dim*y_dim*z_dim;

  C_CENTROID(xc, c, t);
         
  if( xc[0] < x_dim && xc[0] > 0.0 && xc[1] < y_dim && xc[1] > 0.0 &&  xc[2] < z_dim) 
  { 
    source = heat_gen / vol;    /* inside of home, volume averaged heat source */
  } 
  else 
  {
    source = 0.0;  
  }
  dS[eqn]=0.0;

  return source;
}



DEFINE_INIT(initial_condition,d)
{
  cell_t c;
  Thread *t;
  real xc[ND_ND];

  /* loop over all cell threads in the domain */
  thread_loop_c(t,d)
  {
    /* loop over all cells */
    begin_c_loop_all(c,t)
    {
      C_CENTROID(xc,c,t);
      if(0.0 < xc[0] && xc[0] < x_dim && 0.0 < xc[1] && xc[1] < y_dim && 0.0 < xc[2] && xc[2] < z_dim )
      {
        C_T(c,t) = Temp_in;
      }
      else
      {
        C_T(c,t) = Temp_out;
      }
    }
    end_c_loop_all(c,t)
  }
}

