
/** batch rendering code **/
include <threads.scad>
  batch_rendering = ""; 

  if (batch_rendering == "") { 
    render_working_code();
  }

/** working output code **/
  module render_working_code() {
    $fn = 20;
    translate([-20, 10, 0]) easy_render_1();
    translate([-20, 20, 0]) easy_render_2();
    translate([-20, 30, 0]) easy_render_3();
    translate([-20, 40, 0]) easy_render_4();
    translate([-20, 50, 0]) easy_render_5();

    translate([20, 10, 0]) difficult_render_1();
    translate([20, 20, 0]) difficult_render_2();
    translate([20, 30, 0]) difficult_render_3();
    translate([20, 40, 0]) difficult_render_4();
    translate([20, 50, 0]) difficult_render_5();

    easy_render_5_for_dxf();

    //approx 45 seconds to preview
  }

/** working output code **/
  module difficult_render_1() {
    english_thread (diameter=1/4, threads_per_inch=20, length=2);
  }
  module difficult_render_2() {
    english_thread (diameter=1/4, threads_per_inch=20, length=4);
  }
  module difficult_render_3() {
    english_thread (diameter=1/4, threads_per_inch=20, length=6);
  }
  module difficult_render_4() {
    english_thread (diameter=1/4, threads_per_inch=20, length=8);
  }
  module difficult_render_5() {
    english_thread (diameter=1/4, threads_per_inch=20, length=10);
  }
  module easy_render_5_for_dxf() {
    projection(cut = false) {
      rotate([90,0,0]) {
        metric_thread (diameter=8, pitch=5, length=16, square=true, thread_size=5,groove=true, rectangle=0.333);
      }
    }
  }

  module easy_render_1() {
    metric_thread (diameter=8, pitch=1, length=16, square=true, thread_size=1,groove=true, rectangle=0.333);

  }
  module easy_render_2() {
    metric_thread (diameter=8, pitch=2, length=16, square=true, thread_size=2,groove=true, rectangle=0.333);

  }
  module easy_render_3() {
    metric_thread (diameter=8, pitch=3, length=16, square=true, thread_size=3,groove=true, rectangle=0.333);

  }
  module easy_render_4() {
    metric_thread (diameter=8, pitch=4, length=16, square=true, thread_size=4,groove=true, rectangle=0.333);

  }
  module easy_render_5() {
    metric_thread (diameter=8, pitch=5, length=16, square=true, thread_size=5,groove=true, rectangle=0.333);

  }
  