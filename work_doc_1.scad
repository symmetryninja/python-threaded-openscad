
/** batch rendering code **/
include <threads.scad>
  batch_rendering = false; 

  if (!batch_rendering) { 
    render_workspace();
  }

/** working output code **/
  module render_workspace() {
    $fn = 40;
    // translate([-20, -30, 0]) easy_render_1();
    // translate([-20, -15, 0]) easy_render_2();
    // translate([-20, 0, 0]) easy_render_3();
    // translate([-20, 15, 0]) easy_render_4();
    // translate([-20, 30, 0]) easy_render_5();

    // translate([0, -30, 0]) easy_render_6();
    // translate([0, -15, 0]) easy_render_7();
    // translate([0, 0, 0]) easy_render_8();
    // translate([0, 15, 0]) easy_render_9();
    // translate([0, 30, 0]) easy_render_10();

    // translate([20, -30, 0]) difficult_render_1();
    // translate([20, -15, 0]) difficult_render_2();
    // translate([20, 0, 0]) difficult_render_3();
    // translate([20, 15, 0]) difficult_render_4();
    // translate([20, 30, 0]) difficult_render_5();

    // easy_render_5_for_dxf(); 
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
    metric_thread (diameter=8, pitch=2, length=16, square=true, thread_size=1,groove=true, rectangle=0.333);
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
  module easy_render_6() {
    metric_thread (diameter=8, pitch=6, length=16, square=true, thread_size=5,groove=true, rectangle=0.333);
  }
  module easy_render_7() {
    metric_thread (diameter=8, pitch=7, length=16, square=true, thread_size=5,groove=true, rectangle=0.333);
  }
  module easy_render_8() {
    metric_thread (diameter=8, pitch=8, length=16, square=true, thread_size=5,groove=true, rectangle=0.333);
  }
  module easy_render_9() {
    metric_thread (diameter=8, pitch=9, length=16, square=true, thread_size=5,groove=true, rectangle=0.333);
  }
  module easy_render_10() {
    metric_thread (diameter=8, pitch=10, length=16, square=true, thread_size=5,groove=true, rectangle=0.333);
  }
  module easy_render_11() {
    metric_thread (diameter=8, pitch=11, length=16, square=true, thread_size=5,groove=true, rectangle=0.333);
  }
  module easy_render_12() {
    metric_thread (diameter=8, pitch=12, length=16, square=true, thread_size=5,groove=true, rectangle=0.333);
  }
  module easy_render_13() {
    metric_thread (diameter=8, pitch=13, length=16, square=true, thread_size=5,groove=true, rectangle=0.333);
  }
  module easy_render_14() {
    metric_thread (diameter=8, pitch=14, length=16, square=true, thread_size=5,groove=true, rectangle=0.333);
  }
  module easy_render_15() {
    metric_thread (diameter=8, pitch=15, length=16, square=true, thread_size=5,groove=true, rectangle=0.333);
  }
  module easy_render_16() {
    metric_thread (diameter=8, pitch=16, length=16, square=true, thread_size=5,groove=true, rectangle=0.333);
  }
