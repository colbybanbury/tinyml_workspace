/* Copyright 2019 The TensorFlow Authors. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
==============================================================================*/

#include "tensorflow/lite/micro/examples/hello_world/main_functions.h"
#include "mbed.h"

// #define TINYML_MODEL mobilenet_v1_004_96_frozen
// YOU WILL NEED TO DEFINE THIS TINYML MODEL IN YOUR COMPILATION INSTRUCTIONS
// USING -DTINYML_MODEL=<the model you want from tinyml_model_data.cc>
#define STRING(s) #s
#define STRING_VAR(s) STRING(s)

Timer t;

// This is the default main used on systems that have the standard C entry
// point. Other devices (for example FreeRTOS or ESP32) that have different
// requirements for entry code (like an app_main function) should specialize
// this main.cc file in a target-specific subfolder.
int main(int argc, char* argv[]) {
  debug("Starting benchmark.");
  setup();
  while (true) {
    t.reset();
    t.start();
    for (int i = 0; i < 1; i++) {
      loop();
    }
    t.stop();
    debug("<%s>,<%f>,seconds\n", STRING_VAR(TINYML_MODEL), t.read());
  }
}
